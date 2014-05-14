#Make Checkers
#Minimax code was adapted using the Fall 15-112 Optional Lecture Notes on AI at kosbie.net
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import string
import copy
import random

def button1Pressed():
    canvas.data.splash = True
    drawAIButtons()
    
def button2Pressed():
    canvas.data.splash = False
    canvas.data.twoPlayer = True
    canvas.data.onePlayer = False
    redrawAll()

def button3Pressed():
    canvas.data.splash = False
    canvas.data.onePlayer = True
    canvas.data.twoPlayer = False
    canvas.data.AILevel = 1
    redrawAll()

def button4Pressed():
    canvas.data.splash = False
    canvas.data.onePlayer = True
    canvas.data.twoPlayer = False
    canvas.data.AILevel = 3
    redrawAll()
    
def button5Pressed():
    canvas.data.splash = False
    canvas.data.onePlayer = True
    canvas.data.twoPlayer = False
    canvas.data.AILevel = 5
    redrawAll()

def leftMouseMoved(event):
    if not canvas.data.splash:
        canvas.data.mousex = event.x
        canvas.data.mousey = event.y
        redrawAll()

def leftMousePressed(event):
    print canvas.data.AILevel
    if not canvas.data.splash and not canvas.data.gameOver:
        canvas.data.mousePressed = True
        rowi,coli = convert(event.y,event.x) #converts click to board position
        if canvas.data.doubleJump == True: #if jump condition is true:
            try:
                rowf,colf = checkDoubleJump(canvas.data.row_f,canvas.data.col_f) #piece must be doublejump piece
            except:
                return
            if rowi != rowf or colf != coli:
                redrawAll()
                return
        if isLegalMovePressed(rowi,coli): #checks if piece is the player
            canvas.data.row_i,canvas.data.col_i = rowi,coli
            canvas.data.isLegalClick = True
            checkJumps()
        else:
            canvas.data.mousePressed = False
            player = canvas.data.player
            if player > 0:
                player = "Black"
            elif player < 0:
                player = "Red"
            tkMessageBox.showwarning("Error", "Please click your own piece. \n You are: %s" % (player))   
            canvas.data.isLegalClick = False

def leftMouseReleased(event):
    canvas.data.mousePressed = False
    if not canvas.data.splash and not canvas.data.gameOver:
        width = 600
        height = 600
        canvas.data.row_f,canvas.data.col_f = convert(event.y,event.x)
        try: #if first click passed
            rowi,rowf = canvas.data.row_i,canvas.data.row_f
            coli,colf = canvas.data.col_i,canvas.data.col_f
        except:
            return
        if event.x > 0 and event.x < width and event.y > 0 and event.y < height: #checks if click is within bounds
            if canvas.data.isLegalClick and isLegalMove(rowi,coli,rowf,colf):#checks if start and end is legal
                move(rowi,coli,rowf,colf)
                canvas.update()
                if canvas.data.doubleJump == False:
                    canvas.data.player *= -1
                    isGameOver()
                    if not canvas.data.gameOver:
                        canvas.data.AI = True
                        redrawAll()
                        canvas.update()
                        if canvas.data.onePlayer and not canvas.data.gameOver:
                            moveAI()
                            while canvas.data.doubleJump == True:
                                checkJumps()
                                moveAI()
                            canvas.data.player *= -1
                            isGameOver()
                            canvas.data.AI = False
            else:
                if canvas.data.jump:
                    redrawAll()
                    tkMessageBox.showwarning("Error", "You must jump!")
        else:
            redrawAll()
            tkMessageBox.showwarning("Error", "Please stay on the board!")
        canvas.data.mousePressed = False
    redrawAll()

def keyPressed(event):
    if event.char == "r":
        init()
    elif event.char == "m":
        canvas.data.splash = True
        canvas.data.onePlayer = False
        canvas.data.twoPlayer = False
        init()

################################################################################
###                 AI Specific Functions Start Here:                        ###
################################################################################

def moveAI():
    checkJumps()
    board = canvas.data.board
    player = canvas.data.player
    jump = canvas.data.jump
    doubleJump = canvas.data.doubleJump
    level = canvas.data.AILevel
    print level
    if canvas.data.doubleJump:
        jumpRow,jumpCol = checkDoubleJump(canvas.data.row_f,canvas.data.col_f)
    else:
        jumpRow = None
        jumpCol = None
    bestMove,bestScore = minimax(board,player,jump,doubleJump,jumpRow,jumpCol,level)
    coords = list(bestMove)
    try:
        move(coords[0],coords[1],coords[2],coords[3]) #changes values
        canvas.data.row_f = coords[2]
        canvas.data.col_f = coords[3]
    except:
        pass

