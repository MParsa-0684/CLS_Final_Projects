# Optional Project 6 - Simple MIPS Simulator

This project implements a minimal MIPS32 simulator that supports:
- R-type: `ADD`, `SUB`, `SLT`
- I-type: `ADDI`, `LW`, `SW`, `BEQ`
- J-type: `J`

The simulator loads 32-bit machine codes from a hex input file, places them in a 4KB word-addressable memory (1024 words), and executes them starting from `PC = 0`. The program halts when it fetches an all-zero instruction.

## Run (Python CLI)

```bash
python3 mips_sim.py sample_input.txt
```

## Run (Python GUI)

```bash
python3 mips_gui.py
```

## Notes
- Memory is byte-addressable; word accesses use `address / 4`.
- Register `R0` is always forced to `0` after each instruction.
- Immediate values are sign-extended for `ADDI`, `LW`, `SW`, and `BEQ`.

## Task-Oriented Sample Programs

Each sample ends with `00000000` (halt). The expected outputs below are from running the simulator.

### 1) Calculator: sum, sub, pow2 (result in `R1`)
File: `sample_1_calculator.txt`

Purpose:
- Uses `ADDI` to load inputs `a=7` and `b=3`.
- Computes `a+b` into `R1`, then `a-b` into `R1`.
- Computes `a^2` using a loop of repeated addition (`ADD`) with `BEQ` and `J`.
- Final result is `a^2 = 49` in `R1`.

Expected registers:
- `R1 = 49` (final result)
- `R8 = 7`, `R9 = 3`

### 2) Palindrome check of a 5-word “string” (result in `R1`)
File: `sample_2_palindrome.txt`

Purpose:
- Stores a 5-word sequence `[1, 2, 3, 2, 1]` into memory using `ADDI` + `SW`.
- Compares symmetric elements from both ends using `LW`, `SUB`, and `BEQ`.
- Uses `SLT`-free compare by checking if subtraction result is zero.
- If any mismatch: sets `R1 = 0`, else `R1 = 1`.

Expected registers:
- `R1 = 1` (the sequence is a palindrome)

### 3) Find max of 10 values in memory (result in `R3`)
File: `sample_3_max10.txt`

Purpose:
- Stores 10 values into memory using `ADDI` + `SW`.
- Loads the first value as the initial max.
- Iterates remaining values, comparing with `SLT` and conditionally updating `R3`.
- Final max is stored in `R3`.

Values:
`[13, 5, 22, 9, 17, 3, 31, 8, 11, 26]`

Expected registers:
- `R3 = 31`

### 4) Average of 8 values in memory (result in `R3`)
File: `sample_4_avg8.txt`

Purpose:
- Stores 8 values into memory using `ADDI` + `SW`.
- Sums all values with a loop of `LW` and `ADD`.
- Divides by 8 using repeated subtraction (since division isn’t supported).
- Integer average stored in `R3`.

Values:
`[12, 6, 9, 3, 15, 18, 21, 7]` (sum = 91, integer average = 11)

Expected registers:
- `R3 = 11`

### 5) Sum 1..300 using loop (result in `R3`)
File: `sample_5_sum1to300.txt`

Purpose:
- Implements a classic loop to compute `1 + 2 + ... + 300`.
- Uses `BEQ` with a limit value of 301 to stop.
- Final sum stored in `R3`.

Expected registers:
- `R3 = 45150`

## Line-by-Line Explanations (Samples 1–5)

### Sample 1: `sample_1_calculator.txt`
1. `20080007` — `ADDI R8,R0,7`: load `7` into `R8` (a).
2. `20090003` — `ADDI R9,R0,3`: load `3` into `R9` (b).
3. `01090820` — `ADD R1,R8,R9`: `R1 = a + b`.
4. `01090822` — `SUB R1,R8,R9`: `R1 = a - b`.
5. `20010000` — `ADDI R1,R0,0`: clear `R1` (accumulator for pow2).
6. `21020000` — `ADDI R2,R8,0`: copy `a` into `R2` (loop counter).
7. `10400003` — `BEQ R2,R0,3`: if counter is `0`, skip loop body to halt.
8. `00280820` — `ADD R1,R1,R8`: `R1 += a` (one step of repeated addition).
9. `2042FFFF` — `ADDI R2,R2,-1`: decrement loop counter.
10. `08000006` — `J 6`: jump back to line 7 (loop check).
11. `00000000` — `HALT`: stop execution.

