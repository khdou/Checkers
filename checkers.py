#Make Checkers
from Tkinter import *
import string
import copy

def leftMouseMoved(event):
    return

def leftMousePressed(event):
    if canvas.data.getMoveStart:
        canvas.data.getMoveStart = False
        canvas.data.x = event.x
        canvas.data.y = event.y
        moveStart(canvas.data.player)

def leftMouseReleased(event):
    if canvas.data.getMoveEnd:
        canvas.data.getMoveEnd = False
        canvas.data.x = event.x
        canvas.data.y = event.y
        moveEnd(canvas.data.player,canvas.data.x,canvas.data.y)

def keyPressed(event):
    if event.char == "r":
        init()

def redrawAll():
    drawCheckersBoard()
    drawPieces()
    displayBoard()

def isLegalEndMove(player,x0,y0,x1,y1):
    board = canvas.data.board
    row,col = convert(x1,y1)
    if (row % 2 == col %2) or (board[row][col] != 0):
        return False
    return True

def moveEnd(player,x0,y0):
    if canvas.data.getMoveEnd == True:
        cx = canvas.data.width/2
        cy = canvas.data.height/2
        canvas.create_text(cx,cy,text="Please click on your destination",font=("Helvetica",20),fill="white")
        return
    elif canvas.data.getMoveEnd == False:
        redrawAll()
        x1 = canvas.data.x
        y1 = canvas.data.y
        if not isLegalEndMove(player,x0,y0,x1,y1):
            print "illegal, back to moveStart player=",player
            canvas.data.moveStart = True
            moveStart(player)
        else:
            print "legal, back to moveStart player=",canvas.data.player
            canvas.data.moveStart = True
            board = canvas.data.board
            oldRow,oldCol = convert(x0,y0)
            print "oldRow",oldRow,"oldCol",oldCol
            newRow,newCol = convert(x1,y1)
            board[oldRow][oldCol] = 0
            print "hi"
            board[newRow][newCol] = player
            canvas.data.board = board
            canvas.data.player *= -1
            redrawAll()
            moveStart(player)

def convert(x,y): #takes mouseclick input and converts to boardspace
    cellSize = canvas.data.cellSize
    col = x / cellSize
    row = y / cellSize
    return row,col

def isLegalStartMove(player,x,y):
    board = canvas.data.board
    row,col = convert(x,y)
    if board[row][col] == player:
        return True

def moveStart(player):
    if canvas.data.getMoveStart == True:
        cx = canvas.data.width/2
        cy = canvas.data.height/2
        canvas.create_text(cx,cy,text="Please click on your starting piece",font=("Helvetica",20),fill="white")
        return
    elif canvas.data.getMoveStart == False:
        redrawAll()
        x0 = canvas.data.x
        y0 = canvas.data.y
        if not isLegalStartMove(player,x0,y0):
            canvas.data.getMoveStart == True
            print "not legal"
        else:
            print "legal to moveEnd"
            canvas.data.getMoveEnd = True

def startGame():
    while not canvas.data.isEndGame:
        player = canvas.data.currentPlayer 
        move(player)
        canvas.data.currentPlayer *= -1
    return

def drawPieces():
    board = canvas.data.board
    size = canvas.data.size
    cs = canvas.data.cellSize
    for row in xrange(size):
        for col in xrange(size):
            if board[row][col] == 1:
                canvas.create_oval(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="black")
            elif board[row][col] == 2:
                canvas.create_oval(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="black")
                canvas.create_oval(cs*col+cs/3,cs*row+cs/3,cs*(col+1)-cs/3,cs*(row+1)-cs/3,fill="white")
            elif board[row][col] == -1:
                canvas.create_oval(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="red")
            elif board[row][col] == -2:
                canvas.create_oval(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="red")
                canvas.create_oval(cs*col+cs/3,cs*row+cs/3,cs*(col+1)-cs/3,cs*(row+1)-cs/3,fill="white")

def drawCheckersBoard():
    cs = canvas.data.cellSize
    size = canvas.data.size
    for i in xrange(size/2):
        for j in xrange(size):
            if j % 2 == 0:
                canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="khaki2")
                canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="saddlebrown")
            elif j % 2 ==1:
                canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="saddlebrown")
                canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="khaki2")
            
def isLegalEndingMove(start,end):
    if len(end) != 2: #checks starting conditions
        return False
    elif (not end[0].isalpha()) or (not end[1].isdigit()): #checks format
        return False
    size = canvas.data.size
    board = canvas.data.board
    row = 8 - int(end[1]) #converts input into row
    col = (ord(end[0]) - ord("a")) % 32 #accounts for capitals
    print "row=",row,"col=",col,
    if (size <= row or row < 0) or (size <= col or col < 0) or \
        (row % 2 == col % 2) or board[row][col] != 0: #if coordinate is empty or off board\
        return False
    return True

def isLegalStartingMove(start):
    if len(start) != 2: #checks starting conditions
        return False
    elif (not start[0].isalpha()) or (not start[1].isdigit()):
        return False
    size = canvas.data.size
    board = canvas.data.board
    row = 8 - int(start[1]) #converts input into row
    col = (ord(start[0]) - ord("a")) % 32 #accounts for capitals
    if (size <= row or row < 0) or (size <= col or col < 0) or \
        board[row][col] == 0: #if coordinate is empty or off board
        return False
    return True

def getMove():
    start = raw_input("Enter your starting position: ")
    while not isLegalStartingMove(start):
        print "Please enter a 2 digit coordinate in the form of letter,number"
        start = raw_input("Enter your starting position: ")
    end = raw_input("Enter your ending position:")
    while not isLegalEndingMove(start,end):
        print "Please enter a 2 digit coordinate in the form of letter,number"
        end = raw_input("Enter your ending position:")
        
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
    """canvas.data.board =\
    [[ 0, 1, 0, 1, 0, 1, 0, 1],
    [ 1,  0, 2, 0, 1, 0, 1, 0],
    [ 0,  1, 0, 2, 0, 2, 0, 1],
    [ 0,  0, 0, 0, 0, 0, 0, 0],
    [ 0,  0, 0, 0, 0, 0, 0, 0],
    [-1,  0, -1, 0, -2, 0, -1, 0],
    [ 0, -1, 0, -1, 0, -1, 0, -1],
    [-1,  0, -1, 0, -1, 0, -2, 0]]"""
    
def displayBoard():
    board = canvas.data.board
    for i in xrange(len(board)):
        print board[i]

def init():
    loadCheckersBoard()
   # displayBoard()
    redrawAll()
    canvas.data.isEndGame = False
    canvas.data.currentPlayer = 1
    canvas.data.getMoveStart = True
    canvas.data.getMoveEnd = False
    canvas.data.player = 1
    moveStart(canvas.data.player)
  #  startGame()

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