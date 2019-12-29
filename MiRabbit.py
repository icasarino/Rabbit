#########################################################
# Cyphered Implemented as RFC-4503                      #
#                                                       #
# https://tools.ietf.org/html/rfc4503                   #
#########################################################

import BinaryMethods as bm
import TypeConverter as tc

WORD_SIZE = 0x100000000
# print("Insert Key >> ")
# KEY = str(input())
KEY = "holacomoestasvos"
KEY_LEN = len(KEY)
keyArray = []   # Kx Array
counterArray = []   # Cx Array
stateArray = []     # Xx Array
gArray = []         # Applied gFunction over counterArray and stateArray
bitCarry = 0

Aconstants = [0x4D34D34D,0xD34D34D3,0x34D34D34,0x4D34D34D,0xD34D34D3,0x34D34D34,0x4D34D34D,0xD34D34D3]


def validateKey():
    if KEY_LEN != 16:
        raise ValueError('KEY must have 128 bits - 16 Characters')


def setupKey():
    global keyArray, KEY
    tmpKeyArray = []

    validateKey()
    i = 0
    for indice in range(0, KEY_LEN):
        tmpKeyArray.append(KEY[i])
        i += 1
    tmpKeyArray = bm.invertBitsList(tmpKeyArray)
    i = 0
    for indice in range(0, (KEY_LEN >> 1)):
        keyArray.append(tmpKeyArray[i + 1] + tmpKeyArray[i])
        i += 2
    return


def initialize():
    global keyArray, counterArray, stateArray

    for i in range(0, len(keyArray)):
        if bm.even(i):
            stateArray.append(keyArray[(i + 1) % 8] + keyArray[i])
            counterArray.append(keyArray[(i + 4) % 8] + keyArray[(i + 5) % 8])
        else:
            stateArray.append(keyArray[(i + 5) % 8] + keyArray[(i + 4) % 8])
            counterArray.append(keyArray[i] + keyArray[(i + 1) % 8])

def counterUpdate():
    global counterArray, bitCarry, Aconstants

    for i in range(0,8):
        temp = tc.str2int(counterArray[i]) + int(Aconstants[i]) + bitCarry
        bitCarry = temp // WORD_SIZE
        counterArray[i] = hex(temp % WORD_SIZE)

    counterArray = list(map(lambda x: hex(bm.set32bits(tc.hex2int(x))),counterArray))


def square(value):

    value = (value % WORD_SIZE) * (value % WORD_SIZE)
    #print(value.bit_length())
    return value


def gFunction(v1,v2):
    #print(v1.bit_length(),v2.bit_length())
    x = bm.LSB(square(v1 + v2)) ^ bm.MSB(square(v1 + v2))
    return hex(bm.set64bits(bm.rightShift(bm.set64bits(x),32)) >> 32)



def stateUpdate():
    global gArray, stateArray, counterArray
    # The core of the Rabbit algorithm is the next - state function.It is based on the function g, which transforms two
    # 32 - bit inputs into one 32 - bit output, as follows:
    # g(u, v) = LSW(square(u + v)) ^ MSW(square(u + v)) where
    # square(u + v) = ((u + v mod WORDSIZE) * (u + v mod WORDSIZE)).

    # X0 = G0 + (G7 << < 16) + (G6 << < 16) mod WORDSIZE
    # X1 = G1 + (G0 << < 8) + G7 mod WORDSIZE
    # X2 = G2 + (G1 << < 16) + (G0 << < 16) mod WORDSIZE
    # X3 = G3 + (G2 << < 8) + G1 mod WORDSIZE
    # X4 = G4 + (G3 << < 16) + (G2 << < 16) mod WORDSIZE
    # X5 = G5 + (G4 << < 8) + G3 mod WORDSIZE
    # X6 = G6 + (G5 << < 16) + (G4 << < 16) mod WORDSIZE
    # X7 = G7 + (G6 << < 8) + G5 mod WORDSIZE

    for i in range(0,8):
        gArray.append(gFunction(tc.str2int(stateArray[i]),tc.hex2int(counterArray[i])))

    stateArray[0] = (tc.hex2int(gArray[0]) + bm.leftShift(tc.hex2int(gArray[7]), 16) + bm.leftShift(tc.hex2int(gArray[6]), 16)) % WORD_SIZE
    stateArray[1] = (tc.hex2int(gArray[1]) + bm.leftShift(tc.hex2int(gArray[0]), 8) + tc.hex2int(gArray[7])) % WORD_SIZE
    stateArray[2] = (tc.hex2int(gArray[2]) + bm.leftShift(tc.hex2int(gArray[1]), 16) + bm.leftShift(tc.hex2int(gArray[0]), 16)) % WORD_SIZE
    stateArray[3] = (tc.hex2int(gArray[3]) + bm.leftShift(tc.hex2int(gArray[2]), 8) + tc.hex2int(gArray[1])) % WORD_SIZE
    stateArray[4] = (tc.hex2int(gArray[4]) + bm.leftShift(tc.hex2int(gArray[3]), 16) + bm.leftShift(tc.hex2int(gArray[2]), 16)) % WORD_SIZE
    stateArray[5] = (tc.hex2int(gArray[5]) + bm.leftShift(tc.hex2int(gArray[4]), 8) + tc.hex2int(gArray[3])) % WORD_SIZE
    stateArray[6] = (tc.hex2int(gArray[6]) + bm.leftShift(tc.hex2int(gArray[5]), 16) + bm.leftShift(tc.hex2int(gArray[4]), 16)) % WORD_SIZE
    stateArray[7] = (tc.hex2int(gArray[7]) + bm.leftShift(tc.hex2int(gArray[6]), 8) + tc.hex2int(gArray[5])) % WORD_SIZE

    stateArray = list(map(lambda x: hex(bm.set32bits(x)),stateArray))


def reinitializeCounter():
    global counterArray
    # Cj = Cj ^ X(j + 4 mod 8)
    for i in range(0,len(counterArray)):
        counterArray[i] = tc.hex2int(counterArray[i]) ^ tc.hex2int(stateArray[(i + 4) % 8])

    counterArray = list(map(lambda x: hex(bm.set32bits(x)),counterArray))



# TODO: IV Setup 2.4





try:
    setupKey()
except ValueError as err:
    print(err.args[0])

initialize()
for i in range(0,4):
    counterUpdate()
    stateUpdate()

reinitializeCounter()

print(stateArray)
print(counterArray)
# print(gArray)
# print(list(map(lambda x: int(x,16).bit_length(),stateArray)))
# print(list(map(lambda x: int(x,16).bit_length(),counterArray)))