### Sample 2: `sample_2_palindrome.txt`
1. `20010001` — `ADDI R1,R0,1`: preset result to `1` (assume palindrome).
2. `20040001` — `ADDI R4,R0,1`: load first value into `R4`.
3. `AC040000` — `SW R4,0(R0)`: store at `mem[0]`.
4. `20040002` — `ADDI R4,R0,2`: load next value.
5. `AC040004` — `SW R4,4(R0)`: store at `mem[4]`.
6. `20040003` — `ADDI R4,R0,3`: load next value.
7. `AC040008` — `SW R4,8(R0)`: store at `mem[8]`.
8. `20040002` — `ADDI R4,R0,2`: load next value.
9. `AC04000C` — `SW R4,12(R0)`: store at `mem[12]`.
10. `20040001` — `ADDI R4,R0,1`: load last value.
11. `AC040010` — `SW R4,16(R0)`: store at `mem[16]`.
12. `20050000` — `ADDI R5,R0,0`: left pointer = `0`.
13. `20060010` — `ADDI R6,R0,16`: right pointer = `16`.
14. `20070002` — `ADDI R7,R0,2`: number of comparisons.
15. `10E0000A` — `BEQ R7,R0,10`: if no comparisons left, finish.
16. `8CA80000` — `LW R8,0(R5)`: load left value.
17. `8CC90000` — `LW R9,0(R6)`: load right value.
18. `01095022` — `SUB R10,R8,R9`: compute difference.
19. `11400002` — `BEQ R10,R0,2`: if equal, skip failure branch.
20. `20010000` — `ADDI R1,R0,0`: set result to `0` (not palindrome).
21. `08000019` — `J 25`: jump to halt.
22. `20A50004` — `ADDI R5,R5,4`: move left pointer inward.
23. `20C6FFFC` — `ADDI R6,R6,-4`: move right pointer inward.
24. `20E7FFFF` — `ADDI R7,R7,-1`: decrement comparison counter.
25. `0800000E` — `J 14`: repeat comparison loop.
26. `00000000` — `HALT`: stop execution.

### Sample 3: `sample_3_max10.txt`
1. `2004000D` — `ADDI R4,R0,13`: load value.
2. `AC040000` — `SW R4,0(R0)`: store at `mem[0]`.
3. `20040005` — `ADDI R4,R0,5`: load value.
4. `AC040004` — `SW R4,4(R0)`: store at `mem[4]`.
5. `20040016` — `ADDI R4,R0,22`: load value.
6. `AC040008` — `SW R4,8(R0)`: store at `mem[8]`.
7. `20040009` — `ADDI R4,R0,9`: load value.
8. `AC04000C` — `SW R4,12(R0)`: store at `mem[12]`.
9. `20040011` — `ADDI R4,R0,17`: load value.
10. `AC040010` — `SW R4,16(R0)`: store at `mem[16]`.
11. `20040003` — `ADDI R4,R0,3`: load value.
12. `AC040014` — `SW R4,20(R0)`: store at `mem[20]`.
13. `2004001F` — `ADDI R4,R0,31`: load value.
14. `AC040018` — `SW R4,24(R0)`: store at `mem[24]`.
15. `20040008` — `ADDI R4,R0,8`: load value.
16. `AC04001C` — `SW R4,28(R0)`: store at `mem[28]`.
17. `2004000B` — `ADDI R4,R0,11`: load value.
18. `AC040020` — `SW R4,32(R0)`: store at `mem[32]`.
19. `2004001A` — `ADDI R4,R0,26`: load value.
20. `AC040024` — `SW R4,36(R0)`: store at `mem[36]`.
21. `20050000` — `ADDI R5,R0,0`: pointer to start of array.
22. `8CA30000` — `LW R3,0(R5)`: initialize max with first element.
23. `20A50004` — `ADDI R5,R5,4`: advance pointer.
24. `20060009` — `ADDI R6,R0,9`: remaining count (9 items left).
25. `10C00007` — `BEQ R6,R0,7`: if done, finish.
26. `8CA40000` — `LW R4,0(R5)`: load current element.
27. `0064382A` — `SLT R7,R3,R4`: set `R7=1` if current max < value.
28. `10E00001` — `BEQ R7,R0,1`: if not smaller, skip update.
29. `00801820` — `ADD R3,R4,R0`: update max (`R3 = R4`).
30. `20A50004` — `ADDI R5,R5,4`: advance pointer.
31. `20C6FFFF` — `ADDI R6,R6,-1`: decrement remaining count.
32. `08000018` — `J 24`: repeat loop.
33. `00000000` — `HALT`: stop execution.

