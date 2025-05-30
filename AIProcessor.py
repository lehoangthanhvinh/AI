from AISupportFunc import FENToBS,BSToFEN,ChessMove,MakeMove,UnmakeMove
from AIData import Piece,Col,Row,PieceValue,PositionValue
import random,math,time,heapq
depth=3
MemList={}
Now=0
TimeLim=10
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
    global MemList,Now
    Now=time.time()
    (PlayingBoard,MoveCount,TurnCount)=FENToBS(FENCode)
    PosMove=PosibleMove(PlayingBoard)
    FENPart=FENCode.split(' ',6)
    FENTrim=' '.join(FENPart[:4])    
    #remove later
    MemList={}
    #------------
    try:
        return MemList[FENTrim][0]
    except:
        Evalue=EvaluateBoard(PlayingBoard,int(TurnCount))
    if PlayingBoard.turn==0:Maximize(PlayingBoard,0,Evalue,FENTrim,int(TurnCount),-math.inf,math.inf)
    else: Minimize(PlayingBoard,0,Evalue,FENTrim,int(TurnCount),-math.inf,math.inf)
    #for elem in MemList:print(MemList[elem])
    print(f"Response time: {time.time()-Now}")
    if MemList[FENTrim][0]!=((8,8),(8,8)):
        return MemList[FENTrim][0]
    else:
        print("Random Move")
        return random.choice(PosMove)
def Maximize(PlayingBoard,SearchDepth,EvalueScore,FENTrim,TurnCount,alpha,beta):
    try: 
        return MemList[FENTrim][1]
    except:
        pass
    PosMove=PosibleMove(PlayingBoard)
    if not PosMove:
        return -10000
    if SearchDepth>=depth:
        MemList[FENTrim]=(random.choice(PosMove),EvalueScore)
        return EvalueScore
    Response=(((8,8),(8,8)),alpha)
    MoveRating=[]
    for Move in PosMove:
        MoveMade=MakeMove(PlayingBoard,Move[0],Move[1])
        Evalue=EvaluateBoard(PlayingBoard,TurnCount)
        Str='  '*SearchDepth
        #print(f"{Str}Move from {Move[0]} to {Move[1]} Score={Evalue}")
        if Evalue<-10000 or Evalue>10000 or Evalue<EvalueScore-100:
            UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
            continue
        #print(f"{Str}Keep going")
        heapq.heappush(MoveRating,(-Evalue,Move))
        UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
    while MoveRating:
        (Evalue,Move)=heapq.heappop(MoveRating)
        Evalue=-Evalue
        MoveMade=MakeMove(PlayingBoard,Move[0],Move[1])
        NextFENTrim=BSToFEN(PlayingBoard,0,TurnCount)
        NextFENPart=NextFENTrim.split(' ',6)
        NextFENTrim=' '.join(NextFENPart[:4])
        Score=Minimize(PlayingBoard,SearchDepth+1,Evalue,NextFENTrim,TurnCount,Response[1],beta)
        UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
        if Score>Response[1]:
            Response=(Move,Score)
            if Response[1]>=beta: break
    MemList[FENTrim]=Response
    return Response[1]
def Minimize(PlayingBoard,SearchDepth,EvalueScore,FENTrim,TurnCount,alpha,beta):
    try: 
        return MemList[FENTrim][1]
    except:
        pass
    PosMove=PosibleMove(PlayingBoard)
    if not PosMove:
        return 10000
    if SearchDepth>=depth:
        MemList[FENTrim]=(random.choice(PosMove),EvalueScore)
        return EvalueScore
    Response=(((8,8),(8,8)),beta)
    MoveRating=[]
    for Move in PosMove:
        MoveMade=MakeMove(PlayingBoard,Move[0],Move[1])
        Evalue=EvaluateBoard(PlayingBoard,TurnCount)
        Str='  '*SearchDepth
        #print(f"{Str}Move from {Move[0]} to {Move[1]} Score={Evalue}")
        if Evalue<-10000 or Evalue>10000 or Evalue>EvalueScore+100:
            UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
            continue
        #print(f"{Str}Keep going")
        heapq.heappush(MoveRating,(Evalue,Move))
        UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
    while MoveRating:
        (Evalue,Move)=heapq.heappop(MoveRating)
        MoveMade=MakeMove(PlayingBoard,Move[0],Move[1])
        NextFENTrim=BSToFEN(PlayingBoard,1,TurnCount)
        NextFENPart=NextFENTrim.split(' ',6)
        NextFENTrim=' '.join(NextFENPart[:4])
        Score=Maximize(PlayingBoard,SearchDepth+1,Evalue,NextFENTrim,TurnCount+1,alpha,Response[1])
        UnmakeMove(PlayingBoard,Move[1],Move[0],MoveMade)
        if Score<Response[1]:
            Response=(Move,Score)
            if Response[1]<=alpha: break
    MemList[FENTrim]=Response
    return Response[1]
def EvaluateBoard(PlayingBoard,TurnCount):
    Board=PlayingBoard.board
    Score=0
    for i in range(8):
        for j in range(8):
            if Board[i][j]=='.':continue
            if TurnCount<=15:TurnCount=0
            elif TurnCount<=40:TurnCount=1
            else:TurnCount=2
            PositionMap=PositionValue[TurnCount][Board[i][j]]
            if Board[i][j] in Piece[1]:
                Score=Score+PieceValue[Board[i][j]]-PositionMap[7-i][j]
            else: 
                Score=Score+PieceValue[Board[i][j]]+PositionMap[i][j]
    return Score