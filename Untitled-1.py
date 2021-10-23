
#define valid_number that will be put in the grid(1-9)
valid_number = [1,2,3,4,5,6,7,8,9]

#print(grid)
               
def find_empty(grid):
    for i in range(row):
        for j in range(column):
            if grid[i][j] == 0:
                return i,j
    return None

def check_filled(grid):
    for i in range(row):
        for j in range(column):
            if grid[i][j] == 0:
                return False
    return True


def clear_grid():
    for i in range(row):
        for j in range(column):
            grid[i][j] = 0



def check_full_grid():
    if check_rowcolumn(row,column,grid):
        if check_square(row,column,grid):
            return True
    return False


#the check_rowcolumn function is to check if input number is duplciated in row/column
def check_rowcolumn(current_row:int,current_column:int,grid,number:int): #1,8
    for i in range(row):
        if grid[i][current_column]== number:
            return False
    for j in range(column):
        if grid[current_row][j] == number:
            return False
    return True
    
#the check_square function is to check if the number input is duplcated in square(3*3)
def check_square(current_row:int,current_column:int,grid,number:int):
    #check by 3*3 square for current value
    current_row = current_row - (current_row % 3)
    current_column = current_column - (current_column % 3)
    #start checking if this square has invalid value
    for x in range(3):
        for y in range(3):
            if grid[current_row+x][current_column+y] == number:
                return False
            #else:
                #check.add(grid[i+x][j+y])
    return True

#base case is when all grid is filled

def fill_grid(grid):
    random.shuffle(valid_number)
    #define base case
    emtpy_cell = find_empty(grid) 
    if not emtpy_cell:
        return True
    else:   
        #mark next empty celxl
        i,j = emtpy_cell
    #loop through 1-9
    for value in valid_number:
        if check_rowcolumn(i,j,grid,value):
            if check_square(i,j,grid,value):
                grid[i][j] = value
                #print(grid[i][j])
                if check_filled(grid):
                    return True
                else:
                    if fill_grid(grid):
                        return True
    #print(f"reset one cell, reset location is {i},{j}, original value is {grid[i][j]}")
    grid[i][j]=0



#we have to make a function that check number of solution
def check_solution(cur_grid):
    global count
    #define base case
    emtpy_cell = find_empty(cur_grid) 
    if not emtpy_cell:
        return True
    else:   
        #mark next empty celxl
        i,j = emtpy_cell
    #loop through 1-9, no need to random num as we are looking for solution only
    for value in range(1,10):
        if count > 1:
            break
        if check_rowcolumn(i,j,cur_grid,value):
            if check_square(i,j,cur_grid,value):
                cur_grid[i][j] = value
                #print(grid[i][j])
                if check_filled(cur_grid):
                    #possible solition +=1
                    count+=1
                    #break the current loop, backtrack for another possible solution
                    break
                else:
                    if check_solution(cur_grid):
                        return True
    #reset current grid value to 0, backtrack to previous stack
    cur_grid[i][j]=0






def remove_cell(difficulty:int,grid:list):
    global count
    empty_cell = 0
    while empty_cell < difficulty:
        target_row = random.randint(0,8)
        target_col = random.randint(0,8)
        count = 0
        if grid[target_row][target_col]!=0:
            backup = grid[target_row][target_col]
            grid[target_row][target_col] = 0
            #create a deep copy of the current grid that is used for check_solution function to test with
            copy_grid = copy.deepcopy(grid)
            check_solution(copy_grid)

            if count == 1:
                empty_cell+=1
            else:
                grid[target_row][target_col] = backup


        

    return empty_cell,copy_grid