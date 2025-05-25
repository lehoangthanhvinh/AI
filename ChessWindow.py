import pygame
import copy,time
pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Chess Board")
WHITE=( 255, 255, 255)
BLACK=(   0,   0,   0)
WHTSQ=( 200, 200, 200)
BLKSQ=( 100, 100, 100)
REDSQ=( 255,   0,   0)
margin=10
cell_size=100
from ChessData import InitialBoard,ChessImage,Col,Row,Piece
from ChessRule import ChessMove,CheckLegal
from ChessConverter import BSToFEN
from AIProcessor import AIMove,EvaluateBoard
def GameWin():
    global playing
    for i in range(8):
        for j in range(8):
            if Board[i][j] in ('K','k'):
                if Board[i][j] not in Piece[Turn]:
                    image=pygame.image.load("Icon/WINKing.png")
                    image=pygame.transform.scale(image,(80,80))
                    screen.blit(image,(100*j+10,100*i+10))
                else:
                    image=pygame.image.load("Icon/LOSKing.png")
                    image=pygame.transform.scale(image,(80,80))
                    screen.blit(image,(100*j+10,100*i+10))
    playing=0
def GameDraw():
    global playing
    for i in range(8):
        for j in range(8):
            if Board[i][j] in ('K','k'):
                image=pygame.image.load("Icon/DRWKing.png")
                image=pygame.transform.scale(image,(80,80))
                screen.blit(image,(100*j+10,100*i+10))
    playing=0
def BoardUpdate():
    global Checked,MoveCount
    for i in range(64):
        x=i//8;y=i%8
        if (x+y)%2==0: screen.fill(WHTSQ,(y*100,x*100,100,100))
        else: screen.fill(BLKSQ,(y*100,x*100,100,100))
    for i in range(8):
        for j in range(8):
            if Board[i][j]=='.':continue
            image=pygame.image.load(ChessImage[Board[i][j]])
            image=pygame.transform.scale(image,(80,80))
            screen.blit(image,(100*j+10,100*i+10))
    if PlayingBoard.lastmove is not None:
        CurPos=PlayingBoard.lastmove[1]
        PrvPos=PlayingBoard.lastmove[0]
        image=pygame.image.load("Icon/CURPos.png")
        image=pygame.transform.scale(image,(90,90))
        screen.blit(image,(100*CurPos[1]+5,100*CurPos[0]+5))
        image=pygame.image.load("Icon/PRVPos.png")
        image=pygame.transform.scale(image,(60,60))
        screen.blit(image,(100*PrvPos[1]+20,100*PrvPos[0]+20))
    if Movable or Takable:
        for Index in Movable:
            image=pygame.image.load("Icon/Dots.png")
            image=pygame.transform.scale(image,(100,100))
            screen.blit(image,(100*Index[1],100*Index[0]))
        for Index in Takable:
            image=pygame.image.load("Icon/Take.png")
            image=pygame.transform.scale(image,(90,90))
            screen.blit(image,(100*Index[1]+5,100*Index[0]+5))
    Checked=CheckLegal(PlayingBoard)
    if Checked:
        image=pygame.image.load("Icon/Take.png")
        image=pygame.transform.scale(image,(90,90))
        screen.blit(image,(100*Checked[1]+5,100*Checked[0]+5))
    for num in range(64):
        i=num//8
        j=num%8
        if Board[i][j] in Piece[Turn]:
            (Move,Take)=ChessMove(Board[i][j],(i,j),PlayingBoard,True)
            if Move or Take:
                break
    if not (Move or Take):
        if Checked:
            GameWin()
        else:
            GameDraw()
    if MoveCount>=50:
        GameDraw()
    pygame.display.update()
