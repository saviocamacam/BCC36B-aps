#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
#-------------------------------------------------------------------------
from parser import MyParser


class Semantica:

    def __init__(self, code):
        self.tree = MyParser(code).ast


class Tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):
        return self.type


def generatePrunedTree(t):
    if t is not None:
        if len(t.child) == 1 and t.type in {'indice',
                                            'expressao',
                                            'declaracao',
                                            'declaracao-funcao',
                                            'expressao-simples',
                                            'expressao-aditiva',
                                            'expressao-multiplicativa',
                                            'expressao-unaria',
                                            'fator',
                                            'lista-variaveis',
                                            'lista-declaracoes',
                                            'acao',
                                            'lista-parametros',
                                            'corpo',
                                            'lista-argumentos',
                                            'lista-dimensions',
                                            'inicializacao-variaveis',
                                            'atribuicao'}:
            generatePrunedTree(t.child[0])
        else:
            if(t.type and t.value):
                print('[' + t.value)
            else:
                print('[')
                if(t.type == 'atribuicao'):
                    print(':=')
                elif (t.type == 'expressao-aditiva'):
                    print(t.child[1].value)
                elif (t.type == 'operador_relacional'):
                    print(t.child[1].value)
                else:
                    print(t.type)
            for node in t.child:
                i = t.child.index(node)
                if(t.child[i].type not in {'operador-soma', 'simbolo-atribuicao', 'operador-relacional'}):
                    generatePrunedTree(t.child[i])
            print(']')


def printPrunnedTree(tree):
    if tree is not None:
        print('['+ tree.type + ' ' + tree.value)

        for node in tree.child:
            i = tree.child.index(node)
            printPrunnedTree(tree.child[i])
        print(']')


if __name__ == '__main__':
    from sys import argv, exit

    config = 1
    if config:
        f = open(argv[1], encoding='utf-8')
        s = Semantica(f.read())
        generatePrunedTree(s.tree)

        printPrunnedTree(s.tree)

    else:
        import glob, os

        path = "C:/Users/savio/git/compiladores-march/testes"
        os.chdir(path)

        for file in glob.glob("*.tpp"):
            print(file.title())
            f = open(file, encoding='utf-8')
            s = Semantica(f.read())
            generatePrunedTree(s.tree)