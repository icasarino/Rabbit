import functools as ft
import operator as op


def str2int(string):
    intList = list(map(lambda x: str(ord(x)), string))
    return int(ft.reduce(op.concat, intList, "")) # === FOLDL

def concatIntArray(array):
	strIntList = list(map(lambda x: str(abs(x)), array))
	return int(ft.reduce(op.concat, strIntList, ""))
	
def hex2int(hex):
    return int(hex,16)

def int2hex(int):
    return hex(int)

	
def splitByLen(item, maxlen):
    return [item[ind:ind+maxlen] for ind in range(0, len(item), maxlen)]
	
def int2ascii(num):
	array = splitByLen(str(num),3)
	length_array = len(array)
	i = 0
	while(i < length_array):
		while(int(array[i]) > 255):
			if(i == len(array) - 1):
				array.append(array[i][-1:])
				array[i] = array[i][:-1]
				length_array += 1
			else:
				array[i + 1] = array[i][-1:] + array[i + 1]
				array[i] = array[i][:-1]
		i += 1

	return ft.reduce(op.concat,list(map(lambda x: chr(int(x)), array)),"")
	