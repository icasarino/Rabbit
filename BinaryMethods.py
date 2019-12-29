def rightShift(value, offset):
    """
    Realiza un ciclo en los bits
    Diferencia con operador setea el primer bit con el valor del ultimo
    EJ:
        21 -> 10101
        rightShift(21,1) ==> 26 -> 11010
        21 >> 1 ==> 10 -> 01010
    """
    numBits = value.bit_length() - 1
    for i in range(0, offset):
        bit = value & 1
        value = (value >> 1) ^ (bit << numBits)
    return value

def leftShift(value, offset):
    """
    Realiza un ciclo en los bits
    Diferencia con operador setea el último bit con el valor del primero y no agrega bits al número
    EJ:
        21 -> 10101
        leftShift(21,1) ==> 11 -> 01011
        21 << 1 ==> 42 -> 101010
    """
    numBits = value.bit_length() - 1
    mostSignificantValue = 2**(numBits + 1)
    for i in range(0, offset):
        bit = (value >> numBits) & 1
        value = ((value << 1) ^ bit) - mostSignificantValue
    return value


def swapBits(value, offset1, offset2):

    """
    EJ:
        60 -> 111100
        Modificar pos = 1 con pos = 5 (Segundo bit con ultimo)
        bit1 = 000001
        bit2 = 000000
        x (XOR) = 000001
        x (OR) = 000001 | 010000 -> 010001
        value (XOR) = 111100 ^ 010001 = 101101 -> 45
    """

    bit1 = (value >> offset1) & 1 # Mueve el bit a resposicionar al lugar del menos significativo AND 1 ==> Resultado 001 o 000
    bit2 = (value >> offset2) & 1 # Mueve el bit a resposicionar al lugar del menos significativo AND 1 ==> Resultado 001 o 000

    x = bit1 ^ bit2 # XOR entre los dos bits ==> Res 000 o 001
    x = (x << offset1) | (x << offset2) # Resposiciona el bit menos significativo

    return value ^ x # XOR del valor con el reposicionamiento


def invertBits(value):
    bitCount = value.bit_length() - 1
    iterations = bitCount >> 1
    for i in range(0, iterations):
        value = swapBits(value,i, bitCount - i)

    while value.bit_length() < 8:
        value <<= 1
    return value


def invertBitsList(lista):
    return list(map(lambda x: chr(invertBits(ord(x))), lista))


def even(valor):
    """
    & (AND OPERATOR)

    01010 (12) (valor)
    00001 (1)
    00000 (AND) (= 0) ==> valor & 1 === 0 ==> EVEN

    01011 (13) (valor)
    00001 (1)
    00001 (AND) (= 1) ==> valor & 1 === 1 ==> ODD
    """
    return (valor & 1) == 0




def set32bits(value):
    while value.bit_length() < 32:
        value <<= 1
    return value

def set64bits(value):
    while value.bit_length() < 64:
        value <<= 1
    return value

def MSB(value):
    MSWbitLen = value.bit_length() >> 1
    return (value >> MSWbitLen) << MSWbitLen

def LSB(value):
    LSWbitLen = value.bit_length() >> 1
    return leftShift(value,LSWbitLen) >> LSWbitLen

