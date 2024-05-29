.data

	x: .word  10
	z: .word  0
	lol: .word  2
	abc: .word  1 2 3 4 5 6 

	bds: .word  3 4 4 

.text
	lw $8 ARG1
	lw $9 ARG2
	lw $10 ARG3
	lw $11 ARG4
	lw $12 x
	lw $13 z
	lw $14 lol
	lw $15 abc
	lw $16 bds

	li $25 0
	add $23 $15 $13
	lw $23 0($23)
	add $25 $25 $23


_start_:

	blt $13 14 if_0

	li $25 0
	add $25 $25 $12
	addi $25 $25 1
	add $25 $25 $13


	j _start
