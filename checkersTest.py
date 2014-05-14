#Make Checkers
from Tkinter import *
import string
import copy

def leftMouseMoved(event):
    canvas.data.mousex = event.x
    canvas.data.mousey = event.y
    redrawAll()
    return

def leftMousePressed(event):
    canvas.data.mousePressed = True
    row,col = convert(event.y,event.x)
    if canvas.data.jump == True:
        rowf,colf = canDoubleJump()
        if row != rowf or colf != col:
            print "you must jump!"
            return
    if isLegalMovePressed(row,col):
        canvas.data.row_i,canvas.data.col_i = row,col
        canvas.data.isLegalClick = True
    else:
        canvas.data.mousePressed = False
        print "please click your own piece"
        canvas.data.isLegalClick = False

def leftMouseReleased(event):
    width = canvas.data.width
    height = canvas.data.height
    canvas.data.row_f,canvas.data.col_f = convert(event.y,event.x)
    if event.x > 0 and event.x < width and event.y > 0 and event.y < height:
        if canvas.data.isLegalClick and isLegalReleased():
            move()
            checkKing()
            if canDoubleJump():
                return
            canvas.data.jump = False
            canvas.data.player *= -1
        else:
            print "please drag your piece to a legal position"
    else:
        print "please drag your piece to a legal position on the screen"
    isGameOver()
    canvas.data.mousePressed = False
    redrawAll()
    
def isGameOver():
    player = canvas.data.player
    board = canvas.data.board
    for row in xrange(len(board)):
        for col in xrange(len(board)):
            if board[row][col] == player:
                return False
    print "game over"
    canvas.data.gameOver = True
    return True

def keyPressed(event):
    if event.char == "r":
        init()

def checkKing():
    row = canvas.data.row_f
    col = canvas.data.col_f
    print "last row=",row,"last col=",col
    player = canvas.data.player
    print "player =",player
    board = canvas.data.board
    if player == -1 and row == 0:
        print "hello"
        board[row][col] *= 1.0
    elif player == 1 and row == len(board) -1:
        board[row][col] *= 1.0
    canvas.data.board = board
    redrawAll()

def boardSum():
    board = canvas.data.board
    sum = 0
    for row in xrange(len(board)):
        for col in xrange(len(board)):
            sum += board[row][col]
    return sum

def canDoubleJump():
    board = canvas.data.board
    player = canvas.data.player
    rowf = canvas.data.row_f
    colf = canvas.data.col_f
    if canvas.data.jump == True:
        if isValidJump(rowf,colf,rowf+2,colf+2):
            return rowf,colf
        elif isValidJump(rowf,colf,rowf+2,colf-2):
            return rowf,colf
        elif isValidJump(rowf,colf,rowf-2,colf+2):
            return rowf,colf
        elif isValidJump(rowf,colf,rowf-2,colf-2):
            return rowf,colf
    canvas.data.jump == False

def canJump(): #if jump exists on board
    player = canvas.data.player
    board = canvas.data.board
    for row in xrange(1 - player,len(board) - player - 1): 
        for col in xrange(0,len(board)-2):  #SE,NE sweep
            if (board[row][col] == player and type(board[row][col])==int):
                if isValidJump(row,col,row+player*2,col+2):
                    return True
        for col in xrange(2,len(board)):  #SW,NW sweep
            if (board[row][col] == player and type(board[row][col])==int):
                if isValidJump(row,col,row+player*2,col-2):
                    return True
    player *= -1
    for row in xrange(1 - player,len(board) - player - 1): 
        for col in xrange(0,len(board)-2):  #SE,NE sweep
            if (board[row][col] == -1*player and type(board[row][col])==float):
                if isValidJump(row,col,row+player*2,col+2):
                    return True
        for col in xrange(2,len(board)):  #SW,NW sweep
            if (board[row][col] == -1*player and type(board[row][col])==float):
                if isValidJump(row,col,row+player*2,col-2):
                    return True

def redrawAll():
    drawCheckersBoard()
    drawPieces()
    if canvas.data.mousePressed:
        drawMouseDrag()
    elif not canvas.data.mousePressed:
        drawCheckersBoard()
        drawPieces()

def isLegalMovePressed(row,col):
    board = canvas.data.board
    player = canvas.data.player
    if board[row][col] != player:
        return False
    return True

def move():
    col0,col1 = canvas.data.col_i,canvas.data.col_f
    row0,row1 = canvas.data.row_i,canvas.data.row_f
    board = canvas.data.board
    boardCopy = copy.deepcopy(board)
    board[row0][col0] = 0
    board[row1][col1] = boardCopy[row0][col0]
    canvas.data.board = board
    displayBoard(canvas.data.board)
    redrawAll()

def isValidJump(rowi,coli,rowf,colf):
    board = canvas.data.board
    player = canvas.data.player
    if rowf >= len(board) or colf >= len(board):
        return False
    elif rowf < 0 or colf < 0:
        return False
    if board[(rowi+rowf)/2][(coli+colf)/2] == -1*player and board[rowf][colf]==0:
        return True #returns True if jump can be made

