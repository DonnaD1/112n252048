from cmu_graphics import *
import random
import copy
############################################################
# Start Screen
############################################################
def start_redrawAll(app): 
    drawLabel('Welcome to 2048!', 200, 160, size=24, bold=True)
    drawLabel(f'Highest Score: {app.highestScore}', 200, 200, size=24)
    drawLabel('Press R for Regular Mode', 200, 220, size=18)
    drawLabel('Press B for Blitz Mode', 200, 240, size=18)
    drawLabel('Press S for Shop', 200, 280, size=18)
    

def start_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('regular')
        app.mode='Regular'
    elif key == 'b':
        setActiveScreen('blitz')
        app.mode='Blitz'
    elif key == 's':
        setActiveScreen('shop')

############################################################
# Game Screen
############################################################
def onAppStart(app): 
    app.highestScore=0
    app.rocketsOwned=0
    app.torpedoesOwned=0
    app.score=0

def regular_onScreenActivate(app):
    app.rocketSelected=False
    app.torpedoSelected=False

def regular_redrawAll(app):
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
    drawLabel(f'Coins: {app.coins}', 200, 80, size=16)
    drawImage('rocket.png', 75, 400, width=60, height=65)
    drawImage('torpedo.png', 262, 400, width=60, height=65)
    drawLabel(f'{app.rocketsOwned}', 105, 475)
    drawLabel(f'{app.torpedoesOwned}', 292, 475)
    if app.notEnoughPowerUps: 
        drawLabel('Not enough power ups!', 198, 475, size=16)
    if app.win: 
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawLabel('You win!', 200, 200, size=70, bold=True, fill='red')
        drawLabel("Press 'r' to restart", 200, 240, size=30, fill='red', bold=True)
        drawLabel(f'Historical Highest Score: {app.highestScore}', 200, 260, size=16, fill='red', bold=True)
    drawLabel('Press R to go to regular mode and S to access shop', 200, 500, size=15)
    drawLabel('Press space to pause the game', 200, 520, size=15)

def regular_onKeyPress(app, key):
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
    checkWin(app)
    if app.gameOver:
          if key=='r':
              regular_onAppStart(app)
              return 
    elif key=='space': 
         app.paused=not(app.paused)
    if key=='b':
        setActiveScreen('blitz')
        app.mode='Blitz'
    elif key=='s':
        setActiveScreen('shop')

def regular_onMousePress(app, mouseX, mouseY):
    rocketL, rocketT, rocketW, rocketH=75, 400, 60, 65
    if (rocketL<=mouseX<=rocketL+rocketW and
        rocketT<=mouseY<=rocketT+rocketH):
        if app.rocketsOwned==0: 
            app.notEnoughPowerUps=True
            return 
        else: 
            app.notEnoughPowerUps=False
            app.rocketSelected=True
            return 
    if app.rocketSelected:
        activateRocket(app, mouseX, mouseY)
        app.rocketSelected=False
    torpedoL, torpedoT, torpedoW, torpedoH=262, 400, 60, 65
    if (torpedoL<=mouseX<=torpedoL+torpedoW and
        torpedoT<=mouseY<=torpedoT+torpedoH):
        if app.torpedoesOwned==0: 
            app.notEnoughPowerUps=True
            return 
        else: 
            app.notEnoughPowerUps=False
            app.torpedoSelected=True
            return 
    if app.torpedoSelected:
        activateTorpedo(app, mouseX, mouseY)
        app.torpedoSelected=False

def regular_onAppStart(app): #some from Tetris
    app.rows=4
    app.cols=4
    app.boardLeft=75
    app.boardTop=90
    app.boardWidth=250
    app.boardHeight=300
    app.cellBorderWidth=2
    app.board=[([None] * app.cols) for row in range(app.rows)]
    app.gameOver=False
    app.win=False
    app.mode='Regular'
    app.paused=False
    app.playerMove=False
    app.notEnoughPowerUps=False
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

def loadPiece(app): #looked at https://pynative.com/python-weighted-random-choices-with-probability/ for random function
    emptyCells=[]
    for i in range(app.rows): 
        for j in range(app.cols): 
            if app.board[i][j]==None: 
                   emptyCells.append((i, j))
    if emptyCells!=[]: 
        (i, j)=random.choice(emptyCells) 
        valList=[2, 4]
        tileVal=random.choices(valList, weights=(80, 20), k=1)[0]  
        app.board[i][j]=tileVal    

def drawBoard(app): #from Tetris
    for row in range(app. rows):
        for col in range(app.cols):
            color=app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app): #from Tetris
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, value): #from Tetris
    cellLeft, cellTop=getCellLeftTop(app, row, col)
    cellWidth, cellHeight=getCellSize(app)
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

def getCellLeftTop(app, row, col): #from Tetris
    cellWidth, cellHeight=getCellSize(app)
    cellLeft=app.boardLeft+col*cellWidth
    cellTop=app.boardTop+row*cellHeight
    return (cellLeft, cellTop)

def getCellSize(app): #from Tetris
    cellWidth=app.boardWidth / app.cols
    cellHeight=app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def pieceCollisionLR(app, row): #piece collision function if left and right keys are pressed
    valsInRow=[]  #looked at https://www.geeksforgeeks.org/python/2048-game-in-python/ for game logic and algorithms
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
            app.coins+=newVal
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
            if row+1<app.rows and app.board[row][col]==app.board[row+1][col]: #got help during OH for this and elif
                return False
            elif col+1<app.cols and app.board[row][col]==app.board[row][col+1]: 
                return False
    return True

