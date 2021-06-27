#################################################
# Tetris!
#################################################

import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

def tetrisPieces():
    #Seven "standard" pieces (tetrominoes)
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    return [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]

def appStarted(app):
    rows, cols, cellSize, margins = gameDimensions()
    app.rows = rows
    app.cols = cols
    app.cellSize = cellSize
    app.margins = margins
    app.timerDelay = 500

    app.board = []
    for row in range(rows):
        currRow = []
        for col in range(cols):
            currRow.append("blue")
        app.board.append(currRow)
    app.emptyColor = "blue"

    app.tetrisPieces = tetrisPieces()
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
                              "cyan", "green", "orange" ]
    newFallingPiece(app)
    app.isGameOver = False
    app.score = 0

def keyPressed(app, event):
    if event.key == "r":
        app.isGameOver = False
        appStarted(app)
    elif app.isGameOver:
        return
    elif event.key == "Down":
        moveFallingPiece(app, 1, 0)
    elif event.key == "Right":
        moveFallingPiece(app, 0, 1)
    elif event.key == "Left":
        moveFallingPiece(app, 0, -1)
    elif event.key == "Up":
        rotateFallingPiece(app)
    elif event.key == "Space":
        hardDrop(app)

def timerFired(app):
    if not moveFallingPiece(app, 1, 0):
        if app.isGameOver:
            return
        #creates new falling piece after old falling piece is in position
        placeFallingPiece(app)
        newFallingPiece(app)
        if not fallingPieceIsLegal(app):
            app.isGameOver = True

def hardDrop(app):
    while moveFallingPiece(app, 1, 0):
        moveFallingPiece(app, 1, 0)

def placeFallingPiece(app):
    for r in range(len(app.fallingPiece)):
        for c in range(len(app.fallingPiece[0])):
            row = app.fallingPieceRow + r
            col = app.fallingPieceCol + c
            if app.fallingPiece[r][c]:
                app.board[row][col] = app.fallingPieceColor
    removeFullRows(app)   

def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    return True

def rotateFallingPiece(app):
    oldPieceRows = len(app.fallingPiece)
    oldPieceCols = len(app.fallingPiece[0])
    oldRow = app.fallingPieceRow
    oldCol = app.fallingPieceCol
    oldPiece = app.fallingPiece
    rotatePiece = []
    for r in range(oldPieceCols):
        currRow = []
        for c in range(oldPieceRows):
            currRow.append(None)
        rotatePiece.append(currRow)
    for r in range(oldPieceRows):
        for c in range(oldPieceCols):
            newRow = (oldPieceCols-1) - c
            rotatePiece[newRow][r] = oldPiece[r][c]

    app.fallingPiece = rotatePiece

    #updates the new center of the falling piece after the rotation
    oldCenterRow = oldRow + len(oldPiece) //  2
    newCenterRow = app.fallingPieceRow + len(app.fallingPiece) // 2
    newRow = oldRow + len(oldPiece)//2 - len(app.fallingPiece)//2  
    app.fallingPieceRow = newRow 

    oldCenterCol = oldCol + len(oldPiece[0]) //  2
    newCenterCol = app.fallingPieceCol + len(app.fallingPiece[0]) // 2
    newCol = oldCol + len(oldPiece[0])//2 - len(app.fallingPiece[0])//2  
    app.fallingPieceCol = newCol  

    if not fallingPieceIsLegal(app):
        app.fallingPiece = oldPiece
        app.fallingPieceRow = oldRow 
        app.fallingPieceCol = oldCol
        
def fallingPieceIsLegal(app):
    for r in range(len(app.fallingPiece)):
        for c in range(len(app.fallingPiece[0])):
            #only checks pieces in the board that have a color value
            if app.fallingPiece[r][c] == True:
                row = app.fallingPieceRow + r
                col = app.fallingPieceCol + c
                if (not isLegalBounds(app, row, col) or 
                    app.board[row][col] != app.emptyColor):
                    return False
    return True

def isLegalBounds(app, row, col):
    if (( row < 0) or (row >= app.rows) or
        (col < 0) or (col  >= app.cols)):
        return False
    return True

def removeFullRows(app):
    rows = len(app.board)
    cols = len(app.board[0])
    newBoard = []
    for r in range(rows):
        currRow = []
        for c in range(cols):
            currRow.append(app.board[r][c])
        if app.emptyColor not in currRow:
            app.score += 1
        else:
            newBoard.append(currRow)
    #inserts new rows with the empty color at the top of board
    while len(newBoard) < app.rows:
        newBoard.insert(0, [app.emptyColor] * app.cols)
    app.board = newBoard

def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]

    app.fallingPieceRow = 0
    adjustCol = len(app.fallingPiece[0]) // 2
    app.fallingPieceCol = app.cols//2 - adjustCol

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def drawCell(app, canvas, row, col, color):
    x0 = app.margins + col * app.cellSize
    y0 = app.margins + row * app.cellSize
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    canvas.create_rectangle(x0, y0, x1, y1, fill = color)

def drawFallingPiece(app, canvas):
    for r in range(len(app.fallingPiece)):
        for c in range(len(app.fallingPiece[0])):
            row = app.fallingPieceRow + r
            col = app.fallingPieceCol + c
            #checks to make sure there is a cell in the falling piece to draw
            if app.fallingPiece[r][c]:
                drawCell(app, canvas, row, col, app.fallingPieceColor)

def drawGameOver(app, canvas):
    x0 = app.margins 
    y0 = app.height * 0.15
    x1 = app.width - app.margins
    y1 = app.height * 0.35
    canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
    canvas.create_text (app.width/2, app.height * 0.25, text = "GAME OVER!", 
                        font= "Arial 26 bold", fill = "yellow")

def drawScore(app, canvas):
    canvas.create_text(app.width/2, app.margins/2, 
                            text = f'Score = {app.score}', fill = "blue",
                            font = "Arial 15 bold")

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "orange")
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    if app.isGameOver:
        drawGameOver(app, canvas)
    drawScore(app, canvas)

def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    height = rows * cellSize + 2 * margin
    width = cols * cellSize + 2 * margin
    runApp (width = width, height = height)


#################################################
# main
#################################################

def main():
    playTetris()

if __name__ == '__main__':
    main()
