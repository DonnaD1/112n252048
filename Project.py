from cmu_graphics import *
import random

def onAppStart(app): 
    app.rows=4
    app.cols=4
    app.boardLeft = 75
    app.boardTop = 50
    app.boardWidth = 250
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTileColor(app)
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
        tileVal=random.choices(valList, weights=(80, 20), k=1)  
        app.board[i][j]=tileVal



    # app.piecex
    # app.piecey
    # app.pieceWidth
    # app.pieceHeight
    # app.gameOver=False
    # app.level='welcome'
    # app.board=[([None]*app.cols) for row in range(app.rows)]
    # app.pieces=0
    # app.paused=False

# def onStepApp(app): 
#     if app.paused: 
#         return 
#     takeStep(app)

# def takeStep(app):
#     if gameOver(app): 
#         return 
    

def redrawAll(app):
    # drawLabel(f'getGridSize(app) x getGridSize(app) 2048', 200, 30, size=16)\
    # if getGridSize(app)<2: 
    #     drawLabel('Please enter a grid size larger than 1x1!')
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel('2048', 200, 30, size=16)
    # drawLabel(f'getPieceValue(app)', app.piecex, app.piecey)
    # drawRect(app.piecex, app.piecey, app.pieceWidth, app.pieceHeight, fill='color', opacity=20)
    # if app.gameOver==True: 
    #     drawRect(0, 0, app.width, app.height, fill='white', opacity=20)
    #     drawLabel('Game Over', 200, 200, size=70, bold=True, fill='red')
    #     drawLabel('Press space to restart', 200, 240, size=30, fill='red', bold=True)
    # if app.level=='welcome': 
    #     drawLabel('Welcome to 2048!')
    #     drawRect('')
    #     drawLabel('Start')


# def loadNextPiece(app): 


def drawBoard(app):
    for row in range(app. rows):
        for col in range(app.cols):
            color=app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)
#app.width/2, app.height/2, app.width-200, app.height-200
def drawCell(app, row, col, value):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if value==None: 
        color='lightGray'
        opacity=100
        value=''
    else: 
        value=value[0]
        color=app.valueColor[value][0]
        opacity=app.valueColor[value][1]
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth, 
             opacity=opacity)
    if value!='': 
        drawLabel((str(value)), ((cellLeft+cellWidth)/2), ((cellTop+cellHeight)/2), size=16, bold=True)
    

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getPieceValue(app): 
    pieceValue=2
    if pieceCollision(app): 
        pieceValue*=2
    if pieceValue==2: 
        color='beige'
    if pieceValue==4: 
        color='yellow'
    if pieceValue==8: 
        color='orange'
    if pieceValue==16:
        color='red'
    return pieceValue

def pieceCollision(app): 
    pass

def onKeyPress(app, key): 
    if app.gameOver:
        if key=='space':
            onAppStart(app)
            return 
    if key=='left':
        movePiece(app, 0, -1)
    elif key=='right':
        movePiece(app, 0, +1)
    elif key=='down':
        movePiece(app, +1, 0)
    elif key=='up': 
        movePiece(app, -1, 0)
    elif key=='space': 
        app.paused=True

def movePiece(app, drow, dcol): 
    app.pieceTopRow+=drow
    app.pieceLeftCol+=dcol
    if pieceIsLegal(app):
        return True
    else:
        app.pieceTopRow-=drow
        app.pieceLeftCol-=dcol
        return False

def pieceIsLegal(app): 
    pieceRows, pieceCols=len(app.piece), len(app.piece[0])
    for pieceRows in range(pieceRows):
        for pieceCol in range(pieceCols):
            if app.piece[pieceRows][pieceCol]:
                boardRow=pieceRows+app.pieceTopRow
                boardCol=pieceCol+app.pieceLeftCol
                if ((boardRow<0) or (boardRow>=app.rows) or 
                     (boardCol<0) or (boardCol>=app.cols)):
                         return False
                if app.board[boardRow][boardCol]!=None:
                    return False
    return True
def gridSize(app):
    size=input('Enter the size of the grid: ')
    if size>=2: 
        app.rows=size
        app.cols=size
    return ('Grid size=' size)  

runApp()
