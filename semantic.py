# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# lexer.py
# Analisador léxico para a linguagem Tinnny++
# Autores: Sávio Camacam
# -------------------------------------------------------------------------

from myparser import MyParser
import re

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
    return t.type in {'indice',
                      'expressao',
                      'declaracao',
                    #   'declaracao-funcao',
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
                      'atribuicao'}


def analysis(t):
    if t is not None:
        
        if t.type == 'program':
            for node in t.child:
                i = t.child.index(node)
        
        if t.type == 'declaracao-variaveis':
            parent = t.parent
            varType = t.child[0]
            value = t.child[1]
            if value.type == 'lista-variaveis':
                for node in value.child:
                    if node.value not in parent.scope.entries:
                        parent.scope.entries[node.value] = {}    
                        parent.scope.entries[node.value]['used'] = False
                        parent.scope.entries[node.value]['initialized'] = False
                        parent.scope.entries[node.value]['type'] = "variável"
                        parent.scope.entries[node.value]['varType'] = varType.value
                    else:
                        print("Erro: variável '" + node.value + "' já foi declarada")
            else:
                if value.value not in parent.scope.entries:
                    parent.scope.entries[value.value] = {}
                    parent.scope.entries[value.value]['used'] = False
                    parent.scope.entries[value.value]['initialized'] = False
                    parent.scope.entries[value.value]['type'] = "variável"
                    parent.scope.entries[value.value]['varType'] = varType.value
                else:
                    print("Erro: variável '" + value.value + "' já foi declarada")
           
        if t.type == 'var' and t.parent.type != 'lista-variaveis' and t.parent.type != 'declaracao-variaveis':
            initialized = False
            if t.parent.type == ":=":
                i = t.parent.child.index(t)
                
                if i == 0:
                    initialized = True
            parent = t.parent
            found = False
            while parent.type != 'program':
                if t.value in parent.scope.entries:
                    parent.scope.entries[t.value]['used'] = True
                    if not parent.scope.entries[t.value]['initialized']:
                        parent.scope.entries[t.value]['initialized'] = initialized
                    t.varType = parent.scope.entries[t.value]['varType']
                    found = True
                    break
                else:
                    parent = parent.parent
            if not found:
                print("Erro: Variável '" + t.value + "' usada não declarada")

        if t.type == 'declaracao-funcao':
            indice = -1
            if len(t.child) > 1:
                indice = 1
            else:
                indice = 0
            
            parent = t.parent
            while parent.type != "program":
                parent = parent.parent

            parent.scope.entries[t.child[indice].value] = {}
            parent.scope.entries[t.child[indice].value]['used'] = False
            parent.scope.entries[t.child[indice].value]['type'] = "função"
            parent.scope.entries[t.child[indice].value]['varType'] = t.child[0].value
            if len(t.child[indice].child) >= 1:
                retorno_pos = len(t.child[indice].child[1].child) - 1
                if retorno_pos > 0 and t.child[indice].child[1].child[retorno_pos].type != "retorna":
                    print("Erro: função '" + t.child[indice].value + "' deveria retornar um valor do tipo " + t.child[0].value)
                elif retorno_pos <= 0 and t.child[indice].child[1].type != "retorna":
                    print("Erro: função '" + t.child[indice].value + "' deveria retornar um valor do tipo " + t.child[0].value)
            else:
                print("Erro: função '" + t.child[indice].value  + "' deveria retornar um valor do tipo " + t.child[0].value)

        if t.type == 'chamada-funcao':
            parent = t.parent
            found = False
            while parent and parent.type != 'program':
                parent = parent.parent
            
            if t.value == "principal":
                print("Error: chamada para a função principal não permitida")
            elif t.value not in parent.scope.entries:
                print("Error: '" + t.value + "' é uma função usada e não declarada")
            else:
                parent.scope.entries[t.value]['used'] = True

        if t.type == 'parametro':
            parent = t.parent
            
            while parent.type != "cabecalho":
                parent = parent.parent
            parent.scope.entries[t.child[1].value] = {}
            parent.scope.entries[t.child[1].value]['used'] = False
            parent.scope.entries[t.child[1].value]['initialized'] = False
            parent.scope.entries[t.child[1].value]['type'] = "variável"
            parent.scope.entries[t.child[1].value]['varType'] = t.child[0].value

        if t.type == '+':
            if t.child[0] != None:
                analysis(t.child[0])
            if t.child[2] != None:
                analysis(t.child[2])
            if t.child[0].varType != t.child[2].varType:
                print("Warning: coerção implícita de valores entre '" + t.child[0].value + "' e '" + t.child[2].value + "'")

        if t.type == ':=':
            if t.child[0] != None:
                analysis(t.child[0])
            if t.child[2] != None:
                analysis(t.child[2])
            if t.child[0].varType != t.child[2].varType:
                print("Warning: coerção implícita de valores entre '" + t.child[0].value + "' e '" + t.child[2].value + "'")

        
        if t.type == 'numero':
            if re.match(r'[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?', t.value):
                t.varType = "flutuante"
            elif re.match(r'[0-9][0-9]*', t.value):
                t.varType = "inteiro"

        if t.type != ":=" and t.type != "+":
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


def buildPrunnedTree(t):
    if t is not None:
        if len(t.child) == 1 and is_in(t) and t.parent:
            i = t.parent.child.index(t)

            t.parent.child[i] = t.child[0]
            if(t.child[0]):
                t.child[0].parent = t.parent
                buildPrunnedTree(t.parent.child[i])

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
                buildPrunnedTree(t.child[i])

def verifyNotUsedVariables(tree):
    if tree is not None:
        if tree.type == "program":
            if "principal" not in tree.scope.entries:
                print("Error: função 'principal' não declarada")
        if tree.scope.entries:
            # print(tree.scope)
            pass
        for key in tree.scope.entries:
            if not tree.scope.entries[key]['used'] and key != "principal":
                print("Warning: "+ tree.scope.entries[key]['type'] +" '" + key + "' declarada e não usada")
            if tree.scope.entries[key]['type'] == "variável" and not tree.scope.entries[key]['initialized']:
                print("Warning: "+ tree.scope.entries[key]['type'] +" '" + key + "' não inicializada")
        for node in tree.child:
            i = tree.child.index(node)
            verifyNotUsedVariables(tree.child[i])


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
        buildPrunnedTree(s.tree)
        analysis(s.tree)
        verifyNotUsedVariables(s.tree)
        printPrunnedTree(s.tree)

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
            buildPrunnedTree(s.tree)
            print('\n>>\n')
            printPrunnedTree(s.tree)
