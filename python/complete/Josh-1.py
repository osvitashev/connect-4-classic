#CHECKLIST

'''
- Must create interactable game
- Must check for wins and losses
- AI!
'''

import sys

print(f"Python version: {sys.version}")
print(f"Major version: {sys.version_info.major}")
print(f"Minor version: {sys.version_info.minor}")
print(f"Micro version: {sys.version_info.micro}")

import easygui
import pygame
#Initialize
pygame.init()

HORIZONTAL_SPACES = 7 #7 x 6 grid
VERTICAL_SPACES = 6
size_of_spaces = 100

consecutive_circles_to_win = 4

checker_size = 9/10

#positional_score = [[0 for x in range(HORIZONTAL_SPACES)] for x in range(VERTICAL_SPACES)]
POSITIONAL_SCORE = [
    [3, 4, 5, 7, 5, 4, 3],  # Row 0 (top)
    [4, 6, 8, 10, 8, 6, 4], # Row 1
    [5, 8, 10, 12, 10, 8, 5], # Row 2
    [5, 8, 10, 12, 10, 8, 5], # Row 3 (middle row)
    [4, 6, 8, 10, 8, 6, 4],  # Row 4
    [3, 4, 5, 7, 5, 4, 3]   # Row 5 (bottom)
]
POSITIONAL_SCORE = [[-y for y in POSITIONAL_SCORE[x]] for x in range (len(POSITIONAL_SCORE))] #Not sure why but the computer prefers the lowest possible value, thus I made every value negative.

#For debugging
#POSITIONAL_SCORE = [[1,3,1], [4,6,4], [3,4,3]]

# Screen
WIDTH = size_of_spaces*HORIZONTAL_SPACES
HEIGHT = size_of_spaces * VERTICAL_SPACES
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #7 x 6 grid

BACKGROUND_COLOR = (42,136,179)

pygame.display.set_caption("Connect Four")

#Variables
flag = True  #Main loop condition

line_width = 5 #The width of the lines drawn to make the grid

#Positions:
positions = {} #Positions will be stored as {(x,y): "player"}

#Possible moves for the computer
possible_moves = () #Tuples appended in values of horizontal spaces E.g. [0,0,0,0,0,0,0,0] => [0,0,0,0,0,0,0,0] * horizontal spaces

#Turns
#Determines who goes first human is 1 and computer is -1
turn = -1

#Winner
winner = (False, 0)

#Player Colors
P1_COLOR = (255,0,0) #RED
P2_COLOR = (255,255,0) #YELLOW

#Max depth the algorithm should check until
MAX_DEPTH = 7

AGAINST_AI = True

