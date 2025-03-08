import pygame
import random
from pygame import mixer
from time import sleep
import os
import pickle
import mysql.connector as con

''' Set-up'''

connected = True

try:
    mycon = con.connect(user='root', host='localhost', passwd="0011")
    mycursor = mycon.cursor()
    mycursor.execute("create database if not exists Space_Defence")
    mycursor.execute("use space_defence")
    mycursor.execute(
        "create table if not exists scoreboard(Name varchar(20), Coins_Hit int, Bombs_Left int, "
        "Score___Coins_minus_Bombs int)")
except con.errors.DataError:
    print("Error while connecting to server.")
    connected = False

try:
    with open("name.txt", "r") as f:
        name = f.read()
except FileNotFoundError:
    None

# Window
X = 1280
Y = 720

# Time
clock = pygame.time.Clock()
curr_time = 0
press_time = 0
timeGap = 719

# Img
void = pygame.image.load('void.jpg')
backgOriginal = pygame.image.load('bestBG.png')
backg = pygame.transform.scale(backgOriginal, (1280, 720))
Gballimg = pygame.image.load('gold.png')
Bballimg = pygame.image.load('bomb.png')
playerImg = pygame.image.load('playerImg.png')
titleIcon = pygame.image.load("game_icon.ico")

# Screen Shrink
playSizeL = 0
playSizeR = X
playMid = (playSizeR - playSizeL) // 2

# Player
playerX = X / 2
playerY = Y - 100
playerChange = 5

# Balls
ballImg = []
ballX = []
ballY = []
velX = []
velY = []
ball_num = 20  # must be divisible by 2
ballVel = 3
checkDist = 32
Bcount = int(ball_num / 2)
tempScore = 0
Score = 0
scan = True

'''Defining'''


def tick(current, press_time):
    if current - press_time > timeGap:
        return True
    else:
        return False


def rect(x1, x2, windows11):
    windows11.blit(backg, (int(x1), 0), (int(x1), 0, int(x2), int(Y)))


# def flash(x1, x2, windows11):
# pygame.draw.rect(windows11, (190, 0, 0), (int(x1), 0, int(x2), int(Y)))
# clock.tick(100)


def laser(pX, pY, windows11):
    pygame.draw.rect(windows11, (255, 0, 0), (int(pX + 30), 0, 3, int(pY)))


def randomness():
    sign = random.choice([-1, 1])
    velX = random.random() * ballVel * sign
    velY = ((ballVel) ** (2) - (velX) ** 2) ** (1 / 2)
    ballX = random.randint(60, 800)
    ballY = random.randint(60, 400)
    config = [velX, velY, ballX, ballY]
    return config


def static(i):
    ballX[i] = -100
    ballY[i] = -100
    velX[i] = 0
    velY[i] = 0


def player(x, y, windows11):
    windows11.blit(playerImg, (int(x), int(y)))


def ball(x, y, i, windows11):
    if i < ball_num / 2:
        windows11.blit(Bballimg, (int(x[i]), int(y[i])))
    if i >= ball_num / 2:
        windows11.blit(Gballimg, (int(ballX[i]), int(ballY[i])))


def ball_move(ballX, ballY, velX, velY, i):
    global scan, checksum
    if ballY <= 20 or ballY >= Y - 180:  # Experimental Values
        velY *= -1
    if (ballX < playSizeL + 13) and (ballX > playSizeL + 10):
        velX *= -1
        ballX = playSizeL + 13
    if (ballX > playSizeR - 64) and (ballX < playSizeR):
        velX *= -1
        ballX = playSizeR - 64
    ballX = ballX + velX
    ballY = ballY + velY
    if (i >= ball_num / 2 and ballY < -20):
        checksum += 1
        if checksum == ball_num / 2:
            scan = False
    return (ballX, ballY, velX, velY, scan)


def collChk(bs, gs):
    global Score, tempScore, screen
    global playerX, playMid, playSizeR, playSizeL, press_time
    for i in range(ball_num):
        dist = ((playerX - ballX[i]) ** 2) ** (1 / 2)
        if dist < checkDist and i >= ball_num / 2:
            gs.play()
            static(i)
            tempScore += 1
        if dist < checkDist and i < ball_num / 2:
            bs.play()
            static(i)
            if playerX > playMid:
                # flash(playerX, playSizeR, screen)
                playSizeR = playerX
            if playerX <= playMid:
                # flash(0, playSizeL, screen)
                playSizeL = playerX
            playMid = int(playSizeL + (playSizeR - playSizeL) / 2)
            playerX = playMid
            press_time = pygame.time.get_ticks()
            break


