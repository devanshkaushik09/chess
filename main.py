# Creating Chess game 
#Author Devansh Kaushik
import pygame as pg

pg.init()

#display and time 
WIDTH = 900
HEIGHT = 700
screen = pg.display.set_mode((WIDTH,HEIGHT))
font_big = pg.font.Font('freesansbold.ttf',40)
font_b = pg.font.Font('freesansbold.ttf',20)
timer = pg.time.Clock()
fps = 60

#Color Themes
dark_check = 	[(147,196,125),	(41,134,204),(81,37,243)] 
light_check =   [(255,255,255)]
hglt_color =    [(249, 219, 186)]
color_valid_move = [(108,106,105)]
check_color = (205,92,92)


#title and icon
icon = pg.image.load('./assets/chessicon.png')
pg.display.set_icon(icon)
pg.display.set_caption('Chess Game')

# lists for pieces and their locations
w_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook'
            ,'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']

w_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)
               ,(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]


b_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook'
            ,'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']

b_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)
               ,(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]

# list for captured pieces
w_captured_pieces = []
b_captured_pieces = []

# sizes for scaling
norm_size = 70
s_size = 35

# some more variables that will be needed further
# 0 - w turn no selec, 1 - w turn selec, 2 - b turn no selec, 3 - b turn selec
selec_turn  = 0
selected_square = 100

valid_moves = []

# load the images of game pieces (rook,knight,bishop,queen,king,pawn) for w as well as b
b_king = pg.image.load('assets/b_king.png')
b_king = pg.transform.scale(b_king,(norm_size, norm_size))
b_king_s = pg.transform.scale(b_king,(s_size, s_size))

b_queen = pg.image.load('assets/b_queen.png')
b_queen = pg.transform.scale(b_queen,(norm_size, norm_size))
b_queen_s = pg.transform.scale(b_queen,(s_size, s_size))

b_rook = pg.image.load('assets/b_rook.png')
b_rook = pg.transform.scale(b_rook,(norm_size, norm_size))
b_rook_s = pg.transform.scale(b_rook,(s_size, s_size))
                          
b_bishop = pg.image.load('assets/b_bishop.png')
b_bishop = pg.transform.scale(b_bishop,(norm_size, norm_size))
b_bishop_s = pg.transform.scale(b_bishop,(s_size, s_size))

b_knight = pg.image.load('assets/b_knight.png')
b_knight = pg.transform.scale(b_knight,(norm_size, norm_size))
b_knight_s = pg.transform.scale(b_knight,(s_size, s_size))   

b_pawn = pg.image.load('assets/b_pawn.png')
b_pawn = pg.transform.scale(b_pawn,(norm_size, norm_size))
b_pawn_s = pg.transform.scale(b_pawn,(s_size, s_size))

w_king = pg.image.load('assets/w_king.png')
w_king = pg.transform.scale(w_king,(norm_size, norm_size))
w_king_s = pg.transform.scale(w_king,(s_size, s_size))

w_queen = pg.image.load('assets/w_queen.png')
w_queen = pg.transform.scale(w_queen,(norm_size, norm_size))
w_queen_s = pg.transform.scale(w_queen,(s_size, s_size))

w_rook = pg.image.load('assets/w_rook.png')
w_rook = pg.transform.scale(w_rook,(norm_size, norm_size))
w_rook_s = pg.transform.scale(w_rook,(s_size, s_size))

w_bishop = pg.image.load('assets/w_bishop.png')
w_bishop = pg.transform.scale(w_bishop,(norm_size, norm_size))
w_bishop_s = pg.transform.scale(w_bishop,(s_size, s_size))

w_knight = pg.image.load('assets/w_knight.png')
w_knight = pg.transform.scale(w_knight,(norm_size, norm_size))
w_knight_s = pg.transform.scale(w_knight,(s_size, s_size))

w_pawn = pg.image.load('assets/w_pawn.png')
w_pawn = pg.transform.scale(w_pawn,(norm_size, norm_size))
w_pawn_s = pg.transform.scale(w_pawn,(s_size, s_size))

# some more lists for simplification of piece image access
w_images = [w_pawn,w_queen,w_king,w_knight,w_rook,w_bishop]
s_w_images = [w_pawn_s,w_queen_s,w_king_s,w_knight_s,w_rook_s,w_bishop_s]

