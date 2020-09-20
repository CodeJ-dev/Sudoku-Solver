# Jay Doshi
# Sudoku - Solver

import random
import pygame
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Pygame 
WIDTH = 360
HEIGHT = 360
BLOCKSIZE = 40
FPS = 50
WAIT = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Constants
N = HEIGHT // BLOCKSIZE
FAIL = -100000
MAX = 100000

class Cell(object):
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.rect = None
        self.num = num

    def __str__(self):
        return str(self.num)
        
def createBoard(N):
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(Cell(i,j,0))
        board.append(row)
    return board

def printGrid(board):
    for i in board:
        for j in i:
            print(j, end =  " ")
        print()
    print()

def validBoard(board, r, c, num, N):

    for i in range(N):
        if board[r][i].num == num:
            return False

    for i in range(N):
        if board[i][c].num == num:
            return False
    
    row = r // 3 * 3
    col = c // 3 * 3
    
    for j in range(3):
        for k in range(3):
            x = row + j
            y = col + k
            if board[x][y].num == num:
                return False
    
    return True

def backtrack(board, N):

    r = -1
    c = -1

    flag = False

    for i in range(N):
        for j in range(N):
            if board[i][j].num == 0:
                r = i
                c = j
                flag = True
                break
        if flag:
            break

    if not flag:
        return True

    for i in range(1,10):
        if validBoard(board, r, c, i, N):
            board[r][c].num = i
            if backtrack(board, N):
                return True
            board[r][c].num = 0
        
    return False

def shift(board, r1, r2, s, N):
    for i in range(N):
        board[r2 - 1][(i + s) % N].num = board[r1 - 1][i].num
    
def generate(N):
    board = createBoard(N)
    r = random.randint(6,N)
    for i in range(r):
        x = random.randint(1,9)
        if validBoard(board, 0, i, x, N):
            board[0][i].num = x
        else:
            x = random.randint(1,10)
    shift(board, 1, 2, 3, N)
    shift(board, 2, 3, 3, N)
    shift(board, 3, 4, 1, N)
    shift(board, 4, 5, 3, N)
    shift(board, 5, 6, 3, N)
    shift(board, 6, 7, 1, N)
    shift(board, 7, 8, 3, N)
    shift(board, 8, 9, 3, N)
    
    return board

def onsubmitreset():
    window1.quit()
    window1.destroy()

def drawLine(grid):
    for i in range(1, 3):
        pygame.draw.lines(screen, RED, False, [(i * BLOCKSIZE * 3, 0), (i * BLOCKSIZE * 3, HEIGHT)], 5)

    for i in range(1, 3):
        pygame.draw.lines(screen, RED, False, [(0, i * BLOCKSIZE * 3), (WIDTH, i * BLOCKSIZE * 3)], 5)

def fillNumber(grid, x, y):
    if grid[x][y].num == 0:
        rect = grid[x][y].rect
        pygame.draw.rect(screen, BLACK, rect, 0)
        pygame.draw.rect(screen, WHITE, rect, 1)
        drawLine(grid)
        return
    font = pygame.font.Font('freesansbold.ttf', 30) 
    text = font.render(f"{grid[x][y].num}", True, BLUE, BLACK)
    orig = grid[x][y].rect.center
    dx = 10
    dy = 5
    grid[x][y].rect.center = (grid[x][y].rect.center[0] + dx, grid[x][y].rect.center[1] + dy)
    screen.blit(text, grid[x][y].rect)
    grid[x][y].rect.center = orig
    
def drawStartGrid(grid):
    screen.fill(BLACK)
    for x in range(N):
        for y in range(N):
            rect = pygame.Rect(x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
            grid[x][y].rect = rect
            pygame.draw.rect(screen, WHITE, rect, 1)
            if grid[x][y].num != 0:
                fillNumber(grid, x, y)
            
    drawLine(grid)
    
def resetGrid(grid):
    screen.fill(BLACK)
    for x in range(N):
        for y in range(N):
            rect = grid[x][y].rect
            pygame.draw.rect(screen, WHITE, rect, 1)
            
    drawLine(grid)

def getCell(pos):
    if (pos[0] > WIDTH or pos[0] < 0 or pos[1] > HEIGHT or pos[1] < 0):
        return [-1]
    if (pos[0] % BLOCKSIZE == 0 or pos[1] % BLOCKSIZE == 1):
        return [-1]
    x = pos[0] // BLOCKSIZE
    y = pos[1] // BLOCKSIZE
    return [x,y]

def gameFinished(board, N):
    for r in range(N):
        for c in range(N):
            if board[r][c].num == 0:
                return False
    return True

# start Pygame and make window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()

# Game loop
run = True
hasStarted = True
game = True

numPad = {pygame.K_KP1 : 1, pygame.K_KP2 : 2, pygame.K_KP3 : 3, pygame.K_KP4 : 4, pygame.K_KP5 : 5, pygame.K_KP6 : 6, pygame.K_KP7 : 7, pygame.K_KP8 : 8, pygame.K_KP9 : 9}

key = -1
selectX = -1
selectY = -1

while run:
    
    for event in pygame.event.get():
        if (event.type == 'pygame.QUIT'):
            run = False                
        if game and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                key = 1
            if event.key == pygame.K_2:
                key = 2
            if event.key == pygame.K_3:
                key = 3
            if event.key == pygame.K_4:
                key = 4
            if event.key == pygame.K_5:
                key = 5
            if event.key == pygame.K_6:
                key = 6
            if event.key == pygame.K_7:
                key = 7
            if event.key == pygame.K_8:
                key = 8
            if event.key == pygame.K_9:
                key = 9

            if event.key == pygame.K_BACKSPACE:
                print(key,selectX,selectY,board[selectX][selectY])
                if selectX is not -1 and selectY is not -1:
                    board[selectX][selectY].num = 0
                    fillNumber(board, selectX, selectY)
                    pygame.display.update()

            if key != -1 and event.key == pygame.K_RETURN:
                print(key,selectX,selectY,board[selectX][selectY])
                if selectX is not -1 and selectY is not -1:
                    if validBoard(board, selectX, selectY, key, N) and board[selectX][selectY].num == 0:
                        print("Enter")
                        board[selectX][selectY].num = key
                        fillNumber(board, selectX, selectY)
                        pygame.display.update()
                        game = not gameFinished(board, N)
                        print(game)
                    else:
                        print("fail")
                        
            if event.key == pygame.K_SPACE:
                game = False
                backtrack(board, N)
                if not game:
                    for x in range(N):
                        for y in range(N):
                            if board[x][y].num != 0:
                                fillNumber(board, x, y)
                                pygame.display.update()
                                
                                    
        if game and event.type == pygame.MOUSEBUTTONDOWN:
             s = getCell(pygame.mouse.get_pos())
             if s[0] == -1:
                 continue
             selectX = s[0]
             selectY = s[1]     
                    
    if hasStarted:
        board = generate(N)
        drawStartGrid(board)
        pygame.display.update()
        hasStarted = False
        game = True
        pygame.display.update()

    # Tkinter
    if game == False:
        window1 = Tk()
        var3 = IntVar()
        reset = ttk.Checkbutton(window1, text='Reset :', onvalue=1, offvalue=0, variable=var3)
        submit1 = Button(window1, text='Submit', command=onsubmitreset)

        reset.grid(columnspan=1, row=1)
        submit1.grid(columnspan=2, row=2)

        window1.update()
        mainloop()

        if var3.get() == 1:
            resetGrid(board)
            hasStarted = True
            game = True
            pygame.display.update()
     
    pygame.display.update()
    
pygame.quit()
