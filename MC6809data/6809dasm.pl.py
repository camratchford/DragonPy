

IMMEDIATE_WORD = "IMMEDIATE_WORD"
RELATIVE_WORD = "RELATIVE_WORD"
EXTENDED = "EXTENDED"
REGISTER = "REGISTER"
DIRECT = "DIRECT"
RELATIVE = "RELATIVE"
IMMEDIATE = "IMMEDIATE"
INDEXED = "INDEXED"
INHERENT = "INHERENT"
STACK = "STACK"

op_info_dict = {
    0x0: ('NEG', DIRECT),
    0x3: ('COM', DIRECT),
    0x4: ('LSR', DIRECT),
    0x6: ('ROR', DIRECT),
    0x7: ('ASR', DIRECT),
    0x8: ('LSL', DIRECT),
    0x9: ('ROL', DIRECT),
    0xa: ('DEC', DIRECT),
    0xc: ('INC', DIRECT),
    0xd: ('TST', DIRECT),
    0xe: ('JMP', DIRECT),
    0xf: ('CLR', DIRECT),
    0x10: ('page 1+', None),
    0x11: ('page 2+', None),
    0x12: ('NOP', INHERENT),
    0x13: ('SYNC', INHERENT),
    0x16: ('LBRA', RELATIVE_WORD),
    0x17: ('LBSR', RELATIVE_WORD),
    0x19: ('DAA', INHERENT),
    0x1a: ('ORCC', IMMEDIATE),
    0x1c: ('ANDCC', IMMEDIATE),
    0x1d: ('SEX', INHERENT),
    0x1e: ('EXG', REGISTER),
    0x1f: ('TFR', REGISTER),
    0x20: ('BRA', RELATIVE),
    0x21: ('BRN', RELATIVE),
    0x22: ('BHI', RELATIVE),
    0x23: ('BLS', RELATIVE),
    0x24: ('BCC', RELATIVE),
    0x25: ('BCS', RELATIVE),
    0x26: ('BNE', RELATIVE),
    0x27: ('BEQ', RELATIVE),
    0x28: ('BVC', RELATIVE),
    0x29: ('BVS', RELATIVE),
    0x2a: ('BPL', RELATIVE),
    0x2b: ('BMI', RELATIVE),
    0x2c: ('BGE', RELATIVE),
    0x2d: ('BLT', RELATIVE),
    0x2e: ('BGT', RELATIVE),
    0x2f: ('BLE', RELATIVE),
    0x30: ('LEAX', INDEXED),
    0x31: ('LEAY', INDEXED),
    0x32: ('LEAS', INDEXED),
    0x33: ('LEAU', INDEXED),
    0x34: ('PSHS', STACK),
    0x35: ('PULS', STACK),
    0x36: ('PSHU', STACK),
    0x37: ('PULU', STACK),
    0x39: ('RTS', INHERENT),
    0x3a: ('ABX', INHERENT),
    0x3b: ('RTI', INHERENT),
    0x3c: ('CWAI', IMMEDIATE),
    0x3d: ('MUL', INHERENT),
    0x3f: ('SWI', INHERENT),
    0x40: ('NEGA', INHERENT),
    0x43: ('COMA', INHERENT),
    0x44: ('LSRA', INHERENT),
    0x46: ('RORA', INHERENT),
    0x47: ('ASRA', INHERENT),
    0x48: ('LSLA', INHERENT),
    0x49: ('ROLA', INHERENT),
    0x4a: ('DECA', INHERENT),
    0x4c: ('INCA', INHERENT),
    0x4d: ('TSTA', INHERENT),
    0x4f: ('CLRA', INHERENT),
    0x50: ('NEGB', INHERENT),
    0x53: ('COMB', INHERENT),
    0x54: ('LSRB', INHERENT),
    0x56: ('RORB', INHERENT),
    0x57: ('ASRB', INHERENT),
    0x58: ('LSLB', INHERENT),
    0x59: ('ROLB', INHERENT),
    0x5a: ('DECB', INHERENT),
    0x5c: ('INCB', INHERENT),
    0x5d: ('TSTB', INHERENT),
    0x5f: ('CLRB', INHERENT),
    0x60: ('NEG', INDEXED),
    0x63: ('COM', INDEXED),
    0x64: ('LSR', INDEXED),
    0x66: ('ROR', INDEXED),
    0x67: ('ASR', INDEXED),
    0x68: ('LSL', INDEXED),
    0x69: ('ROL', INDEXED),
    0x6a: ('DEC', INDEXED),
    0x6c: ('INC', INDEXED),
    0x6d: ('TST', INDEXED),
    0x6e: ('JMP', INDEXED),
    0x6f: ('CLR', INDEXED),
    0x70: ('NEG', EXTENDED),
    0x73: ('COM', EXTENDED),
    0x74: ('LSR', EXTENDED),
    0x76: ('ROR', EXTENDED),
    0x77: ('ASR', EXTENDED),
    0x78: ('LSL', EXTENDED),
    0x79: ('ROL', EXTENDED),
    0x7a: ('DEC', EXTENDED),
    0x7c: ('INC', EXTENDED),
    0x7d: ('TST', EXTENDED),
    0x7e: ('JMP', EXTENDED),
    0x7f: ('CLR', EXTENDED),
    0x80: ('SUBA', IMMEDIATE),
    0x81: ('CMPA', IMMEDIATE),
    0x82: ('SBCA', IMMEDIATE),
    0x83: ('SUBD', IMMEDIATE_WORD),
    0x84: ('ANDA', IMMEDIATE),
    0x85: ('BITA', IMMEDIATE),
    0x86: ('LDA', IMMEDIATE),
    0x88: ('EORA', IMMEDIATE),
    0x89: ('ADCA', IMMEDIATE),
    0x8a: ('ORA', IMMEDIATE),
    0x8b: ('ADDA', IMMEDIATE),
    0x8c: ('CMPX', IMMEDIATE_WORD),
    0x8d: ('BSR', RELATIVE),
    0x8e: ('LDX', IMMEDIATE_WORD),
    0x90: ('SUBA', DIRECT),
    0x91: ('CMPA', DIRECT),
    0x92: ('SBCA', DIRECT),
    0x93: ('SUBD', DIRECT),
    0x94: ('ANDA', DIRECT),
    0x95: ('BITA', DIRECT),
    0x96: ('LDA', DIRECT),
    0x97: ('STA', DIRECT),
    0x98: ('EORA', DIRECT),
    0x99: ('ADCA', DIRECT),
    0x9a: ('ORA', DIRECT),
    0x9b: ('ADDA', DIRECT),
    0x9c: ('CMPX', DIRECT),
    0x9d: ('JSR', DIRECT),
    0x9e: ('LDX', DIRECT),
    0x9f: ('STX', DIRECT),
    0xa0: ('SUBA', INDEXED),
    0xa1: ('CMPA', INDEXED),
    0xa2: ('SBCA', INDEXED),
    0xa3: ('SUBD', INDEXED),
    0xa4: ('ANDA', INDEXED),
    0xa5: ('BITA', INDEXED),
    0xa6: ('LDA', INDEXED),
    0xa7: ('STA', INDEXED),
    0xa8: ('EORA', INDEXED),
    0xa9: ('ADCA', INDEXED),
    0xaa: ('ORA', INDEXED),
    0xab: ('ADDA', INDEXED),
    0xac: ('CMPX', INDEXED),
    0xad: ('JSR', INDEXED),
    0xae: ('LDX', INDEXED),
    0xaf: ('STX', INDEXED),
    0xb0: ('SUBA', EXTENDED),
    0xb1: ('CMPA', EXTENDED),
    0xb2: ('SBCA', EXTENDED),
    0xb3: ('SUBD', EXTENDED),
    0xb4: ('ANDA', EXTENDED),
    0xb5: ('BITA', EXTENDED),
    0xb6: ('LDA', EXTENDED),
    0xb7: ('STA', EXTENDED),
    0xb8: ('EORA', EXTENDED),
    0xb9: ('ADCA', EXTENDED),
    0xba: ('ORA', EXTENDED),
    0xbb: ('ADDA', EXTENDED),
    0xbc: ('CMPX', EXTENDED),
    0xbd: ('JSR', EXTENDED),
    0xbe: ('LDX', EXTENDED),
    0xbf: ('STX', EXTENDED),
    0xc0: ('SUBB', IMMEDIATE),
    0xc1: ('CMPB', IMMEDIATE),
    0xc2: ('SBCB', IMMEDIATE),
    0xc3: ('ADDD', IMMEDIATE_WORD),
    0xc4: ('ANDB', IMMEDIATE),
    0xc5: ('BITB', IMMEDIATE),
    0xc6: ('LDB', IMMEDIATE),
    0xc8: ('EORB', IMMEDIATE),
    0xc9: ('ADCB', IMMEDIATE),
    0xca: ('ORB', IMMEDIATE),
    0xcb: ('ADDB', IMMEDIATE),
    0xcc: ('LDD', IMMEDIATE_WORD),
    0xce: ('LDU', IMMEDIATE_WORD),
    0xd0: ('SUBB', DIRECT),
    0xd1: ('CMPB', DIRECT),
    0xd2: ('SBCB', DIRECT),
    0xd3: ('ADDD', DIRECT),
    0xd4: ('ANDB', DIRECT),
    0xd5: ('BITB', DIRECT),
    0xd6: ('LDB', DIRECT),
    0xd7: ('STB', DIRECT),
    0xd8: ('EORB', DIRECT),
    0xd9: ('ADCB', DIRECT),
    0xda: ('ORB', DIRECT),
    0xdb: ('ADDB', DIRECT),
    0xdc: ('LDD', DIRECT),
    0xdd: ('STD', DIRECT),
    0xde: ('LDU', DIRECT),
    0xdf: ('STU', DIRECT),
    0xe0: ('SUBB', INDEXED),
    0xe1: ('CMPB', INDEXED),
    0xe2: ('SBCB', INDEXED),
    0xe3: ('ADDD', INDEXED),
    0xe4: ('ANDB', INDEXED),
    0xe5: ('BITB', INDEXED),
    0xe6: ('LDB', INDEXED),
    0xe7: ('STB', INDEXED),
    0xe8: ('EORB', INDEXED),
    0xe9: ('ADCB', INDEXED),
    0xea: ('ORB', INDEXED),
    0xeb: ('ADDB', INDEXED),
    0xec: ('LDD', INDEXED),
    0xed: ('STD', INDEXED),
    0xee: ('LDU', INDEXED),
    0xef: ('STU', INDEXED),
    0xf0: ('SUBB', EXTENDED),
    0xf1: ('CMPB', EXTENDED),
    0xf2: ('SBCB', EXTENDED),
    0xf3: ('ADDD', EXTENDED),
    0xf4: ('ANDB', EXTENDED),
    0xf5: ('BITB', EXTENDED),
    0xf6: ('LDB', EXTENDED),
    0xf7: ('STB', EXTENDED),
    0xf8: ('EORB', EXTENDED),
    0xf9: ('ADCB', EXTENDED),
    0xfa: ('ORB', EXTENDED),
    0xfb: ('ADDB', EXTENDED),
    0xfc: ('LDD', EXTENDED),
    0xfd: ('STD', EXTENDED),
    0xfe: ('LDU', EXTENDED),
    0xff: ('STU', EXTENDED),
    0x1021: ('LBRN', RELATIVE_WORD),
    0x1022: ('LBHI', RELATIVE_WORD),
    0x1023: ('LBLS', RELATIVE_WORD),
    0x1024: ('LBCC', RELATIVE_WORD),
    0x1025: ('LBCS', RELATIVE_WORD),
    0x1026: ('LBNE', RELATIVE_WORD),
    0x1027: ('LBEQ', RELATIVE_WORD),
    0x1028: ('LBVC', RELATIVE_WORD),
    0x1029: ('LBVS', RELATIVE_WORD),
    0x102a: ('LBPL', RELATIVE_WORD),
    0x102b: ('LBMI', RELATIVE_WORD),
    0x102c: ('LBGE', RELATIVE_WORD),
    0x102d: ('LBLT', RELATIVE_WORD),
    0x102e: ('LBGT', RELATIVE_WORD),
    0x102f: ('LBLE', RELATIVE_WORD),
    0x103f: ('SWI2', INHERENT),
    0x1083: ('CMPD', IMMEDIATE_WORD),
    0x108c: ('CMPY', IMMEDIATE_WORD),
    0x108e: ('LDY', IMMEDIATE_WORD),
    0x1093: ('CMPD', DIRECT),
    0x109c: ('CMPY', DIRECT),
    0x109e: ('LDY', DIRECT),
    0x109f: ('STY', DIRECT),
    0x10a3: ('CMPD', INDEXED),
    0x10ac: ('CMPY', INDEXED),
    0x10ae: ('LDY', INDEXED),
    0x10af: ('STY', INDEXED),
    0x10b3: ('CMPD', EXTENDED),
    0x10bc: ('CMPY', EXTENDED),
    0x10be: ('LDY', EXTENDED),
    0x10bf: ('STY', EXTENDED),
    0x10ce: ('LDS', IMMEDIATE_WORD),
    0x10de: ('LDS', DIRECT),
    0x10df: ('STS', DIRECT),
    0x10ee: ('LDS', INDEXED),
    0x10ef: ('STS', INDEXED),
    0x10fe: ('LDS', EXTENDED),
    0x10ff: ('STS', EXTENDED),
    0x113f: ('SWI3', INHERENT),
    0x1183: ('CMPU', IMMEDIATE_WORD),
    0x118c: ('CMPS', IMMEDIATE_WORD),
    0x1193: ('CMPU', DIRECT),
    0x119c: ('CMPS', DIRECT),
    0x11a3: ('CMPU', INDEXED),
    0x11ac: ('CMPS', INDEXED),
    0x11b3: ('CMPU', EXTENDED),
    0x11bc: ('CMPS', EXTENDED),
}

# op_types = {
#     0x0: (True, DIRECT),
#     0x4: (False, REG_A),
#     0x5: (False, REG_B),
#     0x6: (True, INDEXED),
#     0x7: (True, EXTENDED),
# }
#
# OVERWRITE_DATA = {}
# for op in ops:
#     t = (op >> 4) & 0xf
#     op_type = op_types[t]
# #     print hex(op), op_type
#     OVERWRITE_DATA[op] = op_type

for op_code, op_info in op_info_dict.items():
    mnemonic, addr_mode = op_info



