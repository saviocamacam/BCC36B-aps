#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
#-------------------------------------------------------------------------
from locale import str

from ply import yacc
from lexer import Lexer

class Tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):
        return self.type

class Parser:

    def __init__(self, code):
        lex = Lexer()
        self.current_producion = ""
        self.tokens = lex.tokens
        self.precendence = (
            ('left', 'SENAO'),
            ('left', 'EQU', 'NEQ', 'GEQ', 'GRT', 'LEQ', 'LET'),
            ('left', 'ADD', 'SUB'),
            ('left', 'TIMES', 'DIV'),
        )
        parser = yacc.yacc(debug=False, module=self, optimize=False)
        self.ast = parser.parse(code)
        print("")

    def p_programa(self, p):
        'programa : lista_declaracoes'
        p[0] = Tree('program', [p[1]])

    def p_lista_declaracoes(self, p):
        '''
        lista_declaracoes : lista_declaracoes declaracao
            | declaracao
            | error
        '''
        if p.slice[1].type == "error":
            print("Erro de declaracao na linha " + str(p.slice[1].lineno))
        elif len(p) == 3:
            p[0] = Tree('lista-declaracoes', [p[1],p[2]])
        elif len(p) == 2:
            p[0] = Tree('lista-declaracoes', [p[1]])


    def p_declaracao(self, p):
        '''
        declaracao : declaracao_variaveis
            | inicializacao_variaveis
            | declaracao_funcao
        '''
        p[0] = Tree('declaracao', [p[1]])

    def p_declaracao_variaveis(self, p):
        'declaracao_variaveis : tipo COLON lista_variaveis'
        self.current_producion = p
        p[0] = Tree('declaracao', [p[1], p[3]])

    def p_declaracao_variaveis_error(self, p):
        'declaracao_variaveis : tipo COLON error'
        print("Erro na declaração de variáveis na linha " +  str(p.slice[3].lineno))

    def p_inicializacao_variaveis(self, p):
        'inicializacao_variaveis : atribuicao'
        p[0] = Tree('inicializacao-variaveis', [p[1]])

    def p_declaracao_funcao(self, p):
        '''
        declaracao_funcao : tipo cabecalho
            | cabecalho
        '''
        if len(p) == 3:
            p[0] = Tree('declaracao-funcao', [p[1], p[2]])
        elif len(p) == 2:
            p[0] = Tree('declaracao-funcao', [p[1]])

    def p_tipo(self, p):
        '''tipo : INTEIRO 
            | FLUTUANTE'''
        p[0] = Tree('tipo', [], p[1])

    def p_lista_variaveis(self, p):
        '''
        lista_variaveis : lista_variaveis COM var
            | var
        '''
        if len(p) == 4:
            p[0] = Tree('lista-variaveis', [p[1], p[3]])
        elif len(p) == 2:
            p[0] = Tree('lista-variaveis', [p[1]])

    def p_lista_variaveis_error(self, p):
        'lista_variaveis : lista_variaveis COM error'
        print("Erro na declaração de variaveis na linha " + str(p.slice[2].lineno))

    def p_atribuicao(self, p):
        '''
        atribuicao : var simbolo_atribuicao expressao
            | condicional
            | NOT condicional
        '''
        if len(p) == 4:
            p[0] = Tree('atribuicao', [p[1], p[2], p[3]])
        elif len(p) == 2:
            p[0] = Tree('atribuicao', [p[1]])
        elif len(p) == 3:
            p[0] = Tree('atribuicao', [p[2]], p[1])


    def p_condicional(self, p):
        '''
        condicional : expressao_simples operador_relacional expressao_aditiva
            | LPAR condicional RPAR
            | condicional simbolo_condicional condicional
            | condicional simbolo_condicional error
            | LPAR error RPAR
            | error simbolo_condicional condicional
        '''
        if p.slice[1].type == "expressao_simples":
            p[0] = Tree('operador_relacional', [p[1], p[2], p[3]])
        elif p.slice[2].type == "condicional":
            p[0] = Tree('condicional', [p[2]])
        elif p.slice[1].type == "condicional":
            p[0] = Tree('simbolo_condicional', [p[1], p[2], p[3]])

    def p_simbolo_condicional(self, p):
        '''
        simbolo_condicional : OR
            | AND
        '''
        p[0] = Tree('simbolo-condicional', [], p[1])

    def p_simbolo_atribuicao(self, p):
        'simbolo_atribuicao : ASS'
        p[0] = Tree('simbolo-atribuicao', [], p[1])

    def p_atribuicao_error(self, p):
        'atribuicao : var simbolo_atribuicao error'
        print("Erro de atribuição na linha " + str(p.slice[2].lineno))

    def p_cabecalho(self, p):
        'cabecalho : ID LPAR lista_parametros RPAR corpo FIM'
        p[0] = Tree('cabecalho', [p[3], p[5]], p[1])

    def p_cabecalho_error(self, p):
        'cabecalho : ID LPAR lista_parametros RPAR corpo error'
        print("Erro sintático. Função está faltando FIM na linha " + str(p.slice[6].lineno))

    def p_corpo(self, p):
        '''
        corpo : corpo acao
            | empty
        '''
        if len(p) == 3:
            p[0] = Tree('corpo', [p[1], p[2]])
        elif len(p) == 2:
            p[0] = Tree('corpo', [p[1]])

    def p_acao(self, p):
        '''
        acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreve
            | retorna
        '''
        p[0] = Tree('acao', [p[1]])

    def p_se(self, p):
        '''
        se : SE expressao ENTAO corpo FIM
            | SE expressao ENTAO corpo SENAO corpo FIM
        '''
        self.current_producion = p
        if len(p) == 6:
            p[0] = Tree('se', [p[2], p[4]])
        elif len(p) == 8:
            p[0] = Tree('se', [p[2], p[4], p[6]])

    def p_se_error(self, p):
        '''
        se : SE expressao error corpo FIM
            | error SENAO corpo FIM
        '''
        if len(p) == 6:
            print("Erro sintático na linha " + str(p.slice[3].lineno) + ". Esperado um ENTÃO")
        elif len(p) == 5:
            print("Erro sintático na linha " + str(p.slice[1].lineno) + ". Condicional SENÃO mal-formado")

    def p_repita(self, p):
        'repita : REPITA corpo ATE expressao'
        self.current_producion = p
        p[0] = Tree('repita', [p[2], p[4]])

    def p_repita_error(self, p):
        'repita : REPITA corpo error'
        print("Erro. Esperado expressão de termino")

    def p_leia(self, p):
        'leia : LEIA LPAR ID RPAR'
        self.current_producion = p
        p[0] = Tree('leia', [], p[3])

    def p_escreve(self, p):
        'escreve : ESCREVE LPAR expressao RPAR'
        self.current_producion = p
        p[0] = Tree('escreve', [p[3]])

    def p_retorna(self, p):
        'retorna :  RETORNA LPAR expressao RPAR'
        self.current_producion = p
        p[0] = Tree('retorna', [p[3]], p[1])

    def p_var(self, p):
        '''
        var : ID
            | ID indice
        '''
        if len(p) == 2:
            p[0] = Tree('var', [], p[1])
        elif len(p) == 3:
            p[0] = Tree('var', [p[2]], p[1])

    def p_expressao(self, p):
        '''
        expressao : expressao_simples
            | atribuicao
        '''
        self.current_producion = p
        p[0] = Tree('expressao', [p[1]])

    def p_lista_parametros(self, p):
        '''
        lista_parametros : lista_parametros COM parametro
            | parametro
            | empty
        '''
        if len(p) == 4:
            p[0] = Tree('lista-parametros', [p[1], p[3]], p[2])
        elif len(p) == 2:
            p[0] = Tree('lista-parametros', [p[1]])

    def p_indice(self, p):
        '''
        indice : indice LBR expressao RBR
            | LBR expressao RBR
        '''
        self.current_producion = p
        if len(p) == 5:
            p[0] = Tree('indice', [p[1], p[3]])
        elif len(p) == 4:
            p[0] = Tree('indice', [p[2]])

    def p_indice_error(self, p):
        '''
        indice : indice LBR error RBR
            | LBR error RBR
            | error RBR
            | LBR error
        '''
        print("Erro sintático no índice na linha " + str(p.slice[3].lineno))

    def p_expressao_simples(self, p):
        '''
        expressao_simples : expressao_aditiva
            | expressao_simples operador_relacional expressao_aditiva
        '''
        self.current_producion = p
        if len(p) == 2:
            p[0] = Tree('expressao-simples', [p[1]])
        elif len(p) == 4:
            p[0] = Tree('expressao-simples', [p[1], p[2], p[3]])

    def p_parametro(self, p):
        '''
        parametro : tipo COLON ID
            | parametro LBR RBR
        '''
        if p[1].type == "tipo":
            p[0] = Tree('parametro', [p[1]], p[3])
        elif p[1].type == "parametro":
            p[0] == Tree('parametro', [p[1]])


    def p_operador_relacional(self, p):
        '''
        operador_relacional : LET
            | GRT
            | EQU
            | NEQ
            | LEQ
            | GEQ
        '''
        self.current_producion = p
        p[0] = Tree('operador-relacional', [], p[1])

    def p_expressao_aditiva(self, p):
        '''
        expressao_aditiva : expressao_multiplicativa
            | expressao_aditiva operador_soma expressao_multiplicativa
        '''
        self.current_producion = p
        if len(p) == 2:
            p[0] = Tree('expressao-aditiva', [p[1]])
        elif len(p) == 4:
            p[0] = Tree('expressao-aditiva', [p[1], p[2], p[3]])

    def p_expressao_multiplicativa(self, p):
        '''
        expressao_multiplicativa : expressao_unaria
            | expressao_multiplicativa operador_multiplicacao expressao_unaria
        '''
        self.current_producion = p
        if len(p) == 2:
            p[0] = Tree('expressao-multiplicativa', [p[1]])
        elif len(p) == 4:
            p[0] = Tree('expressao-multiplicativa', [p[1], p[2], p[3]])

    def p_operador_soma(self, p):
        '''
        operador_soma : ADD
            | SUB
        '''
        self.current_producion = p
        p[0] = Tree('operador-soma', [], p[1])

    def p_operador_multiplicacao(self, p):
        '''
        operador_multiplicacao : TIMES
            | DIV
        '''
        self.current_producion = p
        p[0] = Tree('operador-multiplicacao', [], p[1])

    def p_expressao_unaria(self, p):
        '''
        expressao_unaria : fator
            | operador_soma fator
        '''
        self.current_producion = p
        if len(p) == 2:
            p[0] = Tree('expressao-unaria', [p[1]])
        elif len(p) == 3:
            p[0] = Tree('expressao-unaria', [p[1], p[2]])

    def p_fator(self, p):
        '''
        fator : LPAR expressao RPAR
            | var
            | chamada_funcao
            | numero
        '''
        self.current_producion = p
        if len(p) == 2:
            p[0] = Tree('fator', [p[1]])
        elif len(p) == 4:
            p[0] = Tree('fator', [p[2]])

    def p_numero(self, p):
        '''
        numero : INTEIRO
            | FLUTUANTE
        '''
        self.current_producion = p
        p[0] = Tree('numero', [], p[1])

    def p_chamada_funcao(self, p):
        'chamada_funcao : ID LPAR lista_argumentos RPAR'
        self.current_producion = p
        p[0] = Tree('chamada-funcao', [p[3]], p[1])

    def p_lista_argumentos(self, p):
        '''
        lista_argumentos : lista_argumentos COM expressao
            | expressao
            | empty
        '''
        self.current_producion = p
        if len(p) == 2:
            p[0] = Tree('lista-argumentos', [p[1]])
        elif len(p) == 4:
            p[0] = Tree('lista-argumentos', [p[1], p[3]])

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        if p:
            print("'%s', linha %d" % (p.value, p.lineno))
        else:
            yacc._restart
            print('Erro sintático: definições incompletas!')
            exit(1)


def generateTree(t):
    if t is not None:
        print('['+ t.type + ' ' + t.value)

        for node in t.child:
            i = t.child.index(node)
            generateTree(t.child[i])
        print(']')

if __name__ == '__main__':

    from sys import argv, exit
    f = open(argv[1],  encoding='utf-8')
    p = Parser(f.read())
    generateTree(p.ast)
    '''


    import glob, os
    path = "C:/Users/savio/git/compiladores-march/testes"
    os.chdir(path)

    for file in glob.glob("*.tpp"):
        print(file.title())
        f = open(file,  encoding='utf-8')
        p = Parser(f.read())
        generateTree(p.ast)
    '''