def minimax(board, player, jump, doubleJump, jumpRow, jumpCol, maxDepth, depth=0):
    # destructive version (modified board directly to create children)
    #print "   "*depth, "minimax player=%d" % player
    if (depth == maxDepth) or len(listMoves(board,player,jump,doubleJump,jumpRow,jumpCol))==0:
        result = (None, heuristicValue(board, player,jump,doubleJump,jumpRow,jumpCol)) #We returning the value and the move that got us to that point
    else:
        AIPlayer = 1
        if player == AIPlayer:
            bestScore = -1000
        else:
            bestScore = 1000
        #If you doing a max, you want to start at the min
    #If you doing a min, it viceversa
        bestMove = None
        for move in listMoves(board,player,jump,doubleJump,jumpRow,jumpCol):
      #      print "   "*depth, "move=%s" % (str(move))
            rowi,coli,rowf,colf = move
            newBoard, newPlayer,newJump,newDoubleJump,newJumpRow,newJumpCol = doMoveAI(board,player,jump,doubleJump,jumpRow,jumpCol,rowi,coli,rowf,colf)
     #       print player,jump,doubleJump
        #    (childMove, score) = minimax(newBoard, newPlayer, newJump,newDoubleJump,newJumpRow,newJumpCol,maxDepth, depth+1) #Recursively call minimax to get the values of all children
            #print "   "*depth, "score=%d" % score
            (childMove, score) = minimax(newBoard, newPlayer, newJump,newDoubleJump,newJumpRow,newJumpCol,maxDepth, depth+1) #Recursively call minimax to get the values of all children
            if (((score > bestScore) and player == AIPlayer) or #If at an even level, take a max
                ((score < bestScore) and (player != AIPlayer)) or #If at an odd level, take a min
                ((score == bestScore) and (random.random()<0.5))): #Otherwise decide randomly!
                bestScore = score
                bestMove = move
        result = (bestMove, bestScore)
    #print "   "*depth, "--> %s" % (str(result))
    return result

def heuristicValue(board,player,jump,doubleJump,jumpRow,jumpCol):
    sum = 0
    sum += boardSum(board) * 20
    for row in xrange(len(board)):
        for col in xrange(len(board)):
            if board[row][col] == 1:
                if type(board[row][col]) == float:
                    sum += 18
                elif type(board[row][col]) == int:
                    sum += row
                    if col == 0 or col == 7:
                        sum += 4
                    if row == 0:
                        sum += 8
            elif board[row][col] == -1:
                sum -= row
                if type(board[row][col]) == float:
                    sum -= 10
                elif type(board[row][col]) == int:
                    sum += row
                    if col == 0 or col == 7:
                        sum -= 4
                    if row == 7:
                        sum += 8
    return sum

###########################

def listMoves(board,player,jump,doubleJump,jumpRow,jumpCol):
    moves = []
    for rowi in xrange(0,len(board)):
        for coli in xrange(0,len(board)):
            for rowf in xrange(rowi-2,rowi+3):
                for colf in xrange(coli-2,coli+3):
                    if isLegalMoveAI(board,player,jump,doubleJump,jumpRow,jumpCol,\
                                   rowi,coli,rowf,colf):
                        moves += [(rowi,coli,rowf,colf)]
    return moves

def isValidJumpAI(board,player,rowi,coli,rowf,colf): #checks if initial and final are valid jump
    if rowf >= len(board) or colf >= len(board):
        return False
    elif rowf < 0 or colf < 0:
        return False
    if abs(colf-coli) != 2:
        return False
    if type(board[rowi][coli]) == int:
        if rowf - rowi != 2*player:
            return False
    if board[(rowi+rowf)/2][(coli+colf)/2] == -1*player and board[rowf][colf]==0:
        return True #returns True if jump can be made

