


reservedWords = ["int", "arr", "var", "if", "end","jump", "label", "func", "return", "", "program"]
reservedSymbols = ["+", "-", "*", "/", "%","=",">", ">=", "<", "<=", "!=", "[", "]"]
allowedReg = list(range(4,18))
ALUaccumulator = 25 #Register 25 holds accumulator vals
ALUHold = 24 #For division and multuolication

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


            #int x = 10
            #array hi = 10 9 8 7 6
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

            elif declareVars == True:
                print("Unexpected: " + str(line) + "")
                return None


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

                if tokens[0] == "program":
                    #program
                    pass


                elif tokens[0] == "if" and len(tokens) == 4:
                    #if x == y
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
                    #end (end an if)

                    destFile.write(str(labelStack.pop(0)) + ":\n")


                elif tokens[0] == "jump" and len(tokens) == 2:
                    #jump lol

                    destFile.write("\tj _" + str(tokens[1]) + "\n")


                elif tokens[0] == "label" and len(tokens) == 2:
                    #label lol

                    destFile.write("_" + str(tokens[1]) + "_:\n")



                elif tokens[0] == "var" and len(tokens) >= 3:

                    #var x = 10 + ...
                    destination = tokens[1]
                    prevOp = "+"

                    if destination not in varDict: #Variable needs to be defined
                        print("Unknown variable: " + str(tokens[1]))
                        return None
                    

                    for token in range(3,len(tokens)):
                        
                        if tokens[token] in reservedSymbols: #Symbol deteced
                            prevOp = token

                        elif tokens[token] in varDict:

                            if prevOp == "+":
                                destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                            elif prevOp == "-":
                                destFile.write("\tsub $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                            if prevOp == "*":
                                destFile.write("\tmul $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmflo $" + str(ALUaccumulator) + "\n")
                            elif prevOp == "/":
                                destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmflo $" + str(ALUaccumulator) + "\n")

                            elif prevOp == "%":
                                destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmfhi $" + str(ALUaccumulator) + "\n")









                        else: #Must be a number, check if actually a number first rhough
                            
                            for character in tokens[token]:
                                if character.isalpha() == True:
                                    print("Unknown variable: " + str(tokens[token]))
                                    return None
                                

                            if prevOp == "+":
                                destFile.write("\taddi $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " "+ str(tokens[token]) + "\n")
                            elif prevOp == "-":
                                destFile.write("\tsubi $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " "+ str(tokens[token]) + "\n")

                                
                            if prevOp == "*":
                                destFile.write("\tmul $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmflo $" + str(ALUaccumulator) + "\n")
                            elif prevOp == "/":
                                destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmflo $" + str(ALUaccumulator) + "\n")

                            elif prevOp == "%":
                                destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmfhi $" + str(ALUaccumulator) + "\n")



                            





                    destFile.write("\n")
                        

                    
                    
                        



                else:
                    print("Unexpected: " + str(line) + "")
                    return None






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


