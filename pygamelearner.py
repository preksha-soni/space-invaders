import pygame
import random
import numpy as np
import math
import sys
from pygame import mixer

pygame.init() #initialise the pygame
screen=pygame.display.set_mode((500,500)) #to determine the size of the screen
pygame.display.set_caption("space invader")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
background=pygame.image.load("background.jpg")
playerimg=pygame.image.load("spaceship.png")
enemyimg=[]
enemyx=[]
enemyy=[]
num_of_enemies=6
playerx=225
playery=400
playerx_change=0
enemyx_change=[]
enemyy_change=[]
bulletimg=pygame.image.load("bullet.png")
bulletx=0
bullety=430
bulletx_change=0
bullety_change=0.5
bullet_state="ready"
score=0
font=pygame.font.Font("freesansbold.ttf",32)
textx=10
texty=10
over=pygame.font.Font("freesansbold.ttf",62)
written=pygame.font.Font(None,32)

def show():
     val=font.render("score:"+str(score),True,(255,255,255))
     screen.blit(val,(textx,texty))

def player():
    screen.blit(playerimg,(playerx,playery))

def enemy(enemyx,enemyy,i):
     screen.blit(enemyimg[i],(enemyx,enemyy))

def fire(x,y):
     global bullet_state
     bullet_state="fire"
     screen.blit(bulletimg,(x,y))

def collision(enemyx,enemyy,bulletx,bullety):
     distance=math.sqrt((math.pow(enemyx-bulletx,2))+(math.pow(enemyy-bullety,2)))
     if distance<5:
          return True
     else:
          return False

def draw_button(text,x,y,w,h,color):
     pygame.draw.rect(screen,color,(x,y,w,h))
     txt=written.render(text,True,(0,0,0))
     screen.blit(txt,(x,y))
     return pygame.Rect(x,y,w,h)

def game_over():
     overg= over.render("GAME OVER",True,(255,255,255))
     screen.blit(overg,(50,220))
     button()
     pygame.display.update()
       

def button():
      while True:
          
          play_button= draw_button("Play Again",200,320,200,50,(255,255,255))
          quit_button=draw_button("Exit",200,400,200,50,(255,255,255))
          for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                         pygame.quit()
                         sys.exit()
                    if event.type==pygame.MOUSEBUTTONDOWN:
                         if play_button.collidepoint(event.pos):
                              reset_game()
                              return

                         elif quit_button.collidepoint(event.pos):
                              pygame.quit()
                              return
          
          pygame.display.update()

def reset_game():
     pygame.display.flip()
     global playerx, bullety, bulletx, bullet_state
     global enemyimg, enemyx,enemyy,enemyx_change,enemyy_change,num_of_enemies

     playerx=225
     bullety=430
     bullet_state="ready"
     enemyimg.clear()
     enemyx.clear()
     enemyy.clear()
     enemyx_change.clear()
     enemyy_change.clear()
     __init__enemy()

def __init__enemy():
     for i in range(num_of_enemies):
          enemyimg.append(pygame.image.load("ghost.png"))
          enemyx.append(random.randint(0,430))
          enemyy.append(random.randint(50,250))
          enemyx_change.append(0.1)
          enemyy_change.append(50)

__init__enemy()

running=True

while running:
    screen.fill((0,0,0)) #for background color....rgb  
    screen.blit(background,(0,0)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerx_change=0.2
            if event.key == pygame.K_LEFT:
                playerx_change= -0.2
            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                     bullet_sound=mixer.Sound("laser.wav")
                     bullet_sound.play()
                     bulletx=playerx
                     fire(bulletx,bullety)
        if event.type==pygame.KEYUP:
             if event.key == pygame.K_RIGHT or  event.key == pygame.K_LEFT:
                 playerx_change=0
        
    playerx+= playerx_change 

    if playerx >= 430:
            playerx=430
    if playerx <=0:
            playerx=0
    
    for i in range(num_of_enemies):
        if enemyy[i]>400:
             for j in range(num_of_enemies):
                  enemyy[j]=2000
                  game_over()
              
        enemyx[i]+=enemyx_change[i]   
        if enemyx[i] >=430:
                enemyx_change[i]=-0.2
                enemyy[i]+=enemyy_change[i]
        if enemyx[i]<=0:
                enemyx_change[i]=0.2
                enemyy[i]+=enemyy_change[i]
        
        col=collision(enemyx[i],enemyy[i],bulletx,bullety)
        if col:
             explosion_sound=mixer.Sound("explosion.wav")
             explosion_sound.play()
             bullety=430
             bullet_state="ready"
             score+=1
             print(score)
             enemyx[i]=random.randint(0,430)
             enemyy[i]=random.randint(50,250)
        enemy(enemyx[i],enemyy[i],i)
    
    if bullety<=0:
         bullety=430
         bullet_state="ready"

    if bullet_state == "fire":
         fire(bulletx,bullety)
         bullety-=bullety_change
   
    player()
    show()
    pygame.display.update()
    