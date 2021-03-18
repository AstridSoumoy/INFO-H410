import math

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
