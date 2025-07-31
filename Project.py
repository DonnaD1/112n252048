from cmu_graphics import *
import random
import copy
############################################################
# Start Screen
############################################################
def start_redrawAll(app): 
    drawLabel('Welcome!', 200, 160, size=24, bold=True)
    drawLabel(f'Highest Number of Moves: {app.highestScore}', 200, 200, size=24)
    drawLabel('Press R for Regular Mode', 200, 220, size=18)
    drawLabel('Press B for Blitz Mode', 200, 240, size=18)
    drawLabel('Press S for Shop', 200, 280, size=18)

def start_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('game')
        app.mode='Regular'
    elif key == 'b':
        setActiveScreen('blitz')
        app.mode='Blitz'
    elif key == 's':
        setActiveScreen('shop')

############################################################
# Game Screen
############################################################
def game_onScreenActivate(app):
    app.score=0
    app.selectedRocket=False

def game_redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel(f'Mode: {app.mode}', 200, 20, size=18)
    drawLabel(f'Score: {app.score}', 200, 40, size=16)
    drawLabel(f'Historical Highest Score: {app.highestScore}', 200, 60, size=16)
    if app.gameOver: 
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawLabel('Game Over', 200, 200, size=70, bold=True, fill='red')
        drawLabel("Press 'r' to restart", 200, 240, size=30, fill='red', bold=True)
        drawLabel(f'Historical Highest Score: {app.highestScore}', 200, 260, size=16, fill='red', bold=True)
    if app.paused: 
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawLabel('Paused', 200, 200, size=70, bold=True, fill='red')
        drawLabel("Press 'space' to unpause", 200, 240, size=30, fill='red', bold=True)
    drawImage('rocket.png', 138, 400, width=60, height=65)

def game_onKeyPress(app, key):
    oldBoard=copy.deepcopy(app.board)
    if key=='left':
        movePiecesLeft(app)
    elif key=='right':
        movePiecesRight(app)
    elif key=='up':
        movePiecesUp(app)
    elif key=='down':
        movePiecesDown(app)
    if app.board!=oldBoard:
        loadPiece(app)
    checkGameOver(app)
    if app.gameOver:
          if key=='r':
              onAppStart(app)
              return 
    elif key=='space': 
         app.paused=not(app.paused)

def onAppStart(app): 
    app.rows=4
    app.cols=4
    app.boardLeft = 75
    app.boardTop = 70
    app.boardWidth = 250
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.gameOver=False
    app.highestScore=0
    app.mode='Regular'
    app.score=0
    app.paused=False
    app.playerMove=False
    loadTileColor(app)
    loadPiece(app)
    loadPiece(app)


def loadTileValue(app): 
    valList=[]
    for i in range(1, 12): 
        value=2**i
        valList.append(value)
    return valList    

def loadTileColor(app): 
    app.valueColor=dict()
    valList=loadTileValue(app)
    for i in range(len(valList)): 
        val=valList[i]
        if val<=64: 
            color='yellow'
            opacity=15*i
        elif val<=256: 
            color='orange'
            opacity=25*(i-4)
        else: 
            color='red'
            opacity=30*(i-8)
        app.valueColor[val]=[color, opacity]


def loadPiece(app): 
    emptyCells=[]
    for i in range(app.rows): 
        for j in range(app.cols): 
            if app.board[i][j]==None: 
                   emptyCells.append((i, j))
    if emptyCells!=[]: 
        (i, j)=random.choice(emptyCells) #learned how to use random (and with weights) from this website: https://pynative.com/python-weighted-random-choices-with-probability/
        valList=[2, 4]
        tileVal=random.choices(valList, weights=(80, 20), k=1)[0]  
        app.board[i][j]=tileVal    

def drawBoard(app):
    for row in range(app. rows):
        for col in range(app.cols):
            color=app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, value):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if value==None: 
        color='lightGray'
        opacity=100
        num=''
    else: 
        color=app.valueColor[value][0]
        opacity=app.valueColor[value][1]
        num=value
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, opacity=opacity)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None,
             border='black',
             borderWidth=app.cellBorderWidth)
    
    if value!='': 
        drawLabel((str(num)), cellLeft+cellWidth/2, cellTop+cellHeight/2, size=16, bold=True)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def pieceCollisionLR(app, row): #piece collision function if left and right keys are pressed
    valsInRow=[]
    for val in row: 
        if val is not None: 
            valsInRow.append(val)
    i=0
    while i<(len(valsInRow)-1): 
        if valsInRow[i]==valsInRow[i+1]:
            newVal=valsInRow[i]+valsInRow[i]
            valsInRow[i]=newVal
            valsInRow[i+1]='Skip'
            i+=2
            app.score+=newVal
        else:
            i+=1
    collidedRow=[]
    for val in valsInRow: 
        if val!='Skip': 
            collidedRow.append(val)
    while len(collidedRow)<len(row): 
        collidedRow.append(None)
    return collidedRow
    
def movePiecesLeft(app):
    for rowNum in range(app.rows): 
        row=app.board[rowNum]
        newRow=pieceCollisionLR(app, row) 
        app.board[rowNum]=newRow

def movePiecesRight(app): 
    for rowNum in range(app.rows):
        row=app.board[rowNum] 
        row.reverse()
        newRow=pieceCollisionLR(app, row) 
        newRow.reverse()
        app.board[rowNum]=newRow

