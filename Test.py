import BinaryMethods as bm

def assertion(query,result):
    return query == result

a = 60

print("Right Shift: bm.rightShift(a,3) == 39", assertion(bm.rightShift(a,3),39)) # ==> 39
print("Left Shift: bm.leftShift(a,2)", assertion(bm.leftShift(a,2),51)) # ==> 51
print("SwapBits Every Complementary Bit: bm.swapBits(bm.swapBits(bm.swapBits(a,0,5),1,4),2,3) == 15",assertion(bm.swapBits(bm.swapBits(bm.swapBits(a,0,5),1,4),2,3),15)) # ==> 15
print("SwapBits Same Bit:bm.swapBits(a,2,2))",assertion(bm.swapBits(a,2,2),60)) # ==> 60


