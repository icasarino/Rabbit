import functools as ft
import operator as op


def str2int(string):
    intList = list(map(lambda x: str(ord(x)), string))
    return int(ft.reduce(op.concat, intList, "")) # === FOLDL

def hex2int(hex):
    return int(hex,16)

def int2hex(int):
    return hex(int)