def isLegalMoveAI(board,player,jump,doubleJump,jumpRow,jumpCol,rowi,coli,rowf,colf):
    if board[rowi][coli] != player:
        return False
    if not isOnBoardAI(rowi) or not isOnBoardAI(rowf) or not isOnBoardAI(coli) or not isOnBoardAI(colf):
        return False
    if (rowf % 2 == colf % 2) or (board[rowf][colf] != 0): #basic position on dark squares
        #print "please click on a dark square"
        return False
    if doubleJump:
        if (rowi,coli) != (jumpRow,jumpCol):  
            return False
    if not jump: #no jump on the board
        if type(board[rowi][coli]) == float:
            if abs(rowi-rowf) != 1 or abs(coli-colf) != 1:
                #print "please move 1 square away"
                return False
            return True
        elif type(board[rowi][coli]) == int: #checks going in the right direction
            if rowf - rowi != 1*player or abs(coli-colf) != 1:
                #print "please move 1 square away"
                return False
            return True
    elif jump: #jump exists on board
        if type(board[rowi][coli]) == float:
            if abs(rowi-rowf) != 2 or abs(coli-colf) != 2: #not jump move
                #print "you must jump"
                return False
            elif not isValidJumpAI(board,player,rowi,coli,rowf,colf): #not valid jump
                return False
        elif type(board[rowi][coli]) == int:
            if rowf-rowi != 2*player or abs(coli-colf) !=2:
                #print "you must jump"
                return False
            elif not isValidJumpAI(board,player,rowi,coli,rowf,colf):
                return False
    return True

def checkKingedAI(board,player,jump,doubleJump,rowf,colf,): #checks if piece gets kinged
    if player == -1 and rowf == 0 and type(board[rowf][colf]) == int:
        board[rowf][colf] *= 1.0
    elif player == 1 and rowf == len(board) -1 and type(board[rowf][colf]) == int:
        board[rowf][colf] *= 1.0
    return board

def checkDoubleJumpAI(board,player,rowf,colf): #checks if piece can jump again
    if isValidJumpAI(board,player,rowf,colf,rowf+2,colf+2): #don't need to make AI version
        return rowf,colf
    elif isValidJumpAI(board,player,rowf,colf,rowf+2,colf-2):
        return rowf,colf
    elif isValidJumpAI(board,player,rowf,colf,rowf-2,colf+2):
        return rowf,colf
    elif isValidJumpAI(board,player,rowf,colf,rowf-2,colf-2):
        return rowf,colf
    return False

def isValidJumpAI(board,player,rowi,coli,rowf,colf): #checks if initial and final are valid jump
    if rowf >= len(board) or colf >= len(board):
        return False
    elif rowf < 0 or colf < 0:
        return False
    if abs(colf-coli) != 2:
        return False
    if type(board[rowi][coli]) == int:
        if rowf - rowi != 2*player:
            return False
    if board[(rowi+rowf)/2][(coli+colf)/2] == -1*player and board[rowf][colf]==0:
        return True #returns True if jump can be made

def checkJumpsAI(board,player): #if jump exists on board
    for row in xrange(1 - player,len(board) - player - 1): 
        for col in xrange(0,len(board)-2):  #SE,NE sweep
            if board[row][col] == player:
                if isValidJumpAI(board,player,row,col,row+player*2,col+2):
                    return True
        for col in xrange(2,len(board)):  #SW,NW sweep
            if board[row][col] == player:
                if isValidJumpAI(board,player,row,col,row+player*2,col-2):
                    return True
    player *= -1
    for row in xrange(1 - player,len(board) - player - 1): 
        for col in xrange(0,len(board)-2):  #SE,NE sweep
            if (board[row][col] == -1*player and type(board[row][col])==float):
                if isValidJumpAI(board,player,row,col,row+player*2,col+2):
                    return True
        for col in xrange(2,len(board)):  #SW,NW sweep
            if (board[row][col] == -1*player and type(board[row][col])==float):
                if isValidJumpAI(board,player,row,col,row+player*2,col-2):
                    return True

def doMoveAI(board,player,jump,doubleJump,jumpRow,jumpCol,rowi,coli,rowf,colf): #AI version of move() without redraw
    boardCopy = copy.deepcopy(board)
    boardCopy[rowi][coli] = 0
    boardCopy[rowf][colf] = board[rowi][coli]
    boardCopy = checkKingedAI(boardCopy,player,jump,doubleJump,rowf,colf)
    if abs(rowf-rowi) == 2 and abs(colf-coli) == 2: #if it was a jump
        boardCopy[(rowi+rowf)/2][(coli+colf)/2] = 0
        if checkDoubleJumpAI(boardCopy,player,rowf,colf):
            jump = True
            doubleJump = True
            jumpRow,jumpCol = checkDoubleJumpAI(boardCopy,player,rowf,colf)
            player *= -1 #if player can double jump, change so it'll be changed back
        else:
            doubleJump = False
            jump = False
            jumpRow,jumpCol = None,None
    player *= -1 #changed to new player
    if checkJumpsAI(boardCopy,player):
        jump = True
    return boardCopy,player,jump,doubleJump,jumpRow,jumpCol #do the move and return the next boardstate

def isOnBoardAI(n): #if index is in board
    if n < 0 or n >= 8:
        return False
    return True

################################################################################
###              Player-Controlled Checkers Functions Start Here:            ###
################################################################################

