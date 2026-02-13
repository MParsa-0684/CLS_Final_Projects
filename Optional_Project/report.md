# Report - Optional Project 6

## Implementation Summary
The simulator models three hardware components as software variables:
- `memory[1024]` (4KB, byte-addressable) storing both instructions and data
- `regs[32]` (general-purpose registers, `regs[0]` forced to zero)
- `PC` (program counter in bytes, initialized to 0)

Execution loop:
1. Fetch 32-bit instruction from `memory[PC/4]`.
2. Halt if instruction is all zeros.
3. Increment `PC` by 4.
4. Decode fields via shifts and masks.
5. Execute based on `opcode` (and `funct` for R-type).
6. Force `regs[0] = 0`.

Supported instructions:
- R-type: `ADD`, `SUB`, `SLT`
- I-type: `ADDI`, `LW`, `SW`, `BEQ`
- J-type: `J`

## Sample Input
`sample_input.txt` contains:
```
20080005
20090003
01095022
0109582A
AC0A0000
00000000
```

## Sample Output (Registers After Halt)
Command:
```
./mips_sim sample_input.txt
```
Output:
```
Final register values:
R00 = 0
R01 = 0
R02 = 0
R03 = 0
R04 = 0
R05 = 0
R06 = 0
R07 = 0
R08 = 5
R09 = 3
R10 = 2
R11 = 0
R12 = 0
R13 = 0
R14 = 0
R15 = 0
R16 = 0
R17 = 0
R18 = 0
R19 = 0
R20 = 0
R21 = 0
R22 = 0
R23 = 0
R24 = 0
R25 = 0
R26 = 0
R27 = 0
R28 = 0
R29 = 0
R30 = 0
R31 = 0
```

Memory check:
- `Mem[0] = 2` (stored by `SW $t2, 0($zero)`)
