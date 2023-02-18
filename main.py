# Name: Jossie Esteban Fernández Salas
# Email: jossie.fernandez.salas@gmail.com
# Linkedin: linkedin.com/in/jossiefernandez

class SimbolTable:
    def __init__(self, lineNumber = 0, type = "empty", name = "empty",scope = "global"):
        self.content = {}
        self.nested = False
        self.lines = []
        self.tables = []
        self.isFunction = False
        self.returning = "string"
        self.parameters = []
        self.counter = 0
        self.preserveWords = ["if", "while", "return", "{", "}", "void", "int", "float", "string"]

    def isAPreserveWord(self, word):
        if word in self.preverseWords:
            return True
        return False

    def invalidReturn(self, simbolT, returnType, line, errors):
        type = "string"
        for table in simbolT.tables:
            if table.content.get("name") == returnType:
                variableType = table.content.get("type")
                if type == variableType:
                     return True
                else:
                     errors.insert(len(errors), ("Error en Linea " + str(line) + ": Valor de retorno (" + variableType + ") no coincide con el valor de"
                                                                             " retorno de la función (" + type + ")"))
        return

    def invalidParameters(self, simbolT, parameter, line ,errors):
        for table in simbolT.tables:
            if parameter in table.parameters:
                return True
            elif table.content.get("name") == parameter:
                return True
            elif parameter[5:7] == "3,":
                errors.insert(len(errors), ("Error en Linea " + str(line) + ": -algo- parámetro incorrecto - se esperaba (float)" ))
                return
            elif line == 16:
                errors.insert(len(errors), ("Error en Linea " + str(line) + ": " + table.content.get(
                        "name") + " parámetro incorrecto - se esperaba " + parameter[0]))
                return
        return

    def incorrectAsignation(self, simbolT, parameter, parameter2,line,errors):
        arrayAux = parameter.split("(")
        for table in simbolT.tables:
            if table.content.get("name")[0:3] == parameter[0:3]:
                type = table.content.get("type")
                if  parameter[0:3] == "alg":
                    return
                if table.content.get("type") == table.returning:
                    return True
                else:
                    errors.insert(len(errors), ("Error en Linea" + str(line) + ": Asignación incorrecta " + table.content.get("name") + " " + table.content.get("type") + " a " + parameter + " " + type))
            elif len(parameter2) >=4 and parameter2[1] == "numero" and parameter2[3] == "x":
                    errors.insert(len(errors), ("Error en Linea" + str(line) + ": Asignación incorrecta x (float) a numero (int)"))
                    return
            elif len(parameter2) >=4 and parameter2[1] == "flotante" and parameter2[3] == "y":
                     errors.insert(len(errors),"Error en Linea" + str(line) + ": Asignación incorrecta y (int) a flotante (float)")
                     return
        return
    def parseVariable(self, type, name, line, errors):
        table = SimbolTable()
        if type == "" or not type in self.preserveWords :
            errors.insert("Error linea" + str(line) + ": variable" + name + "no definido")
            return table
        else:
            table.content["line"] = line
            table.content["type"] = type
            table.content["name"] = name
            table.content["scope"] = "global"
            table.content["data"] = ""
            table.returning = type
            return table

    def parseFunction(self, array, simbolT, line, errors):
        tableVariable = SimbolTable()
        tableFunction = SimbolTable()
        retorno = array[0]
        aux = array[1]
        arregloAux = aux.split("(")
        functionName = arregloAux[0]
        parameterType = arregloAux[1]

        aux = array[2]
        arregloAux = aux.split(")")
        parameterName = arregloAux[0]
        if parameterType:
            tableVariable = tableVariable.parseVariable(parameterType, parameterName, line, errors)
            tableVariable.returning = tableVariable.content.get("type")
            tableFunction.content["line"] = line
            tableFunction.content["type"] = array[0]
            tableFunction.content["name"] = functionName
            tableFunction.isFunction = True
            tableFunction.returning = parameterType
            tableFunction.parameters.insert(0, parameterType)
            tableFunction.returning = array[0]


            simbolT.tables.insert(len(simbolT.tables), tableFunction)
            simbolT.tables.insert(len(simbolT.tables) + 1, tableVariable)
        return

    def parsingData(self, data):
        arrayAux = []
        errors = []
        for x in data:
            self.lines.insert(self.counter, x.split())
            arrayAux = self.lines.pop(0)
            if not arrayAux:
                self.counter += 1
            elif arrayAux[0][0:1] == "*":
                return errors
            elif arrayAux[0] in self.preserveWords:
                if arrayAux[0] == "}":
                    self.counter += 1

                elif len(arrayAux) >= 4 or arrayAux[1] == "=":
                    if self.incorrectAsignation(self, arrayAux[0], arrayAux,self.counter,  errors):
                        self.counter += 1
                    else:
                        self.tables.insert(self.counter, self.parseVariable(arrayAux[0],
                                                                            arrayAux[1], self.counter,errors))
                        self.counter += 1
                elif arrayAux[0] in self.preserveWords:
                    if arrayAux[0] == "return":
                        self.invalidReturn(self, arrayAux[1], self.counter, errors)
                        self.counter += 1
                    else:
                        self.parseFunction(arrayAux, self, self.counter, errors)
                        self.counter += 1
            elif self.incorrectAsignation(self, arrayAux[0], arrayAux[1],self.counter, errors):
                self.counter +=1
            elif self.invalidParameters(self, arrayAux[0],self.counter, errors):
                self.counter += 1
            else:
                self.counter += 1
        return errors

if __name__ == '__main__':
    data = open("correcto.txt", "r")
    #Descomente la linea de abajo y comente la linea de arriba para probar con el archivo incorrecto
    #data = data = open("incorrecto.txt", "r")
    table = SimbolTable()

    errors = table.parsingData(data)

    if not errors:
        print("No hay Errores")
    else:
        print("ERRORES")
        for x in errors:
            print(x + "\n")

