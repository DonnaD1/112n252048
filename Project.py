from cmu_graphics import *
import random

############################################################
# Start Screen
############################################################
def start_redrawAll(app): 
    drawLabel('Welcome!', 200, 160, size=24, bold=True)
    drawLabel(f'Highest Number of Moves: {app.maxMoveNum}', 200, 200, size=24)
    drawLabel('Press R for Regular Mode', 200, 220, size=18)
    drawLabel('Press B for Blitz Mode', 200, 240, size=18)
    drawLabel('Press S for Shop', 200, 280, size=18)

def start_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('game')
    elif key == 'b':
        setActiveScreen('blitz')
    elif key == 's':
        setActiveScreen('shop')

############################################################
# Game Screen
############################################################
def game_onScreenActivate(app):
    app.moves = 0

def game_redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel(f'Mode: {app.mode}', 200, 20, size=18)
    drawLabel(f'Moves: {app.moves}', 200, 40, size=16)
    drawLabel(f'Highest Steps: {app.highScore}', 200, 60, size=16)
    if app.gameOver:
        drawLabel('Game Over! Press space to restart', 200, 200, size=20)
    if app.gameOver: 
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawLabel('Game Over', 200, 200, size=70, bold=True, fill='red')
        drawLabel('Press space to restart', 200, 240, size=30, fill='red', bold=True)

def game_onKeyPress(app, key):
    if key == 'r':
        app.maxMoveNum = max(app.maxMoveNum, app.moves)
        setActiveScreen('start')
    if key=='left':
        movePiecesLeft(app)
        loadPiece(app)
    elif key=='right':
        movePiecesRight(app)
        loadPiece(app)
    elif key=='up': 
        movePiecesUp(app)
        loadPiece(app)
    elif key=='down':
        movePiecesDown(app)
        loadPiece(app)
    checkGameOver(app)

def onAppStart(app): 
    app.rows=4
    app.cols=4
    app.boardLeft = 75
    app.boardTop = 50
    app.boardWidth = 250
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.gameOver=False
    app.maxMoveNum=0
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

# def onKeyPress(app, key): 
    # if app.gameOver:
    #      if key=='space':
    #          onAppStart(app)
    #          return 
    
#     elif key=='space': 
#         app.paused=True

def pieceCollisionLR(row): #piece collision function if left and right keys are pressed
    valsInRow=[]
    for val in row: 
        if val is not None: 
            valsInRow.append(val)
    i=0
    while i<(len(valsInRow)-1): 
        if valsInRow[i]==valsInRow[i+1]:
            valsInRow[i]=valsInRow[i]+valsInRow[i]
            valsInRow[i+1]='Skip'
            i+=2
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
        newRow=pieceCollisionLR(row) 
        app.board[rowNum]=newRow

def movePiecesRight(app): 
    for rowNum in range(app.rows):
        row=app.board[rowNum] 
        row.reverse()
        newRow=pieceCollisionLR(row) 
        newRow.reverse()
        app.board[rowNum]=newRow

def pieceCollisionUD(col): 
    valsInCol=[]
    for val in col:
        if val is not None: 
            valsInCol.append(val)
    i=0
    while i<(len(valsInCol)-1): 
        if valsInCol[i]==valsInCol[i+1]:
            valsInCol[i]=valsInCol[i]+valsInCol[i]
            valsInCol[i+1]='Skip'
            i+=2
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
        newCol=pieceCollisionUD(col)
        for row in range(app.rows): 
            app.board[row][colNum]=newCol[row]

def movePiecesDown(app): 
    for colNum in range(app.cols): 
        col=[]
        for row in range(app.rows):
            col.append(app.board[row][colNum])
        col.reverse()
        newCol=pieceCollisionUD(col)
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


runAppWithScreens(initialScreen='start')
