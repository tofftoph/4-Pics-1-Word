from tkinter import *
from tkinter import messagebox
import random

root = Tk()


class Finals(Frame):
    # INSTANCE ATTRIBUTES
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('4 pics 1 word')

        # TOP FRAME WIDGET FOR COINS AND LEVEL
        topFrame = Frame(self.master, width=450, height=30, bg='royal blue')

        lvlLabel = Label(topFrame, text='Level: ', bg='royal blue', fg='white', font='arial 15 bold')
        coinpic = PhotoImage(file='zz_coins.png')
        coinlbl = Label(topFrame, image=coinpic, bg='royal blue')
        coinlbl.image = coinpic

        # ENCAPSULATE LEVEL
        self.__level = 1
        self.lvlTxt = Label(topFrame, text=self.__level, fg='white', bg='royal blue', font='arial 15 bold')

        self.coinAmount = 100
        self.coinAmountlbl = Label(topFrame, text=self.coinAmount, fg='white', bg='royal blue', font='arial 15 bold')

        # BUTTON WIDGETS
        self.skipPic = PhotoImage(file='zz_arrow1.png')
        self.skipBtn = Button(self.master, image=self.skipPic, highlightthickness=0, bd=0, command=self.skipImage)
        self.hintPic = PhotoImage(file='zz_hint1.png')
        self.hint = Button(self.master, image=self.hintPic, highlightthickness=0, bd=0, command=self.hint)
        self.exitPic = PhotoImage(file='zz_exit.png')
        self.exitBtn = Button(self.master, image=self.exitPic, highlightthickness=0, bd=0, command=self.on_exit)
        self.delBtn = Button(self.master, text='DELETE', bg='steel blue', fg='white', command=self.delLetter)

        self.picts()
        self.retrieveData()

        # KEYBOARD FRAME
        self.kbFrame = Frame(self.master)

        # ENTRY WIDGET
        self.var = StringVar()
        self.var.trace('w', self.checkAnswer)
        self.entry = Entry(self.master, width=45, textvariable=self.var)
        self.entry.bind("<Button-1>", lambda e: self.keyboard())

        # WIDGET PLACEMENTS
        topFrame.place(x=0, y=0)
        coinlbl.place(x=330, y=2)
        lvlLabel.place(x=5, y=2)
        self.lvlTxt.place(x=65, y=2)
        self.coinAmountlbl.place(x=360, y=2)

        self.skipBtn.place(x=380, y=180)
        self.hint.place(x=373, y=390)
        self.exitBtn.place(x=10, y=500)
        self.delBtn.place(x=30, y=400)

        self.kbFrame.place(x=85, y=400)
        self.entry.place(x=80, y=360)
        self.place()

        # CALL KEYBOARD
        self.keyboard()

    # INSTANCE METHODS HERE
    def picts(self):
        f = open("picList.txt", "r")
        x = f.readlines()

        self.picfiles = list()
        for p in x:
            fn = p.strip().split(';')
            self.picfiles.append(fn[1])

        self.pics = PhotoImage(file=self.picfiles[self.__level - 1] + ".png")
        lblpic = Label(self.master, image=self.pics)
        lblpic.place(x=70, y=40)

    def changeImage(self):
        self.__level += 1
        self.lvlTxt.config(text=self.__level)
        self.entry.delete(0, END)

        if self.__level > 50:
            messagebox.showinfo('Congratulations!', 'You have finished the game!')
            if messagebox.askyesno('Continue', 'Start new game?'):
                self.__level = 1
                self.lvlTxt.config(text=self.__level)
                self.coinAmount = 100
                self.coinAmountlbl.config(text=self.coinAmount)
                self.pics.config(file=self.picfiles[self.__level - 1] + '.png')
            else:
                self.__level = 50
                self.lvlTxt.config(text=self.__level)
                self.pics.config(file=self.picfiles[self.__level - 1] + ".png")

        self.pics.config(file=self.picfiles[self.__level - 1] + ".png")

    def skipImage(self):
        if self.coinAmount != 0 and self.coinAmount > 0:
            self.changeImage()
            self.coinAmount -= 10
            self.coinAmountlbl.config(text=self.coinAmount)
        else:
            messagebox.showinfo('Oops', 'Out of coins.')

    def hint(self):
        try:
            if self.coinAmount != 0 and self.coinAmount > 0:
                word = self.picfiles[self.__level - 1]
                x = len(word)
                self.entry.insert(INSERT, word[random.randint(0, x - 1)].upper())
                self.coinAmount -= 2
                self.coinAmountlbl.config(text=self.coinAmount)
            else:
                messagebox.showinfo('Oops', 'Out of coins.')
        except:
            messagebox.showerror('Oops!', 'An error occurred.')

    def delLetter(self):
        self.entry.delete(len(self.entry.get()) - 1, END)

    def checkAnswer(self, *args):
        try:
            s = self.var.get()
            answer = self.picfiles[self.__level - 1]

            if s == answer.upper():
                self.coinAmount += 10
                self.coinAmountlbl.config(text=self.coinAmount)
                messagebox.showinfo('Correct', 'You got the right answer.')
                self.changeImage()
                self.keyboard()
                return True

            elif len(s) > len(answer):
                messagebox.showwarning('Oops', 'Too many letters!')
                self.entry.delete(len(self.entry.get()) - 1, END)
                return False
        except:
            messagebox.showerror('Oops!', 'An error occurred.')

    def on_exit(self):
        with open('4picstxt.txt', 'w') as f:
            data = str(self.__level) + ',' + str(self.coinAmount) + ',' + str(self.picfiles[self.__level - 1])
            f.writelines(data)
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def retrieveData(self):
        try:
            with open('4picstxt.txt', 'r') as f:
                x = f.readlines()

            for data in x:
                level, coins, picture = data.split(',')

                if level != '' and coins != '' and picture != '':
                    self.lvlTxt.config(text=level)
                    self.coinAmountlbl.config(text=coins)
                    self.pics.config(file=picture + ".png")

                    self.__level = int(level)
                    self.coinAmount = int(coins)
        except:
            messagebox.showerror('Oops!', 'An error occurred.')

    # KEYBOARD HERE
    def select(self, value):
        self.entry.insert(END, value)

    def randomizeBtn(self):
        buttons = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                   'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                   'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        word = self.picfiles[self.__level - 1].upper()
        ranWord = random.sample(list(word), len(word))

        if len(word) >= 9:
            randomBtn = random.sample(ranWord + random.sample(buttons, 1), 10)
        elif len(word) >= 8:
            randomBtn = random.sample(ranWord + random.sample(buttons, 2), 10)
        elif len(word) >= 7:
            randomBtn = random.sample(ranWord + random.sample(buttons, 3), 10)
        elif len(word) >= 6:
            randomBtn = random.sample(ranWord + random.sample(buttons, 4), 10)
        elif len(word) >= 5:
            randomBtn = random.sample(ranWord + random.sample(buttons, 5), 10)
        elif len(word) >= 4:
            randomBtn = random.sample(ranWord + random.sample(buttons, 6), 10)
        elif len(word) >= 3:
            randomBtn = random.sample(ranWord + (random.sample(buttons, 7)), 10)
        return randomBtn

    def keyboard(self):
        varRow = 2
        varColumn = 0

        for button in self.randomizeBtn():
            command = lambda x=button: self.select(x)

            Button(self.kbFrame, text=button, width=4, font='bold', bg="steel blue", fg="white",
                   activebackground="Medium aquamarine", activeforeground="white", relief='raised', padx=1,
                   pady=1, bd=1, command=command).grid(row=varRow, column=varColumn)

            varColumn += 1

            if varColumn > 4 and varRow == 2:
                varColumn = 0
                varRow += 1
            if varColumn > 4 and varRow == 3:
                varColumn = 0
                varRow += 1
            if varColumn > 4 and varRow == 4:
                varColumn = 0
                varRow += 1


root.geometry('450x550')
app = Finals(root)
root.resizable(0, 0)
root.mainloop()

