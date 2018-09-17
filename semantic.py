# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
# -------------------------------------------------------------------------

from myparser import MyParser


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


def is_in(t):
    if t.type in {'indice',
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
        return True
    else:
        return False


def analysis(t):
    if t is not None:
        if t.type == 'program':
            for node in t.child:
                i = t.child.index(node)

        for node in t.child:
            i = t.child.index(node)
            analysis(t.child[i])


def printIdealTree(t):
    if t is not None:
        if len(t.child) == 1 and is_in(t):
            printIdealTree(t.child[0])
        else:
            if t.type and t.value:
                print('[' + t.value)
            else:
                print('[')
                if t.type == 'atribuicao':
                    print(':=')
                elif t.type == 'expressao-aditiva':
                    print(t.child[1].value)
                elif t.type == 'operador_relacional':
                    print(t.child[1].value)
                elif t.type == 'expressao-unaria':
                    if(t.child[0].type == 'operador-soma' and t.child[0].value == '+'):
                        print('+')
                    elif (t.child[0].type == 'operador-soma' and t.child[0].value == '-'):
                        print('-')
                else:
                    print(t.type)
            for node in t.child:
                i = t.child.index(node)
                if t.child[i].type not in {'operador-soma', 'simbolo-atribuicao', 'operador-relacional'}:
                    printIdealTree(t.child[i])
            print(']')


def alingmentOfChilds(node, name):
    newChild = []
    newChild.append(node.child[1])
    node = node.child[0]
    while len(node.child) == 2 and node.type == name:
        node.child[1].parent = node
        newChild.append(node.child[1])
        node = node.child[0]
    node.child[0].parent = node
    newChild.append(node.child[0])
    newChild.reverse()
    node.child = newChild
    # for node in t.child:
    #    print(node.parent.type)


def buildPrunnetTree(t):
    if t is not None:
        if len(t.child) == 1 and is_in(t) and t.parent:
            i = t.parent.child.index(t)

            t.parent.child[i] = t.child[0]
            if(t.child[0]):
                t.child[0].parent = t.parent
                buildPrunnetTree(t.parent.child[i])

        else:
            if t.type == 'corpo':
                newChild = []
                newChild.append(t.child[1])
                node = t.child[0]
                while len(node.child) == 2 and node.type == 'corpo':
                    node.child[1].parent = t
                    newChild.append(node.child[1])
                    node = node.child[0]
                node.child[0].parent = t
                newChild.append(node.child[0])
                newChild.reverse()
                t.child = newChild
            elif t.type == 'indice':
                newChild = []
                newChild.append(t.child[1])
                node = t.child[0]
                while len(node.child) == 2 and node.type == 'indice':
                    node.child[1].parent = t
                    newChild.append(node.child[1])
                    node = node.child[0]
                node.child[0].parent = t
                newChild.append(node.child[0])
                newChild.reverse()
                t.child = newChild
            elif t.type == 'lista-dimensions':
                newChild = []
                newChild.append(t.child[1])
                node = t.child[0]
                while len(node.child) == 2 and node.type == 'lista-dimensions':
                    node.child[1].parent = t
                    newChild.append(node.child[1])
                    node = node.child[0]
                node.child[0].parent = t
                newChild.append(node.child[0])
                newChild.reverse()
                t.child = newChild
            elif t.type == 'lista-argumentos':
                newChild = []
                newChild.append(t.child[1])
                node = t.child[0]
                while len(node.child) == 2 and node.type == 'lista-argumentos':
                    node.child[1].parent = t
                    newChild.append(node.child[1])
                    node = node.child[0]
                node.child[0].parent = t
                newChild.append(node.child[0])
                newChild.reverse()
                t.child = newChild
            elif t.type == 'lista-parametros':
                newChild = []
                newChild.append(t.child[1])
                node = t.child[0]
                while len(node.child) == 2 and node.type == 'lista-parametros':
                    node.child[1].parent = t
                    newChild.append(node.child[1])
                    node = node.child[0]
                node.child[0].parent = t
                newChild.append(node.child[0])
                newChild.reverse()
                t.child = newChild
            elif t.type == 'lista-declaracoes':
                newChild = []
                newChild.append(t.child[1])
                node = t.child[0]
                while len(node.child) == 2 and node.type == 'lista-declaracoes':
                    node.child[1].parent = t
                    newChild.append(node.child[1])
                    node = node.child[0]
                node.child[0].parent = t
                newChild.append(node.child[0])
                newChild.reverse()
                t.child = newChild
            elif t.type == 'lista-variaveis':
                newChild = []
                newChild.append(t.child[1])
                node = t.child[0]
                while len(node.child) == 2 and node.type == 'lista-variaveis':
                    node.child[1].parent = t
                    newChild.append(node.child[1])
                    node = node.child[0]
                node.child[0].parent = t
                newChild.append(node.child[0])
                newChild.reverse()
                t.child = newChild

            elif t.type == 'atribuicao':
                t.type = ':='
            elif t.type == 'expressao-aditiva':
                t.type = t.child[1].value
            elif t.type == 'operador_relacional':
                t.type = t.child[1].value

            elif t.type == 'expressao-unaria':
                if(t.child[0].type == 'operador-soma' and t.child[0].value == '+'):
                    t.type = '+'
                elif (t.child[0].type == 'operador-soma' and t.child[0].value == '-'):
                    t.type = '-'

            for node in t.child:
                i = t.child.index(node)
                if t.child[i] and t.child[i].type in {'operador-soma', 'simbolo-atribuicao', 'operador-relacional'}:
                    t.child[i] = None
                buildPrunnetTree(t.child[i])


def printPrunnedTree(tree):
    if tree is not None:
        if tree.type and tree.value:
            print('[' + tree.value)
        else:
            print('[' + tree.type + ' ' + tree.value)

        for node in tree.child:
            i = tree.child.index(node)
            printPrunnedTree(tree.child[i])
        print(']')


if __name__ == "__main__":
    from sys import argv, exit
    import sys
    from io import StringIO

    config = 1
    if config:
        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result

        f = open(argv[1], encoding='utf-8')
        s = Semantica(f.read())
        # printIdealTree(s.tree)
        # print('\n>>\n')
        buildPrunnetTree(s.tree)
        printPrunnedTree(s.tree)
        # analysis(s.tree)

        sys.stdout = old_stdout
        result_string = result.getvalue()
        # result_string = result_string.replace('\n', '')
        # result_string = result_string.replace('\t', '')
        print(result_string)

        # s.newTree = buildPrunedTreeFromString(result_string)

    else:
        import glob
        import os

        path = "C:/Users/savio/git/compiladores-march/testes"
        os.chdir(path)

        for file in glob.glob("*.tpp"):
            print(file.title())
            f = open(file, encoding='utf-8')
            s = Semantica(f.read())
            buildPrunnetTree(s.tree)
            print('\n>>\n')
            printPrunnedTree(s.tree)
