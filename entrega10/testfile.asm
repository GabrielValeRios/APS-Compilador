SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
segment . data
segment . bss
x_0 RESD 1
y_0 RESD 1
section .text
global _start
print :
POP EBX
POP EAX
PUSH EBX
XOR ESI , ESI
print_dec :
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, 0
PUSH EDX
INC ESI
CMP EAX, 0
JZ print_next
JMP print_dec
print_next :
CMP ESI , 0
JZ print _ exit
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [res] , ECX
MOV ECX, res
MOV EDX, 1
INT 0 x80
JMP prin t_next
print _ exit :
RET
binop_je :
JE binop_true
JMP binop_ false
binop_jg :
JG binop_true
JMP binop_false
binop_jl :
JL binop_true
JMP binop_false
binop_false :
MOV EBX, False
JMP binop_exit
binop_true :
MOV EBX, True
bin op_exit :
RET
_ start :
MOV EBX,5
MOV [x_0], EBX
MOV EBX,3
MOV EAX,2
ADD EBX, EAX
MOV [y_0], EBX
LOOP_0
MOV EAX,10
CMP EAX, EBX
CALL binop_jl
CMP EBX, False
JE EXIT_0
MOV EBX, x_0
MOV EAX,1
ADD EBX, EAX
MOV [x_0], EBX
JUMP LOOP_0
EXIT_0
LOOP_1
MOV EAX,10
CMP EAX, EBX
CALL binop_jl
CMP EBX, False
JE EXIT_1
MOV EBX, [x_0]
PUSH EBX
CALL print
JUMP LOOP_1
EXIT_1
LOOP_2
MOV EBX, [y_0]
PUSH EBX
CALL print
JUMP LOOP_2
EXIT_2
MOV EBX, [x_0]
PUSH EBX
CALL print
