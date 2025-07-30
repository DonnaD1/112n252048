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
        tileVal=random.choices(valList, weights=(80, 20), k=1)[0]  
        app.board[i][j]=tileVal
  
def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel('2048', 200, 30, size=16)

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
             fill=color, border='black',
             borderWidth=app.cellBorderWidth, 
             opacity=opacity)
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

def onKeyPress(app, key): 
    # if app.gameOver:
    #      if key=='space':
    #          onAppStart(app)
    #          return 
    if key=='left':
        movePiecesLeft(app)
        loadPiece(app)
    elif key=='right':
        movePiecesRight(app)
        loadPiece(app)
#     elif key=='down':
#         movePiece(app, +1, 0)
#     elif key=='up': 
#         movePiece(app, -1, 0)
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


runApp()
