# Creating Chess game 
#Author Devansh Kaushik
import pygame as pg

pg.init()

#display and time 
WIDTH = 900
HEIGHT = 700
screen = pg.display.set_mode((WIDTH,HEIGHT))
font_b = pg.font.Font('freesansbold.ttf',10)
font_b = pg.font.Font('freesansbold.ttf',20)
timer = pg.time.Clock()
fps = 60

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
s_size = 25

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
            pg.draw.rect(screen,(255,255,255),[pos_x,pos_y,sq_size,sq_size])
        else:
            pos_x = col*160 + 80
            pos_y = row*80
            pg.draw.rect(screen,(255,255,255),[pos_x,pos_y,sq_size,sq_size])
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
                pg.draw.rect(screen,(249, 219, 186),[w_locations[i][0]*80,w_locations[i][1]*80,80,80])
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
        

#Game Loop
run = True
while run:
    timer.tick(fps)
    screen.fill((81,37,243))
    
    draw_board()
    draw_pieces()
    # handling the events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button== 1:
            pos_x = event.pos[0] // 80
            pos_y = event.pos[1] // 80 

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

    # updating the display
    # here the diff b/w "flip" and "update" is flip updates complete display but "update" does specific part
    pg.display.flip()
pg.quit()