b_images = [b_pawn,b_queen,b_king,b_knight,b_rook,b_bishop]
s_b_images = [b_pawn_s,b_queen_s,b_king_s,b_knight_s,b_rook_s,b_bishop_s]

index_list = ['pawn','queen','king','knight','rook','bishop']


#drawing the checker board
def draw_board():
    sq_size = 80
    for i in range(32):
        row = i//4
        col = i%4
        if(row%2 == 0):
            pos_x = col*160
            pos_y = row*80
            pg.draw.rect(screen,light_check[0],[pos_x,pos_y,sq_size,sq_size])
        else:
            pos_x = col*160 + 80
            pos_y = row*80
            pg.draw.rect(screen,light_check[0],[pos_x,pos_y,sq_size,sq_size])
        # horizontal box
        pg.draw.rect(screen,(194,189,132),[0,640,WIDTH,60])
        
        # vertical box
        pg.draw.rect(screen,(194,189,132),[640,0,260,HEIGHT])
        pg.draw.rect(screen,(0,0,0),[640,0,260,HEIGHT],3)
        pg.draw.rect(screen,(0,0,0),[0,640,WIDTH,60],3)
        
        selec_turn_text = ['White: Select a piece','White: Select the destination'
                           ,'Black: Select a piece','Black: Select the destination']
        screen.blit(font_b.render(selec_turn_text[selec_turn],True,'black'),(40,660))

#drawing the peices on the board along with highlightion effect            
def draw_pieces():
    
    offset = 5
    for i in range(len(w_pieces)):
        index = index_list.index(w_pieces[i])
        
        #first highlightion is drawn
        if(selec_turn < 2): #white turn
            if(selected_square == i):
                pg.draw.rect(screen,hglt_color[0],[w_locations[i][0]*80,w_locations[i][1]*80,80,80])
        #then piece is drawn       
        screen.blit(w_images[index],((w_locations[i][0]) * 80 + offset, (w_locations[i][1]) * 80+offset))
        
    for i in range(len(b_pieces)):
        index = index_list.index(b_pieces[i])
        
        #first highlightion is drawn
        if(selec_turn > 1): #black turn
            if(selected_square == i):
                pg.draw.rect(screen,(249, 219, 186),[b_locations[i][0]*80,b_locations[i][1]*80,80,80])
                
        #then piece is drawn       
        screen.blit(b_images[index],((b_locations[i][0]) * 80 + offset, (b_locations[i][1]) * 80+offset))

#drawing captured pieces on the board
def draw_captures():
    for i in range(len(w_captured_pieces)):
        cap_piece = w_captured_pieces[i]
        index = index_list.index(cap_piece)
        screen.blit(s_b_images[index],(700,8+30*i))
        
    for i in range(len(b_captured_pieces)):
        cap_piece = b_captured_pieces[i]
        index = index_list.index(cap_piece)
        screen.blit(s_w_images[index],(800,8+30*i))

#drawing the checks (if presents)
def draw_checks():
    
    if selec_turn < 2:
        if 'king' in w_pieces:
            index = w_pieces.index('king')
            loc = w_locations[index]
            for i in range(len(b_options)):
                if loc in b_options[i]:
                    pg.draw.rect(screen,check_color,[loc[0]*80,loc[1]*80,80,80])        
    else:
        if 'king' in b_pieces:
            index = b_pieces.index('king')
            loc = b_locations[index]
            for i in range(len(w_options)):
                if loc in w_options[i]:
                    pg.draw.rect(screen,check_color,[loc[0]*80,loc[1]*80,80,80])   
                 
#check valid moves for the selected piece
def check_valid_moves():
    if(selec_turn < 2):
        option_list = w_options
    else:
        option_list = b_options
    
    valid_options = option_list[selected_square]
    return valid_options  
            
#drawing valid moves on the screen
def draw_valids(valids):
    
    for i in range(len(valids)):
        pg.draw.circle(screen,color_valid_move[0],(valids[i][0] * 80 + 40,valids[i][1] * 80 + 40),12)
    
