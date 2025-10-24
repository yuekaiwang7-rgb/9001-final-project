#COMP9001 Final Project Yuekai Wang
import pygame
import random
import math

#Production of the game's initial interface
pygame.init()

#Difficulty set
DIFFICULTIES = {
    "EASY":   {"enemies": 3, "enemy_speed": (1, 2), "win_score": 5},
    "NORMAL": {"enemies": 5, "enemy_speed": (2, 3), "win_score": 10},
    "HARD":   {"enemies": 7, "enemy_speed": (3, 5), "win_score": 15},
}

current_mode = "NORMAL"
game_state   = "MENU"  #MENU / PLAYING

screen=pygame.display.set_mode((800,600)) #Set the size of the game window
pygame.display.set_caption('COMP9001 Final Project Yuekai Wang') #Set the game title
bgImg=pygame.image.load('9001 bg.png') #Import the game background image

#Add game background music
pygame.mixer.music.load('9001 bg.wav')
pygame.mixer.music.play(-1) #Make the game background music play in a loop

#Added music for hitting the enemy
hit_sound = pygame.mixer.Sound('9001 hit.wav')

#Set player
playerImg=pygame.image.load('9001 player.png')
playerX = 400 #Set the initial horizontal coordinate of the player
playerY = 500
playerStep =0 #Set the moving speed of the player

#Set the score
score = 0
font = pygame.font.Font('freesansbold.ttf',32) #Set the font and size
status_font = pygame.font.Font('freesansbold.ttf', 24)

#Displays the player's score
def show_score():
    text = f"Score:{score}" #Set the player score in the upper left corner of the window
    score_render = font.render(text, True, (0,255,0)) #Set the font color to green
    screen.blit(score_render,(10,10)) #Set the position of the score display

def show_status_bar():
    #Display current mode and target score
    text = f"Mode: {current_mode}   Target: {target_score}"
    render = status_font.render(text, True, (255, 255, 255))
    screen.blit(render, (10, 46))

#Menu screen function
menu_title_font = pygame.font.Font('freesansbold.ttf', 40)
menu_font = pygame.font.Font('freesansbold.ttf', 28)

def draw_menu():
    # Draw the background image
    screen.blit(bgImg, (0, 0))

    #title
    t1 = menu_title_font.render("Select Difficulty", True, (255, 255, 0))
    screen.blit(t1, (220, 180))

    #choose difficulty
    t2 = menu_font.render("1: EASY   2: NORMAL   3: HARD", True, (255, 255, 255))
    screen.blit(t2, (180, 250))

    #current choice
    t3 = menu_font.render(f"Current: {current_mode}", True, (180, 255, 200))
    screen.blit(t3, (280, 300))

    #Prompt text
    t4 = menu_font.render("Press ENTER to Start", True, (255, 255, 255))
    screen.blit(t4, (250, 360))

#Game over
is_over = False
is_win = False
target_score = 0
over_font = pygame.font.Font('freesansbold.ttf',64) #Set the font and size

#Setting the game end prompt message
def check_is_over():
    if is_over:
        text = "Game Over !" #Set the game end prompt message
        render = over_font.render(text, True, (255,0,0)) #Set the font color of Game Over to red
        screen.blit(render,(200,250)) #Set the display position of Game Over

number_of_enemies = 0  #Set the number of enemies

#Creating the Enemy Class
class Enemy:
    def __init__(self):
        self.img = pygame.image.load('9001 enemy.png') #Import enemy images
        self.x = random.randint(0,600) #Set the enemy's random horizontal coordinate
        self.y = random.randint(50,250) #Set the enemy's random vertical coordinate
        self.step = random.randint(1,2) #random speed

    #When an enemy is hit, reset his position and revive him
    def reset(self):
        self.x = random.randint(200,600) #The resurrection position of the hit enemy Random horizontal coordinate
        self.y = random.randint(50,200)

enemies = [] #Save all enemies

def distance(bx,by,ex,ey): #Calculate the distance between the bullet and the enemy
    a = bx - ex #Subtract their horizontal coordinates
    b = by - ey
    return math.sqrt(a*a + b*b) #Calculate straight-line distance

def start_game():
    #Resets a game based on current_mode: enemy count and speed from DIFFICULTIES.
    global enemies, bullets, score, is_over, number_of_enemies, is_win, target_score

    cfg = DIFFICULTIES[current_mode]
    number_of_enemies = cfg["enemies"]

    #Clear old state
    score = 0
    is_over = False
    is_win = False
    target_score = cfg["win_score"]
    bullets.clear()
    enemies.clear()

    #Respawns enemies at random speeds within a given range.
    lo, hi = cfg["enemy_speed"]
    for _ in range(number_of_enemies):
        e = Enemy()
        e.step = random.randint(lo, hi)
        e.x = random.randint(0, 600)
        e.y = random.randint(50, 250)
        enemies.append(e)