class Computer:
    def __init__(self):
        self.computer_moves = []
        self.player_moves = []
    
    def possible_moves(self,positions, HORIZONTAL_SPACES, VERTICAL_SPACES) -> list[tuple[int,int]]:
        possible_moves = []

        for x_pos in range(HORIZONTAL_SPACES): #Iterate through each possible x position
            if is_valid_placement(positions, x_pos):
                y_pos = VERTICAL_SPACES - 1 #Start at the bottom of the grid

                while (x_pos, y_pos) in positions:
                    if y_pos >= 1:
                        y_pos -= 1
                    
                    else:
                        break

                if y_pos >= 1: #The bottom of the grid is y=1 not y=0
                    possible_moves.append((x_pos, y_pos))
        
        return possible_moves
    
    
    def evaluate_board(self, positions, POSITIONAL_SCORE, HORIZONTAL_SPACES, VERTICAL_SPACES) -> int:
        evaluation = 0
        #Iterate through each circle
        for x in range(HORIZONTAL_SPACES):
            for y in range(VERTICAL_SPACES):

                if (x,y) in positions: #If the current circle is in possible positions
                    player = positions[(x,y)] #Indexing the dictionary of positions to get the player

                    if player == 1:
                        evaluation += POSITIONAL_SCORE[y][x]
                    
                    elif player == -1:
                        evaluation -= POSITIONAL_SCORE[y][x]  
                    
                    ''' MAKES IT WORSE FOR SOME REASON.
                    in_a_row = 1

                    #Checks every tile for possible connections (e.g. 2 in a row, or 3 in a row and updates the evaluation)
                    valuations = [check_horizontal(positions, consecutive_circles_to_win, in_a_row, (x,y), player), 
                                check_vertical(positions, consecutive_circles_to_win, in_a_row, (x,y), player), 
                                check_top_right_diag(positions, consecutive_circles_to_win, in_a_row, (x,y), player), 
                                check_top_left_diag(positions, consecutive_circles_to_win, in_a_row, (x,y), player)]
                    
                    for value in valuations:
                        if value == 2:
                            evaluation += 5 *player
                        
                        elif value == 3:
                            evaluation += 20 *player
                            '''

        return evaluation

    def minimax(self, positions, winner, maximizingPlayer, MAX_DEPTH, POSITIONAL_SCORE, HORIZONTAL_SPACES, VERTICAL_SPACES, alpha, beta):
        
        valid_moves = self.possible_moves(positions, HORIZONTAL_SPACES, VERTICAL_SPACES) #Checking each of the candidate moves
        winner = check_winner(positions, consecutive_circles_to_win, winner) #Checks if a winner has been found

        if MAX_DEPTH == 0: #If the algorithm has finished analyzing
            return None, self.evaluate_board(positions, POSITIONAL_SCORE, HORIZONTAL_SPACES, VERTICAL_SPACES)

        if winner[0]:
            if winner[1] == 1: #Player wins
                return None, -1000
            
            elif winner[1] == -1: #Computer wins
                return None, 1000

            elif winner[1] == 0: #Draw
                return None, 0

        if maximizingPlayer: #Computer's turn (Trying to maximize score)
            value = -float('inf') #Start at the lowest possible evaluation
            best_move = None
            
            for move in valid_moves:

                #Pretend the move occurs
                new_positions = positions.copy()

                new_positions.update({move:-1})

                #Evaluate this position

                _, evaluation = self.minimax(new_positions, winner, False, MAX_DEPTH-1, POSITIONAL_SCORE, HORIZONTAL_SPACES, VERTICAL_SPACES, alpha, beta) #Check each daughter node before evaluating

                if evaluation > value:
                    value = evaluation
                    best_move = move
            
                #Alpha is the best overall move
                alpha = max(value, alpha)

                if alpha >= beta:
                    break
            return best_move, value
        
        elif not(maximizingPlayer): #Player's turn (Trying to minimize score)
            value = float('inf') #Start at the highest possible evaluation

            for move in valid_moves:

                #Pretend the move occurs
                new_positions = positions.copy()

                new_positions.update({move:1})

                #Evaluate this position

                _, evaluation = self.minimax(new_positions, winner, True, MAX_DEPTH-1, POSITIONAL_SCORE, HORIZONTAL_SPACES, VERTICAL_SPACES, alpha, beta)

                if evaluation < value:
                    value = evaluation
                    best_move = move
                
                beta = min(value, beta)
                if alpha >= beta:
                    break

            return best_move, value

    def play_move(self, positions, turn, best_move):
        positions.update({best_move: turn})

        turn = switch_turn(turn)
        
        return positions, turn
                
def close_window(flag):
    flag = False
    return flag 

def draw_window(screen, BACKGROUND_COLOR):
    screen.fill(BACKGROUND_COLOR)

def draw_grid(WIDTH, HEIGHT, screen, line_width, HORIZONTAL_SPACES, VERTICAL_SPACES, size_of_spaces):
    for x in range(HORIZONTAL_SPACES): #Lines draw vertically, from 0 to WIDTH
        x_pos = x*(WIDTH/HORIZONTAL_SPACES) #Starts at 0, ends at WIDTH
        pygame.draw.line(screen, (0,0,0), (x_pos, 0), (x_pos, HEIGHT), line_width)
    
    for y in range(VERTICAL_SPACES):
        y_pos = y*(HEIGHT/VERTICAL_SPACES)
        pygame.draw.line(screen, (0,0,0), (0, y_pos), (WIDTH, y_pos), line_width)


def choose_position(size_of_spaces, positions, turn, VERTICAL_SPACES) -> list[dict, int]:
    mouse_x = pygame.mouse.get_pos()[0] #Only the x coordinate of the mouse is needed
        
    x_pos = mouse_x//size_of_spaces
    y_pos = VERTICAL_SPACES-1 #Must pick the bottom-most tile

    if is_valid_placement(positions, x_pos):
        
        while (x_pos, y_pos) in positions:
            if y_pos >= 1:
                y_pos -= 1
            else:
                print("Pick another tile!")  #Skips the rest of the function
                return positions, turn

        positions.update({(x_pos, y_pos): turn})

        turn = switch_turn(turn)
        
        return positions, turn
    
    else:
        print("Invalid placement")
        return positions, turn