### Sample 4: `sample_4_avg8.txt`
1. `2004000C` — `ADDI R4,R0,12`: load value.
2. `AC040000` — `SW R4,0(R0)`: store at `mem[0]`.
3. `20040006` — `ADDI R4,R0,6`: load value.
4. `AC040004` — `SW R4,4(R0)`: store at `mem[4]`.
5. `20040009` — `ADDI R4,R0,9`: load value.
6. `AC040008` — `SW R4,8(R0)`: store at `mem[8]`.
7. `20040003` — `ADDI R4,R0,3`: load value.
8. `AC04000C` — `SW R4,12(R0)`: store at `mem[12]`.
9. `2004000F` — `ADDI R4,R0,15`: load value.
10. `AC040010` — `SW R4,16(R0)`: store at `mem[16]`.
11. `20040012` — `ADDI R4,R0,18`: load value.
12. `AC040014` — `SW R4,20(R0)`: store at `mem[20]`.
13. `20040015` — `ADDI R4,R0,21`: load value.
14. `AC040018` — `SW R4,24(R0)`: store at `mem[24]`.
15. `20040007` — `ADDI R4,R0,7`: load value.
16. `AC04001C` — `SW R4,28(R0)`: store at `mem[28]`.
17. `20050000` — `ADDI R5,R0,0`: pointer to start of array.
18. `20060008` — `ADDI R6,R0,8`: count = 8.
19. `20040000` — `ADDI R4,R0,0`: sum = 0.
20. `10C00005` — `BEQ R6,R0,5`: if count is 0, finish sum loop.
21. `8CA70000` — `LW R7,0(R5)`: load current element.
22. `00872020` — `ADD R4,R4,R7`: add into sum.
23. `20A50004` — `ADDI R5,R5,4`: advance pointer.
24. `20C6FFFF` — `ADDI R6,R6,-1`: decrement count.
25. `08000013` — `J 19`: repeat sum loop.
26. `20030000` — `ADDI R3,R0,0`: quotient = 0.
27. `20060008` — `ADDI R6,R0,8`: divisor = 8.
28. `0086382A` — `SLT R7,R4,R6`: check if sum < divisor.
29. `10E00001` — `BEQ R7,R0,1`: if sum >= divisor, continue division.
30. `08000021` — `J 33`: if sum < divisor, finish.
31. `00862022` — `SUB R4,R4,R6`: sum -= divisor.
32. `20630001` — `ADDI R3,R3,1`: quotient++.
33. `0800001B` — `J 27`: repeat division loop.
34. `00000000` — `HALT`: stop execution.

### Sample 5: `sample_5_sum1to300.txt`
1. `20030000` — `ADDI R3,R0,0`: sum = 0.
2. `20010001` — `ADDI R1,R0,1`: i = 1.
3. `2002012D` — `ADDI R2,R0,301`: limit = 301.
4. `00611820` — `ADD R3,R3,R1`: sum += i.
5. `20210001` — `ADDI R1,R1,1`: i++.
6. `10220001` — `BEQ R1,R2,1`: if i == 301, exit loop.
7. `08000003` — `J 3`: jump back to line 4 (loop body).
8. `00000000` — `HALT`: stop execution.
