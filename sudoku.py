############################################################
# A sudoku game made with pygame
# Made by: Jack Tsai
# Created/Last updated on : 16/11/2021
############################################################
import pygame
import time
import Data.Method.method as method

pygame.init()                                           

####################################################
# Global Setting ,set here for easy update in future
####################################################

screen = pygame.display.set_mode
background_color = (192,192,192)
#below variable is for button 
button_height = 53
button_width = 251
#mark the first button location
button_xy = (275,450)
gap = 20
#default font
default_font = "Data/8-BitMadness.ttf"
#set resolution
res = (800,900)

class board:
#define the row and column lenth
    def __init__(self,row,column) -> None:
        self.row = row
        self.column = column
        self.grid = [[0 for _ in range(self.row)]for _ in range(self.column)]
    
    def setup(self,screen):
        screen.fill(background_color)
        #declare game windows title
        pygame.display.set_caption("Sudoku game")
        #game icon ,attribute to Freepik on flaticon.com
        icon = pygame.image.load('Data/Image/icon.png')
        pygame.display.set_icon(icon)
        #set up difficulty button
        easy = pygame.image.load('Data/Image/easy.png')
        screen.blit(easy,self.button_pos(0))
        normal = pygame.image.load('Data/Image/normal.png')
        screen.blit(normal,self.button_pos(1))
        hard = pygame.image.load('Data/Image/hard.png')
        screen.blit(hard,self.button_pos(2))

        #Since pygame.render does not support multi -line, we will have to do line break in other way
        intro_text = ["Please select the difficulty of this game by clicking","button below"]
        intro_font = pygame.font.Font(default_font,30)
        introduction = [intro_font.render(line,True,(0,0,0)) for line in intro_text]
        how_to_play_text = ["How to play:","Click on the box to select","After select input a number to fill it","You can revert and empty the box by select and input 0",
                            "Press Space when you are finish to check if you are correct"]
        how_to_play = [intro_font.render(line,True,(0,0,0)) for line in how_to_play_text]
        for i,text in enumerate(introduction):
            screen.blit(text,(35,100+i*30))
        #added 1 and len(introduction) to add extra line between 2 text
        for i,text in enumerate(how_to_play):
            screen.blit(text,(35,100+(i+len(introduction)+1)*30))

    def button_pos(self,button_no):
        xy = list(button_xy)
        xy[1] = button_no*(gap+button_height) + button_xy[1]
        xy = tuple(xy)
        return xy


    def draw_board(self,screen,grid,status,playtime):
        #################################################
        # status 0 --> no msg
        # status 1 --> invalid input
        # status 2 --> Victory
        # status 3 --> Incorrect answer
        #################################################
        screen.fill(background_color)
        #draw grid
        number_font = pygame.font.Font(default_font,65)
        for i in range(10):
            if i%3 ==0:
                pygame.draw.line(screen,(0,0,0),(40+80*i,40),(40+80*i,760),5)
                pygame.draw.line(screen,(0,0,0),(40,40+80*i),(760,40+80*i),5)
            else:
                pygame.draw.line(screen,(0,0,0),(40+80*i,40),(40+80*i,760),2)
                pygame.draw.line(screen,(0,0,0),(40,40+80*i),(760,40+80*i),2)

        #add number
        for i in range(self.row):
            for j in range(self.column):
                if grid[i][j]!=0:
                    value = number_font.render(str(grid[i][j]),True,(0,66,200))
                    #row and col need to be reversed
                    screen.blit(value,(40+80*j+25,40+80*i+20))

        #print status msg
        if status != 0:
            msg_font = pygame.font.Font(default_font,30)
            if status == 1:
                text = msg_font.render("Invalid number/input",True,(255,0,0))
                screen.blit(text,(40,820))
            elif status == 2:
                text = msg_font.render("You have solved the puzzle!!! Click anywhere to start a new game",True,(0,255,0))
                screen.blit(text,(40,820))
            elif status == 3:
                text = msg_font.render("Sorry, your answer is not correct",True,(255,0,0))
                screen.blit(text,(40,820))

        #draw time
        time_font = pygame.font.Font(default_font,35)
        timer = time_font.render("Time :"+ format_time(playtime),True,(0,0,0))
        screen.blit(timer,(580,820))

    def insert(self,i,j,copy_grid,key):
        status = 0
        #compare to ori_grid, if it is not editable, return
        if self.grid[i][j]!=0:
            return copy_grid,status
        # erase 
        if key == 0:
            copy_grid[i][j] = 0
            return copy_grid,status
        #insert/replace with new num
        if (0 < key <10):
            if copy_grid[i][j] == key or (method.check_rowcolumn(i,j,copy_grid,key) and method.check_square(i,j,copy_grid,key)):
                copy_grid[i][j] = key
                return copy_grid,status
            else:
                status = 1
                return copy_grid,status

