import math
import pygame
import time


def findBlankTile(sudoMatrix):
    for i in range(len(sudoMatrix[0])):
        for j in range(len(sudoMatrix)):
            if sudoMatrix[i][j] == 0:
                return [i,j]
    return -1
    
def isValid(num, pos, sudoMatrix):
    SQUARE_NUMBER = 3
    line = pos[0]
    col = pos[1]
    for i in range(len(sudoMatrix[0])):
        if num == sudoMatrix[line][i]:
            return False
    for j in range(len(sudoMatrix)):
        if num == sudoMatrix[j][col]:
            return False
        
    horizontal = math.floor(line / SQUARE_NUMBER)
    vertical = math.floor(col / SQUARE_NUMBER)
    
    for i in range(SQUARE_NUMBER):
        for j in range(SQUARE_NUMBER):
            if num == sudoMatrix[horizontal*SQUARE_NUMBER + i][vertical*SQUARE_NUMBER + j]:
                return False
        
    return True

    

def solveSudoku(sudoMatrix):
    pos = findBlankTile(sudoMatrix)
    if pos == -1 :
        return True
    
    for num in range(1, 10):
        if isValid(num, pos, sudoMatrix):
            sudoMatrix[pos[0]][pos[1]] = num
            if solveSudoku(sudoMatrix): 
                return True
            
    sudoMatrix[pos[0]][pos[1]] = 0
    return False


def solveSudokuGUI(board, wrong):
    for event in pygame.event.get(): #so that touching anything doesn't freeze the screen
        if event.type == pygame.QUIT:
            exit()
                
    pos = findBlankTile(board.board)
    if pos == -1 :
        return True
    
    for num in range(1, 10):
        if isValid(num, pos, board.board):
            board.board[pos[0]][pos[1]] = num
            board.tiles[pos[0]][pos[1]].value = num
            board.tiles[pos[0]][pos[1]].correct = True
            board.redraw({}, wrong, "")
            if solveSudokuGUI(board, wrong): 
                return True
            
            board.board[pos[0]][pos[1]] = 0
            board.tiles[pos[0]][pos[1]].value = 0
            board.tiles[pos[0]][pos[1]].incorrect = True
            board.tiles[pos[0]][pos[1]].correct = False
            board.redraw({}, wrong, "")
            
    return False


def print_board(board, elapsedTime):
    '''Prints the board'''
    boardString = ""
    for i in range(9):
        for j in range(9):
            boardString += str(board[i][j]) + " "
            if (j+1)%3 == 0 and j != 0 and (j+1) != 9:
                boardString += "| "

            if j == 8:
                boardString += "\n"

            if j == 8 and (i+1)%3 == 0 and (i+1) != 9:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)
    print("elapsed time : " + str(elapsedTime) + " seconds \n")
    
    
def generate():
    """return  [
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]"""
    return  [
        [0, 0, 5, 3, 6, 0, 4, 8, 0],
        [0, 4, 0, 9, 0, 0, 0, 0, 0],
        [2, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 1, 0],
        [0, 3, 0, 0, 0, 0, 9, 0, 8],
        [0, 0, 0, 4, 0, 0, 6, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 4, 9, 0, 0, 0],
        [3, 0, 0, 8, 5, 0, 0, 0, 6]
    ]

class Board:
    '''A sudoku board made out of Tiles'''
    def __init__(self, window):
        self.board = generate()
        self.solvedBoard = generate()
        solveSudoku(self.solvedBoard)
        self.tiles = [[Tile(self.board[i][j], window, i*60, j*60) for j in range(9)] for i in range(9)]
        self.window = window

    def draw_board(self):
        '''Fills the board with Tiles and renders their values'''
        for i in range(9):
            for j in range(9):
                if j%3 == 0 and j != 0: #vertical lines
                    pygame.draw.line(self.window, (0, 0, 0), ((j//3)*180, 0), ((j//3)*180, 540), 4)

                if i%3 == 0 and i != 0: #horizontal lines
                    pygame.draw.line(self.window, (0, 0, 0), (0, (i//3)*180), (540, (i//3)*180), 4)

                self.tiles[i][j].draw((0,0,0), 1)

                if self.tiles[i][j].value != 0: #don't draw 0s on the grid
                    self.tiles[i][j].display(self.tiles[i][j].value, (21+(j*60), (16+(i*60))), (0, 0, 0))  #20,5 are the coordinates of the first tile
        #bottom-most line
        pygame.draw.line(self.window, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)
        
    def redraw(self, keys, wrong, time):
        '''Redraws board with highlighted tiles'''
        self.window.fill((255,255,255))
        self.draw_board()
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected:  #draws the border on selected tiles
                    self.tiles[j][i].draw((50, 205, 50), 4)

                elif self.tiles[i][j].correct:
                    self.tiles[j][i].draw((34, 139, 34), 4)

                elif self.tiles[i][j].incorrect:
                    self.tiles[j][i].draw((255, 0, 0), 4)

        if len(keys) != 0: #draws inputs that the user places on board but not their final value on that tile
            for value in keys:
                self.tiles[value[0]][value[1]].display(keys[value], (21+(value[0]*60), (16+(value[1]*60))), (128, 128, 128))

        if wrong > 0:
            font = pygame.font.SysFont('Bauhaus 93', 30) #Red X
            text = font.render('X', True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont('Bahnschrift', 40) #Number of Incorrect Inputs
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont('Bahnschrift', 40) #Time Display
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()
        
    
class Tile:
    '''Represents each white tile/box on the grid'''
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60) #dimensions for the rectangle
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        '''Draws a tile on the board'''
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color):
        '''Displays a number on that tile'''
        font = pygame.font.SysFont('lato', 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos): #checks if a point is inside a rect
            self.selected = True
        return self.selected


def solveIt():
    startTime = time.time()
    board = generate()
    solveSudoku(board)
    endTime = time.time()
    print_board(board, endTime-startTime)
    
    
def solveItWithGUI():
    pygame.init()
    screen = pygame.display.set_mode((540, 590))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku")

    #loading screen when generating grid
    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))
    
    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Grid", True, (0, 0, 0))
    screen.blit(text, (230, 290))
    pygame.display.flip()
    
    wrong = 0
    board = Board(screen)
    solveSudokuGUI(board, wrong)

if __name__ == '__main__':
    #solveIt()
    solveItWithGUI()
    
    
    