def timerFired():
    if canvas.data.splash:
        deltaDraw()
        delay = 20
        canvas.after(delay, timerFired)
    else:
        return    
    # pause, then call timerFired again

def isGameOver():
    checkJumps()
    player = canvas.data.player
    board = canvas.data.board
    jump = canvas.data.jump
    doubleJump = canvas.data.doubleJump
    jumpRow = canvas.data.row_f
    jumpCol = canvas.data.col_f
    if len(listMoves(board,player,jump,doubleJump,jumpRow,jumpCol)) == 0:
        if player == 1:
            color = "Red"
        elif player == -1:
            color = "Black"
        tkMessageBox.showinfo("Game Over","Game Over! \n %s Wins!" % (color))
        canvas.data.gameOver = True
        print "gameOver"
    else:
        print listMoves(board,player,jump,doubleJump,jumpRow,jumpCol)

def checkKinged(row,col): #checks if piece gets kinged
    player = canvas.data.player
    board = canvas.data.board
    if player == -1 and row == 0 and type(board[row][col]) == int:
        board[row][col] *= 1.0
        canvas.data.board = board
        redrawAll()
        return
    elif player == 1 and row == len(board) -1 and type(board[row][col]) == int:
        board[row][col] *= 1.0
        canvas.data.board = board
        redrawAll()
        return

def boardSum(board):
    sum = 0
    for row in xrange(len(board)):
        for col in xrange(len(board)):
            sum += board[row][col]
    return sum

def checkDoubleJump(rowf,colf): #checks if piece can jump again
    board = canvas.data.board
    player = canvas.data.player
    if isValidJump(rowf,colf,rowf+2,colf+2):
        canvas.data.doubleJump = True
        return rowf,colf
    elif isValidJump(rowf,colf,rowf+2,colf-2):
        canvas.data.doubleJump = True
        return rowf,colf
    elif isValidJump(rowf,colf,rowf-2,colf+2):
        canvas.data.doubleJump = True
        return rowf,colf
    elif isValidJump(rowf,colf,rowf-2,colf-2):
        canvas.data.doubleJump = True
        return rowf,colf
    return False

def checkJumps(): #if jump exists on board
    player = canvas.data.player
    board = canvas.data.board
    for row in xrange(1 - player,len(board) - player - 1): 
        for col in xrange(0,len(board)-2):  #SE,NE sweep
            if board[row][col] == player:
                if isValidJump(row,col,row+player*2,col+2):
                    canvas.data.jump = True
        for col in xrange(2,len(board)):  #SW,NW sweep
            if board[row][col] == player:
                if isValidJump(row,col,row+player*2,col-2):
                    canvas.data.jump = True
    player *= -1
    for row in xrange(1 - player,len(board) - player - 1): 
        for col in xrange(0,len(board)-2):  #SE,NE sweep
            if (board[row][col] == -1*player and type(board[row][col])==float):
                if isValidJump(row,col,row+player*2,col+2):
                    canvas.data.jump = True
        for col in xrange(2,len(board)):  #SW,NW sweep
            if (board[row][col] == -1*player and type(board[row][col])==float):
                if isValidJump(row,col,row+player*2,col-2):
                    canvas.data.jump = True

def redrawAll():
    if canvas.data.splash:
        #canvas.delete()
        #canvas.delete(ALL)
        #loadSplashScreen()
        drawBackground()
        drawOval()
        return
    else:
        canvas.delete(ALL)
        drawCheckersBoard()
        drawPieces()
        board = canvas.data.board
        player = canvas.data.player
        jump = canvas.data.jump
        doubleJump = canvas.data.doubleJump
        if canvas.data.mousePressed:
            drawMouseHover()
            drawMouseDrag()
        drawSideBox()

def isLegalMovePressed(row,col): #returns if piece is the player
    board = canvas.data.board
    player = canvas.data.player
    try:
        if board[row][col] != player:
            return False
        return True
    except:
        return False

def move(rowi,coli,rowf,colf): #moves piece from initial position to end
    board = canvas.data.board
    boardCopy = copy.deepcopy(board)
    board[rowi][coli] = 0
    board[rowf][colf] = boardCopy[rowi][coli]
    checkKinged(rowf,colf)
    if abs(rowf-rowi) == 2 and abs(colf-coli) == 2: #if it was a jump
        board[(rowi+rowf)/2][(coli+colf)/2] = 0
        canvas.data.board = board
        if checkDoubleJump(rowf,colf):
            canvas.data.jump = True
            canvas.data.doubleJump = True
        else:
            canvas.data.doubleJump = False
            canvas.data.jump = False
    canvas.data.board = board
    #displayBoard(canvas.data.board)
    redrawAll()

