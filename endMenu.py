import pickle
from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as fonts
from tkinter import messagebox
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


def again():
    root.destroy()
    os.system('SpaceDefence.py')


def special():
    messagebox.showinfo("Congratulations!", "YOU HAVE DONE IT \nYOU HAVE SAVED YOUR SPACESHIP AND PLANET FROM "
                                            "ABSOLUTE DEVASTATION WHILE MANAGING TO DESTROY THE WHOLE ENEMY FORCE")


check = True


def showAnalysis():
    global check
    if check:
        new = Toplevel()
        new.title("Space Defence")
        new.iconbitmap("game_icon.ico")
        new.wm_geometry("200x200")
        new.resizable(False, False)
        check = False

        with open("score.dat", "rb") as f:
            lister = pickle.load(f)
        header = Label(new, text="GAME ANALYSIS").pack()
        coinLbl = Label(new, text="Coins collected: " + str(lister[1])).pack()
        bombLbl = Label(new, text="Bombs left: " + str(lister[2])).pack()
        calc = Label(new, text="Score=coins collected-bombs left= " + str(lister[0]), padx=10).pack()


# creating buttons, images etc
testImage = Image.open("void.jpg")
testImage = testImage.resize((1280, 720))
analysisImg = ImageTk.PhotoImage(Image.open("analysis.png").resize((24, 24)))
bgImage = ImageTk.PhotoImage(testImage)
bgLabel = Label(root, image=bgImage)
font = fonts.Font(family="ComicSansMS", size=40)
try:
    with open("score.dat", "rb") as t:
        try:
            displayScore = pickle.load(t)[0]
            CHECK = float(displayScore)
        except pickle.UnpicklingError:
            with open("score.dat", "wb") as u:
                displayScore = '0'
                pickle.dump([0, 0, 0], u)
except FileNotFoundError:
    displayScore = "0"

with open("name.txt", "r")as f:
    name = f.read()

scoreLabel = Label(root, text=name+" Scored: " + str(displayScore), font="ComicSansMS", bg="purple1", fg="black")
title = Label(root, text="GAME OVER", font=font, bg="red", fg="black")
restart = Button(root, text="RESTART", bg="deepskyblue", fg="white", activebackground="steelblue", bd=5,
                 font="ComicSansMS",
                 relief=RAISED, activeforeground="white", height=1, width=10, command=again)
Quit = Button(root, text="QUIT", bg="thistle3", fg="black", activebackground="thistle4", bd=5, font="ComicSansMS",
              relief=RAISED, activeforeground="black", command=root.destroy, height=1, width=10)
mainMenu = Button(root, text="MAIN MENU", bg="cyan2", fg="black", activebackground="cyan3", bd=5,
                  font="ComicSansMS",
                  relief=RAISED, activeforeground="black", height=1, width=15, command=MainMenu)
analysisButton = Button(root, image=analysisImg, relief=RAISED, bd=5, command=showAnalysis)

# displaying created elements on screen
bgLabel.grid(row=0, column=0, rowspan=10, columnspan=15)
scoreLabel.grid(row=2, column=7)
title.grid(row=0, column=7)
restart.grid(row=4, column=7)
Quit.grid(row=6, column=7)
mainMenu.grid(row=5, column=7)
analysisButton.grid(row=2, column=8)

with open("check.txt", "r+") as p:
    if p.read() == "True":
        special()
    p.seek(0, 0)
    p.write("False")
root.mainloop()

with open("score.dat", "wb") as f:
    pickle.dump([0, 0, 0], f)