'''Main Body'''


def body():
    # Initializing
    pygame.init()
    mixer.init()

    # Globalising
    global void, backg, Gballimg, Bballimg, Bcount, ball_num
    global playerX, playerY, velX, velY, playSizeL, playSizeR
    global Bball_sound, Gball_sound, screen
    global tempScore, check, scan, Score, checksum, curr_time

    with open("check.txt", "w") as f:
        f.write("False")
    # A/V
    while mixer.music.get_busy():
        sleep(1)
    pygame.display.set_caption("Space Defence")
    pygame.display.set_icon(titleIcon)
    screen = pygame.display.set_mode((X, Y))
    void = void.convert()
    backg = backg.convert()
    Gballimg = Gballimg.convert_alpha()
    Bballimg = Bballimg.convert_alpha()
    Gball_sound = mixer.Sound('cheer.wav')
    Gball_sound.set_volume(0.1)
    Bball_sound = mixer.Sound('explosion.wav')
    Bball_sound.set_volume(0.1)
    bullet_sound = mixer.Sound('laser.wav')
    bullet_sound.set_volume(0.1)
    mixer.music.load('background.wav')
    mixer.music.play(-1)

    # Ball Generation
    for i in range(ball_num):
        config = randomness()
        velX.append(config[0])
        velY.append(config[1])
        ballX.append(config[2])
        ballY.append(config[3])

    '''Game Loop'''

    running = 1
    while running:
        # Press Quit
        for event in pygame.event.get():  # End 1
            if event.type == pygame.QUIT:
                running = 0

        # Screen Refresh 
        curr_time = pygame.time.get_ticks()
        screen.fill((0, 0, 0))
        screen.blit(backg, (0, 0))
        screen.blit(void, (0, 0))
        rect(playSizeL, playSizeR - playSizeL, screen)
        mixer.music.set_volume(0.2)
        checksum = 0

        # Input
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and tick(curr_time, press_time):
            laser(playerX, playerY, screen)
            bullet_sound.play()
            mixer.music.set_volume(0.1)
            collChk(Bball_sound, Gball_sound)
        if key[pygame.K_LEFT] and playerX > playSizeL + playerChange:
            playerX -= playerChange
        if key[pygame.K_a] and playerX > playSizeL + 20 + playerChange:
            playerX -= playerChange
        if key[pygame.K_RIGHT] and playerX < playSizeR - playerChange - 64:
            playerX += playerChange
        if key[pygame.K_d] and playerX < playSizeR - playerChange - 20:
            playerX += playerChange

        # Ball Movement
        for i in range(ball_num):
            if ballX[i] > playSizeR + ballVel or ballX[i] < playSizeL - ballVel:
                static(i)
            ballX[i], ballY[i], velX[i], velY[i], check = ball_move(ballX[i], ballY[i], velX[i], velY[i], i)

            if not check:  # End 2
                running = 0
                break

            ball(ballX, ballY, i, screen)  # Ball Blit

        # Break Statement
        if running == 0:
            mixer.music.stop()
            pygame.quit()
            break

        player(playerX, playerY, screen)  # Player Blit
        pygame.display.update()
        clock.tick(60)

    '''Score'''
    for i in range(int(ball_num / 2)):
        if ballY[i] < 0:
            Bcount -= 1
    Score = tempScore - Bcount
    if Score < 0:
        Score = 0
    if Score >= 10:
        with open("check.txt", "w") as f:
            f.write("True")

    scoreList = [Score, tempScore, Bcount]

    # Writing Score into File
    with open("score.dat", "wb") as f:
        pickle.dump(scoreList, f)

    if connected:
        mycursor.execute("select Score___Coins_minus_Bombs from scoreboard where Name='{}'".format(name))
        data = mycursor.fetchone()
        if data is not None:
            if Score > data[0]:
                mycursor.execute("insert into scoreboard values(%s, %s, %s, %s)", (name, tempScore, Bcount, Score))
                mycon.commit()
                mycursor.execute(
                    "delete from scoreboard where Name='{}' and score___Coins_minus_Bombs<{}".format(name, Score))
                mycon.commit()
        else:
            mycursor.execute("insert into scoreboard values(%s, %s, %s, %s)", (name, tempScore, Bcount, Score))
            mycon.commit()

    # Opening EndMenu
    os.system('endMenu.py')


if __name__ == "__main__":
    body()
