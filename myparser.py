#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
#-------------------------------------------------------------------------
from locale import str

from ply import yacc
from lexer import Lexer
from io import StringIO  # Python3

import sys


class Scope:
    def __init__(self, name):
        self.name = name
        self.subscopes = []
        self.entries = {}

    def get_entries(self):
        return self.entries

    def __str__(self):
        return self.name


class Entry:
    def __init__(self, name, valor):
        self.name = name
        self.valor = valor


class Tree:
    def __init__(self, type_node, child=[], value=''):
        self.parent = None
        self.type = type_node
        self.varType = None
        self.child = child
        self.value = value
        self.scope = Scope(type_node)

    def __str__(self):
        return self.type


class MyParser:
    def __init__(self, code):
        lex = Lexer()
        self.scopes = []
        s = Scope('global')
        self.scopes.append(s)
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
        p[1].parent = p[0]
        '''
        for child in p[1].child:
            print(child.type)
        '''


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
            p[1].parent = p[0]
            p[2].parent = p[0]
        elif len(p) == 2:
            p[0] = Tree('lista-declaracoes', [p[1]])
            p[1].parent = p[0]


    def p_declaracao(self, p):
        '''
        declaracao : declaracao_variaveis
            | inicializacao_variaveis
            | declaracao_funcao
            | error
        '''
        if p.slice[1].type == "error":
            print("Erro de declaracao na linha " + str(p.slice[1].lineno))
        else:
            p[0] = Tree('declaracao', [p[1]])
            if p[1]:
                p[1].parent = p[0]

    def p_declaracao_variaveis(self, p):
        'declaracao_variaveis : tipo COLON lista_variaveis'
        p[0] = Tree('declaracao-variaveis', [p[1], p[3]])
        p[1].parent = p[0]
        p[3].parent = p[0]

    def p_declaracao_variaveis_error(self, p):
        'declaracao_variaveis : tipo COLON error'
        print("Erro na declaração de variáveis na linha " +  str(p.slice[3].lineno))

    def p_inicializacao_variaveis(self, p):
        'inicializacao_variaveis : atribuicao'
        p[0] = Tree('inicializacao-variaveis', [p[1]])
        p[1].parent = p[0]

    def p_declaracao_funcao_nova(self, p):
        '''
        declaracao_funcao_nova : INTEIRO ID LPAR lista_parametros RPAR corpo retorna FIM
            | FLUTUANTE ID LPAR lista_parametros RPAR corpo retorna FIM
            | ID LPAR lista_parametros RPAR corpo FIM
        '''
        if(len(p) == 9):
            if (not p[4]):
                p[0] = Tree('declaracao-funcao', [p[6], p[7]], p[2])
                p[6].parent = p[0]
            else:
                p[0] = Tree('declaracao-funcao', [p[4], p[6], p[7]], p[2])
        else:
            if (p[3] is None):
                p[0] = Tree('cabecalho', [p[5]], p[1])
                p[5].parent = p[0]
            else:
                p[0] = Tree('cabecalho', [p[3], p[5]], p[1])
                p[3].parent = p[0]
                if(p[5]):
                    p[5].parent = p[0]

    def p_declaracao_funcao_nova_error(self, p):
        '''declaracao_funcao_nova : INTEIRO ID LPAR lista_parametros RPAR corpo error FIM
            | FLUTUANTE ID LPAR lista_parametros RPAR corpo error FIM
        '''
        print("Error: Função " + p[2] + " precisa retornar um valor " + p[1] + " mas retorna vazio na linha " + str(p.slice[7].lineno));

    def p_declaracao_funcao(self, p):
        '''
        declaracao_funcao : tipo cabecalho
            | cabecalho
        '''
        if len(p) == 3:
            p[0] = Tree('declaracao-funcao', [p[1], p[2]])
            p[1].parent = p[0]
            p[2].parent = p[0]
        elif len(p) == 2:
            p[0] = Tree('declaracao-funcao', [p[1]])
            p[1].parent = p[0]

    def p_declaracao_funcao_error(self, p):
        '''
        declaracao_funcao : tipo cabecalho error
            | cabecalho error
        '''
        print("Erro de declaracao na linha " + str(p.slice[1].lineno))

    def p_cabecalho(self, p):
        'cabecalho : ID LPAR lista_parametros RPAR corpo FIM'

        if(p[3] is None):
            p[0] = Tree('cabecalho', [p[5]], p[1])
            p[5].parent = p[0]
        elif p[3] and p[5]:
            p[0] = Tree('cabecalho', [p[3], p[5]], p[1])
            p[3].parent = p[0]
            p[5].parent = p[0]
        else:
            p[0] = Tree('cabecalho', [], p[1])

    def p_cabecalho_error(self, p):
        'cabecalho : ID LPAR lista_parametros RPAR corpo error'
        print("Erro sintático. Função está faltando FIM na linha " + str(p.slice[6].lineno))

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
            p[1].parent = p[0]
            p[3].parent = p[0]
        elif len(p) == 2:
            p[0] = Tree('lista-variaveis', [p[1]])
            p[1].parent = p[0]

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
            p[1].parent = p[0]
            p[2].parent = p[0]
            p[3].parent = p[0]
        elif len(p) == 2:
            p[0] = Tree('atribuicao', [p[1]])
            p[1].parent = p[0]
        elif len(p) == 3:
            p[0] = Tree('atribuicao', [p[2]], p[1])
            p[2].parent = p[0]


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
            p[1].parent = p[0]
            p[2].parent = p[0]
            p[3].parent = p[0]
        elif p.slice[2].type == "condicional":
            p[0] = Tree('condicional', [p[2]])
            p[2].parent = p[0]
        elif p.slice[1].type == "condicional":
            p[0] = Tree('simbolo_condicional', [p[1], p[2], p[3]])
            p[1].parent = p[0]
            p[2].parent = p[0]
            p[3].parent = p[0]

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



    def p_corpo(self, p):
        '''
        corpo : corpo acao
            | empty
        '''
        if len(p) == 3:
            if p[1] is None:
                p[0] = Tree('corpo', [p[2]])
                p[2].parent = p[0]
            elif p[2] is None:
                p[0] = Tree('corpo', [p[1]])
                p[1].parent = p[0]
            else:
                p[0] = Tree('corpo', [p[1], p[2]])
                p[1].parent = p[0]
                p[2].parent = p[0]
        '''elif len(p) == 2:
            p[0] = Tree('corpo', [p[1]])'''

    def p_acao(self, p):
        '''
        acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
        '''
        p[0] = Tree('acao', [p[1]])
        if(p[1]):
            p[1].parent = p[0]

    def p_se(self, p):
        '''
        se : SE expressao ENTAO corpo FIM
            | SE expressao ENTAO corpo SENAO corpo FIM
        '''

        if len(p) == 6:
            p[0] = Tree('se', [p[2], p[4]])
            p[2].parent = p[0]
            p[4].parent = p[0]
        elif len(p) == 8:
            p[0] = Tree('se', [p[2], p[4], p[6]])
            p[2].parent = p[0]
            p[4].parent = p[0]
            p[6].parent = p[0]

    def p_se_error(self, p):
        '''
        se : SE expressao error corpo FIM
            | error SENAO corpo FIM
            | SE expressao SENAO corpo error
        '''
        if len(p) == 6:
            print("Erro sintático na linha " + str(p.slice[3].lineno) + ". Esperado um ENTÃO")
        elif len(p) == 5:
            print("Erro sintático na linha " + str(p.slice[1].lineno) + ". Condicional SENÃO mal-formado")
        elif len(p) == 6 and p.slice[5].type == "error":
            print("Erro sintático na linha " + str(p.slice[1].lineno) + ". SENÃO espera um FIM")


    def p_repita(self, p):
        'repita : REPITA corpo ATE expressao'
        p[0] = Tree('repita', [p[2], p[4]])
        p[2].parent = p[0]
        p[4].parent = p[0]

    def p_repita_error(self, p):
        'repita : REPITA corpo error'
        print("Erro. Esperado expressão de termino")

    def p_leia(self, p):
        'leia : LEIA LPAR expressao RPAR'
        p[0] = Tree('leia', [p[3]], p[1])
        p[3].parent = p[0]

    def p_escreva(self, p):
        'escreva : ESCREVA LPAR expressao RPAR'
        p[0] = Tree('escreva', [p[3]], p[1])
        p[3].parent = p[0]

    def p_retorna(self, p):
        'retorna :  RETORNA LPAR expressao RPAR'
        p[0] = Tree('retorna', [p[3]], p[1])
        p[3].parent = p[0]

    def p_retorna_error(self, p):
        'retorna :  RETORNA LPAR error RPAR'

        if(p[3].value == ')'):
            print("Erro. Chamada de retorno precisa de pelo menos um valor.")
        else:
            print("Erro. Chamada de retorno precisa de um valor válido")

    def p_var(self, p):
        '''
        var : ID
            | ID indice
            | ID lista_dimensions
        '''
        if len(p) == 2:
            p[0] = Tree('var', [], p[1])
        elif len(p) == 3:
            p[0] = Tree('var', [p[2]], p[1])
            if p[2] != None:
                p[2].parent = p[0]

    def p_expressao(self, p):
        '''
        expressao : expressao_simples
            | atribuicao
        '''

        p[0] = Tree('expressao', [p[1]])
        p[1].parent = p[0]

    def p_lista_parametros(self, p):
        '''
        lista_parametros : lista_parametros COM parametro
            | parametro
            | empty
        '''
        if len(p) == 4:
            p[0] = Tree('lista-parametros', [p[1], p[3]])
            if(p[1]):
                p[1].parent = p[0]
            if(p[3]):
                p[3].parent = p[0]
        elif len(p) == 2:
            p[0] = Tree('lista-parametros', [p[1]])
            if (p[1]):
                p[1].parent = p[0]

    def p_indice(self, p):
        '''
        indice : indice LBR expressao RBR
            | LBR expressao RBR
        '''

        if len(p) == 5:
            p[0] = Tree('indice', [p[1], p[3]])
            p[1].parent = p[0]
            p[3].parent = p[0]
        elif len(p) == 4:
            p[0] = Tree('indice', [p[2]])
            p[2].parent = p[0]

    def p_indice_error(self, p):
        '''
        indice : indice LBR error RBR
            | LBR error RBR
            | error RBR
            | LBR error
        '''
        print(p.slice[3])
        if(len(p) == 5):
            print("Erro sintático no índice na linha " + str(p.slice[3].lineno))
        elif p.slice[2].type == "error":
            print("Erro sintático no índice na linha " + str(p.slice[2].lineno))

    def p_expressao_simples(self, p):
        '''
        expressao_simples : expressao_aditiva
            | expressao_simples operador_relacional expressao_aditiva
        '''

        if len(p) == 2:
            p[0] = Tree('expressao-simples', [p[1]])
            p[1].parent = p[0]
        elif len(p) == 4:
            p[0] = Tree('expressao-simples', [p[1], p[2], p[3]])
            p[1].parent = p[0]
            p[2].parent = p[0]
            p[3].parent = p[0]

    def p_parametro(self, p):
        '''
        parametro : tipo COLON var
            | parametro
        '''
        if p.slice[1].type == "tipo":
            p[0] = Tree('parametro', [p[1], p[3]])
            p[1].parent = p[0]
            p[3].parent = p[0]
        elif p.slice[1].type == 'parametro':
            p[0] = Tree('parametro', [p[1]])
            p[1].parent = p[0]

    def p_lista_dimensions(self, p):
        '''
        lista_dimensions : dimension
            | lista_dimensions dimension
        '''
        if len(p) == 3:
            p[0] = Tree('lista-dimensions', [p[1], p[2]])
            p[1].parent = p[0]
            p[2].parent = p[0]
        elif len(p) == 2:
            p[0] = Tree('lista-dimensions', [p[1]])
            p[1].parent = p[0]

    def p_dimension(self, p):
        'dimension : LBR RBR'
        p[0] = Tree('dimension', [], 'dim')


    def p_operador_relacional(self, p):
        '''
        operador_relacional : LET
            | GRT
            | EQU
            | NEQ
            | LEQ
            | GEQ
        '''

        p[0] = Tree('operador-relacional', [], p[1])

    def p_expressao_aditiva(self, p):
        '''
        expressao_aditiva : expressao_multiplicativa
            | expressao_aditiva operador_soma expressao_multiplicativa
        '''

        if len(p) == 2:
            p[0] = Tree('expressao-aditiva', [p[1]])
            p[1].parent = p[0]
        elif len(p) == 4:
            p[0] = Tree('expressao-aditiva', [p[1], p[2], p[3]])
            p[1].parent = p[0]
            p[2].parent = p[0]
            p[3].parent = p[0]

    def p_expressao_multiplicativa(self, p):
        '''
        expressao_multiplicativa : expressao_unaria
            | expressao_multiplicativa operador_multiplicacao expressao_unaria
        '''

        if len(p) == 2:
            p[0] = Tree('expressao-multiplicativa', [p[1]])
            p[1].parent = p[0]
        elif len(p) == 4:
            p[0] = Tree('expressao-multiplicativa', [p[1], p[2], p[3]])
            p[1].parent = p[0]
            p[2].parent = p[0]
            p[3].parent = p[0]

    def p_operador_soma(self, p):
        '''
        operador_soma : ADD
            | SUB
        '''

        p[0] = Tree('operador-soma', [], p[1])

    def p_operador_multiplicacao(self, p):
        '''
        operador_multiplicacao : TIMES
            | DIV
        '''

        p[0] = Tree('operador-multiplicacao', [], p[1])

    def p_expressao_unaria(self, p):
        '''
        expressao_unaria : fator
            | operador_soma fator
        '''

        if len(p) == 2:
            p[0] = Tree('expressao-unaria', [p[1]])
            p[1].parent = p[0]
        elif len(p) == 3:
            p[0] = Tree('expressao-unaria', [p[1], p[2]])
            p[1].parent = p[0]
            p[2].parent = p[0]

    def p_fator(self, p):
        '''
        fator : LPAR expressao RPAR
            | var
            | chamada_funcao
            | numero
        '''

        if len(p) == 2:
            p[0] = Tree('fator', [p[1]])
            p[1].parent = p[0]
        elif len(p) == 4:
            p[0] = Tree('fator', [p[2]])
            p[2].parent = p[0]

    def p_numero(self, p):
        '''
        numero : INTEIRO
            | FLUTUANTE
        '''

        p[0] = Tree('numero', [], p[1])

    def p_chamada_funcao(self, p):
        'chamada_funcao : ID LPAR lista_argumentos RPAR'
        if(p[3] is not None):
            p[0] = Tree('chamada-funcao', [p[3]], p[1])
            p[3].parent = p[0]
        else:
            p[0] = Tree('chamada-funcao', [], p[1])

    def p_lista_argumentos(self, p):
        '''
        lista_argumentos : lista_argumentos COM expressao
            | expressao
            | empty
        '''

        if len(p) == 2 and p[1] is not None:
            p[0] = Tree('lista-argumentos', [p[1]])
            p[1].parent = p[0]
        elif len(p) == 4:
            p[0] = Tree('lista-argumentos', [p[1], p[3]])
            p[1].parent = p[0]
            p[3].parent = p[0]

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        print(p)
        if p:
            print("'%s', linha %d" % (p.value, p.lineno))
        else:
            yacc._restart
            print('Erro sintático: definições incompletas!')
            exit(1)


def generatetree(t):
    if t is not None:
        print('['+ t.type + ' ' + t.value)

        for node in t.child:
            i = t.child.index(node)
            generatetree(t.child[i])
        print(']')


if __name__ == '__main__':
    from sys import argv, exit
    config = 1
    if config:
        f = open(argv[1],  encoding='utf-8')
        p = MyParser(f.read())
        generatetree(p.ast)

    else:
        import glob, os
        path = "C:/Users/savio/git/compiladores-march/testes"
        os.chdir(path)

        for file in glob.glob("*.tpp"):
            print(file.title())
            f = open(file,  encoding='utf-8')
            p = MyParser(f.read())
            generatetree(p.ast)