def isValidJump(rowi,coli,rowf,colf): #checks if initial and final are valid jump
    board = canvas.data.board
    player = canvas.data.player
    if rowf >= len(board) or colf >= len(board):
        return False
    elif rowf < 0 or colf < 0:
        return False
    if abs(colf-coli) != 2:
        return False
    if type(board[rowi][coli]) == int:
        if rowf - rowi != 2*player:
            return False
    if board[(rowi+rowf)/2][(coli+colf)/2] == -1*player and board[rowf][colf]==0:
        return True #returns True if jump can be made

def isOnBoard(n): #if index is in board
    board = canvas.data.board
    if n < 0 or n >= len(board):
        return False
    return True

def isLegalMove(rowi,coli,rowf,colf):
    player = canvas.data.player
    board = canvas.data.board
    if board[rowi][coli] != player:
        return False
    if not isOnBoard(rowi) or not isOnBoard(rowf) or not isOnBoard(coli) or not isOnBoard(colf):
        return False
    if (rowf % 2 == colf % 2) or (board[rowf][colf] != 0): #basic position on dark squares
        #print "please click on a dark square"
        return False
    if canvas.data.doubleJump:
        if isValidJump(rowi,coli,rowf,colf):
            return True
        return False
    if not canvas.data.jump: #no jump on the board
        if type(board[rowi][coli]) == float:
            if abs(rowi-rowf) != 1 or abs(coli-colf) != 1:
                #print "please move 1 square away"
                return False
            return True
        elif type(board[rowi][coli]) == int: #checks going in the right direction
            if rowf - rowi != 1*player or abs(coli-colf) != 1:
                #print "please move 1 square away"
                return False
            return True
    elif canvas.data.jump: #jump exists on board
        if type(board[rowi][coli]) == float:
            if abs(rowi-rowf) != 2 or abs(coli-colf) != 2: #not jump move
                #print "you must jump"
                return False
            elif not isValidJump(rowi,coli,rowf,colf): #not valid jump
                return False
        elif type(board[rowi][coli]) == int:
            if rowf-rowi != 2*player or abs(coli-colf) !=2:
                #print "you must jump"
                return False
            elif not isValidJump(rowi,coli,rowf,colf):
                return False
    return True

def convert(x,y): #takes mouseclick input and converts to boardspace
    cellSize = canvas.data.cellSize
    col = x / cellSize
    row = y / cellSize
    return col,row

def countCaptured():
    board = canvas.data.board
    blackCount = 12
    redCount = 12
    for row in xrange(len(board)):
        for col in xrange(len(board)):
            if board[row][col] > 0:
                blackCount -= 1
            elif board[row][col] < 0:
                redCount -= 1
    return blackCount,redCount

def drawMouseHover():
    rowi,coli = canvas.data.row_i,canvas.data.col_i
    rowf,colf = convert(canvas.data.mousey,canvas.data.mousex)
    cs = canvas.data.cellSize
    if isLegalMove(rowi,coli,rowf,colf):
        canvas.create_rectangle(cs*colf,cs*rowf,cs*(colf+1),cs*(rowf+1),fill="saddlebrown",outline="white",width=3)

