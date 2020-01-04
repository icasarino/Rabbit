#########################################################
# Cyphered Implemented as RFC-4503                      #
#                                                       #
# https://tools.ietf.org/html/rfc4503                   #
#########################################################

import BinaryMethods as bm
import TypeConverter as tc
import sys as s
################################################### GLOBAL VARIABLES ###################################################
WORD_SIZE = 0x100000000
MESSAGE = KEY = OPTION = ""
KEY_LEN = 0

fileName = s.argv[0]
keyArray = []   	# Kx Array
counterArray = []   # Cx Array
stateArray = []     # Xx Array
gArray = []         # Applied gFunction over counterArray and stateArray
sArray = []			#128 bit extraction Scheme array
sValue = 0
bitCarry = 0

Aconstants = [0x4D34D34D,0xD34D34D3,0x34D34D34,0x4D34D34D,0xD34D34D3,0x34D34D34,0x4D34D34D,0xD34D34D3]

################################################### METHODS ###################################################
def printHelp(errorString):
	global fileName
	raise ValueError('\n'+errorString +'\n\nUsage:\n    python.exe '+ fileName +' <[E|D]> <KEY> <MESSAGE>\n\nThe algorithm can be used interactively if no arguments are used\n')

def getShellData():
	global MESSAGE, KEY, OPTION, KEY_LEN
	
	if(s.argv[1] == "E" or s.argv[1] == "D"):
		OPTION = s.argv[1]
	else:
		printHelp("Use E for the encryption process or D for decryption process")
	
	try:
		KEY = s.argv[2]
		KEY_LEN = len(KEY)
		MESSAGE = s.argv[3]
	except:
		printHelp("Verify Command Usage, you may want to use no arguments and proceed interactively")

		
def getData():
	global MESSAGE, KEY, OPTION, KEY_LEN
	print("Insert message >> ")
	MESSAGE = str(input())
	print("Insert Key >> ")
	KEY = str(input())
	#KEY = "holacomoestasvos"
	KEY_LEN = len(KEY)
	print("E to encrypt message, D to decrypt >> ")
	OPTION = str(input())
	
	if(OPTION != "E" and OPTION != "D"):
		raise ValueError('Invalid Option Value')	
	

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
	return value


def gFunction(v1,v2):
	x = bm.LSB(square(v1 + v2)) ^ bm.MSB(square(v1 + v2))
	return hex(bm.set64bits(x))



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

	stateArray[0] = (tc.hex2int(gArray[0]) + bm.rightShift(tc.hex2int(gArray[7]), 16) + bm.rightShift(tc.hex2int(gArray[6]), 16)) % WORD_SIZE
	stateArray[1] = (tc.hex2int(gArray[1]) + bm.rightShift(tc.hex2int(gArray[0]), 24) + tc.hex2int(gArray[7])) % WORD_SIZE
	stateArray[2] = (tc.hex2int(gArray[2]) + bm.rightShift(tc.hex2int(gArray[1]), 16) + bm.rightShift(tc.hex2int(gArray[0]), 16)) % WORD_SIZE
	stateArray[3] = (tc.hex2int(gArray[3]) + bm.rightShift(tc.hex2int(gArray[2]), 24) + tc.hex2int(gArray[1])) % WORD_SIZE
	stateArray[4] = (tc.hex2int(gArray[4]) + bm.rightShift(tc.hex2int(gArray[3]), 16) + bm.rightShift(tc.hex2int(gArray[2]), 16)) % WORD_SIZE
	stateArray[5] = (tc.hex2int(gArray[5]) + bm.rightShift(tc.hex2int(gArray[4]), 24) + tc.hex2int(gArray[3])) % WORD_SIZE
	stateArray[6] = (tc.hex2int(gArray[6]) + bm.rightShift(tc.hex2int(gArray[5]), 16) + bm.rightShift(tc.hex2int(gArray[4]), 16)) % WORD_SIZE
	stateArray[7] = (tc.hex2int(gArray[7]) + bm.rightShift(tc.hex2int(gArray[6]), 24) + tc.hex2int(gArray[5])) % WORD_SIZE

	stateArray = list(map(lambda x: hex(bm.set32bits(x)),stateArray))


