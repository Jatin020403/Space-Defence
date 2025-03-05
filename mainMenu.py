from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import os

# initialise
root = Tk()
root.title("Space Defence")
root.iconbitmap("game_icon.ico")
root.wm_geometry("1280x720")
root.resizable(False, False)


# functions for buttons
def credits():
    messagebox.showinfo("Credits", "Jatin--Gameplay\nShounak--Graphics\nHardik--Menus")


def start():
    root.destroy()
    os.system('SpaceDefence.py')


def getHelp():
    root.destroy()
    os.system("HelpMenu.py")


check = True
name = ""


def editIt():
    global check
    if check:
        new = Toplevel()
        new.title("Change Name")
        new.iconbitmap("game_icon.ico")
        new.wm_geometry("400x150")
        new.resizable(False, False)
        check = False

        inputBox = Entry(new, bg="azure", width=50, relief=RIDGE, bd=3)
        inputBox.pack()

        def getIt():
            global name, check, root
            name = inputBox.get()
            if name != "":
                userLabel["text"] = "Player: " + name
                with open("name.txt", "w") as g:
                    g.write(name)
            check = True
            new.destroy()

        confirm = Button(new, text="SUBMIT", relief=RAISED, bd=3, width=5,
                         command=getIt).pack()


# creating buttons, images etc
testImage = Image.open("void.jpg")
testImage = testImage.resize((1280, 720))
bgImage = ImageTk.PhotoImage(testImage)
titleImage = Image.open("titleNew.png")
titleImage = titleImage.resize((400, 75))
tImage = ImageTk.PhotoImage(titleImage)
editImg = ImageTk.PhotoImage(Image.open("edit.png").resize((24, 24)))


def namer():
    global name
    try:
        with open("name.txt", "r+") as f:
            name = f.read()
            if name == "":
                name = "New Player"
            f.seek(0, 0)
            f.write(name)
    except FileNotFoundError:
        with open("name.txt", "w") as f:
            name = "New Player"
            f.write(name)


namer()
bgLabel = Label(root, image=bgImage)
title = Label(root, image=tImage, height=75, width=400, bg='black')
userLabel = Label(root, text="Player: " + name, font=("ComicSansMS", 20), height=1, anchor="w",
                  bg="lightblue", relief=RIDGE, bd=5, padx=5)
play = Button(root, text="PLAY", bg="deepskyblue", fg="white", activebackground="steelblue", bd=5,
              font="ComicSansMS",
              relief=RAISED, activeforeground="white", height=1, width=10, command=start)
credit = Button(root, text="CREDITS", bg="navajowhite2", fg="black", activebackground="navajowhite4", bd=5,
                font="ComicSansMS",
                relief=RAISED, activeforeground="black", command=credits, height=1, width=10)
Quit = Button(root, text="QUIT", bg="thistle3", fg="black", activebackground="thistle4", bd=5, font="ComicSansMS",
              relief=RAISED, activeforeground="black", command=root.destroy, height=1, width=10)
Help = Button(root, text="HELP", bg="springgreen2", fg="black", activebackground="springgreen4", bd=5,
              font="ComicSansMS",
              relief=RAISED, activeforeground="black", height=1, width=10, command=getHelp)
editName = Button(root, image=editImg, relief=RAISED, bd=5, command=editIt)

# displaying created elements on screen
bgLabel.grid(row=0, column=0, rowspan=10, columnspan=15)
title.grid(row=0, column=7)
userLabel.grid(row=3, column=7)
editName.grid(row=3, column=8)
play.grid(row=4, column=7)
Help.grid(row=5, column=7)
credit.grid(row=6, column=7)
Quit.grid(row=7, column=7)

root.mainloop()
