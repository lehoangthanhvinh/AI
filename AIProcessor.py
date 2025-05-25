from AISupportFunc import FENToBS,BSToFEN,ChessMove,MakeMove,UnmakeMove
from AIData import Piece,Col,Row,PieceValue,PositionValue
import random,math
depth=3
MemList={}
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
def AIMove(FENCode):
    global MemList
    (PlayingBoard,MoveCount,TurnCount)=FENToBS(FENCode)
    PosMove=PosibleMove(PlayingBoard)
    #remove later
    MemList={}
    #------------
    if PlayingBoard.turn==0:Maximize(PlayingBoard,0,int(MoveCount),int(TurnCount),-math.inf)
    else: Minimize(PlayingBoard,0,int(MoveCount),int(TurnCount),math.inf)
    FENPart=FENCode.split(' ',6)
    FENTrim=' '.join(FENPart[:4])
    for elem in MemList:print(elem)
    try:
        return MemList[FENTrim][0]
    except:
        print("Random Move")
        return random.choice(PosMove)
def Maximize(PlayingBoard,SearchDepth,MoveCount,TurnCount,CurScore):
    EvalFEN=BSToFEN(PlayingBoard,MoveCount,TurnCount)
    FENPart=EvalFEN.split(' ',6)
    FENTrim=' '.join(FENPart[:4])
    try: 
        return MemList[FENTrim][1]
    except:
        pass
    Score=EvaluateBoard(PlayingBoard,TurnCount)
    if Score>=100000 or Score<=-100000 or SearchDepth==depth:
        return Score
    PosMove=PosibleMove(PlayingBoard)
    if not PosMove:
        return -100000
    Score=-math.inf
    for Move in PosMove:
        MoveMade=MakeMove(PlayingBoard,Move[0],Move[1])
        EvalScore=Minimize(PlayingBoard,SearchDepth+1,MoveCount,TurnCount,Score)
        UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
        #print(f"Move from {Col[Move[0][1]]+Row[Move[0][0]]} to {Col[Move[1][1]]+Row[Move[1][0]]}, Score={EvalScore}")
        if Score<EvalScore:
            Score=EvalScore
            MemList[FENTrim]=(Move,Score)
            if Score<CurScore:
                return Score
    return Score
def Minimize(PlayingBoard,SearchDepth,MoveCount,TurnCount,CurScore):
    EvalFEN=BSToFEN(PlayingBoard,MoveCount,TurnCount)
    FENPart=EvalFEN.split(' ',6)
    FENTrim=' '.join(FENPart[:4])
    try: 
        return MemList[FENTrim][1]
    except:
        pass
    Score=EvaluateBoard(PlayingBoard,TurnCount)
    if Score>=100000 or Score<=-100000 or SearchDepth==depth:
        return Score
    PosMove=PosibleMove(PlayingBoard)
    if not PosMove:
        return 100000
    Score=math.inf
    for Move in PosMove:
        MoveMade=MakeMove(PlayingBoard,Move[0],Move[1])
        EvalScore=Maximize(PlayingBoard,SearchDepth+1,MoveCount,TurnCount+1,Score)
        UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
        #print(f"Move from {Col[Move[0][1]]+Row[Move[0][0]]} to {Col[Move[1][1]]+Row[Move[1][0]]}, Score={EvalScore}")
        if Score>EvalScore:
            Score=EvalScore
            MemList[FENTrim]=(Move,Score)
            if Score>CurScore:
                return Score
    return Score
def EvaluateBoard(PlayingBoard,TurnCount):
    Board=PlayingBoard.board
    Score=0
    for i in range(8):
        for j in range(8):
            if Board[i][j]=='.':continue
            PositionMap=PositionValue[min((9+TurnCount)//25,2)][Board[i][j]]
            if Board[i][j] in Piece[1]:
                Score=Score+PieceValue[Board[i][j]]-PositionMap[7-i][j]
            else: 
                Score=Score+PieceValue[Board[i][j]]+PositionMap[i][j]
    return Score