class Bullet:
    def __init__(self):
        self.img = pygame.image.load('9001 bullet.png')
        self.x = playerX + 16 #Set the horizontal coordinate of the bullet to be linked to the player
        self.y = playerY + 10
        self.step = 10 #speed

    #Bullet hits the enemy
    def hit(self):
        global score, is_win, target_score #Referencing global variables

        for e in enemies:
            if distance(self.x, self.y, e.x, e.y)< 30:  #If the distance is less than 30, the bullet is considered to have hit the enemy.
                hit_sound.play() #Play music that hits an enemy
                bullets.remove(self) #Remove the bullet
                e.reset() #Calling the method to revive the enemy
                score = score + 1 #Each time you hit an enemy, your score increases by one.
                print(score)

                if score >= target_score: #win
                    is_win = True
                    enemies.clear()
                return True
        return False

bullets = [] #Save existing bullets

#Bullet display and movement
def show_bullets():
    for b in bullets:
        screen.blit(b.img,(b.x,b.y)) #Set the bullet's position
        b.hit()  #Call the function for the bullet to hit the attack object
        b.y =  b.y - b.step #Set the movement of the bullet

        if b.y < 0:  #If the bullet's position exceeds the boundaries of the game window
            bullets.remove(b) #Remove Bullet

#Display the enemy and move it up, down, left and right
def show_enemy():
    global is_over #Calling global variables

    for e in enemies:
        screen.blit(e.img,(e.x,e.y)) #Set the enemy's position
        e.x = e.x +e.step #Set the enemy's movement

        if e.x > 736 or e.x <0: #Control the enemy's movement in the display window
            e.step = e.step * -1 #The enemy moves laterally in the opposite direction
            e.y = e.y +40 #Enemy moves down

            if e.y > 420 : #Set the conditions for the game to end. Player failure
                is_over = True
                print("Game Over!")
                enemies.clear() #Clear the enemy

def move_player(): #Set the player's movement
    global playerX #Calling global variables
    playerX =  playerX + playerStep

 #Control the player to keep moving in the game window interface
    if playerX > 736:  #right
        playerX = 736

    if playerX < 0:  # left
        playerX = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Exit the game
            running = False  # Terminate the loop
            break

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            break

        #When Game Over: Only receive R/M
        if is_over or is_win:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    is_over = False
                    is_win = False
                    start_game()  #Restart current difficulty
                    game_state = "PLAYING"

                elif event.key == pygame.K_m:
                    is_over = False
                    is_win = False
                    bullets.clear()
                    enemies.clear()
                    game_state = "MENU"  #Return to the menu and reselect the difficulty
            continue  #Eat other events to prevent movement/firing

        #Key controls in MENU mode
        if game_state == "MENU":

            if event.type == pygame.KEYDOWN:

                #player choose difficulty
                if event.key == pygame.K_1:
                    current_mode = "EASY"

                elif event.key == pygame.K_2:
                    current_mode = "NORMAL"

                elif event.key == pygame.K_3:
                    current_mode = "HARD"

                #use return to start the game
                elif event.key == pygame.K_RETURN:
                    start_game()  #Initialize a game
                    game_state = "PLAYING"  #Enter the game state
            continue  #Do not handle other events below (such as shooting, moving)

        #Controlling player movement with the keyboard
        if event.type ==pygame.KEYDOWN: #Determine whether the user is using the keyboard

            if event.key == pygame.K_RIGHT: #Set the action of pressing the right arrow
                playerStep = 3 #speed Right is the positive direction

            elif event.key == pygame.K_LEFT: #Set the action of pressing the left arrow
                playerStep = -3 #speed

            elif event.key == pygame.K_SPACE: #Set the action of pressing the space bar
                print('Fire the bullet...')

                bullets.append(Bullet())

        if event.type == pygame.KEYUP: #Set the action for releasing the keyboard
            playerStep = 0 #The player stops moving

    #menu state
    if game_state == "MENU":
        draw_menu()
        pygame.display.update()
        continue

    screen.blit(bgImg, (0, 0))  # Set the position of the background image
    screen.blit(playerImg,(playerX,playerY)) #Set the initial position of the player
    move_player() #Calling a function
    show_score()
    show_status_bar()
    show_enemy()
    show_bullets()
    check_is_over()

    if is_over:
        tip = font.render("Press R to Retry   |   Press M for Menu", True, (255, 255, 255))
        screen.blit(tip, (120, 330))
        pygame.display.update()
        continue

    if is_win:
        win_text = over_font.render("You Win!", True, (255, 0, 0))
        screen.blit(win_text, (240, 250))
        tip = font.render("Press R to Retry   |   Press M for Menu", True, (255, 255, 255))
        screen.blit(tip, (120, 330))
        pygame.display.update()
        continue

    pygame.display.update()