def drawMouseDrag():
    x = canvas.data.mousex
    y = canvas.data.mousey
    cs = canvas.data.cellSize
    try:
        row = canvas.data.row_i
        col = canvas.data.col_i
    except:
        return
    board = canvas.data.board
    player = canvas.data.player
    if board[row][col] == 1:
        canvas.create_rectangle(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="saddlebrown",outline="white",width=3)
        canvas.create_arc(x-cs/2,y-cs/2,x+cs/2,y+cs/2,fill="gray20",start=45,extent=180)
        canvas.create_arc(x-cs/2,y-cs/2,x+cs/2,y+cs/2,fill="gray1",start=225,extent=180)              
        canvas.create_oval(x-cs/2+cs*0.04,y-cs/2+cs*0.04,x+cs/2-cs*0.04,y+cs/2-cs*0.04,fill="gray10")
        canvas.create_arc(x-cs/2+cs*0.1,y-cs/2+cs*0.1,x+cs/2-cs*0.1,y+cs/2-cs*0.1,fill="gray1",start=45,extent=180)
        canvas.create_arc(x-cs/2+cs*0.1,y-cs/2+cs*0.1,x+cs/2-cs*0.1,y+cs/2-cs*0.1,fill="gray20",start=225,extent=180)
        canvas.create_oval(x-cs/2+cs*0.12,y-cs/2+cs*0.12,x+cs/2-cs*0.12,y+cs/2-cs*0.12,fill="gray10")        
        #canvas.create_oval(x-cs/2,y-cs/2,x+cs/2,y+cs/2,fill="black",width=5,outline="white")
    elif board[row][col] == -1:
        canvas.create_rectangle(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="saddlebrown",outline="white",width=3)
        canvas.create_arc(x-cs/2,y-cs/2,x+cs/2,y+cs/2,fill="red2",start=45,extent=180)
        canvas.create_arc(x-cs/2,y-cs/2,x+cs/2,y+cs/2,fill="red4",start=225,extent=180)
        canvas.create_oval(x-cs/2+cs*0.04,y-cs/2+cs*0.04,x+cs/2-cs*0.04,y+cs/2-cs*0.04,fill="red3")
        canvas.create_arc(x-cs/2+cs*0.1,y-cs/2+cs*0.1,x+cs/2-cs*0.1,y+cs/2-cs*0.1,fill="red4",start=45,extent=180)
        canvas.create_arc(x-cs/2+cs*0.1,y-cs/2+cs*0.1,x+cs/2-cs*0.1,y+cs/2-cs*0.1,fill="red2",start=225,extent=180)
        canvas.create_oval(x-cs/2+cs*0.12,y-cs/2+cs*0.12,x+cs/2-cs*0.12,y+cs/2-cs*0.12,fill="red3")
    if type(board[row][col]) == float:
        canvas.create_oval(x-cs/6,y-cs/6,x+cs/6,y+cs/6,fill="white")
    
def drawPieces():
    board = canvas.data.board
    size = canvas.data.size
    cs = canvas.data.cellSize
    for row in xrange(size):
        for col in xrange(size):
            if board[row][col] == 1:
                canvas.create_arc(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="gray20",start=45,extent=180)
                canvas.create_arc(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="gray1",start=225,extent=180)                
                canvas.create_oval(cs*col+cs*0.04,cs*row+cs*0.04,cs*(col+1)-cs*0.04,cs*(row+1)-cs*0.04,fill="gray10")
                canvas.create_arc(cs*col+cs*0.1,cs*row+cs*0.1,cs*(col+1)-cs*0.1,cs*(row+1)-cs*0.1,fill="gray1",start=45,extent=180)
                canvas.create_arc(cs*col+cs*0.1,cs*row+cs*0.1,cs*(col+1)-cs*0.1,cs*(row+1)-cs*0.1,fill="gray20",start=225,extent=180)
                canvas.create_oval(cs*col+cs*0.12,cs*row+cs*0.12,cs*(col+1)-cs*0.12,cs*(row+1)-cs*0.12,fill="gray10")
            elif board[row][col] == -1:
                canvas.create_arc(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="red2",start=45,extent=180)
                canvas.create_arc(cs*col,cs*row,cs*(col+1),cs*(row+1),fill="red4",start=225,extent=180)                
                canvas.create_oval(cs*col+cs*0.04,cs*row+cs*0.04,cs*(col+1)-cs*0.04,cs*(row+1)-cs*0.04,fill="red3")
                canvas.create_arc(cs*col+cs*0.1,cs*row+cs*0.1,cs*(col+1)-cs*0.1,cs*(row+1)-cs*0.1,fill="red4",start=45,extent=180)
                canvas.create_arc(cs*col+cs*0.1,cs*row+cs*0.1,cs*(col+1)-cs*0.1,cs*(row+1)-cs*0.1,fill="red2",start=225,extent=180)
                canvas.create_oval(cs*col+cs*0.12,cs*row+cs*0.12,cs*(col+1)-cs*0.12,cs*(row+1)-cs*0.12,fill="red3")
            if type(board[row][col]) == float:
                canvas.create_oval(cs*col+cs/3,cs*row+cs/3,cs*(col+1)-cs/3,cs*(row+1)-cs/3,fill="white")
            #canvas.create_text(cs*row+cs/2,cs*col+cs/2,text="(%d,%d)" % (col,row),fill="blue")

def drawCheckersBoard():
    cs = canvas.data.cellSize
    size = canvas.data.size
    for i in xrange(size/2):
        for j in xrange(size):
            if j % 2 == 0:
                canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="khaki")
                canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="saddlebrown")
            elif j % 2 == 1:
                canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="saddlebrown")
                canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="khaki")