def pieceCollisionUD(app, col): 
    valsInCol=[]
    for val in col:
        if val is not None: 
            valsInCol.append(val)
    i=0
    while i<(len(valsInCol)-1): 
        if valsInCol[i]==valsInCol[i+1]:
            newVal=valsInCol[i]+valsInCol[i]
            valsInCol[i]=newVal
            valsInCol[i+1]='Skip'
            i+=2
            app.score+=newVal
        else:
            i+=1
    collidedCol=[]
    for val in valsInCol: 
        if val!='Skip': 
            collidedCol.append(val)
    while len(collidedCol)<len(col): 
        collidedCol.append(None)
    return collidedCol

def movePiecesUp(app):
    for colNum in range(app.cols): 
        col=[]
        for row in range(app.rows):
            col.append(app.board[row][colNum])
        newCol=pieceCollisionUD(app, col)
        for row in range(app.rows): 
            app.board[row][colNum]=newCol[row]

def movePiecesDown(app): 
    for colNum in range(app.cols): 
        col=[]
        for row in range(app.rows):
            col.append(app.board[row][colNum])
        col.reverse()
        newCol=pieceCollisionUD(app, col)
        newCol.reverse()
        for row in range(app.rows): 
            app.board[row][colNum]=newCol[row]

def isBoardFull(app): 
    for row in range(app.rows): 
        for col in range(app.cols): 
            if app.board[row][col]==None:
                return False
    return True
    
def noLegalMoves(app): 
    for row in range(app.rows): 
        for col in range(app.cols): 
            if row+1<app.rows and app.board[row][col]==app.board[row+1][col]: 
                return False
            elif col+1<app.cols and app.board[row][col]==app.board[row][col+1]: 
                return False
    return True

def checkGameOver(app): 
    if noLegalMoves(app) and isBoardFull(app): 
        app.gameOver=True
        app.highestScore = max(app.highestScore, app.score)

def game_onMousePress(app, mouseX, mouseY): 
    rocketX, rocketY, rocketW, rocketH = 138, 400, 60, 65
    if (rocketX<=mouseX<=rocketX+rocketW and
        rocketY<=mouseY<= rocketY+rocketH):
        app.rocketSelected = True
        print("Rocket selected")
        return      
    if app.rocketSelected:
        activateRocket(app, mouseX, mouseY)
        app.rocketSelected = False


def activateRocket(app, mouseX, mouseY): 
    for row in range(app.rows):
        for col in range(app.cols):
            cellLeft, cellTop=getCellLeftTop(app, row, col)
            cellWidth, cellHeight=getCellSize(app)
            if (cellLeft<=mouseX<=cellLeft+cellWidth and
                cellTop<=mouseY<=cellTop+cellHeight):
                rocketPowerUp = rocket(col)  
                rocketPowerUp.use(app)
                print(f"Rocket used on column {col}")
                app.rocketSelected = False
                return  



############################################################
# Blitz Screen
############################################################
def blitz_onScreenActivate(app):
    app.score=0
    app.timer=2
    app.counter=0

def blitz_redrawAll(app):
    game_redrawAll(app)
    drawLabel(f'Time left: {app.timer}s', 200, 80, size=14)

def blitz_onKeyPress(app, key):
    oldBoard=copy.deepcopy(app.board)
    if key=='left':
        movePiecesLeft(app)
    elif key=='right':
        movePiecesRight(app)
    elif key=='up': 
        movePiecesUp(app)
    elif key=='down':
        movePiecesDown(app)
    if app.board != oldBoard:
        loadPiece(app)
        app.timer = 2
    checkGameOver(app)
    if app.gameOver:
          if key=='r':
              onAppStart(app)
              return 
    elif key=='space': 
         app.paused=not(app.paused)

def onAppStart(app): 
    app.rows=4
    app.cols=4
    app.boardLeft = 75
    app.boardTop = 90
    app.boardWidth = 250
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.gameOver=False
    app.highestScore=0
    app.mode='Blitz'
    app.score=0
    app.paused=False
    app.stepsPerSecond=1
    loadTileColor(app)
    loadPiece(app)
    loadPiece(app)

def blitz_onStep(app): 
    if app.paused==False and app.gameOver==False: 
        app.counter+=1
        if app.counter>2:
            app.counter=0
            app.timer-=1
        if app.timer<=0: 
            moveAutomatically(app)
            app.timer=2

def moveAutomatically(app): 
    moves=[movePiecesLeft, movePiecesRight, movePiecesUp, movePiecesDown] 
    solveMoveAuto(app, moves)

def solveMoveAuto(app, moves): 
    if moves==[]: 
        app.gameOver=True
        return None
    else:
        random.shuffle(moves)
        move=moves[0]
        oldBoard=copy.deepcopy(app.board)
        move(app)
        newBoard=app.board
        if canMakeMove(oldBoard, newBoard): 
            loadPiece(app)
            return True
        else: 
            app.board=oldBoard
        return solveMoveAuto(app, moves[1:])

def canMakeMove(oldBoard, newBoard): 
    return newBoard!=oldBoard

############################################################
# Power ups
############################################################
class rocket: 
    def __init__(self, col): 
        self.col=col

    def use(self, app): 
        for row in range(app.rows): 
            app.board[row][self.col]=None
        loadPiece(app)
    
class torpedo: 
    def __init__(self, row): 
        self.row=row

    def use(self, app): 
        app.board.pop(self.row)
        newRow=[None]*app.cols
        app.board.insert(0, newRow) 

runAppWithScreens(initialScreen='start', height=500)
