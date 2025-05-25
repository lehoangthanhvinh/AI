from ChessData import MoveSet,Piece
import copy
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