def drawSideBox():
    canvas.create_rectangle(600,0,900,600,fill="saddlebrown")
    canvas.create_rectangle(610,10,890,590,fill="khaki",width=0)
    startx,starty = 630, 490
    size = 75
    redCaptured,blackCaptured = countCaptured()
    for piece in xrange(redCaptured):
        p = piece * 15
        player = 1
        drawCaptured(startx,starty,p,player,size)
    startx,starty = 630,40
    for piece in xrange(blackCaptured):
        p = piece * 15
        player = -1
        drawCaptured(startx,starty,p,player,size)
    canvas.create_text(630,150,text="Captured : %d" % (blackCaptured),font=("Helvetica",20,"bold"),anchor=W)
    canvas.create_text(630,450,text="Captured : %d" % (redCaptured), font=("Helvetica",20,"bold"),anchor=W,fill="red")
    player = canvas.data.player
    if canvas.data.gameOver:
        if player == -1:
            color = "Black"
        elif player == 1:
            color = "Red"
        canvas.create_text(640,240,text="Game Over!",font=("Helvetica",25,"bold"),anchor=W,fill=color)
        canvas.create_text(640,270,text="%s Wins!" % (color),font=("Helvetica",25,"bold"),anchor=W,fill=color)
        canvas.create_text(640,315,text="Press \"R\" to Restart",font=("Helvetica",15,"bold"),anchor=W,fill="black")
        canvas.create_text(640,340,text="Or \"M\" for the Main Menu",font=("Helvetica",15,"bold"),anchor=W,fill="black")
    elif player == -1:
        canvas.create_rectangle(620,270,880,330,fill="",outline="red",width=5)
        canvas.create_text(640,300,text="Player 1's turn",font=("Helvetica",25,"bold"),anchor=W,fill="red")
    elif player == 1:
        canvas.create_rectangle(620,270,880,330,fill="",outline="black",width=5)
        canvas.create_text(640,300,text="Player 2's turn",font=("Helvetica",25,"bold"),anchor=W,fill="black")
    if canvas.data.onePlayer and canvas.data.AI:
        canvas.create_text(640,350,text="AI is thinking...",font=("Helvetica",25,"bold"),anchor=W,fill="black")

def drawCaptured(startx,starty,p,player,size):
    if player == -1:
        canvas.create_arc(startx+p,starty,startx+75+p,starty+75,fill="red2",start=45,extent=180)
        canvas.create_arc(startx+p,starty,startx+75+p,starty+75,fill="red4",start=225,extent=180)                
        canvas.create_oval(startx+size*0.04+p,starty+size*0.04,startx+75-size*0.04+p,starty+75-size*0.04,fill="red3")
        canvas.create_arc(startx+size*0.1+p,starty+size*0.1,startx+75-size*0.1+p,starty+75-size*0.1,fill="red4",start=45,extent=180)
        canvas.create_arc(startx+size*0.1+p,starty+size*0.1,startx+75-size*0.1+p,starty+75-size*0.1,fill="red2",start=225,extent=180)
        canvas.create_oval(startx+size*0.12+p,starty+size*0.12,startx+75-size*0.12+p,starty+75-size*0.12,fill="red3")
    elif player == 1:
        canvas.create_arc(startx+p,starty,startx+75+p,starty+75,fill="gray20",start=45,extent=180)
        canvas.create_arc(startx+p,starty,startx+75+p,starty+75,fill="gray1",start=225,extent=180)                
        canvas.create_oval(startx+size*0.04+p,starty+size*0.04,startx+75-size*0.04+p,starty+75-size*0.04,fill="gray10")
        canvas.create_arc(startx+size*0.1+p,starty+size*0.1,startx+75-size*0.1+p,starty+75-size*0.1,fill="gray1",start=45,extent=180)
        canvas.create_arc(startx+size*0.1+p,starty+size*0.1,startx+75-size*0.1+p,starty+75-size*0.1,fill="gray20",start=225,extent=180)
        canvas.create_oval(startx+size*0.12+p,starty+size*0.12,startx+75-size*0.12+p,starty+75-size*0.12,fill="gray10")        

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
        print board[i],","
    return

def loadSplashScreen():
    width = canvas.data.width
    height = canvas.data.height
    b1 = Button(canvas,text="Single Player",command=button1Pressed,activebackground="saddlebrown",\
        activeforeground="white",bg="khaki",height=1,width=14,font=("Helvetica",20,"bold"),overrelief="sunken")
    canvas.create_window(width/3, height*.65, window=b1)
    b2 = Button(canvas,text="Multiplayer",command=button2Pressed,activebackground="saddlebrown",\
        activeforeground="white",bg="khaki",height=1,width=14,font=("Helvetica",20,"bold"),overrelief="sunken")
    canvas.create_window(width*.65, height*.65, window=b2)