def isLegalReleased():
    player = canvas.data.player
    board = canvas.data.board
    coli,colf = canvas.data.col_i, canvas.data.col_f
    rowi,rowf = canvas.data.row_i, canvas.data.row_f
    if (rowf % 2 == colf % 2) or (board[rowf][colf] !=0): #basic position on dark squares
        print "please click on a dark square"
        return False
    if type(board[rowi][coli]) == float:
        if (abs(rowi - rowf) == 2) and (abs(coli - colf) == 2): #jump conditions, placed before move
            if isValidJump(rowi,coli,rowf,colf):
                board[(rowi+rowf)/2][(coli+colf)/2] = 0
                canvas.data.board = board
                canvas.data.jump = True
                print "what"
                return True#if it can jump, move is made. If it can't, returns False
            return False
        elif (abs(rowi - rowf) != 1) or (abs(coli - colf) != 1): #simple move
            print "please move 1 square away"
            return False
        print "hello2"
    elif type(board[rowi][coli]) == int:
        if (rowf - rowi == 2*player) and (abs(coli - colf) == 2): #row must be increasing
            if isValidJump(rowi,coli,rowf,colf):
                board[(rowi+rowf)/2][(coli+colf)/2] = 0
                canvas.data.board = board
                canvas.data.jump = True
                return True #if it can jump, move is made. If it can't, returns False
            return False
        elif (rowf - rowi != 1*player) or (abs(coli - colf) != 1): #row must be increasing based on player
            return False
    if canJump() and abs(rowi - rowf) != 2:
        print "you must jump!"
        return False
    return True

def convert(x,y): #takes mouseclick input and converts to boardspace
    cellSize = canvas.data.cellSize
    col = x / cellSize
    row = y / cellSize
    return col,row

def startGame():
    while not canvas.data.isEndGame:
        player = canvas.data.currentPlayer 
        move(player)
        canvas.data.currentPlayer *= -1
    return

def drawMouseDrag():
    x = canvas.data.mousex
    y = canvas.data.mousey
    cs = canvas.data.cellSize
    rowi = canvas.data.row_i
    coli = canvas.data.col_i
    board = canvas.data.board
    player = canvas.data.player
    if board[rowi][coli] == 1:
        canvas.create_oval(cs*coli,cs*rowi,cs*(coli+1),cs*(rowi+1),fill="black",width=5,outline="white")
        canvas.create_oval(x-cs/2,y-cs/2,x+cs/2,y+cs/2,fill="black",width=5,outline="white")
    elif board[rowi][coli] == -1:
        canvas.create_oval(cs*coli,cs*rowi,cs*(coli+1),cs*(rowi+1),fill="red",width=5,outline="white")
        canvas.create_oval(x-cs/2,y-cs/2,x+cs/2,y+cs/2,fill="red",width=5,outline="white")
    board[rowi][coli] == 0
    canvas.data.board = board

def drawPieces():
    board = canvas.data.board
    size = canvas.data.size
    cs = canvas.data.cellSize
    for row in xrange(size):
        for col in xrange(size):
            if board[row][col] == 1:
                canvas.create_oval(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="black")
            elif board[row][col] == -1:
                canvas.create_oval(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="red")
            if type(board[row][col]) == float:
                canvas.create_oval(cs*col+cs/3,cs*row+cs/3,cs*(col+1)-cs/3,cs*(row+1)-cs/3,fill="white")

def drawCheckersBoard():
    cs = canvas.data.cellSize
    size = canvas.data.size
    for i in xrange(size/2):
        for j in xrange(size):
            if j % 2 == 0:
                canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="khaki2")
                canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="saddlebrown")
            elif j % 2 == 1:
                canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="saddlebrown")
                canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="khaki2")

def addPieces():
    size = canvas.data.size
    board = canvas.data.board
    for row in xrange(size): #This prints all the pieces on the board
        if row % 2 == 0 and row < 3:
            for col in xrange(1,size,2):
                board[row][col] = 1
        elif row % 2 != 0 and row < 3: #col < 3 for 1s
            for col in xrange(0,size,2):
                board[row][col] = 1
        elif row % 2 == 0 and row > 4:
            for col in xrange(1,size,2):
                board[row][col] = -1
        elif row % 2 != 0 and row > 4: #col >4 for 2s
            for col in xrange(0,size,2):
                board[row][col] = -1
    canvas.data.board = board

def loadCheckersBoard():
    size = canvas.data.size
    board = [0]*size
    for i in xrange(size):
        board[i] = [0]*size
    canvas.data.board = board
    addPieces()
    
def displayBoard(board):
    for i in xrange(len(board)):
        print board[i]

def init():
    loadCheckersBoard()
   # displayBoard()
    canvas.data.isEndGame = False
    canvas.data.currentPlayer = 1
    canvas.data.getMoveStart = True
    canvas.data.getMoveEnd = False
    canvas.data.player = 1
    canvas.data.jump = False
    canvas.data.gameOver = False
    canvas.data.mousePressed = False
    redrawAll()

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    size = 8
    width = 600
    height = 600
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.cellSize = width/8
    canvas.data.size = 8
    canvas.data.width = width
    canvas.data.height = height
    canvas.data.board = [[]]
    init()
    # set up events
    canvas.bind("<B1-Motion>", leftMouseMoved)
    root.bind("<Button-1>", leftMousePressed)
    root.bind("<B1-ButtonRelease>", leftMouseReleased)
    root.bind("<Key>", keyPressed)
    #timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()