from ChessData import BoardState,Col,Row,InitialBoard
def BSToFEN(PlayingBoard,MoveCount,TurnCount):
    # thiet lap
    Board=PlayingBoard.board
    Turn=PlayingBoard.turn
    Castle=PlayingBoard.castle
    LastMove=PlayingBoard.lastmove
    FENCode=''
    #truong 1 (ban co)
    Counter=0
    for i in range(8):
        for j in range(8):
            if Board[i][j]!='.':
                if Counter!=0:
                    FENCode=FENCode+str(Counter)
                    Counter=0
                FENCode=FENCode+Board[i][j]
            else: Counter+=1
        if Counter!=0:
            FENCode=FENCode+str(Counter)
            Counter=0
        if i<7:FENCode=FENCode+'/'
    FENCode=FENCode+' '
    #truong 2 (luot di)
    if Turn==0:
        FENCode=FENCode+'w'
    else:
        FENCode=FENCode+'b'
    FENCode=FENCode+' '
    #truong 3 (nhap thanh)
    Castlable='KQkq'
    for i in range(4):
        if (Castle >> i) & 1:
            FENCode += Castlable[i]
    if not FENCode:
        FENCode = '-'
    FENCode += ' '
    #truong 4 (bat tot qua duong)
    if LastMove is not None:
        FromHere=LastMove[0]
        ToThere=LastMove[1]
        if Board[ToThere[0]][ToThere[1]] in ('P','p') and abs(FromHere[0]-ToThere[0])==2:
            FENCode=FENCode+str(Col[FromHere[1]])+str(Row[(FromHere[0]+ToThere[0])//2])
        else:
            FENCode=FENCode+'-'
    else:
        FENCode=FENCode+'-'
    #truong 5,6 (dem nuoc di)
    FENCode=f"{FENCode} {MoveCount} {TurnCount}"
    #ket qua
    return FENCode
BSToFEN(InitialBoard,0,1)