#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
#-------------------------------------------------------------------------

import ply.lex as lex
from ply.ctokens import t_ID


class Lexer:
    def __init__(self):
        self.lexer = lex.lex(debug=False,module=self, optimize=False)

    keywords = {
        u'se': 'SE',
        u'então': 'ENTAO',
        u'senão': 'SENAO',
        u'fim': 'FIM',
        u'repita': 'REPITA',
        u'inteiro': 'INTEIRO',
        u'flutuante': 'FLUTUANTE',
        u'retorna': 'RETORNA',
        u'até': 'ATE',
        u'leia': 'LEIA',
        u'escreve': 'ESCREVE',
    }

    tokens = ['ASS', 'COLON', 'LPAR', 'RPAR', 'ADD', 'SUB', 'TIMES', 'DIV',
              'LEQ', 'GEQ', 'EQU', 'NEQ', 'LET', 'GRT', 'LBR', 'RBR', 'COM',
              'ID', 'NOT', 'AND', 'OR'] + list(keywords.values())

    t_ASS = r':='
    t_COLON = r':'
    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_ADD = r'\+'
    t_SUB = r'\-'
    t_TIMES = r'\*'
    t_DIV = r'/'
    t_LEQ = r'<='
    t_GEQ = r'>='
    t_EQU = r'='
    t_NEQ = r'<>'
    t_LET = r'<'
    t_GRT = r'>'
    t_LBR = r'\['
    t_RBR = r'\]'
    t_COM = r','
    t_NOT = r'!'
    t_AND = r'&&'
    t_OR = r'\|\|'

    def t_INTEIRO(self, t):
        r'[0-9][0-9]*'
        t.type = self.keywords.get(t.value, 'INTEIRO')
        return t

    def t_FLUTUANTE(self, t):
        r'[0-9][0-9]*\.[0-9]*([Ee][-]?[0-9]+)?'
        t.type = self.keywords.get(t.value,'FLUTUANTE')
        return t



    def t_ID(self, t):
        r'[a-zA-Zá-ñÁ-Ñ][a-zA-Zá-ñÁ-Ñ0-9_]*'
        t.type = self.keywords.get(t.value,'ID')
        return t

    def t_COMMENT(self, t):
        r'\{[^}]*\}'

    '''
    \{[^}]*[{]*\}
    '''

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        print("Caractere ilegal '%s', linha %d, coluna %d"
              % (t.value[0], t.lineno, t.lexpos))
        t.lexer.skip(1)

    def t_ERRORCT(self, t):
        r'[{}]'
        print("Erro de comentário na linha %d, coluna %d" % (t.lineno, t.lexpos))
        t.lexer.skip(1)

    def test(self, code):
        lex.input(code)
        while True:
            t = lex.token()
            if not t:
                break
            print('<' + t.type +',' + t.value + '>')

if __name__ == '__main__':
    from sys import argv
    lexer  = Lexer()
    for filename in argv[1:]:
        f = open(filename, encoding='utf-8')
        print(f.name)
        lexer.test(f.read())
        print("\n")