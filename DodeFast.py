from sly import Lexer as Lexer
from sly import Parser as Parser
from SocketClient import *
import random
class BasicLexer(Lexer):

    tokens = { DECLARATION, ASSIGNATION, ENCASO, CUANDO, PRINT, ENTONS, SINO, FINENCASO, VAR, INT,
                SEMI, LBRACK, RBRACK, GREATEREQ, LESSEREQ, EQ, GREATER, LESSER,
                MINUS, TWO_POINTS, INICIO, FINAL, PROC, LLAMAR,
                INC, DEC, INI, PARENTHESIS_LEFT, PARENTHESIS_RIGHT, COMA, MOVER, ALEATORIO,
                 REPITA, HASTAENCONTRAR, DESDE, HASTA, HAGA, FINDESDE,AF,F,DFA,IFA,DFB,IFB,A,
                 DAA,IAA,DAB,IAB,AA}

    ignore = " \t"

#----Simbolos------
    SEMI = r";"
    LBRACK = r"{"
    RBRACK = r"}"
    EQ = r"="
    GREATEREQ = r">="
    LESSEREQ = r"<="
    GREATER = r">"
    LESSER = r"<"
    MINUS = r"-"
    COMA = r","
    PARENTHESIS_LEFT = r"\("
    PARENTHESIS_RIGHT = r"\)"
    TWO_POINTS = r":"

#----Movimientos---

    AF = r'AF'
    F = r'F'
    DFA = r'DFA'
    IFA = r'IFA'
    DFB = r'DFB'
    IFB = r'IFB'
    A  = r'A'
    DAA = r'DAA'
    IAA = r'IAA'
    DAB = r'DAB'
    IAB = r'IAB'
    AA = r'AA'

#----Palabras------
    INICIO = r'Inicio'
    FINAL = r'Final'
    INC = r'Inc'
    DEC = r'Dec'
    INI = r'Ini'
    MOVER = r'Mover'
    ALEATORIO = r'Aleatorio'
    PROC = r'Proc'
    LLAMAR = r'Llamar'
    DECLARATION = r"DCL"
    ASSIGNATION = "DEFAULT"
    ENCASO = r"EnCaso"
    CUANDO = r"Cuando"
    ENTONS = r"Entons"
    SINO = r"SiNo"
    FINENCASO = r"Fin-EnCaso"
    REPITA = 'Repita'
    HASTAENCONTRAR ='HastaEncontrar'
    DESDE = 'Desde'
    HASTA = 'Hasta'
    HAGA = 'Haga'
    FINDESDE= 'Fin-Desde'
    PRINT = "Print"
    VAR = r"[a-zA-Z_][a-zA-Z0-9_@#]*"


    @_(r"\d+")
    def INT(self, t):
        t.value = int(t.value)
        return t

