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
    app.piecex
    app.piecey
    app.pieceWidth
    app.pieceHeight

def redrawAll(app):
    drawLabel('2048', 200, 30, size=16)
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel(f'getPieceValue(app)', app.piecex, app.piecey)
    drawRect(app.piecex, app.piecey, app.pieceWidth, app.pieceHeight, fill='color', opacity=20)


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
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

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
    if key=='up': 
        piece.cy+=app.pieceWidth
        val=getPieceValue
    if key=='down': 
        piece.cy+=app.pieceWidth
    if key=='left': 
        piece.cx+=app.pieceHeight
    if key=='right': 
        piece.cx+=app.pieceHeight


runApp()
