from semantic import Semantica
from llvmlite import ir

types = {
    "inteiro": ir.IntType,
    "flutuante": ir.FloatType,
    int: ir.IntType,
    float: ir.FloatType,
    None: ir.VoidType
}

linkage = "common"
align = 4


class Generator:
    def __init__(self, code, filename):
        self.builder = None
        self.tree = Semantica(code).tree
        self.module = ir.Module(filename + ".tpp")
        self.Zero32 = ir.Constant(ir.IntType(32), 0)
        self.Zero32F = ir.Constant(ir.FloatType(), 0.0)

        _escrevaI = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
        self.escrevaI = ir.Function(self.module, _escrevaI, "escrevaInteiro")

        _escrevaF = ir.FunctionType(ir.VoidType(), [ir.FloatType()])
        self.escrevaF = ir.Function(self.module, _escrevaF, "escrevaFlutuante")

        _leiaI = ir.FunctionType(ir.IntType(32), [])
        self.leiaI = ir.Function(self.module, _leiaI, "leiaInteiro")

        _leiaF = ir.FunctionType(ir.FloatType(), [])
        self.leiaF = ir.Function(self.module, _leiaF, "leiaFlutuante")
        self.gen(self.tree)
        self.save_module(filename)

    def save_module(self, filename):
        with open(filename + ".ll", "w") as f:
            f.write(str(self.module))

    def pre_gen(self, t):
        return t.type in {'declaracao-funcao', 'se', '>', '<', '>=', '<=', '<>', '=', '+', '-', '*', '/', ':=', 'repita', 'retorna', 'chamada-funcao', 'escreva'}

    def gen(self, t):
        if t is not None:
            if t.type == 'declaracao-variaveis':
                if t.parent.type == 'lista-declaracoes':
                    varType = t.child[0]
                    value = t.child[1]

                    _type = types[varType.value]
                    var_type = _type() if _type == ir.FloatType else _type(32)

                    

                    if value.type == 'lista-variaveis':
                        for node in value.child:
                            
                            if node.child[0].type == "indice":
                                var_type = ir.ArrayType(ir.IntType(64), node.child[0].value)

                            llvm_var = ir.GlobalVariable(
                                self.module, var_type, node.value)
                            llvm_var.initializer = ir.Constant(
                                var_type, 0.0 if _type == ir.FloatType else 0)
                            llvm_var.align = align
                            t.parent.scope.entries[node.value]['llvm'] = llvm_var
                    else:
                        if value.child and value.child[0].type == "numero":
                            var_type = ir.ArrayType(ir.IntType(64), int(value.child[0].value))

                        llvm_var = ir.GlobalVariable(
                            self.module, var_type, value.value)
                        if value.child and value.child[0].type == "numero":
                            llvm_var.initializer = ir.Constant(ir.IntType(64), 0)
                            llvm_var.align = 16
                        else:
                            llvm_var.initializer = ir.Constant(
                                var_type, 0.0 if _type == ir.FloatType else 0)
                            llvm_var.align = align
                        t.parent.scope.entries[value.value]['llvm'] = llvm_var

                if t.parent.type == 'corpo':
                    varType = t.child[0]
                    value = t.child[1]

                    _type = types[varType.value]
                    var_type = _type() if _type == ir.FloatType else _type(32)

                    if value.type == 'lista-variaveis':
                        for node in value.child:
                            llvm_var = self.builder.alloca(
                                var_type, name=node.value)
                            llvm_var.initializer = ir.Constant(
                                var_type, 0.0 if _type == ir.FloatType else 0)
                            llvm_var.align = align
                            t.parent.scope.entries[node.value]['llvm'] = llvm_var
                    else:
                        if value.child and value.child[0].type == "numero":
                            var_type = ir.ArrayType(ir.IntType(64), int(value.child[0].value))
                        llvm_var = self.builder.alloca(
                            var_type, name=value.value)
                        llvm_var.initializer = ir.Constant(
                            var_type, 0.0 if _type == ir.FloatType else 0)
                        llvm_var.align = align
                        t.parent.scope.entries[value.value]['llvm'] = llvm_var

            if t.type == 'declaracao-funcao':
                indice = -1
                if len(t.child) > 1:
                    indice = 1
                    varType = t.child[0]
                    _type = types[varType.value]
                    var_type = _type() if _type == ir.FloatType else _type(32)
                    zero = ir.Constant(
                        var_type, 0.0 if _type == ir.FloatType else 0)
                    t_func = ir.FunctionType(var_type, ())
                    name = t.child[1].value
                    if t.child[1].value == "principal":
                        name = "main"
                    func = ir.Function(self.module, t_func,
                                       name=name)

                    parent = t.parent
                    while parent.type != "program":
                        parent = parent.parent

                    parent.scope.entries[t.child[indice].value]['llvm'] = func

                    entry_block = func.append_basic_block(
                        'entry-' + t.child[1].value)
                    end_block = func.append_basic_block(
                        'exit-' + t.child[1].value)
                    self.builder = ir.IRBuilder(entry_block)
                    returnVal = self.builder.alloca(
                        var_type, name='retorno')
                    self.builder.store(zero, returnVal)
                    

                    parent.scope.entries[t.child[indice].value]['return'] = returnVal
                    func_params = []
                    if t.child[indice].child[0] and t.child[indice].child[0].type == "lista-parametros":
                        # print(t.child[indice].scope.entries)
                        for child in t.child[indice].child[0].child:
                            _type = types[child.child[0].value]
                            param_type = _type() if _type == ir.PointerType(ir.FloatType()) else ir.PointerType(_type(32))
                            arg = ir.Argument(
                                func, param_type, child.child[1].value)
                            func_params.append(arg)
                            t.child[indice].scope.entries[child.child[1].value]["llvm"] = arg

                        func.args = func_params

                    self.gen(t.child[indice])
                    retorno = t.child[indice].child[-1]
                    if retorno.type == "corpo":
                        retorno = retorno.child[-1]
                    # print(retorno)
                    # self.builder.store(retorno.llvm, returnVal)
                    self.builder.branch(end_block)
                    self.builder = ir.IRBuilder(end_block)
                    self.builder.ret(self.builder.load(returnVal, "retFin"))
                else:
                    indice = 0

            if t.type == "retorna":
                parent = t.parent
                while parent.type != "cabecalho":
                    parent = parent.parent

                function_repita = parent.value

                while parent.type != "program":
                    parent = parent.parent

                ret = parent.scope.entries[function_repita]['return']
                self.gen(t.child[0])
                t.llvm = t.child[0].llvm
                # print(t.llvm)
                # print(t.child[0].value)
                
                if t.child[0].type == "var":
                    parent = t.parent
                    while parent.type != 'program':
                        if t.child[0].value in parent.scope.entries:
                            t.llvm = parent.scope.entries[t.child[0].value]['llvm']
                            t.llvm = self.builder.load(t.llvm, name="temp-")
                            break
                        else:
                            parent = parent.parent
                # print(t.llvm)
                self.builder.store(t.llvm, ret)
                

            if t.type == 'numero':
                _type = types[t.varType]
                num_type = _type() if _type == ir.FloatType else _type(32)
                if t.varType == 'inteiro':
                    num = ir.Constant(num_type, int(t.value))
                    t.llvm = num
                elif t.varType == 'flutuante':
                    num = ir.Constant(num_type, float(t.value))
                    t.llvm = num

            if t.type == '>' or t.type == '<' or t.type == '>=' or t.type == '<=' or t.type == '<>' or t.type == '=':
                self.gen(t.child[0])
                self.gen(t.child[2])
                left_side = t.child[0]
                right_side = t.child[2]
                if t.child[0].type == "var":
                    left_side.llvm = self.builder.load(
                        t.child[0].llvm, name=t.child[0].value)
                if t.child[2].type == "var":
                    right_side.llvm = self.builder.load(
                        t.child[2].llvm, name=t.child[2].value)

                symbol = t.type
                if symbol == "<>":
                    symbol = "!="
                elif symbol == "=":
                    symbol = "=="
                exp = self.builder.icmp_signed(
                    symbol, left_side.llvm, right_side.llvm, name='exp-test')
                t.llvm = exp

            if t.type == "repita":

                parent = t.parent
                while parent.type != "cabecalho":
                    parent = parent.parent

                function_repita = parent.value

                while parent.type != "program":
                    parent = parent.parent

                llvm = parent.scope.entries[function_repita]['llvm']

                loop = llvm.append_basic_block("repita-loop")
                test = llvm.append_basic_block("test-loop")
                end = llvm.append_basic_block("end")

                self.builder.branch(loop)
                self.builder.position_at_end(loop)
                self.gen(t.child[0])
                self.builder.branch(test)

                self.builder.position_at_end(test)
                self.gen(t.child[1])

                self.builder.cbranch(t.child[1].llvm, loop, end)
                self.builder.position_at_end(end)

            if t.type == "escreva":
                self.gen(t.child[0])
                value = t.child[0]
                # print(value.type)
                temp = None
                if value.type == "var":
                    temp = self.builder.load(value.llvm,name="write" + value.value)
                else:
                    temp = value.llvm
                self.builder.call(self.escrevaI if value.varType == "inteiro" else self.escrevaF, [temp])

            if t.type == "leia":
                self.gen(t.child[0])
                res = None
                if t.child[0].varType == "inteiro":
                    res = self.builder.call(self.leiaI, [],name="readI" + t.child[0].value)
                elif t.child[0].varType == "flutuante":
                    res = self.builder.call(self.leiaF, [],name="readF" + t.child[0].value)
                self.builder.store(res, t.child[0].llvm)

            if t.type == "chamada-funcao":
                # print(t.value)
                self.gen(t.child[0])
                params = []
                for child in t.child[0].child:
                    params.append(child.llvm)
                    
                # print(t.child[0].llvm)
                # print(t.child[0].varType)
                
                parent = t.parent
                while parent.type != "program":
                    parent = parent.parent

                llvm = parent.scope.entries[t.value]['llvm']
                ret = self.builder.call(llvm, params, name="retorno-" + t.value)
                # print(ret)

                t.llvm = ret
            

            if t.type == 'se':
                parent = t.parent
                while parent.type != "cabecalho":
                    parent = parent.parent

                function_se = parent.value

                while parent.type != "program":
                    parent = parent.parent

                llvm = parent.scope.entries[function_se]['llvm']

                if_true = llvm.append_basic_block('if_true')
                if_false = llvm.append_basic_block('if_false')
                if_end = llvm.append_basic_block('if_end')

                self.gen(t.child[0])
                print(t.child[0])
                self.builder.cbranch(t.child[0].llvm, if_true, if_false)
                self.builder.position_at_end(if_true)
                self.gen(t.child[1])
                self.builder.branch(if_end)

                self.builder.position_at_end(if_false)
                if len(t.child) == 3:
                    self.gen(t.child[2])
                self.builder.branch(if_end)

                self.builder.position_at_end(if_end)

            if t.type == 'var':
                parent = t.parent
                while parent.type != 'program':
                    if t.value in parent.scope.entries:
                        t.llvm = parent.scope.entries[t.value]['llvm']
                        
                        if t.child and  t.child[0].type == "numero":
                            if self.builder:
                                int_ty = ir.IntType(64)
                                t.llvm = self.builder.gep(t.llvm, [int_ty(0), int_ty(int(t.child[0].value))], name='ptr_' + t.value + "_" + t.child[0].value)
                                t.llvm = self.builder.load(t.llvm, "teste")
                            
                        break
                    else:
                        parent = parent.parent

            if t.type == "+" or t.type == "-" or t.type == "*" or t.type == "/":
                self.gen(t.child[0])
                self.gen(t.child[2])
                left_side = t.child[0]
                right_side = t.child[2]

                if t.child[0].type != "numero":
                    left_side.llvm = self.builder.load(
                        t.child[0].llvm, "left_side")

                if t.child[2].type != "numero":
                    right_side.llvm = self.builder.load(
                        t.child[2].llvm, "right_side")

                temp = None
                if t.type == "+":
                    temp = self.builder.add(
                        left_side.llvm, right_side.llvm, name='temp' + t.type)
                    t.llvm = temp
                elif t.type == "-":
                    temp = self.builder.sub(
                        left_side.llvm, right_side.llvm, name='temp' + t.type)
                    t.llvm = temp
                elif t.type == "*":
                    temp = self.builder.mul(
                        left_side.llvm, right_side.llvm, name='temp' + t.type)
                    t.llvm = temp
                elif t.type == "/":
                    temp = self.builder.sdiv(
                        left_side.llvm, right_side.llvm, name='temp' + t.type)
                    t.llvm = temp

            if t.type == ":=":
                self.gen(t.child[0])
                self.gen(t.child[2])
                print(t.child[0])
                print(t.child[2].value)
                
                right_side = t.child[2]
                if right_side.llvm:
                    if right_side.type == 'var':
                        right_side.llvm = self.builder.load(
                            right_side.llvm, "right_side")
                    self.builder.store(right_side.llvm, t.child[0].llvm)

            if t.scope.entries:
                # print(t)
                # print(t.scope.entries)
                pass

            if not self.pre_gen(t):
                for node in t.child:
                    i = t.child.index(node)
                    self.gen(t.child[i])


def printScopeDetails(tree):
    if tree is not None:
        print(tree.scope)
        for node in tree.child:
            i = tree.child.index(node)
            printScopeDetails(tree.child[i])


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
        filename = argv[1]
        f = open(filename, encoding='utf-8')
        filename = filename[:-4]
        g = Generator(f.read(), filename)
        # printPrunnedTree(g.tree)

    else:
        import glob
        import os

        path = "C:/Users/savio/git/compiladores-march/testes"
        os.chdir(path)

        for file in glob.glob("*.tpp"):
            print(file.title())
            f = open(file, encoding='utf-8')
            s = Semantica(f.read())
            # buildPrunnedTree(s.tree)
            print('\n>>\n')
            # printPrunnedTree(s.tree)