class BasicParser(Parser):
    tokens = BasicLexer.tokens

    X = 0

    def __init__(self):
        self.env = { }

    @_('expr SEMI')
    def statement(self,p):
        return (p.expr)

    @_('INICIO TWO_POINTS LBRACK Bloque RBRACK FINAL SEMI DecFunc')
    def statement(self,p):
        return ("inicio", p.DecFunc, p.Bloque)

    @_('declaracion Bloque')
    def Bloque(self,p):
        return ["multStatements", p.declaracion] + [p.Bloque]

    @_('expr SEMI')
    def declaracion(self, p):
        return (p.expr)

    @_('var_assign')
    def declaracion(self, p):
        return p.var_assign

    @_('func_call Bloque')
    def Bloque(self,p):
      return ["multStatements", p.func_call] + [p.Bloque]

    @_('')
    def Bloque(self,p):
      pass

    @_('Proc_dec SEMI DecFunc')
    def DecFunc(self,p):
        print("afhj")
        return ['multi_proc', p.Proc_dec] + [p.DecFunc]

    @_('')
    def DecFunc(self,p):
        pass

    @_('PROC VAR PARENTHESIS_LEFT Parametros PARENTHESIS_RIGHT LBRACK func_Bloque RBRACK')
    def Proc_dec(self,p):
        parametros = p.Parametros
        return ('proc_def', p.VAR, parametros, p.func_Bloque)

    @_('parametro Parametros')
    def Parametros(self,p):
        return ["parametros",p.parametro] + p.Parametros

    @_('COMA parametro Parametros')
    def Parametros(self,p):
        return [p.parametro] + p.Parametros

    @_('')
    def Parametros(self,p):
        return []

    @_('expr')
    def parametro(self,p):
        return p.expr

    @_('func_Dec INICIO TWO_POINTS LBRACK func_expr RBRACK FINAL SEMI')
    def func_Bloque(self,p):
        return

    @_('var_assign func_Dec')
    def func_Dec(self,p):
        return

    @_('')
    def func_Dec(self,p):
        pass

    @_('funciones func_expr')
    def func_expr(self,p):
        return

    @_('loops func_expr')
    def func_expr(self,p):
        return

    @_('')
    def func_expr(self,p):
      pass

    @_('Ini')
    def funciones(self,p):
      return p.Ini

    @_('Inc')
    def funciones(self,p):
        return p.Inc

    @_('Dec')
    def funciones(self,p):
        return p.Dec

    @_('Mover')
    def funciones(self,p):
      return p.Mover

    @_('Aleatorio')
    def funciones(self,p):
      return p.Aleatorio

    @_('Condicion')
    def funciones(self,p):
      return p.Condicion

    @_('EnCasoA')
    def Condicion(self,p):
      return p.EnCasoA

    @_('EnCasoB')
    def Condicion(self,p):
      return p.EnCasoB

    @_('Repita')
    def loops(self,p):
      return p.Repita

    @_('Desde')
    def loops(self,p):
      return p.Desde

    @_('REPITA LBRACK func_expr RBRACK HASTAENCONTRAR Evaluation SEMI')
    def Repita(self,p):
        return ('while_loop', p.statement, p.Evaluation)

    @_('DESDE var EQ expr HASTA expr HAGA LBRACK func_expr RBRACK FINDESDE SEMI')
    def Desde(self, p):
        return ('for_loop', p.var, p.expr0, p.expr1, p.statement)


    @_('INC PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def Inc(self, p):
        return ('fun_call', p.INC, p.var, p.expr)

    @_('DEC PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def Dec(self, p):
        return ('fun_call', p.DEC, p.var, p.expr)

    @_('INI PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def Ini(self, p):
        return ('fun_call', p.INI, p.var, p.expr)

    @_('MOVER PARENTHESIS_LEFT movimientos PARENTHESIS_RIGHT')
    def Mover(self, p):
        return ('fun_call', p.MOVER, p.movimientos)

    @_('ALEATORIO PARENTHESIS_LEFT PARENTHESIS_RIGHT')
    def Aleatorio(self, p):
        return ('fun_call', p.ALEATORIO)

    @_('ENCASO CuandoA SiNo FINENCASO SEMI')
    def EnCasoA(self, p):
        return ("EnCasoA", p.CuandoA, p.SiNo)

    @_('ENCASO var CuandoC SiNo FINENCASO SEMI')
    def EnCasoB(self,p):
        self.X = p.var
        print(self.X)
        tree = ["EnCasoB", p.CuandoC, p.SiNo]
        tree[1][0][1][1] = self.X
        return tree

    @_('CuandoB CuandoA')
    def CuandoA(self, p):
        return [p.CuandoB] + p.CuandoA

    @_('CuandoB')
    def CuandoA(self, p):
        return [p.CuandoB]

    @_('CUANDO Evaluation Entons')
    def CuandoB(self, p):
        return ("Cuando",p.Evaluation, p.Entons)


    @_('CuandoD CuandoC')
    def CuandoC(self, p):
        return [p.CuandoD] + p.CuandoC

    @_('CuandoD')
    def CuandoC(self, p):
        return [p.CuandoD]

    @_('CUANDO EvaluationB Entons')
    def CuandoD(self, p):
        return ["Cuando", p.EvaluationB, p.Entons]

    @_('var Cond expr')
    def Evaluation(self,p):
        return(p.Cond, p.var, p.expr)

    @_('Cond expr')
    def EvaluationB(self,p):
        return [p.Cond, self.X, p.expr]


    @_('ENTONS LBRACK func_expr RBRACK')
    def Entons(self, p):
        return p.statement

    @_('SINO LBRACK func_expr RBRACK')
    def SiNo(self, p):
        return ("SiNo", p.statement)

    @_('EQ')
    def Cond(self, p):
        return "Equals"

    @_('GREATEREQ')
    def Cond(self, p):
        return "GreaterEq"

    @_('LESSEREQ')
    def Cond(self, p):
        return "LesserEq"

    @_('GREATER')
    def Cond(self, p):
        return "Greater"

    @_('LESSER')
    def Cond(self, p):
        return "Lesser"

    @_('DECLARATION VAR ASSIGNATION expr SEMI')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.expr)

    @_('DECLARATION VAR SEMI')
    def var_assign(self, p):
        return ('var_assign', p.VAR, 0)

    @_('INT')
    def expr(self, p):
        return ('num', p.INT)

    @_('MINUS INT')
    def expr(self, p):
        return ('num', -1*p.INT)

    @_('VAR')
    def expr(self, p):
        return ('var', p.VAR)

    @_('VAR')
    def var(self, p):
        return ('var', p.VAR)

    @_('AF')
    def movimientos(self,p):
        return p.AF
    @_('A')
    def movimientos(self,p):
        return p.AF
    @_('F')
    def movimientos(self,p):
        return p.AF
    @_('IFA')
    def movimientos(self, p):
        return p.AF
    @_('DFA')
    def movimientos(self, p):
        return p.AF
    @_('DFB')
    def movimientos(self, p):
        return p.AF
    @_('IFB')
    def movimientos(self, p):
        return p.AF
    @_('DAA')
    def movimientos(self, p):
        return p.AF
    @_('IAA')
    def movimientos(self, p):
        return p.AF
    @_('DAB')
    def movimientos(self, p):
        return p.AF
    @_('IAB')
    def movimientos(self, p):
        return p.AF
    @_('AA')
    def movimientos(self, p):
        return p.AF


    #Cambiar a funcDef
    #@_('PROC VAR PARENTHESIS_LEFT PARENTHESIS_RIGHT INICIO TWO_POINTS statement FINAL SEMI')
    #def sentencia(self, p):
    #    return ('process_def', p.VAR, p.statement)
    #Cambiar a funcDef
    #@_('PROC VAR PARENTHESIS_LEFT expr PARENTHESIS_RIGHT INICIO TWO_POINTS statement FINAL SEMI')
    #def sentencia(self, p):
    #    return ('process_def_parameters', p.VAR, p.expr, p.statement)

    @_('LLAMAR VAR PARENTHESIS_LEFT Parametros PARENTHESIS_RIGHT')
    def func_call(self, p):
        return ('process_call', p.VAR, p.Parametros)

    def error(self, p):
        return ("error", "Parsing Error! Maybe you mixed the order or misspelled something")

class BasicExecute:

    def __init__(self, env):
        self.env = env
        self.ip = 0


    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] ==  "inicio":
            self.walkTree(node[1])
            self.walkTree(node[2])

        if node[0] == "multStatements":
            result = []
            for i in range(1, len(node)):
                res = self.walkTree(node[i])
                result.append(res)

            return result

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == "error":
            return node[1]

        if node[0] == 'EnCasoA':


            for i in range(len(node[1])):
                result = self.walkTree(node[1][i])
                if result:
                    return self.walkTree(node[1][i][2])
                    break

            return self.walkTree(node[len(node)-1])

        if node[0] == 'EnCasoB':

            for i in range(len(node[1])):
                result = self.walkTree(node[1][i])
                if result:
                    return self.walkTree(node[1][i][2])
                    break

            return self.walkTree(node[len(node)-1])


        if node[0] == "Cuando":
            return self.walkTree(node[1])

        if node[0] == "print":
            return ("print", self.walkTree(node[1]))

        if node[0] == "SiNo":
            return self.walkTree(node[1])

        if node[0] == 'Equals':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == "Greater":
            try:
                return self.walkTree(node[1]) > self.walkTree(node[2])
            except:
                return("Error in comparation. Check if the data types are comparable.")

        if node[0] == "Lesser":
            try:
                return self.walkTree(node[1]) < self.walkTree(node[2])
            except:
                return("Error in comparation. Check if the data types are comparable.")

        if node[0] == "LesserEq":
            try:
                return self.walkTree(node[1]) <= self.walkTree(node[2])
            except:
                return("Error in comparation. Check if the data types are comparable.")
        if node[0] == "GreaterEq":
            try:
                return self.walkTree(node[1]) >= self.walkTree(node[2])
            except:
                return "Error in comparation. Check if the data types are comparable."

        if node[0] == 'fun_call':
            if node[1] == 'Inc':
                self.env[node[2][1]] = self.walkTree(node[2]) + self.walkTree(node[3])
                return(self.env[node[2][1]])
            elif node[1] == 'Dec':
                self.env[node[2][1]] = self.walkTree(node[2]) - self.walkTree(node[3])
                return(self.env[node[2][1]])
            elif node[1] == 'Ini':
                self.env[node[2][1]] = self.walkTree(node[3])
                return(self.env[node[2][1]])
            elif node[1] == 'Mover':
                HOST = ""
                PORT = 0
                sendData(node[2].encode(), HOST, PORT)
            elif node[1] == 'Aleatorio':

                movimientos = ['AF','F','DFA','IFA','DFB','IFB'
                                ,'A','DAA','IAA','DAB','IAB','AA']
                movimiento = random.choice(movimientos)
                sendData(movimiento.encode())

            else:
                return("Function not defined")

        if node[0] == 'process_def':
            if 'var_assign' in node[2]:
                print("After Inicio:, only expressions are allowed, which represent any element of the language, with the exception of the declaration of variables.")
            else:
                self.env[node[1]] = node[2]

        if node[0] == 'process_call':
            try:
                return self.walkTree(self.env[node[1]])
            except:
                print("The called function is not defined")

        if node[0] == 'proc_def':
            pass

        if node[0] == 'process_def_parameters':
            if 'var_assign' in node[3]:
                print("After Inicio:, only expressions are allowed, which represent any element of the language, with the exception of the declaration of variables.")
            else:
                if node[2] in node[3]:
                    self.env[node[1]] = tuple([node[3],node[2]])
                    print("Se guardo")
                else:
                    print("Error, the defined procedure does not use the set parameter")

        if node[0] == 'process_call_parameters':
            try:
                x = list(self.env[node[1]])
                y = list(x[0])
                z = x[1]
                cont = 0
                while z != y[cont]:
                    cont+=1
                y[cont] = node[2]
                return self.walkTree(tuple(y))
            except:
                print("The called function is not defined")


        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return "Undefined variable '"+node[1]+"' found!"
        if node[0]== 'while_loop':
            loop_sentence = node[1][1]
            loop_setup = self.walkTree(node[2])
            val= node[2][1][1]
            i= self.walkTree(node[2][1])
            print (i)
            while True:
                #self.walkTree(loop_sentence)
                print(node[1])
                self.walkTree(node[1])
                if self.walkTree(node[2]):
                    print ("Se cumple la condición")
                    break
                #i+=1
                #del env[node[2][1][1]]
                #self.env[val] = i


        if node[0] == 'for_loop':
            #return ('for_loop', p.var, p.expr, p.expr, p.statement)
            try:
                tempKey = node[1][1]
                tempVal = self.env[node[1][1]]
            except:
                pass

            self.env[node[1][1]] = node[2][1]

            try:
                loop_count = self.env[node[2][0]]
            except:
                loop_count = node[2][1]

            val = node[2][0]
            print(val)
            loop_limit = node[3][1]
            res = self.walkTree(node[2])
            for i in range(loop_count+1, loop_limit+1):
                self.env[node[1][1]] = self.env[node[1][1]] + 1
                if res is not None:
                    self.walkTree(node[4])

            del self.env[node[1][1]]
            try:
                self.env[tempKey] = tempVal
            except:
                pass
#----------------------Lexing run--------------------

if __name__ == '__main__':
    lexer = BasicLexer()
    env = {}
    while True:
        try:
            text = input('DodeFast >>> ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
'''
#--------------------Parsing run----------------------

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('DodeFast >>> ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
'''
"""
#---------------------Full run-----------------------

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('DodeFast >>> ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            tree = parser.parse(lex)
            BasicExecute(tree, env)
#            print(tree)
"""