def reinitializeCounter():
	global counterArray
	# Cj = Cj ^ X(j + 4 mod 8)
	for i in range(0,len(counterArray)):
		counterArray[i] = tc.hex2int(counterArray[i]) ^ tc.hex2int(stateArray[(i + 4) % 8])

	counterArray = list(map(lambda x: hex(bm.set32bits(x)),counterArray))


def extractionScheme():
	
	global sArray,sValue

	sArray.append(bm.LSB(tc.hex2int(stateArray[0])) ^ bm.MSB(tc.hex2int(stateArray[5])))
	sArray.append(bm.MSB(tc.hex2int(stateArray[0])) ^ bm.LSB(tc.hex2int(stateArray[3])))
	sArray.append(bm.LSB(tc.hex2int(stateArray[2])) ^ bm.MSB(tc.hex2int(stateArray[7])))
	sArray.append(bm.MSB(tc.hex2int(stateArray[2])) ^ bm.LSB(tc.hex2int(stateArray[5])))
	sArray.append(bm.LSB(tc.hex2int(stateArray[4])) ^ bm.MSB(tc.hex2int(stateArray[1])))
	sArray.append(bm.MSB(tc.hex2int(stateArray[4])) ^ bm.LSB(tc.hex2int(stateArray[7])))
	sArray.append(bm.LSB(tc.hex2int(stateArray[6])) ^ bm.MSB(tc.hex2int(stateArray[3])))
	sArray.append(bm.MSB(tc.hex2int(stateArray[6])) ^ bm.LSB(tc.hex2int(stateArray[1])))

	# S[15..0]    = X0[15..0]  ^ X5[31..16]
	# S[31..16]   = X0[31..16] ^ X3[15..0]
	# S[47..32]   = X2[15..0]  ^ X7[31..16]
	# S[63..48]   = X2[31..16] ^ X5[15..0]
	# S[79..64]   = X4[15..0]  ^ X1[31..16]
	# S[95..80]   = X4[31..16] ^ X7[15..0]
	# S[111..96]  = X6[15..0]  ^ X3[31..16]
	# S[127..112] = X6[31..16] ^ X1[15..0]
	
	
	
# TODO: IV Setup 2.4


def encryptMessage(string):
	retVal = ""
	i = 0
	retVal += hex(tc.str2int(string[i:]) ^ sValue)[2:]
	'''
	while(i + 16 < len(string)):
		retVal += hex(tc.str2int(string[i:i + 16]) ^ sValue)[2:]
		i = i + 16
	
	if(i + 16 >= len(string)):
		retVal += hex(tc.str2int(string[i:]) ^ sValue)[2:]
	'''
	
	return retVal

def decryptMessage(hex_string):
	retVal = ""
	i = 0
	retVal += tc.int2ascii(int(hex_string[i:],16) ^ sValue)
	'''
	while(i + 32 < len(hex_string)):
		retVal += tc.int2ascii(int(hex_string[i:i + 32],16) ^ sValue)
		i = i + 32
	
	if(i + 32 >= len(hex_string)):
		retVal += tc.int2ascii(int(hex_string[i:],16) ^ sValue)
	'''
	
	return retVal
	
################################################### MAIN PROCEDURE ###################################################


try:
	if(len(s.argv) == 0):
		getData()
	else:
		getShellData()
		
	setupKey()
except (ValueError, IndexError) as err:
	print(err.args[0])
	s.exit(1)


initialize()

for i in range(0,4):
	counterUpdate()
	stateUpdate()

reinitializeCounter()
extractionScheme()

if(OPTION == "E"):
	print(encryptMessage(MESSAGE))
else:
	print(decryptMessage(MESSAGE))