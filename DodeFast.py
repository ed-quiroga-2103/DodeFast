from sly import Lexer as Lexer
from sly import Parser as Parser

class BasicLexer(Lexer):

    tokens = { DECLARATION, ASSIGNATION, ENCASO, CUANDO, ENTONS, SINO, FINENCASO, VAR, INT,
                SEMI, LBRACK, RBRACK, GREATEREQ, LESSEREQ, EQ, GREATER, LESSER,
                MINUS, INC, DEC, INI, PARENTHESIS_LEFT, PARENTHESIS_RIGHT, COMA, MOVER, ALEATORIO}

    ignore = " "

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

#----Palabras------
    INC = r'Inc'
    DEC = r'Dec'
    INI = r'Ini'
    MOVER = r'Mover'
    ALEATORIO = r'Aleatorio'
    DECLARATION = r"DCL"
    ASSIGNATION = "DEFAULT"
    ENCASO = r"EnCaso"
    CUANDO = r"Cuando"
    ENTONS = r"Entons"
    SINO = r"SiNo"
    FINENCASO = r"Fin-EnCaso"
    VAR = r"[a-zA-Z_][a-zA-Z0-9_]*"


    @_(r"\d+")
    def INT(self, t):
        t.value = int(t.value)
        return t

class BasicParser(Parser):
    tokens = BasicLexer.tokens

    X = 0

    def __init__(self):
        self.env = { }
    @_('')
    def statement(self, p):
        pass

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('EnCasoA')
    def statement(self, p):
        return p.EnCasoA

    @_('EnCasoB')
    def statement(self, p):
        return p.EnCasoB

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


    @_('ENTONS LBRACK statement RBRACK')
    def Entons(self, p):
        return p.statement

    @_('SINO LBRACK statement RBRACK')
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

    @_('INC PARENTHESIS_LEFT statement COMA statement PARENTHESIS_RIGHT')
    def statement(self, p):
        return ('fun_call', p.INC, p.statement0, p.statement1)

    @_('DEC PARENTHESIS_LEFT statement COMA statement PARENTHESIS_RIGHT')
    def statement(self, p):
        return ('fun_call', p.DEC, p.statement0, p.statement1)

    @_('INI PARENTHESIS_LEFT statement COMA statement PARENTHESIS_RIGHT')
    def statement(self, p):
        return ('fun_call', p.INI, p.statement0, p.statement1)

    @_('MOVER PARENTHESIS_LEFT statement PARENTHESIS_RIGHT')
    def statement(self, p):
        return ('fun_call', p.MOVER, p.statement)

    @_('ALEATORIO PARENTHESIS_LEFT PARENTHESIS_RIGHT')
    def statement(self, p):
        return ('fun_call', p.ALEATORIO)

    def error(self, p):
        print("Parsing Error! Maybe you mixed the order or misspelled something")

class BasicExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

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

        if node[0] == "SiNo":
            return self.walkTree(node[1])

        if node[0] == 'Equals':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == "Greater":
            try:
                return self.walkTree(node[1]) > self.walkTree(node[2])
            except:
                print("Error")

        if node[0] == "Lesser":
            try:
                return self.walkTree(node[1]) < self.walkTree(node[2])
            except:
                print("Error")

        if node[0] == "LesserEq":
            try:
                return self.walkTree(node[1]) <= self.walkTree(node[2])
            except:
                print("Error")
        if node[0] == "GreaterEq":
            try:
                return self.walkTree(node[1]) >= self.walkTree(node[2])
            except:
                print("Error")

        if node[0] == 'fun_call':
            if node[1] == 'Inc':
                self.env[node[2][1]] = self.walkTree(node[2]) + self.walkTree(node[3])
                print(self.env[node[2][1]])
            elif node[1] == 'Dec':
                self.env[node[2][1]] = self.walkTree(node[2]) - self.walkTree(node[3])
                print(self.env[node[2][1]])
            elif node[1] == 'Ini':
                self.env[node[2][1]] = self.walkTree(node[3])
                print(self.env[node[2][1]])
            else:
                print("Las funciones no estan definidas")

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
            return node[1]
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

#----------------------Lexing run--------------------
"""
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
            BasicExecute(tree, env)

#            print(tree)
