.data
	ARG1: .word  4
	ARG2: .word  5
	ARG3: .word  6
	ARG4: .word  7

# i counter (for loop)

		# int i = 0
	i: .word  0
		# int arrCopy = 0
	arrCopy: .word  0
# Array declaration with elements

		# array arr = 1, 2, 3, 4, 5
	arr: .word  1, 2, 3, 4, 5 

# Total number of elements in array

		# int arrSize = 5
	arrSize: .word  5
# endIndex for swapping

		# int endIndex = 0
	endIndex: .word  0
# Temp for swapping

		# int temp = 0
	temp: .word  0
		# program
.text
	lw $8 ARG1
	lw $9 ARG2
	la $10 ARG3
	la $11 ARG4
	lw $12 i
	lw $13 arrCopy
	la $14 arr
	lw $15 arrSize
	lw $16 endIndex
	lw $17 temp

# Set half size of the array to iterate over

		# var arrSize = arrSize / 2
	li $21 0
	add $21 $21 $15
	addi $24 $0 2
	div $21 $24
	mflo $21
	add $15 $0 $21


		# var arrCopy = arrSize
	li $21 0
	add $21 $21 $15
	add $13 $0 $21


		# label start_for
_start_for_:

# Loop condition check

		# if i < arrSize
	blt $12 $15 if_0

    # Calculate endIndex for current iteration

		#     var endIndex = arrCopy - i - 1
	li $21 0
	add $21 $21 $13
	sub $21 $21 $12
	subi $21 $21 1
	add $16 $0 $21


    # Swapping elements: store arr[endIndex] in temp

		#     var temp = arr[endIndex]
	li $21 0
	sll $23 $16 2
	add $23 $23 $14
	lw $23 0($23)
	add $21 $21 $23
	add $17 $0 $21


    # Place arr[i] in arr[endIndex]

		#     var arr[endIndex] = arr[i]
	sll $22 $16 2
	add $22 $22 $14
	li $21 0
	sll $23 $12 2
	add $23 $23 $14
	lw $23 0($23)
	add $21 $21 $23
	sw $21 0($22)


    # Place temp (original arr[endIndex]) in arr[i]

		#     var arr[i] = temp
	sll $22 $12 2
	add $22 $22 $14
	li $21 0
	add $21 $21 $17
	sw $21 0($22)


    # Increment i for the next iteration

		#     var i = i + 1
	li $21 0
	add $21 $21 $12
	addi $21 $21 1
	add $12 $0 $21


    # Jump to start of the loop

		#     jump start_for
	j _start_for_

		# end
if_0:
