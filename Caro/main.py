import time
import turtle
import random

global store_move

def winCase(sumcol):
    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2):
        return 4
    elif keyScore(sumcol[3],sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(),reverse = True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0
    
def optimizeMove(board,col):
    if col == 'w':
        anticol = 'b'
    else:
        anticol = 'w' 
    movecol = (0,0)
    maxscorecol = ''
    if check_board(board):
        movecol = ( int((len(board))*random.random()),int((len(board[0]))*random.random()))
    else:
        moves = validMove(board)
        for move in moves:
            y,x = move
            if maxscorecol == '':
                scorecol=avoidMark(board,col,anticol,y,x)
                maxscorecol = scorecol
                movecol = move
            else:
                scorecol=avoidMark(board,col,anticol,y,x)
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = move
    return movecol

def listenMouse(x,y):
    global board,colors,win, store_move
    x,y = locationIndex(x,y)
    if x == -1 and y == -1 and len(store_move) != 0:
        x, y = store_move[-1]
        del(store_move[-1])
        board[y][x] = " "
        x, y = store_move[-1]
        del(store_move[-1])
        board[y][x] = " "
        return
    if not check_inside(board, y, x):
        return
    
    if board[y][x] == ' ':  
        drawPieces(x,y,colors['b'])
        board[y][x]='b'
        store_move.append((x, y))
        game_res = check_win(board)
        if game_res in ["AI Won!", "Human Won!", "Draw"]:
            print (game_res)
            win = True
            return
        ay,ax = optimizeMove(board,'w')
        drawPieces(ax,ay,colors['w'])
        board[ay][ax]='w'            
        store_move.append((ax, ay))
        game_res = check_win(board)
        if game_res in ["AI Won!", "Human Won!", "Draw"]:
            print (game_res)
            win = True
            return

def movement(board,y,x,dy,dx,length):
    yf = y + length*dy 
    xf = x + length*dx
    while not check_inside(board,yf,xf):
        yf -= dy
        xf -= dx        
    return yf,xf
    
def mark(scorecol):
    sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1            
    return sumcol
    
def getColSum(sumcol):
    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())
            
def listMark(lis,col):    
    blank = lis.count(' ')
    filled = lis.count(col)   
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

def accessList(board,y,x,dy,dx,yf,xf):
    row = []
    while y != yf + dy or x !=xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row
    
def getRowSum(board,cordi,dy,dx,cordf,col):
    colscores = []
    y,x = cordi
    yf,xf = cordf
    row = accessList(board,y,x,dy,dx,yf,xf)
    for start in range(len(row)-4):
        score = listMark(row[start:start+5],col)
        colscores.append(score)
    
    return colscores

def col_mark_total(board,col):
    f = len(board)
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    for start in range(len(board)):
        scores[(0,1)].extend(getRowSum(board,(start, 0), 0, 1,(start,f-1), col))
        scores[(1,0)].extend(getRowSum(board,(0, start), 1, 0,(f-1,start), col))
        scores[(1,1)].extend(getRowSum(board,(start, 0), 1,1,(f-1,f-1-start), col))
        scores[(-1,1)].extend(getRowSum(board,(start,0), -1, 1,(0,start), col))
        if start + 1 < len(board):
            scores[(1,1)].extend(getRowSum(board,(0, start+1), 1, 1,(f-2-start,f-1), col)) 
            scores[(-1,1)].extend(getRowSum(board,(f -1 , start + 1), -1,1,(start+1,f-1), col))           
    return mark(scores)
    
def col_mark_total_one(board,col,y,x):
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}  
    scores[(0,1)].extend(getRowSum(board,movement(board,y,x,0,-1,4), 0, 1,movement(board,y,x,0,1,4), col))    
    scores[(1,0)].extend(getRowSum(board,movement(board,y,x,-1,0,4), 1, 0,movement(board,y,x,1,0,4), col))    
    scores[(1,1)].extend(getRowSum(board,movement(board,y,x,-1,-1,4), 1, 1,movement(board,y,x,1,1,4), col))
    scores[(-1,1)].extend(getRowSum(board,movement(board,y,x,-1,1,4), 1,-1,movement(board,y,x,1,-1,4), col))    
    return mark(scores)

def clear_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def check_board(board):
    return board == [[' ']*len(board)]*len(board)

def check_inside(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)

def check_win(board):
    black = col_mark_total(board,'b')
    white = col_mark_total(board,'w')
    getColSum(black)
    getColSum(white)
    if 5 in black and black[5] == 1:
        turtle.color("yellow")
        turtle.write("Human Won!", font=("Arial", 20, "normal"))
        return 'Human Won!'
    elif 5 in white and white[5] == 1:
        turtle.color("yellow")
        turtle.write("AI Won!", font=("Arial", 20, "normal"))
        return 'AI Won!'

    if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or validMove(board)==[]:
        return 'Draw'  
    return 'Play again!'


def validMove(board): 
    taken = []
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
    cord = {}    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i,j))

    for direction in directions:
        dy,dx = direction
        for coord in taken:
            y,x = coord
            for length in [1,2,3,4]:
                move = movement(board,y,x,dy,dx,length)
                if move not in taken and move not in cord:
                    cord[move]=False
    return cord
    
def keyScore(score3,score4):
    for key4 in score4:
        if score4[key4] >=1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >=2:
                        return True
    return False
    
def avoidMark(board,col,anticol,y,x):
    global colors
    M = 1000
    res,adv, dis = 0, 0, 0
    board[y][x]=col
    sumcol = col_mark_total_one(board,col,y,x)       
    a = winCase(sumcol)
    adv += a * M
    getColSum(sumcol)
    adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4] 
    board[y][x]=anticol
    sumanticol = col_mark_total_one(board,anticol,y,x)  
    d = winCase(sumanticol)
    dis += d * (M-100)
    getColSum(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]
    res = adv + dis
    board[y][x]=' '
    return res


def createGame(size):
    global win,board,screen,colors, store_move
    turtle.title("CARO - Game Playing Agent - 2020088")
    store_move = []
    win = False
    board = clear_board(size)
    screen = turtle.Screen()
    screen.onclick(listenMouse)
    screen.setup(screen.screensize()[1]*2,screen.screensize()[1]*2)
    screen.setworldcoordinates(-1,size,size,-1)
    screen.bgcolor(0.6, 0.3, 0)
    screen.tracer(500)
    colors = {'w':turtle.Turtle(),'b':turtle.Turtle(), 'g':turtle.Turtle()}
    colors['w'].color('white')
    colors['b'].color('black')
    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)
    border = turtle.Turtle()
    border.speed(9)
    border.penup()
    side = (size-1)/2
    i=-1
    for start in range(size):
        border.goto(start,side + side *i)    
        border.pendown()
        i*=-1
        border.goto(start,side + side *i)     
        border.penup() 
    i=1
    for start in range(size):
        border.goto(side + side *i,start)
        border.pendown()
        i *= -1
        border.goto(side + side *i,start)
        border.penup() 
    border.ht()
    screen.listen()
    screen.mainloop()
    
def locationIndex(x,y):
    intx,inty = int(x),int(y)
    dx,dy = x-intx,y-inty
    if dx > 0.5:
        x = intx +1
    elif dx<-0.5:
        x = intx -1
    else:
        x = intx
    if dy > 0.5:
        y = inty +1
    elif dx<-0.5:
        y = inty -1
    else:
        y = inty
    return x,y

def drawPieces(x,y,colturtle):
    colturtle.goto(x,y-0.4)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.4)
    colturtle.end_fill()
    colturtle.penup()
    
if __name__ == '__main__':
    createGame(15)