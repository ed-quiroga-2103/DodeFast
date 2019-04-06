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

#----Movimientos---

    AF = 'AF_Mov'
    F = 'F_Mov'
    DFA = 'DFA_Mov'
    IFA = 'IFA_Mov'
    DFB = 'DFB_Mov'
    IFB = 'IFB_Mov'
    A  = 'A_Mov'
    DAA = 'DAA_Mov'
    IAA = 'IAA_Mov'
    DAB = 'DAB_Mov'
    IAB = 'IAB_Mov'
    AA = 'AA_Mov'

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
        return [p.func_Dec, ["proc_func"]+p.func_expr]

    @_('var_assign func_Dec')
    def func_Dec(self,p):
        return [p.var_assign] + p.func_Dec

    @_('')
    def func_Dec(self,p):
        return []

    @_('funciones func_expr')
    def func_expr(self,p):
        return [p.funciones] + p.func_expr

    @_('loops func_expr')
    def func_expr(self,p):
        return [p.loops] + p.func_expr

    @_('')
    def func_expr(self,p):
      return []

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
        return ('while_loop', p.func_expr, p.Evaluation)

    @_('DESDE var EQ expr HASTA expr HAGA LBRACK func_expr RBRACK FINDESDE SEMI')
    def Desde(self, p):
        return ('for_loop', p.var, p.expr0, p.expr1, p.func_expr)


    @_('INC PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def Inc(self, p):
        return ('fun_call', p.INC, p.var, p.expr)

    @_('DEC PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def Dec(self, p):
        return ('fun_call', p.DEC, p.var, p.expr)

    @_('INI PARENTHESIS_LEFT var COMA expr PARENTHESIS_RIGHT SEMI')
    def Ini(self, p):
        return ('fun_call', p.INI, p.var, p.expr)

    @_('MOVER PARENTHESIS_LEFT movimientos PARENTHESIS_RIGHT SEMI')
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
        return p.func_expr

    @_('SINO LBRACK func_expr RBRACK')
    def SiNo(self, p):
        return ("SiNo", p.func_expr)

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
        return '1'
    @_('A')
    def movimientos(self,p):
        return '7'
    @_('F')
    def movimientos(self,p):
        return '2'
    @_('IFA')
    def movimientos(self, p):
        return '4'
    @_('DFA')
    def movimientos(self, p):
        return '3'
    @_('DFB')
    def movimientos(self, p):
        return '5'
    @_('IFB')
    def movimientos(self, p):
        return '6'
    @_('DAA')
    def movimientos(self, p):
        return '8'
    @_('IAA')
    def movimientos(self, p):
        return '9'
    @_('DAB')
    def movimientos(self, p):
        return 'A'
    @_('IAB')
    def movimientos(self, p):
        return 'B'
    @_('AA')
    def movimientos(self, p):
        return 'C'

    @_('LLAMAR VAR PARENTHESIS_LEFT Parametros PARENTHESIS_RIGHT SEMI')
    def func_call(self, p):
        return ('process_call', p.VAR, p.Parametros)

    def error(self, p):
        return ("error", "Parsing Error! Maybe you mixed the order or misspelled something")

class BasicExecute:

    def __init__(self, env):
        self.env = env
        self.ip = 0
        self.error = ""


    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        if isinstance(node,list) and len(node) ==1:
            return self.walkTree(node[0])
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

            print("EnCaso")
            for i in range(len(node[1])):
                result = self.walkTree(node[1][i])
                print(result)
                if result:
                    print(node[1][i][2])
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
                HOST = str(self.ip)
                PORT = 65000
                sendData(node[2].encode(), HOST, PORT)
            elif node[1] == 'Aleatorio':

                movimientos = ['AF','F','DFA','IFA','DFB','IFB'
                                ,'A','DAA','IAA','DAB','IAB','AA']
                movimiento = random.choice(movimientos)
                sendData(movimiento.encode())

            else:
                return("Function not defined")

        if node[0] == 'multi_proc':
            if node[1][0] == 'proc_def':
                if node[1][2] == []:
                    arbol = node[1][3]

                    arbol = arbol[1]
                    self.env[node[1][1]] = (arbol,[])
                else:
                    x = node[1][2]
                    x = x[1:]
                    cont = 0

                    if node[1][3][1] == None:
                        print("WARNING: You are defining a empty process")
                        self.env[node[1][1]] = (node[1][3][1],x)
                    else:
                        self.env[node[1][1]] = (node[1][3][1],x)
                        print("Process saved")
            else:
                print("There's no process defined")
        if node[0] == "proc_func":
            for i in range(1,len(node)):
                self.walkTree(node[i])

        if node[0] == 'process_call':
        #try:
            parametros = node[2]
            parametros = parametros[1:]
            proc = list(self.env[node[1]])
            proced = list(proc[0])
            previos =list(proc[1])
            cont = 0
            if parametros != []:
                for i in range(len(proced)):
                    if isinstance(proced[i],tuple):
                        if proced[i][0] == "while_loop":
                            print("here")
                            for j in range(len(proced[i][1])):
                                proced[i][1][j] = list(proced[i][1][j])

                                if not proced[i][1][j][1] == "Mover" and not proced[i][1][j][1] == "Aleatorio":
                                    proced[i][1][j][2] = parametros[previos.index(proced[i][1][j][2])]
                                proced[i] = list(proced[i])
                                proced[i][2] = list(proced[i][2])
                                proced[i][2][1] = parametros[previos.index(proced[i][2][1])]
                        elif proced[i][0] == "for_loop":
                            proced[i] = list(proced[i])
                            for j in range(len(proced[i][4])):
                                proced[i][4][j] = list(proced[i][4][j])
                                proced[i][4][j][2] = parametros[previos.index(proced[i][4][j][2])]
                        else:
                            proced[i] = list(proced[i])
                            if proced[i][1] != "Mover" and proced[i][1] != "Aleatorio":
                                proced[i][2] = parametros[previos.index(proced[i][2])]

            else:
                pass

            print(proced)

            return self.walkTree(proced)





#Inicio: {} Final; Proc Racso(a,s,d,f,h,j) {Inicio: {} Final;};

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
                self.error = "Undefined variable '"+node[1]+"' found!"
                return "Undefined variable '"+node[1]+"' found!"
        if node[0]== 'while_loop':
            loop_sentence = node[1]
            loop_setup = self.walkTree(node[2])
            val= node[2][1][1]
            i= self.walkTree(node[2][1])
            print(loop_sentence)
            while True:
                for i in node[1]:
                    self.walkTree(i)
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
            for i in range(loop_count+1, loop_limit+1):
                self.env[node[1][1]] = self.env[node[1][1]] + 1

                for i in node[4]:
                    self.walkTree(i)

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
