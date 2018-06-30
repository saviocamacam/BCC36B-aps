#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
#-------------------------------------------------------------------------
from parser import Parser

class Semantica:

    def __init__(self, code):
        self.tree = Parser(code)


class Tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):
        return self.type


def generatePrunedTree(t):
    if t is not None:
        if len(t.child) == 1 and len(t.child[0].child) == 1:
            generatePrunedTree(t.child[0].child[0])
        else:
            print('[' + t.type + ' ' + t.value)
            for node in t.child:
                i = t.child.index(node)
                generatePrunedTree(t.child[i])
        print(']')


if __name__ == '__main__':
    from sys import argv, exit

    config = 1
    if config:
        f = open(argv[1], encoding='utf-8')
        s = Semantica(f.read())
        generatePrunedTree(s.ast)

    else:
        import glob, os

        path = "C:/Users/savio/git/compiladores-march/testes"
        os.chdir(path)

        for file in glob.glob("*.tpp"):
            print(file.title())
            f = open(file, encoding='utf-8')
            s = Semantica(f.read())
            generatePrunedTree(s.tree)