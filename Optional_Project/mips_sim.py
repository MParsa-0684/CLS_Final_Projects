#!/usr/bin/env python3
import sys
from typing import List

MEM_WORDS = 1024
WORD_SIZE = 4


def parse_hex_line(line: str) -> int:
    p = line.lstrip()
    if not p or p.startswith("#") or p.startswith("//"):
        return None
    # Allow inline comments starting with // or #
    for token in ("//", "#"):
        idx = p.find(token)
        if idx != -1:
            p = p[:idx].strip()
    if not p:
        return None
    return int(p, 16)


def run_sim(hex_lines: List[str]) -> List[int]:
    memory = [0] * MEM_WORDS
    regs = [0] * 32
    pc = 0

    idx = 0
    for line in hex_lines:
        val = parse_hex_line(line)
        if val is None:
            continue
        if idx >= MEM_WORDS:
            raise ValueError("Program too large for memory")
        memory[idx] = val & 0xFFFFFFFF
        idx += 1

    while True:
        word_index = pc // WORD_SIZE
        if word_index >= MEM_WORDS:
            raise ValueError(f"PC out of bounds: 0x{pc:08X}")

        instr = memory[word_index]
        if instr == 0:
            break

        pc += WORD_SIZE

        opcode = (instr >> 26) & 0x3F
        rs = (instr >> 21) & 0x1F
        rt = (instr >> 16) & 0x1F
        rd = (instr >> 11) & 0x1F
        funct = instr & 0x3F
        imm = instr & 0xFFFF
        simm = imm if imm < 0x8000 else imm - 0x10000
        addr = instr & 0x03FFFFFF

        if opcode == 0x00:
            if funct == 0x20:
                regs[rd] = (regs[rs] + regs[rt]) & 0xFFFFFFFF
            elif funct == 0x22:
                regs[rd] = (regs[rs] - regs[rt]) & 0xFFFFFFFF
            elif funct == 0x2A:
                regs[rd] = 1 if to_signed(regs[rs]) < to_signed(regs[rt]) else 0
            else:
                raise ValueError(f"Unsupported funct: 0x{funct:02X}")
        elif opcode == 0x08:
            regs[rt] = (regs[rs] + simm) & 0xFFFFFFFF
        elif opcode == 0x23:
            byte_addr = to_signed(regs[rs]) + simm
            check_aligned(byte_addr)
            check_bounds(byte_addr)
            mem_index = byte_addr // WORD_SIZE
            regs[rt] = memory[mem_index]
        elif opcode == 0x2B:
            byte_addr = to_signed(regs[rs]) + simm
            check_aligned(byte_addr)
            check_bounds(byte_addr)
            mem_index = byte_addr // WORD_SIZE
            memory[mem_index] = regs[rt] & 0xFFFFFFFF
        elif opcode == 0x04:
            if regs[rs] == regs[rt]:
                pc = (pc + (simm << 2)) & 0xFFFFFFFF
        elif opcode == 0x02:
            pc = (pc & 0xF0000000) | (addr << 2)
        else:
            raise ValueError(f"Unsupported opcode: 0x{opcode:02X}")

        regs[0] = 0

    return [to_signed(r) for r in regs]


def to_signed(val: int) -> int:
    val &= 0xFFFFFFFF
    return val if val < 0x80000000 else val - 0x100000000


def check_aligned(byte_addr: int) -> None:
    if byte_addr % WORD_SIZE != 0:
        raise ValueError(f"Unaligned address: {byte_addr}")


def check_bounds(byte_addr: int) -> None:
    if byte_addr < 0 or byte_addr >= MEM_WORDS * WORD_SIZE:
        raise ValueError(f"Address out of bounds: {byte_addr}")


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <hex_input_file>", file=sys.stderr)
        return 1

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        lines = f.readlines()

    try:
        regs = run_sim(lines)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    print("Final register values:")
    for i, v in enumerate(regs):
        print(f"R{i:02d} = {v}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
