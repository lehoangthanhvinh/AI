Col=('a','b','c','d','e','f','g','h')
Row=('8','7','6','5','4','3','2','1')
def TestFunc(EnPassant):
    if EnPassant!='-': EnPassant=(Row.index(EnPassant[1]),Col.index(EnPassant[0]))
    print(EnPassant)
TestFunc('e4')