


reservedWords = ["int", "arr", "var", "if", "end","jump", "label", "func", "return", "", "program"]
reservedSymbols = ["+", "-", "*", "/", "=",">", ">=", "<", "<=", "!=", "[", "]"]
allowedReg = list(range(4,25))

debug = False




def run(sourceFile):

    varDict = {} #contains var:type
    regDict = {} #contains var:reg
    labelStack = [] #Label stack is if_n (n is a number)
    labCount = 0 #Label counter (n)
    destFileName = "output.asm"
    declareVars = True
    firstRun = True
    with open(destFileName, 'w') as destFile:
        destFile.write(".data\n")

        for line in sourceFile:
            tokens = []
            tokens = line.split() #Split by whitespace



            if len(tokens) == 0:
                continue

            destFile.write("\n")
            if debug == True:
                destFile.write("\t\t# " + str(tokens) + "\n")


            if tokens[0] == "int" and len(tokens) == 4: #int assignment
                varDict[str(tokens[1])] = "int"
                regDict[str(tokens[1])] = ""

                destFile.write("\t" + str(tokens[1]) + ": .word " + " " + str(tokens[3]) + "\n")

            elif tokens[0] == "array" and len(tokens) >= 4: #int assignment
                varDict[str(tokens[1])] = "array"
                regDict[str(tokens[1])] = ""

                destFile.write("\t" + str(tokens[1]) + ": .word " + " ")
                
                for i in range(3,len(tokens)):
                    destFile.write(str(tokens[i]) + " ")

                destFile.write("\n")
            elif tokens[0] == "program" and len(tokens) == 1:
                destFile.write(".text\n")
                declareVars = False


            if declareVars == False:

                if firstRun == True: #Load variables into registers

                    regIndex = allowedReg[0]
                    for key in varDict:
                        
                        if regIndex > allowedReg[-1]:
                            print("Out of registers")
                            return None

                        destFile.write("\tlw $" + str(regIndex) + " " + str(key) + "\n")
                        regDict[key] = regIndex

                        regIndex+=1
                    firstRun = False

                if tokens[0] == "if" and len(tokens) == 4:
                    #Note - load value into reg before use - can only compare vars not vals

                    operator = tokens[2]
                    labelStack.insert(0,"if_" + str(labCount))

                    if operator == "==":
                        destFile.write("\tbne $" + str(tokens[1]) + " " + str(tokens[3]) + " if_" + str(labCount) + "\n")
                    elif operator == "!=":
                        destFile.write("\tbeq $" + str(tokens[1]) + " " + str(tokens[3]) + " if_" + str(labCount) + "\n")
                    elif operator == ">":
                        destFile.write("\tble $" + str(tokens[1]) + " " + str(tokens[3]) + " if_" + str(labCount) + "\n")
                    elif operator == ">=":
                        destFile.write("\tblt $" + str(tokens[1]) + " " + str(tokens[3]) + " if_" + str(labCount) + "\n")
                    elif operator == "<":
                        destFile.write("\tbge $" + str(tokens[1]) + " " + str(tokens[3]) + " if_" + str(labCount) + "\n")
                    elif operator == "<=":
                        destFile.write("\tbgt $" + str(tokens[1]) + " " + str(tokens[3]) + " if_" + str(labCount) + "\n")
                    labCount += 1

                elif tokens[0] == "end" and len(tokens) == 1:

                    destFile.write(str(labelStack.pop(0)) + ":\n")


                elif tokens[0] == "jump" and len(tokens) == 2:

                    destFile.write("\tj _" + str(tokens[1]) + "\n")


                elif tokens[0] == "label" and len(tokens) == 2:

                    destFile.write("_" + str(tokens[1]) + "_:\n")


    return 1








                    
                    














def main():
    #sourceFileName = input("Source file: ")
    sourceFileName = "source.txt"

    with open(sourceFileName, 'r') as sourceFile:
        if run(sourceFile) == None:
            print("Failed compilation")

    #try:

    #    with open(sourceFileName, 'r') as sourceFile:
    #        if run(sourceFile) == None:
    #            print("Failed compilation")

    #except:
    #    print("Failed to open source file: " + str(sourceFileName))            




if __name__ == "__main__":
    main()