#this function is to return the coordinate of which box is selected
def click(pos,screen):   
    i,j = (pos[1]-40)//80,(pos[0]-40)//80
    if not (0<=i<9 and 0<=j<9):
        return 0,None
    return 0,(i,j)

#this function is to draw red outline for selected box
def selected(screen,x,y):
    if x is None or y is None:
        return
    pygame.draw.line(screen,(255,0,0),(40+80*x,40+80*y),(40+80*(x+1),40+80*y),5)
    pygame.draw.line(screen,(255,0,0),(40+80*x,40+80*(y+1)),(40+80*(x+1),40+80*(y+1)),5)
    pygame.draw.line(screen,(255,0,0),(40+80*x,40+80*y),(40+80*x,40+80*(y+1)),5)
    pygame.draw.line(screen,(255,0,0),(40+80*(x+1),40+80*y),(40+80*(x+1),40+80*(y+1)),5)

def check_win(screen,ori_grid,player_grid):
    if ori_grid == player_grid:
        return True
    return False

def format_time(seconds:int):
    sec = seconds % 60
    minute = seconds//60

    formatted_time  = f" {minute:02d} : {sec:02d}"
    return formatted_time

#create board
bo = board(9,9)

def main(grid:list):
    #create the window/screen
    global background_color
    screen = pygame.display.set_mode(res)

    #declare a varibale to control game running
    running = True
    #a varibale to store difficulty , if difficulty is 0 , it means no difficulty have been chosen yet
    difficulty_flag = 0
    #a flag to decide what status msg should be printed or not
    status = 0
    #the select variable is a flag to show if any cell is selected 
    select = False
    screen.fill(background_color)
 
    while running:    
        #inintialize difficulty page
        while difficulty_flag ==0 and running:
            bo.setup(screen)
            pygame.display.update()
            #allow player to set difficulty
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    running = False
                    return
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x,y = pos[0],pos[1]
                    #update difficulty flag base on difficulty selected
                    if bo.button_pos(0)[0] <= x <= bo.button_pos(0)[0]+button_width and bo.button_pos(0)[1]<y<bo.button_pos(0)[1]+button_height:
                        difficulty_flag=30
                    elif bo.button_pos(1)[0] <= x <= bo.button_pos(1)[0]+button_width and bo.button_pos(1)[1]<y<bo.button_pos(1)[1]+button_height:
                        difficulty_flag=40
                    elif bo.button_pos(2)[0] <= x <= bo.button_pos(2)[0]+button_width and bo.button_pos(2)[1]<y<bo.button_pos(2)[1]+button_height:
                        difficulty_flag=50
                    #if player click anywhere else, ignore and skip to next player event
                    else:
                        continue
                    #initialize the grid base on selected difficulty
                    method.fill_grid(grid)
                    ans_grid = [[grid[i][j] for j in range(len(grid[0]))]for i in range(len(grid))]
                    print(ans_grid)
                    method.remove_cell(difficulty_flag,grid)
                    #create a copy of grid that is used for comparison later
                    copy_grid = [[grid[i][j] for j in range(len(grid[0]))]for i in range(len(grid))]
                    '''
                    #debug line
                    copy_grid = ans_grid
                    '''
                    screen.fill(background_color)
                    start_time = time.time()
                    #initiate the board and sudoku game
                    bo.draw_board(screen,bo.grid,status,0)
                    pygame.display.update()
        #start           
        playtime = round(time.time() - start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                running = False
            if status!=2 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                #print(f"clicked position {pos}")
                status,clicked = click(pos,screen)
                #update select base after clicking
                if clicked is not None:
                    select = True
                else:
                    select = False
            elif status==2 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                difficulty_flag = 0
                status = 0
                break
            if event.type == pygame.KEYDOWN:
                if 0<= event.key-48 <=9 and select:
                    copy_grid,status = bo.insert(clicked[0],clicked[1],copy_grid,event.key-48)
                    #deselect once insertion is done            
                    select = False
                elif event.key == pygame.K_SPACE:
                    if check_win(screen,ans_grid,copy_grid):
                        status = 2
                        grid = [[0 for _ in range(bo.row)]for _ in range(bo.column)] 
                        print(f"current grid is {grid}") 
                    else:
                        status = 3
                    select = False
                else:
                    #any other keydown should be invalid input
                    status = 1
                    #de-select
                    select = False
        if difficulty_flag != 0:
        #continously draw the updated board
            bo.draw_board(screen,copy_grid,status,playtime)
            if select:
                selected(screen,clicked[1],clicked[0])
        pygame.display.update()

    #method.fill_grid(grid)

main(bo.grid)