#Functions to check moves for each individual piece
#For Pawn
def check_pawn(position,color):
    moves_list = []
    
    if color is 'white':
        if (position[0],position[1] + 1) not in w_locations and \
            (position[0],position[1] + 1) not in b_locations and position[1] < 7:
            moves_list.append((position[0],position[1] + 1))
            
        if (position[0],position[1] + 2) not in w_locations and \
            (position[0],position[1] + 2) not in b_locations and position[1] == 1:
            moves_list.append((position[0],position[1] + 2))
        
        if (position[0] + 1,position[1] + 1) in b_locations:    
            moves_list.append((position[0] + 1,position[1] + 1))
            
        if (position[0] - 1, position[1] + 1) in b_locations:    
            moves_list.append((position[0] - 1,position[1] + 1))
    
    #color is black
    else:
        if (position[0],position[1] - 1) not in w_locations and \
            (position[0],position[1] - 1) not in b_locations and position[1] > 0:
            moves_list.append((position[0],position[1] - 1))
            
        if (position[0],position[1] - 2) not in w_locations and \
            (position[0],position[1] - 2) not in b_locations and position[1] == 6:
            moves_list.append((position[0],position[1] - 2))
        
        if (position[0] + 1,position[1] - 1) in w_locations:    
            moves_list.append((position[0] + 1,position[1] - 1))
            
        if (position[0] - 1, position[1] - 1) in w_locations:    
            moves_list.append((position[0] - 1,position[1] - 1))
           
    return moves_list    

#For Rook     
def check_rook(position,color):
    
    moves_list = []
    if color is 'white':
        enemy_locs = b_locations
        own_locs = w_locations
    else:
        own_locs = b_locations
        enemy_locs = w_locations
    for i in range(4): # for all four directions
        path = True
        chain = 1
        if(i == 0): #down
            x = 0 
            y = 1
        elif (i == 1): # up
            x = 0
            y = -1   
        elif (i == 2): #right
            x = 1
            y = 0   
        else: #left
            x = -1
            y = 0
        
        while path:
            if(position[0] + (chain * x),position[1] + (chain * y)) not in own_locs and \
                   0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7 :

                moves_list.append((position[0] + (chain * x),position[1] + (chain * y)))
                if(position[0] + (chain * x),position[1] + (chain * y)) in enemy_locs:
                    path = False
                chain += 1 
            else:
                path = False
    
    return moves_list

#For Knight
def check_knight(position,color):
    moves_list = []
    if color is 'white':
        enemy_locs = b_locations
        own_locs = w_locations
    else:
        own_locs = b_locations
        enemy_locs = w_locations
        
        
    # 8 squares for knight to move
    targets = [(1,2),(1,-2),(2,-1),(2,1),(-1,2),(-1,-2),(-2,1),(-2,-1)]
    
    for i in range(8):
        trgt = (position[0] + targets[i][0],position[1] + targets[i][1])
        if trgt not in own_locs and 0 <= trgt[0] <= 7 and 0 <= trgt[1] <= 7:
            moves_list.append(trgt)
            
            
    return moves_list

#For Bishop
def check_bishop(position,color):
     
    moves_list = []
    if color is 'white':
        enemy_locs = b_locations
        own_locs = w_locations
    else:
        own_locs = b_locations
        enemy_locs = w_locations
    for i in range(4): # for all four directions
        path = True
        chain = 1
        if(i == 0): #down right
            x = 1 
            y = 1
        elif (i == 1): # up right
            x = 1
            y = -1   
        elif (i == 2): #down left
            x = -1
            y = 1   
        else: #up left
            x = -1
            y = -1
        
        while path:
            if(position[0] + (chain * x),position[1] + (chain * y)) not in own_locs and \
                   0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7 :

                moves_list.append((position[0] + (chain * x),position[1] + (chain * y)))
                if(position[0] + (chain * x),position[1] + (chain * y)) in enemy_locs:
                    path = False
                chain += 1 
            else:
                path = False 
        
        
    return moves_list

#For Queen
def check_queen(position,color):
    moves_list = check_bishop(position,color)
    second_list = check_rook(position,color)
    
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

