#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
#-------------------------------------------------------------------------
from parser import Parser

class Semantica:

    def __init__(self, code):
        self.tree = Parser(code).ast

def generateTree(t):
    if t is not None:
        print('['+ t.type + ' ' + t.value)

        for node in t.child:
            i = t.child.index(node)
            generateTree(t.child[i])
        print(']')

if __name__ == '__main__':
    from sys import argv, exit

    config = 1
    if config:
        f = open(argv[1], encoding='utf-8')
        s = Semantica(f.read())
        generateTree(s.ast)

    else:
        import glob, os

        path = "C:/Users/savio/git/compiladores-march/testes"
        os.chdir(path)

        for file in glob.glob("*.tpp"):
            print(file.title())
            f = open(file, encoding='utf-8')
            p = Parser(f.read())
            generateTree(p.ast)