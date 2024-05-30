import time
import math


reservedWords = ["int", "array", "var", "if", "end","jump", "label", "func", "return", "call", "", "program"]
reservedSymbols = ["+", "-", "*", "/", "%","=",">", ">=", "<", "<=", "!=", "[", "]"]
allowedReg = list(range(8,15))
ALUaccumulator = 25 #Register 25 holds accumulator vals
ALUHold = 24 #For division and multuolication
indexHold = 23 #array indexing
memReg = 22 #Array defining
ALUholdMove = 21 #moving low and high
wordSize = 4 #4 bytes


debug = True #Enable for debug in the assembly output




def run(sourceFile):

    varDict = {

        "ZERO" : "int",
        "ARG1" : "int",
        "ARG2" : "int",
        "ARG3" : "array",
        "ARG4" : "array"

    } #contains var:type
    #note - take 2 addresses and 2 variables by default

    regDict = {

        "ZERO" : "0",
        "ARG1" : "4",
        "ARG2" : "5",
        "ARG3" : "6",
        "ARG4" : "7"

    } #contains var:reg (v registers)




    labelStack = [] #Label stack is if_n (n is a number)
    knownFunctions = {} #list of known functions
    labCount = 0 #Label counter (n)
    destFileName = "output.asm"
    declareVars = True
    firstRun = True
    with open(destFileName, 'w') as destFile:
        destFile.write(".data\n")


        destFile.write("\t" + str("ARG1") + ": .word " + " " + str(4) + "\n")
        destFile.write("\t" + str("ARG2") + ": .word " + " " + str(5) + "\n")
        destFile.write("\t" + str("ARG3") + ": .word " + " " + str(6) + "\n")
        destFile.write("\t" + str("ARG4") + ": .word " + " " + str(7) + "\n")

        for line in sourceFile:
            tokens = []
            tokens = line.split() #Split by whitespace



            if len(tokens) == 0:
                continue

            destFile.write("\n")
            if debug == True and tokens[0] != "#":
                destFile.write("\t\t# " + str(line))


            #int x = 10
            #array hi = 10 9 8 7 6
            if tokens[0] == "int" and len(tokens) == 4: #int assignment
                varDict[str(tokens[1])] = "int"
                regDict[str(tokens[1])] = ""

                destFile.write("\t" + str(tokens[1]) + ": .word " + " " + str(tokens[3]))

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



            elif tokens[0] == "#" and len(tokens) > 1:
                # Comment
                destFile.write(str(line))
                continue
                
            elif declareVars == True:
                print("Unexpected: " + str(line) + "")
                return None


            if declareVars == False:

                if firstRun == True: #Load variables into registers


                    regIndex = allowedReg[0]
                    for key in varDict:
                        
                        if key == "ZERO":
                            pass

                        else:
                            if regIndex > allowedReg[-1] + 5: #add 4 to make sure ARGX is not counted, stored in V registers only
                                print("Out of registers")
                                return None

                            if varDict[key] == "array":
                                destFile.write("\tla $" + str(regIndex) + " " + str(key) + "\n")

                            else:
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

                    if tokens[1] in regDict and tokens[3] in regDict:
                        operator = tokens[2]
                        labelStack.insert(0,"if_" + str(labCount))
                        if operator == "==":
                            destFile.write("\tbeq $" + str(regDict[tokens[1]]) + " $" + str(regDict[tokens[3]]) + " if_" + str(labCount) + "\n")
                        elif operator == "!=":
                            destFile.write("\tbne $" + str(regDict[tokens[1]]) + " $" + str(regDict[tokens[3]]) + " if_" + str(labCount) + "\n")
                        elif operator == ">":
                            destFile.write("\tbgt $" + str(regDict[tokens[1]]) + " $" + str(regDict[tokens[3]]) + " if_" + str(labCount) + "\n")
                        elif operator == ">=":
                            destFile.write("\tbge $" + str(regDict[tokens[1]]) + " $" + str(regDict[tokens[3]]) + " if_" + str(labCount) + "\n")
                        elif operator == "<":
                            destFile.write("\tblt $" + str(regDict[tokens[1]]) + " $" + str(regDict[tokens[3]]) + " if_" + str(labCount) + "\n")
                        elif operator == "<=":
                            destFile.write("\tble $" + str(regDict[tokens[1]]) + " $" + str(regDict[tokens[3]]) + " if_" + str(labCount) + "\n")
                        labCount += 1
                    else:
                        print("Unknown variable: " + str(tokens))






                elif tokens[0] == "end" and len(tokens) == 1:
                    #end (end an if)

                    destFile.write(str(labelStack.pop(0)) + ":\n")


                elif tokens[0] == "jump" and len(tokens) == 2:
                    #jump lol

                    destFile.write("\tj _" + str(tokens[1]) + "_\n")


                elif tokens[0] == "label" and len(tokens) == 2:
                    #label lol

                    destFile.write("_" + str(tokens[1]) + "_:\n")



                elif tokens[0] == "var" and len(tokens) >= 3:
                    #var x = 10 + ...
                    destination = tokens[1]
                    prevOp = "+"

                
                    isArrayAri = False

                    arrayDefine = destination.split("[")
                    #print(arrayDefine)

                    if destination not in varDict and len(arrayDefine) == 0: #Variable needs to be defined
                        print("Unknown variable: " + str(tokens[1]))
                        return None


                    if varDict[arrayDefine[0]] == "array":
                        isArrayAri = True
                        indexVariable = arrayDefine[1][:-1]
                        
                        if indexVariable not in varDict:
                            print("Unknown variable: " + str(indexVariable))
                            return None


                        destFile.write("\tsll $" + str(memReg) + " $"+ str(regDict[indexVariable]) + " "+ str(int(math.log2(wordSize))) + "\n")
                        destFile.write("\tadd $" + str(memReg) + " $"+ str(memReg) + " $"+ str(regDict[arrayDefine[0]]) + "\n")


                    destFile.write("\tli $" + str(ALUaccumulator) + " 0" + "\n")
                    for token in range(3,len(tokens)):
                        if tokens[token] in reservedSymbols: #Symbol deteced
                            prevOp = tokens[token]




                        if tokens[token][-1] == "]": #Array

                            tokens[token] = tokens[token].split("[")

                            if tokens[token][0] in varDict and varDict[tokens[token][0]] == "array":
                                #notes - can only use ONE variable, cant load immediate offset, program multiplies for you

                                arrIndex = tokens[token][1][0:-1]
                                
                                if arrIndex in varDict:
                                    #MEMORY ADDRESS



                                    #Issue here

                                    #print("\tsll $" + str(indexHold) + " $"+ str(regDict[tokens[token][0]]) + " "+ str(int(math.log2(wordSize))) + "\n")
                                    #print("\tsll $" + str(indexHold) + " $"+ str(regDict[arrIndex]) + " "+ str(int(math.log2(wordSize))) + "\n")
                                    
                                    destFile.write("\tsll $" + str(indexHold) + " $"+ str(regDict[arrIndex]) + " "+ str(int(math.log2(wordSize))) + "\n")

                                    #print("\tadd $" + str(indexHold) + " $"+ str(indexHold) + " $"+ str(regDict[arrIndex]) + "\n")
                                    destFile.write("\tadd $" + str(indexHold) + " $"+ str(indexHold) + " $"+ str(regDict[tokens[token][0]]) + "\n")
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    #destFile.write("\tadd $" + str(indexHold) + " $"+ str(regDict[tokens[token][0]]) + " $"+ str(regDict[arrIndex]) + "\n")
                                    destFile.write("\tlw $" + str(indexHold) + " 0($"+ str(indexHold) + ")\n")

                                    if prevOp == "+":
                                        destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " $"+ str(indexHold) + "\n")
                                    elif prevOp == "-":
                                        destFile.write("\tsub $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " $"+ str(indexHold) + "\n")
                                    if prevOp == "*":
                                        destFile.write("\tmul $" + str(ALUaccumulator) + " $"+ str(indexHold) + "\n")
                                        destFile.write("\tmflo $" + str(ALUholdMove) + "\n")
                                        destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")

                                    elif prevOp == "/":
                                        destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(indexHold) + "\n")
                                        destFile.write("\tmflo $" + str(ALUholdMove) + "\n")
                                        destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")

                                    elif prevOp == "%":
                                        destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(indexHold) + "\n")
                                        destFile.write("\tmfhi $" + str(ALUholdMove) + "\n")
                                        destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")

                                
                                else:
                                    print("Variable is not array: " + str(arrIndex))
                            else:
                                print("Variable is not array: " + str(tokens[token][0]))




                        elif tokens[token] in varDict:

                            if prevOp == "+":
                                destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                            elif prevOp == "-":
                                destFile.write("\tsub $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                            if prevOp == "*":
                                destFile.write("\tmul $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmflo $" + str(ALUholdMove) + "\n")
                                destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")
                            elif prevOp == "/":
                                destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmflo $" + str(ALUholdMove) + "\n")
                                destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")

                            elif prevOp == "%":
                                destFile.write("\tdiv $" + str(ALUaccumulator) + " $"+ str(regDict[tokens[token]]) + "\n")
                                destFile.write("\tmfhi $" + str(ALUholdMove) + "\n")
                                destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")


                        else: #Must be a number, check if actually a number first rhough
                            
                            skip = False
                            for character in tokens[token]:
                                if character.isalpha() == True:
                                    print("Unknown variable: " + str(tokens[token]))
                                    return None
                                elif character in reservedSymbols:
                                    skip = True

                            if skip == False:

                                if prevOp == "+":
                                    destFile.write("\taddi $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " "+ str(tokens[token]) + "\n")
                                elif prevOp == "-":
                                    destFile.write("\tsubi $" + str(ALUaccumulator) + " $"+ str(ALUaccumulator) + " "+ str(tokens[token]) + "\n")

                                    
                                if prevOp == "*":
                                    destFile.write("\taddi $" + str(ALUHold) + " $0 " + str(tokens[token]) + "\n")
                                    destFile.write("\tmul $" + str(ALUaccumulator) + " " + str(ALUaccumulator) + " $" + str(ALUHold) + "\n")
                                    destFile.write("\tmflo $" + str(ALUholdMove) + "\n")
                                    destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")
                                elif prevOp == "/":
                                    destFile.write("\taddi $" + str(ALUHold) + " $0 " + str(tokens[token]) + "\n")
                                    destFile.write("\tdiv $" + str(ALUaccumulator) + " $" + str(ALUaccumulator) + " $" + str(ALUHold) + "\n")
                                    destFile.write("\tmflo $" + str(ALUholdMove) + "\n")
                                    destFile.write("\tadd $" + str(ALUaccumulator) + " $"+ str(ALUholdMove) + " $"+ str(ALUaccumulator) + "\n")

                                elif prevOp == "%":
                                    destFile.write("\taddi $" + str(ALUHold) + " $0 " + str(tokens[token]) + "\n")
                                    destFile.write("\tdiv $" + str(ALUaccumulator) + " $" + str(ALUaccumulator) + " $" + str(ALUHold) + "\n")
                                    destFile.write("\tmfhi $" + str(ALUaccumulator) + "\n")



                    if isArrayAri == True:
                        destFile.write("\tsw $" + str(ALUaccumulator) + " 0($" + str(memReg) + ")\n")
                        pass
                    else:
                        destFile.write("\tadd $" + str(regDict[tokens[1]]) + " $0 $" + str(ALUaccumulator) + "\n")
                    destFile.write("\n")



                elif tokens[0] == "call" and len(tokens) >= 3:
                    #call a b c
                    #ONLY TAKES REGISTER ARGUMENTS
                    if tokens[1] in knownFunctions:
                        
                        for argument in range(2,len(tokens)):
                            if tokens[argument] in regDict: #move to $a0 to $a3
                                destFile.write("\taddi $" + str(4 + argument - 2) + " $0 " + str(regDict[tokens[argument]]) + "\n")
                            else:
                                print("Unknown parameter: " + str(tokens[argument]))


                        destFile.write("\tjal func_" + str(knownFunctions[tokens[1]]) + "\n") #Jump to label
                    

                    else:
                        print("Unknown function: " + str(tokens[1]))

                    pass



                elif tokens[0] == "func" and len(tokens) == 2:
                    #func label
                    #By default ARG1-4 MUST be used inside a function
                    #ARG1 and 2 are ints rest are arrays

                    knownFunctions[tokens[1]] = tokens[1]

                    counterReg = 0
                    destFile.write("func_" + str(tokens[0]) + ":\n") #Function label
                    for reg in allowedReg:

                        destFile.write("\taddi $" + str(reg) + " $0 " + str(counterReg) +"($sp)\n")
                        counterReg -= wordSize

                    destFile.write("\taddi $sp $0 " + str(len(allowedReg) * wordSize) + "\n")




                elif tokens[0] == "return" and (len(tokens) == 3 or len(tokens) == 2):
                    #return value value1
                    #Specify 0 in second field if no second return argument
                    #First into $v0 and second into $v1, effectively a move command
                    #Also pops off used registers


                    #Resotre registers
                    #COME BACK


                    counterReg = 0
                    for reg in allowedReg:

                        destFile.write("\taddi $" + str(reg) + " $0 " + str(counterReg) +"($sp)\n")
                        counterReg += wordSize

                    destFile.write("\taddi $sp $0 " + str(len(allowedReg) * wordSize) + "\n")


                    #Move return vals
                    if len(tokens) == 2:
                        if tokens[1] in varDict:
                                destFile.write("\taddi $v0 $0 "+ str(tokens[1]) + "\n")
                        else:
                            print("Variable is not defined: " + str(tokens[1]))


                    if len(tokens) == 3:
                        if tokens[1] in varDict or tokens[2] in varDict:
                                
                                destFile.write("\taddi $v0 $0 "+ str(tokens[1]) + "\n")
                                destFile.write("\taddi $v1 $0 "+ str(tokens[1]) + "\n")
                        else:
                            print("Variable is not defined: " + str(tokens))

                    
                    else:
                        print("Variable is not defined: " + str(tokens))


                    pass




                else:
                    print("Unexpected: " + str(line) + "")
                    return None



    if labelStack != []:
        print("Missing end statement\n")
        return None


    return 1








                    
                    














def main():
    startTime = time.time()
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


    stopTime = time.time()
    print("Compiled in: " + str((stopTime - startTime)*1000) + "ms\n") 




if __name__ == "__main__":
    main()



    
