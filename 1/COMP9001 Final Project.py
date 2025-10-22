#COMP9001 final project Yuekai Wang
import pygame
import random
import math

#Production of the game's initial interface
pygame.init()
screen=pygame.display.set_mode((800,600)) #Set the size of the game window
pygame.display.set_caption('COMP9001 final project Yuekai Wang') #Set the game title
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

#Displays the player's score
def show_score():
    text = f"Score:{score}" #Set the player score in the upper left corner of the window
    score_render = font.render(text, True, (0,255,0)) #Set the font color to green
    screen.blit(score_render,(10,10)) #Set the position of the score display

#Game over
is_over = False
over_font = pygame.font.Font('freesansbold.ttf',64) #Set the font and size

#Setting the game end prompt message
def check_is_over():
    if is_over:
        text = "Game Over !" #Set the game end prompt message
        render = over_font.render(text, True, (255,0,0)) #Set the font color of Game Over to red
        screen.blit(render,(200,250)) #Set the display position of Game Over

number_of_enemies = 3  #Set the number of enemies

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
for i in range(number_of_enemies):  #Add Enemies
    enemies.append(Enemy())

def distance(bx,by,ex,ey): #Calculate the distance between the bullet and the enemy
    a = bx - ex #Subtract their horizontal coordinates
    b = by - ey
    return math.sqrt(a*a + b*b) #Calculate straight-line distance

class Bullet:
    def __init__(self):
        self.img = pygame.image.load('9001 bullet.png')
        self.x = playerX + 16 #Set the horizontal coordinate of the bullet to be linked to the player
        self.y = playerY + 10
        self.step = 10 #speed

      #Bullet hits the enemy
    def hit(self):
        global score #Referencing global variables

        for e in enemies:
            if distance(self.x, self.y, e.x, e.y)< 30:  #If the distance is less than 30, the bullet is considered to have hit the enemy.
                hit_sound.play() #Play music that hits an enemy
                bullets.remove(self) #Remove the bullet
                e.reset() #Calling the method to revive the enemy
                score = score + 1 #Each time you hit an enemy, your score increases by one.
                print(score)

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

        if event.type==pygame.QUIT:  #Exit the game
             running = False  #Terminate the loop

#Controlling player movement with the keyboard
        if event.type ==pygame.KEYDOWN: #Determine whether the user is using the keyboard

            if event.key == pygame.K_RIGHT: #Set the action of pressing the right arrow
                playerStep = 3 #speed Right is the positive direction

            elif event.key == pygame.K_LEFT: #Set the action of pressing the left arrow
                playerStep = -3 #speed

            elif event.key == pygame.K_SPACE: #Set the action of pressing the space bar
                print('Fire the bullet...')

                #Create a bullet
                bullets.append(Bullet())

        if event.type == pygame.KEYUP: #Set the action for releasing the keyboard
            playerStep = 0 #The player stops moving

    screen.blit(bgImg, (0, 0))  # Set the position of the background image
    screen.blit(playerImg,(playerX,playerY)) #Set the initial position of the player
    move_player() #Calling a function
    show_score()
    show_enemy()
    show_bullets()
    check_is_over()
    pygame.display.update()