def is_valid_placement(positions, x_pos):
    return (x_pos, 0) not in positions

def switch_turn(turn):
    if turn == 1: #Switches the players turn
        turn = -1
    
    elif turn == -1:
        turn = 1
    
    return turn

def draw_positions(positions, P1_COLOR, P2_COLOR, checker_size) -> tuple[bool, int]:
    for k,v in positions.items(): #Positions stored as {(x,y):turn}
        try:
            x = k[0] 
            y = k[1]
        except:
            print(k)

        center_of_circle = ((x*size_of_spaces)+ size_of_spaces/2, (y*size_of_spaces) + size_of_spaces/2) #Getting the center of the circle
        
        if v == 1:
            pygame.draw.circle(screen, P1_COLOR, center_of_circle, size_of_spaces*(1/2)*checker_size) #Drawn slightly smaller for visual effect
        elif v == -1:
            pygame.draw.circle(screen, P2_COLOR, center_of_circle, size_of_spaces*(1/2)*checker_size)

def check_horizontal(positions, consecutive_circles_to_win, in_a_row, k, v):
    #Check forwards (horizontally)
    for x in range(1, consecutive_circles_to_win):
        if (k[0] +x, k[1]) in positions and positions[k[0] +x, k[1]] == v:
            in_a_row += 1
        else:
            break
    
    #Checking backwards (horizontally)
    for x in range(1, consecutive_circles_to_win):
        if (k[0] - x, k[1]) in positions and positions[k[0] - x, k[1]] == v:
            in_a_row += 1
        else:
            break
            
    return in_a_row

def check_vertical(positions, consecutive_circles_to_win, in_a_row, k, v):
    #Check from top to bottom
    for x in range(1, consecutive_circles_to_win):
        if (k[0], k[1]-x) in positions and positions[k[0], k[1]-x] == v:
            in_a_row += 1
        else:
            break
    return in_a_row

def check_top_right_diag(positions, consecutive_circles_to_win, in_a_row, k, v):
    for x in range(1, consecutive_circles_to_win): #Checking diagonally, right upwards
        if (k[0] +x, k[1]+x) in positions and positions[k[0] +x, k[1]+x] == v:
            in_a_row += 1
        else:
            break
    
    for x in range(1, consecutive_circles_to_win):
        if (k[0] -x, k[1]-x) in positions and positions[k[0] -x, k[1]-x] == v:
            in_a_row += 1
        else:
            break
        
    return in_a_row

def check_top_left_diag(positions, consecutive_circles_to_win, in_a_row, k, v):
    for x in range(1, consecutive_circles_to_win): #Checking diagonally, right upwards
        if (k[0] -x, k[1]+x) in positions and positions[k[0] -x, k[1]+x] == v:
            in_a_row += 1
        else:
            break
    
    for x in range(1, consecutive_circles_to_win):
        if (k[0] +x, k[1]-x) in positions and positions[k[0] +x, k[1]-x] == v:
            in_a_row += 1
        else:
            break

    return in_a_row

def check_winner(positions, consecutive_circles_to_win, winner):
    #There is a winner if they get four in a row, either vertically, horizontally, or diagonally.
    
    #Stored as (True, player)
    
    in_a_row = 1 #Starts at 1 since we're including the starting circle

    for k,v in positions.items():
        if k is not None:

            if consecutive_circles_to_win in [
                                            check_horizontal(positions, consecutive_circles_to_win, in_a_row, k, v), 
                                            check_vertical(positions, consecutive_circles_to_win, in_a_row, k, v), 
                                            check_top_right_diag(positions, consecutive_circles_to_win, in_a_row, k, v), 
                                            check_top_left_diag(positions, consecutive_circles_to_win, in_a_row, k, v)
                                            ]:
                winner = (True, v)
                break


            elif len(positions) == HORIZONTAL_SPACES*VERTICAL_SPACES:
                    winner = (True, 0)


            else:
                winner = (False, 0)

    return winner

