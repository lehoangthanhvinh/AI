from AIData import BoardState,Col,Row,Piece,MoveSet,Pressure,CheckBoard,TracingRay,CrossRay,PlusRay
import copy,time
def FENToBS(FENCode):
    [BoardCode,Turn,CastleCode,EnPassant,MoveCount,TurnCount]=FENCode.split(" ",6)
    Board=[['.' for _ in range(8)] for _ in range(8)]
    i=0
    for char in BoardCode:
        if char.isdigit():
            i+=int(char)
        elif char=='/':
            continue
        else:
            Board[i//8][i%8]=char
            i+=1
    if Turn=='w': Turn=0
    else: Turn=1
    if EnPassant!='-': 
        EnPassant=(Row.index(EnPassant[1]),Col.index(EnPassant[0]))
        if EnPassant[0]==2:
            LastMove=((1,EnPassant[1]),(3,EnPassant[1]))
        elif EnPassant[0]==5:
            LastMove=((6,EnPassant[1]),(4,EnPassant[1]))
    else: LastMove=None
    Castle=0
    if 'K' in CastleCode: Castle+=1
    if 'Q' in CastleCode: Castle+=2
    if 'k' in CastleCode: Castle+=4
    if 'q' in CastleCode: Castle+=8
    PlayingBoard=BoardState(Board,Turn,Castle,LastMove)
    return (PlayingBoard,MoveCount,TurnCount)
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
def MaxDivision(a,b):
    returnValue=1
    for i in range(1,max(abs(a),abs(b))+1):
        if abs(a)%i==0 and abs(b)%i==0:
            returnValue=i
    return returnValue
def InRange(x,y):
    if x<0 or x>7 or y<0 or y>7:
        return 0
    return 1
def CheckLegal(PlayingBoard):
    KingPos=()
    Side=PlayingBoard.turn
    Board=PlayingBoard.board
    for i in range(64):
        x=i//8
        y=i%8
        if Board[x][y]==Piece[Side][0]:
            KingPos=(x,y)
            break
    Side=1-Side
    for i in range(8):
        for j in range(8):
            if Board[i][j] in Piece[Side]:
                (Movable,Takable)=ChessMove(Board[i][j],(i,j),PlayingBoard,False)
                if KingPos in Takable: return KingPos
    return 0
def KingMove(PieceID,Move,PlayingBoard,Movable,Takable):
    Board=PlayingBoard.board
    Castle=PlayingBoard.castle
    from ChessWindow import Checked
    if Checked==0:
        if PieceID=='K':
            if Castle&3:
                if Castle&1 and (7,5) in Movable and Board[7][6]=='.':
                    Movable.append((7,6))
                if Castle&2 and (7,3) in Movable and Board[7][2]=='.' and Board[7][1]=='.':
                    Movable.append((7,2))
        if PieceID=='k':
            if Castle&12:
                if Castle&4 and (0,5) in Movable and Board[0][6]=='.':
                    Movable.append((0,6))
                if Castle&8 and (0,3) in Movable and Board[0][2]=='.' and Board[0][1]=='.':
                    Movable.append((0,2))
def PawnMove(PieceID,Move,PlayingBoard,Movable,Takable):
    Board=PlayingBoard.board
    x=Move[0]
    y=Move[1]
    LastMove=PlayingBoard.lastmove
    if PieceID=='P':
        if x==6 and (5,y) in Movable and Board[4][y]=='.':
            Movable.append((4,y))
        if InRange(x-1,y+1) and Board[x-1][y+1] in Piece[1]:
            Takable.append((x-1,y+1))
        if InRange(x-1,y-1) and Board[x-1][y-1] in Piece[1]:
            Takable.append((x-1,y-1))
        if LastMove is not None:
            if x==3 and LastMove[0][0]==1 and abs(LastMove[0][1]-y)==1:
                if Board[LastMove[1][0]][LastMove[1][1]]=='p':
                    Takable.append((2,LastMove[0][1]))
    elif PieceID=='p':
        if x==1 and (2,y) in Movable and Board[3][y]=='.':
            Movable.append((3,y))
        if InRange(x+1,y+1) and Board[x+1][y+1] in Piece[0]:
            Takable.append((x+1,y+1))
        if InRange(x+1,y-1) and Board[x+1][y-1] in Piece[0]:
            Takable.append((x+1,y-1))
        if LastMove is not None:
            if x==4 and LastMove[0][0]==6 and abs(LastMove[0][1]-y)==1:
                if Board[LastMove[1][0]][LastMove[1][1]]=='P':
                    Takable.append((5,LastMove[0][1]))
def ChessMove(PieceID,Pos,PlayingBoard,Called):
    Board=PlayingBoard.board
    x=Pos[0]
    y=Pos[1]
    Movable=[]
    Takable=[]
    MoveRule=MoveSet[PieceID]
    for i in range(len(MoveRule[0])):
        d=MaxDivision(MoveRule[0][i],MoveRule[1][i])
        dx=MoveRule[0][i]//d
        dy=MoveRule[1][i]//d
        for j in range(1,d+1):
            x0=x+dx*j
            y0=y+dy*j
            if InRange(x0,y0):
                if(Board[x0][y0]=='.'): Movable.append((x0,y0))
                else:
                    if not any(PieceID in group and Board[x0][y0] in group for group in Piece):
                        if PieceID not in ('P','p'): Takable.append((x0,y0))
                    break
            else: break
    if PieceID in ('P','p'):PawnMove(PieceID,Pos,PlayingBoard,Movable,Takable)
    if Called:
        for MkMove in Movable+Takable:
            EvalBoard=copy.deepcopy(PlayingBoard)
            EvalBoard.board[MkMove[0]][MkMove[1]]=EvalBoard.board[x][y]
            EvalBoard.board[x][y]='.'
            if CheckLegal(EvalBoard)!=0:
                if MkMove in Movable: Movable.remove(MkMove)
                else: Takable.remove(MkMove)
    if PieceID in ('K','k'):KingMove(PieceID,Pos,PlayingBoard,Movable,Takable)
    if Called and PlayingBoard.castle and PieceID in ('K','k'):
        CastleSqr=((0,2),(0,6),(7,6),(7,2))
        for MkMove in CastleSqr:
            if MkMove in Movable:
                EvalBoard=copy.deepcopy(PlayingBoard)
                EvalBoard.board[MkMove[0]][MkMove[1]]=EvalBoard.board[x][y]
                EvalBoard.board[x][y]='.'
                if CheckLegal(EvalBoard)!=0: Movable.remove(MkMove)
    return (Movable,Takable)
def PosibleMove(PlayingBoard):
    Board=PlayingBoard.board
    Turn=PlayingBoard.turn
    Castle=PlayingBoard.castle
    PosMove=[]
    for i in range(8):
        for j in range(8):
            if Board[i][j] in Piece[Turn]:
                (Movable,Takable)=ChessMove(Board[i][j],(i,j),PlayingBoard,True)
                for Move in Movable+Takable:
                    PosMove.append(((i,j),Move))
    return PosMove
def MakeMove(PlayingBoard,FromHere,ToThere):
    Board=PlayingBoard.board
    PieceCaptured=Board[ToThere[0]][ToThere[1]]
    Special=0
    if Board[FromHere[0]][FromHere[1]] in ('P','p') and ToThere[0] in (0,7):
        Board[FromHere[0]][FromHere[1]]='Q' if Board[FromHere[0]][FromHere[1]]=='P' else 'q'
        Special=1
    if Board[FromHere[0]][FromHere[1]] in ('P','p') and ToThere[1]!=FromHere[1] and Board[ToThere[0]][ToThere[1]]=='.': 
        Board[FromHere[0]][ToThere[1]]='.'
        Special=2
    if Board[FromHere[0]][FromHere[1]] in ('K','k') and abs(ToThere[1]-FromHere[1])==2:
        if ToThere[1]==6:
            Board[FromHere[0]][5]='R' if Board[FromHere[0]][FromHere[1]]=='K' else 'r'
            Board[FromHere[0]][7]='.'
        elif ToThere[1]==2:
            Board[FromHere[0]][3]='R' if Board[FromHere[0]][FromHere[1]]=='K' else 'r'
            Board[FromHere[0]][0]='.'
        Special=3
    Board[ToThere[0]][ToThere[1]]=Board[FromHere[0]][FromHere[1]]
    Board[FromHere[0]][FromHere[1]]='.'
    PlayingBoard.turn=1-PlayingBoard.turn
    return (PieceCaptured,Special)
def UnmakeMove(PlayingBoard,FromHere,ToThere,MoveCode):
    Board=PlayingBoard.board
    PieceCaptured=MoveCode[0]
    Special=MoveCode[1]
    if Special==1:
        Board[FromHere[0]][FromHere[1]]='P' if Board[FromHere[0]][FromHere[1]] in Piece[0] else 'p'
    elif Special==2:
        Board[ToThere[0]][FromHere[1]]='p' if Board[FromHere[0]][FromHere[1]] in Piece[0] else 'P'
    elif Special==3:
        if Board[FromHere[0]][FromHere[1]+1] in ('R','r'):
            Board[FromHere[0]][0]=Board[FromHere[0]][FromHere[1]+1]
            Board[FromHere[0]][FromHere[1]+1]='.'
        elif Board[FromHere[0]][FromHere[1]-1] in ('R','r'):
            Board[FromHere[0]][7]=Board[FromHere[0]][FromHere[1]-1]
            Board[FromHere[0]][FromHere[1]-1]='.'
    Board[ToThere[0]][ToThere[1]]=Board[FromHere[0]][FromHere[1]]
    Board[FromHere[0]][FromHere[1]]=PieceCaptured
    PlayingBoard.turn=1-PlayingBoard.turn
def PressureBoard(PresBoard,Board,AfterBoard):
    Now=time.time()
    if AfterBoard is None:
        for i in range(8):
            for j in range(8):
                PieceID=Board[i][j]
                if PieceID=='.':continue
                if PieceID in ('K','k','N','n','P','p'):
                    CheckRule=CheckBoard[PieceID]
                else:
                    CheckRule=TracingRay[PieceID]
                CheckPress(PresBoard,PieceID,(i,j),CheckRule,1)
    else:
        pass
    #for row in PresBoard:print(row)
    #print(time.time()-Now)
def CheckPress(PresBoard,PieceID,Position,Rule,PlusValue):
    Side=(PieceID==PieceID.lower())
    if PieceID in ('K','k','N','n','P','p'):
        for i in range(5):
            for j in range(5):
                if InRange(Position[0]+i-2,Position[1]+j-2) and Rule[i][j]:
                    PresBoard[Position[0]+i-2][Position[1]+j-2][Side]+=Pressure[PieceID]*PlusValue
    else:
        for Dir in Rule:
            for i in range(1,8):
                if InRange(Position[0]+Dir[0]*i,Position[1]+Dir[1]*i):
                    PresBoard[Position[0]+Dir[0]*i][Position[1]+Dir[1]*i][Side]+=Pressure[PieceID]*PlusValue
                    if Board[Position[0]+Dir[0]*i][Position[1]+Dir[1]*i]!='.': break
Board=[
    ['r','.','.','.','.','r','k','.'],
    ['p','b','p','p','.','p','p','.'],
    ['.','p','n','.','.','q','.','p'],
    ['b','.','.','.','p','.','.','.'],
    ['.','.','B','.','P','.','.','.'],
    ['P','.','N','P','.','N','.','.'],
    ['.','P','P','.','.','P','P','P'],
    ['R','.','.','Q','R','.','K','.']
]
PresBoard=[[[0,0] for _ in range(8)] for _ in range(8)]
PressureBoard(PresBoard,Board,None)
#TestBoard=BoardState(Board,1,15,None)
#MoveCode=MakeMove(TestBoard,(5,5),(2,5))
#for row in TestBoard.board: print(row)
#print('\n')
#UnmakeMove(TestBoard,(2,5),(5,5),MoveCode)
#for row in TestBoard.board: print(row)