#For King
def check_king(position,color):
    
    moves_list = []
    if color is 'white':
        enemy_locs = b_locations
        own_locs = w_locations
    else:
        own_locs = b_locations
        enemy_locs = w_locations
        
    # 8 squares for king to move
    targets = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
    
    for i in range(8):
        trgt = (position[0] + targets[i][0],position[1] + targets[i][1])
        if trgt not in own_locs and 0 <= trgt[0] <= 7 and 0 <= trgt[1] <= 7:
            moves_list.append(trgt)
    
    return moves_list

#checking all the valid moves for a particular position
def check_options(pieces,locations,turn):
    
    moves_list = []
    
    list_of_all_moves = []
    
    for i in range(len(pieces)):
        loc = locations[i]
        piece = pieces[i]
        
        if piece is 'pawn':
            moves_list = check_pawn(loc,turn) 

        elif piece is 'knight':
            moves_list = check_knight(loc,turn) 
            
        elif piece is 'bishop':
            moves_list = check_bishop(loc,turn) 
        
        elif piece is 'rook':
            moves_list = check_rook(loc,turn) 
        
        elif piece is 'queen':
            moves_list = check_queen(loc,turn) 
        
        else:
            moves_list = check_king(loc,turn) 

        list_of_all_moves.append(moves_list)
    
    return list_of_all_moves
winner = ''
#Game Loop
b_options = check_options(b_pieces,b_locations,'black')
w_options = check_options(w_pieces,w_locations,'white')
run = True
while run:
    timer.tick(fps)
    screen.fill(dark_check[1])
    
    draw_board()
    draw_checks()
    draw_pieces()
    draw_captures()
    
    #drawing valid moves
    if selected_square != 100:
        valid_moves = check_valid_moves()
        draw_valids(valid_moves)
    
    # handling the events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button== 1:
            pos_x = event.pos[0] // 80
            pos_y = event.pos[1] // 80 

            if winner is '':
                click_pos = (pos_x,pos_y)
                if selec_turn < 2:
                    if click_pos in w_locations:
                        selected_square = w_locations.index(click_pos)
                        if selec_turn == 0:
                            selec_turn = 1
                    if click_pos in valid_moves and selected_square != 100:
                        w_locations[selected_square] = click_pos

                        #if it captures
                        if click_pos in b_locations:

                            index_of_b_piece = b_locations.index(click_pos)

                            #addind that captured piece to list
                            w_captured_pieces.append(b_pieces[index_of_b_piece])

                            #removing it from lists
                            b_locations.pop(index_of_b_piece)
                            b_pieces.pop(index_of_b_piece)
                        b_options = check_options(b_pieces,b_locations,'black')
                        w_options = check_options(w_pieces,w_locations,'white')

                        selec_turn = 2
                        selected_square = 100
                        valid_moves = []

                        #checkinng winner
                        if 'king' in w_captured_pieces:
                            winner = 'white'
                            
                #for black to move
                if selec_turn > 1:
                    if click_pos in b_locations:
                        selected_square = b_locations.index(click_pos)
                        if selec_turn == 2:
                            selec_turn = 3
                    if click_pos in valid_moves and selected_square != 100:
                        b_locations[selected_square] = click_pos

                        #if it captures
                        if click_pos in w_locations:

                            index_of_w_piece = w_locations.index(click_pos)

                            #addind that captured piece to list
                            b_captured_pieces.append(w_pieces[index_of_w_piece])

                            #removing it from lists
                            w_locations.pop(index_of_w_piece)
                            w_pieces.pop(index_of_w_piece)

                        w_options = check_options(w_pieces,w_locations,'white')
                        b_options = check_options(b_pieces,b_locations,'black')

                        selec_turn = 0
                        selected_square = 100
                        valid_moves = []

                        if 'king' in b_captured_pieces:
                            winner = 'black'
    if winner != '':                
        pg.draw.rect(screen,(dark_check[0]),[220,220,200,200])
        won_text = ['WHITE','WON']
        if winner is 'white':
            screen.blit(font_big.render(won_text[0],True,'white'),(255,260))
            screen.blit(font_big.render(won_text[1],True,'white'),(275,320))
        if winner is 'black':
            screen.blit(font_big.render("Black",True,'white'),(255,260))
            screen.blit(font_big.render(won_text[1],True,'white'),(275,320))
    # updating the display
    # here the diff b/w "flip" and "update" is flip updates complete display but "update" does specific part
    pg.display.flip()
pg.quit()