def end_game(screen, BACKGROUND_COLOR, WIDTH, HEIGHT, line_width, HORIZONTAL_SPACES, VERTICAL_SPACES, size_of_spaces, positions, P1_COLOR, P2_COLOR, checker_size, winner):
    draw_window(screen, BACKGROUND_COLOR) #Draws the screen

    draw_grid(WIDTH, HEIGHT, screen, line_width, HORIZONTAL_SPACES, VERTICAL_SPACES, size_of_spaces) #Draws the grid for the connect 4 board

    draw_positions(positions, P1_COLOR, P2_COLOR, checker_size)
    pygame.display.flip()

    easygui.msgbox(f"Player {winner[1]} has won the game!", title="Computer says...")
    
    if winner[1] == -1:
        easygui.msgbox("YOU HAVE FAILED", title="Computer says...")

    elif winner[1] == 1:
        easygui.msgbox(f"YAAAYYYYYYYYYYYYY", title="Computer says...")


if AGAINST_AI:
    computer = Computer()

print("\n")
print("\n")
easygui.msgbox("In all board games, there is one that differentiates itself from the rest. \nOne that requires a higher intellect.\nA game of pure skill, where strategy and foresight are the only weapons.\nA battle of wits, where each move is calculated, each decision weighed with precision.\nNo luck, no randomness, only mastery of the mind.\nA game that separates the casual player from the true champion.\nIt is a game where every action counts, every moment is crucial, and victory is earned through perseverance and brilliance.", title="Introduction")
print("\n")
pygame.time.wait(1000)
easygui.msgbox("USER! I challenge you to a game of Connect 4!", title="Computer says...")
pygame.time.wait(1000)
response = easygui.buttonbox("Do you accept?", title = "Computer says...", choices = ["Yes", "Yes", "Yes"])

if response == None:
    easygui.msgbox("You think you're clever huh?", title="Computer says...")

flag = True

if flag:
    print("\n")

    print("Very well then... Too late to back out now...")

#Loop
while flag:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            easygui.msgbox("YOU MAY NOT CLOSE THE GAME", title="Computer says...")
            #flag = close_window(flag) #Closes the loop

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            values = choose_position(size_of_spaces, positions, turn, VERTICAL_SPACES) #Updates the dictionary with all the positions

            positions = values[0]
            turn = values[1] #Switches the turn

            winner = check_winner(positions, consecutive_circles_to_win, winner)  #Checks if the position is winning for a player

            if winner[0]:
                flag = close_window(flag)
                end_game(screen, BACKGROUND_COLOR, WIDTH, HEIGHT, line_width, HORIZONTAL_SPACES, VERTICAL_SPACES, size_of_spaces, positions, P1_COLOR, P2_COLOR, checker_size, winner)
                break
        

    if AGAINST_AI and flag:
        if turn == -1: 
            draw_positions(positions, P1_COLOR, P2_COLOR, checker_size) #Minimax takes a while so it is worth it to update screen beforehand
            pygame.display.flip()
            best_move, _ = computer.minimax(positions, winner, True, MAX_DEPTH, POSITIONAL_SCORE, HORIZONTAL_SPACES, VERTICAL_SPACES, -float("inf"), float("inf"))
            positions, turn = computer.play_move(positions, turn, best_move)
            
            winner = check_winner(positions, consecutive_circles_to_win, winner)  #Checks if the position is winning for a player

            print(positions)

            if winner[0]:
                flag = close_window(flag)
                end_game(screen, BACKGROUND_COLOR, WIDTH, HEIGHT, line_width, HORIZONTAL_SPACES, VERTICAL_SPACES, size_of_spaces, positions, P1_COLOR, P2_COLOR, checker_size, winner)
                break


    draw_window(screen, BACKGROUND_COLOR) #Draws the screen

    draw_grid(WIDTH, HEIGHT, screen, line_width, HORIZONTAL_SPACES, VERTICAL_SPACES, size_of_spaces) #Draws the grid for the connect 4 board

    draw_positions(positions, P1_COLOR, P2_COLOR, checker_size) #Draws the different positions from the board

    pygame.display.flip() #Updates the screen


if not flag:
    print(positions) #Updates the screen
    pygame.time.wait(1000)
    response = easygui.buttonbox("Would you like to try again?", title = "Computer says...", choices = ["No", "No", "No"])
    pygame.quit()
 