def checkGameOver(app): 
    if noLegalMoves(app) and isBoardFull(app): 
        app.gameOver=True
        app.highestScore=max(app.highestScore, app.score)

def activateRocket(app, mouseX, mouseY): #used ChatGPT for this (specifics are in README)
    for row in range(app.rows): 
        for col in range(app.cols):
            cellLeft, cellTop=getCellLeftTop(app, row, col)
            cellWidth, cellHeight=getCellSize(app)
            if (cellLeft<=mouseX<=cellLeft+cellWidth and
                cellTop<=mouseY<=cellTop+cellHeight):
                rocket=Rocket(col)
                rocket.use(app)
                app.rocketSelected=False 
                app.rocketsOwned-=1

def activateTorpedo(app, mouseX, mouseY): 
    for row in range(app.rows):
        for col in range(app.cols):
            cellLeft, cellTop=getCellLeftTop(app, row, col)
            cellWidth, cellHeight=getCellSize(app)
            if (cellLeft<=mouseX<=cellLeft+cellWidth and
                cellTop<=mouseY<=cellTop+cellHeight):
                torpedoPowerUp=Torpedo(row) 
                torpedoPowerUp.use(app)
                app.torpedoSelected=False 
                app.torpedoesOwned-=1
                return

def checkWin(app): 
    for row in range(app.rows): 
        for col in range(app.cols): 
            if app.board[row][col]==2048: 
                app.win=True
                app.highestScore=max(app.highestScore, app.score)
    return False

############################################################
# Blitz Screen
############################################################
def blitz_onScreenActivate(app):
    app.score=0
    app.timer=2
    app.counter=0

def blitz_redrawAll(app):
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
    drawLabel(f'Time left: {app.timer}s', 200, 80, size=14)
    drawLabel('Press R to go to regular mode', 200, 465, size=15)
    drawLabel('Press space to pause the game', 200, 480, size=15)

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
        app.timer=2
    checkGameOver(app)
    if app.gameOver:
          if key=='r':
              blitz_onAppStart(app)
              return 
    elif key=='space': 
         app.paused=not(app.paused)
    if key == 'r':
        setActiveScreen('regular')
        app.mode='Regular'

def blitz_onAppStart(app): 
    app.rows=4
    app.cols=4
    app.boardLeft=75
    app.boardTop=90
    app.boardWidth=250
    app.boardHeight=300
    app.cellBorderWidth=2
    app.board=[([None]*app.cols) for row in range(app.rows)]
    app.gameOver=False
    app.mode='Blitz'
    app.paused=False
    app.stepsPerSecond=1
    app.coins=0
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

def solveMoveAuto(app, moves): #looked at ttps://www.w3schools.com/python/ref_random_shuffle.asp for random functions
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
class Rocket: 
    def __init__(self, col): 
        self.col=col

    def use(self, app): 
        for row in range(app.rows): 
            app.board[row][self.col]=None
        loadPiece(app)
    
class Torpedo: 
    def __init__(self, row): 
        self.row=row

    def use(self, app): 
        app.board[self.row]=[None]*app.cols
        loadPiece(app)
############################################################
# Shop
############################################################
def shop_onScreenActivate(app):
    app.rocketsOwned=0
    app.torpedoesOwned=0
    app.notEnoughCoins=False

def shop_redrawAll(app): 
    drawImage('rocket.png', 30, 40, width=100, height=120)
    drawLabel(f'Rockets owned: {app.rocketsOwned}', 250, 110, size=20)
    drawLabel('Rocket price: 100', 250, 130, size=20)
    drawRect(30, 160, 100, 50, fill='yellow', opacity=60)
    drawLabel('Buy', 80, 185, size=20)
    drawImage('torpedo.png', 30, 230, width=100, height=120)
    drawLabel(f'Torpedos owned: {app.torpedoesOwned}', 250, 300, size=20)
    drawLabel('Torpedo price: 100', 250, 330, size=20)
    drawRect(30, 350, 100, 50, fill='orange', opacity=60)
    drawLabel('Buy', 80, 375, size=20)
    drawLabel(f'Coins: {app.coins}', 250, 450, bold=True)
    if app.notEnoughCoins: 
        drawLabel('Not enough coins!', 250, 30, size=24, bold=True)
    drawLabel('Press R to go to regular mode', 200, 480, size=15)
    drawLabel('Press B to go to blitz mode', 200, 500, size=15)

def shop_onMousePress(app, mouseX, mouseY):
    rocketL, rocketT, rocketW, rocketH=30, 160, 100, 50
    if (rocketL<=mouseX<=rocketL+rocketW and
        rocketT<=mouseY<=rocketT+rocketH):
            if app.coins<100: 
                app.notEnoughCoins=True
            else: 
                app.rocketsOwned+=1
                app.coins -= 100
    torpedoL, torpedoT, torpedoW, torpedoH=0, 350, 100, 50
    if (torpedoL<=mouseX<=torpedoL+torpedoW and
        torpedoT<=mouseY<=torpedoT+torpedoH):
        if app.coins<100: 
                app.notEnoughCoins=True
        else: 
            app.torpedoesOwned+=1
            app.coins -= 100

def shop_onKeyPress(app, key): 
    if key == 'r':
        setActiveScreen('regular')
        app.mode='Regular'
    elif key == 'b':
        setActiveScreen('blitz')
        app.mode='Blitz'

runAppWithScreens(initialScreen='start', height=550)
