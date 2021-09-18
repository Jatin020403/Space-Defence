from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as fonts
import os

# initialise
root = Tk()
root.title("Space Defence")
root.iconbitmap("game_icon.ico")
root.wm_geometry("1280x720")
root.resizable(False, False)


# functions for buttons
def MainMenu():
    root.destroy()
    os.system("mainMenu.py")


count = 0
countCheck = True


def nextUp(x):
    global count
    if count == 3 or count == -7:
        coin["image"] = coinImage
        content["text"] = "This is a coin.\nHit it with the laser to increase your score by 1."
        if x == "prev":
            count = -10
        else:
            count = 0
    elif count == 0 or count == -8:
        coin["image"] = bombImage
        content[
            "text"] = "This is a bomb.\nIf you hit it with the laser, it will burst, destroying your spaceship to " \
                      "either\n" \
                      "right or left side of it(including the coins in that area), whichever side it's closer to. "
        count += 1
    elif count == 1 or count == -9:
        coin["image"] = playerImg
        content[
            "text"] = "This is your defence drone.\nYou can move it left, right using arrow keys.\nTo shoot the laser, " \
                      "press the spacebar."
        count += 1
    elif count == 2 or count == -10:
        coin["image"] = trophyImg
        content[
            "text"] = "Your goal is to destroy all the bombs in such a way that they don't " \
                      "destroy any coins.\n Also, you should collect all the coins."
        count += 1


def refresh(x):
    root.after(1, x)


def prevCheck():
    global count, countCheck
    if countCheck:
        count = -10
        countCheck = False


# creating buttons, images etc
testImage = Image.open("void.jpg")
testImage = testImage.resize((1280, 720))
coinImage = ImageTk.PhotoImage(Image.open("gold.png").resize((128, 128)))
bombImage = ImageTk.PhotoImage(Image.open("bomb.png").resize((128, 128)))
playerImg = ImageTk.PhotoImage(Image.open("playerImg.png").resize((128, 128)))
trophyImg = ImageTk.PhotoImage(Image.open("trophy.png").resize((128, 128)))
bgImage = ImageTk.PhotoImage(testImage)
bgLabel = Label(root, image=bgImage)
fontTitle = fonts.Font(family="ComicSansMS", size=40)

title = Label(root, text="HELP", font=fontTitle, bg="springgreen2", fg="black", width=5)
goBack = Button(root, text="HOME", bg="cyan2", fg="black", activebackground="cyan3", bd=5,
                font="ComicSansMS",
                relief=RAISED, activeforeground="black", height=1, width=5, command=MainMenu, anchor="center")
coin = Label(root, image=coinImage)
content = Label(root, text="This is a coin.\nHit it with the laser to increase your score by 1.",
                font="ComicSansMS", bg="lightgoldenrod")
nextButton = Button(root, text="NEXT", bg="indianred1", fg="black", activebackground="Indianred3", relief=RAISED,
                    width=5, height=1, bd=5, font="ComicSansMS", command=lambda: refresh(nextUp("hello")))
prevButton = Button(root, text="PREV", bg="indianred1", fg="black", activebackground="Indianred3", relief=RAISED,
                    width=5, height=1, bd=5, font="ComicSansMS",
                    command=lambda: [refresh(prevCheck()), refresh(nextUp("prev"))])

# displaying created elements on screen
bgLabel.grid(row=0, column=0, rowspan=14, columnspan=7)
title.grid(row=0, column=3)
coin.grid(row=1, column=3)
content.grid(row=6, column=3)
goBack.grid(row=0, column=0)
nextButton.grid(row=10, column=5)
prevButton.grid(row=10, column=0)
root.mainloop()