def drawAIButtons():
    width = canvas.data.width
    height = canvas.data.height
    b3 = Button(text="Beginner",command=button3Pressed,activebackground="saddlebrown",\
        activeforeground="white",bg="khaki",height=1,width=14,font=("Helvetica",15,"bold"),overrelief="sunken")
    canvas.create_window(width/3, height*.75, window=b3)
    b4 = Button(text="Intermediate",command=button4Pressed,activebackground="saddlebrown",\
        activeforeground="white",bg="khaki",height=1,width=14,font=("Helvetica",15,"bold"),overrelief="sunken")
    canvas.create_window(width/3, height*.85, window=b4)
    b5 = Button(text="Advanced",command=button5Pressed,activebackground="saddlebrown",\
        activeforeground="white",bg="khaki",height=1,width=14,font=("Helvetica",15,"bold"),overrelief="sunken")
    canvas.create_window(width/3, height*.95, window=b5)

def drawOval():
    left = canvas.data.ovalX % 400
    width = 5 + 300   
    oval = canvas.create_oval(left, 250, left+width, 300, fill="red")
    canvas.data.oval = oval

def deltaDrawOval():
    oval = canvas.data.oval
    left = canvas.data.ovalX % 500
    width = 305
    canvas.coords(oval,(left+10,250,305,300))
    canvas.data.ovalX = left+10

def deltaDraw():
    deltaDrawOval()
    #drawMenuAnimation()

def drawBackground():
    cs = 30
    for i in xrange(15):
        for j in xrange(20):
            if j % 2 == 0:
                if i < 1 or i > 13 or j < 2 or j > 17:
                    canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="khaki")
                    canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="saddlebrown")
            elif j % 2 == 1:
                if i < 1 or i > 13 or j < 3 or j > 17:
                    canvas.create_rectangle(cs*(2*i),cs*j,cs*(2*i+1),cs*(j+1),fill="saddlebrown")
                    canvas.create_rectangle(cs*(2*i+1),cs*j,cs*(2*i+2),cs*(j+1),fill="khaki")
    
def drawMenuAnimation():
    height = canvas.data.height
    width = canvas.data.width
    a = 500
    b = canvas.data.b
    canvas.create_rectangle(0,0,width,height,fill="white")
    canvas.create_oval(width/2-b/2,50,width/2+b/2,550,fill="red")
#    if b > 0:
 #       canvas.create_arc(width/2-b/2-20,50,width/2+b/2+20,550,fill="blue",start=90,extent=180)
  #  canvas.create_arc(width/3-b/2,50,width/2+b/2,550,fill="red",start=90,extent=180)
 #   canvas.create_arc(width/2-b/2+40,50,width/2+b/2,550,fill="red",start=270,extent=180)
  #  canvas.create_rectangle(width/2,50,width/2+20,550,fill="red")
    canvas.create_text(width/2,height*.3,text="Checkers",fill="black",font=("Helvetica",40))
    canvas.create_text(width/2,height*.4,text="By Kevin Dou",fill="black",font=("Helvetica",20))
    canvas.data.b -= 10*canvas.data.a
    if canvas.data.b < 0 or canvas.data.b > 500:
        canvas.data.a *= -1
        canvas.data.b -= 10* canvas.data.a

def init():
    loadCheckersBoard()
   # displayBoard()
    canvas.data.isEndGame = False
    canvas.data.currentPlayer = 1
    canvas.data.getMoveStart = True
    canvas.data.getMoveEnd = False
    canvas.data.player = -1
    canvas.data.jump = False
    canvas.data.gameOver = False
    canvas.data.mousePressed = False
    canvas.data.doubleJump = False
    canvas.data.AI = False
    canvas.data.AILevel = 1
    canvas.data.a = +1
    canvas.data.b = 500
    canvas.data.ovalX= 200
    if canvas.data.splash:
        loadSplashScreen()
        redrawAll()
        canvas.data.onePlayer = False
        canvas.data.twoPlayer = False
        timerFired()
    elif canvas.data.onePlayer:
        redrawAll()
    elif canvas.data.twoPlayer:
        redrawAll()

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    size = 8
    width = 900
    height = 600
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.cellSize = 75
    canvas.data.size = 8
    canvas.data.width = width
    canvas.data.height = height
    canvas.data.board = [[]]
    canvas.data.splash = True
    canvas.data.onePlayer = False
    canvas.data.twoPlayer = False
    init()
    # set up events
    canvas.bind("<B1-Motion>", leftMouseMoved)
    root.bind("<Button-1>", leftMousePressed)
    root.bind("<B1-ButtonRelease>", leftMouseReleased)
    root.bind("<Key>", keyPressed)
   # timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()