def MakeMove(FromHere,ToThere):
    global MoveCount
    if Board[FromHere[0]][FromHere[1]] in ('P','p') or Board[ToThere[0]][ToThere[1]]!='.':
        MoveCount=0
    else:
        MoveCount+=1
    if Board[FromHere[0]][FromHere[1]] in ('P','p'):
        if ToThere[1]!=FromHere[1] and Board[ToThere[0]][ToThere[1]]=='.':
            Board[FromHere[0]][ToThere[1]]='.'
        if (ToThere[0]==0 or ToThere[0]==7) and Turn in HumanTurn:
            if Board[FromHere[0]][FromHere[1]]=='P':
                promote=[['Q','R'],['B','N']]
                screen.fill(WHITE)
                for i in range(2):
                    for j in range(2):
                        image=pygame.image.load(ChessImage[promote[i][j]])
                        image=pygame.transform.scale(image,(320,320))
                        screen.blit(image,(400*j+40,400*i+40))
                        pygame.display.update()
                wait=True
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            y,x=event.pos
                            y=y//400
                            x=x//400
                            Board[FromHere[0]][FromHere[1]]=promote[x][y]
                            wait=False
            elif Board[FromHere[0]][FromHere[1]]=='p':
                promote=[['q','r'],['b','n']]
                screen.fill(WHITE)
                for i in range(2):
                    for j in range(2):
                        image=pygame.image.load(ChessImage[promote[i][j]])
                        image=pygame.transform.scale(image,(320,320))
                        screen.blit(image,(400*j+40,400*i+40))
                        pygame.display.update()
                wait=True
                while wait:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            y,x=event.pos
                            y=y//400
                            x=x//400
                            Board[FromHere[0]][FromHere[1]]=promote[x][y]
                            wait=False
        elif (ToThere[0]==0 or ToThere[0]==7) and Turn in AITurn:
            Board[FromHere[0]][FromHere[1]]=DefaultPromote[Turn]
    elif Board[FromHere[0]][FromHere[1]] in ('K','k'):
        if(abs(FromHere[1]-ToThere[1])==2):
            if ToThere[1]==2:
                Board[FromHere[0]][abs(FromHere[1]+ToThere[1])//2]=Board[FromHere[0]][0]
                Board[FromHere[0]][0]='.'
            elif ToThere[1]==6:
                Board[FromHere[0]][abs(FromHere[1]+ToThere[1])//2]=Board[FromHere[0]][7]
                Board[FromHere[0]][7]='.'
    Board[ToThere[0]][ToThere[1]]=Board[FromHere[0]][FromHere[1]]
    Board[FromHere[0]][FromHere[1]]='.'
    Castle=PlayingBoard.castle
    if Castle&3:
        if Board[7][4]!='K':
            Castle=Castle&12
        else:
            if Board[7][7]!='R':
                Castle=Castle&14
            if Board[7][0]!='R':
                Castle=Castle&13
    if Castle&12:
        if Board[0][4]!='k':
            Castle=Castle&3
        else:
            if Board[0][7]!='r':
                Castle=Castle&11
            if Board[0][0]!='r':
                Castle=Castle&7
    PlayingBoard.castle=Castle
running=True    
while running:
    Movable=[]
    Takable=[]
    MoveCount=0
    TurnCount=1
    HumanTurn=[0,]
    AITurn=[1]
    PlayingBoard=copy.deepcopy(InitialBoard)
    Board=PlayingBoard.board
    Turn=PlayingBoard.turn
    Choose=None
    Checked=0
    DefaultPromote=['Q','q']
    playing=True
    BoardUpdate()
    while playing:
        if Turn in HumanTurn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing=0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    y,x=event.pos
                    if (Choose is None):
                        if (Board[x//cell_size][y//cell_size] in Piece[Turn]):
                            Choose=(x//cell_size,y//cell_size)
                            (Movable,Takable)=ChessMove(Board[x//cell_size][y//cell_size],(x//cell_size,y//cell_size),PlayingBoard,True)
                    else:
                        if (x//cell_size,y//cell_size) in Movable or (x//cell_size,y//cell_size) in Takable:
                            MakeMove(Choose,(x//cell_size,y//cell_size))
                            print(f"Evaluate value: {EvaluateBoard(PlayingBoard,TurnCount)}, Turn {TurnCount}")
                            PlayingBoard.lastmove=(Choose,(x//cell_size,y//cell_size))
                            Turn=1-Turn
                            if Turn==0:
                                TurnCount+=1
                            PlayingBoard.turn=Turn
                        Choose=None
                        Movable=[]
                        Takable=[]
                    BoardUpdate()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing=0
            ReturnMove=AIMove(BSToFEN(PlayingBoard,MoveCount,TurnCount))
            try:
                (FromHere,ToThere,Promote)=ReturnMove
                if Promote in ('Q','R','B','N'): DefaultPromote[0]=Promote
                elif Promote in ('q','r','b','n'): DefaultPromote[1]=Promote
            except:
                (FromHere,ToThere)=ReturnMove
            (Movable,Takable)=ChessMove(Board[FromHere[0]][FromHere[1]],(FromHere[0],FromHere[1]),PlayingBoard,True)
            if (ToThere[0],ToThere[1]) in Movable or (ToThere[0],ToThere[1]) in Takable:
                MakeMove(FromHere,ToThere)
                print(f"Evaluate value: {EvaluateBoard(PlayingBoard,TurnCount)}, Turn {TurnCount}")
                PlayingBoard.lastmove=(FromHere,ToThere)
                Turn=1-Turn
                if Turn==0:
                    TurnCount+=1
                PlayingBoard.turn=Turn
                Choose=None
                Movable=[]
                Takable=[]
                BoardUpdate()
                #time.sleep(0.5)
            else:
                playing=0
    ending=1
    if running:
        while ending:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    ending=0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    ending=0
