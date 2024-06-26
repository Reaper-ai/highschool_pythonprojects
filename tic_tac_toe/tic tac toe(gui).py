from tkinter import *
from tkinter import messagebox
import os
import sys
p = 'x'
winflag = False
c = 0
scrx = scro = 0

def messageBox(title,message,g): # pop up message

    def nxtround():
      global scrx,scro , c, winflag
      win.destroy()
      if g == 'X':
          scrx += 1
          score.config(text='X:O  ' + str(scrx) + ':' + str(scro) )
      elif g == 'O':
          scro +=1
          score.config(text='X:O  ' + str(scrx) + ':' + str(scro))
      for t in [b1,b2,b3,b4,b5,b6,b7,b8,b9]:
          t.config(text='', state='normal')
      winflag = False
      c = 0
      return winflag, c

    def newgame():
        global root
        win.destroy()
        root.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def closefn():
        root.destroy()


    win = Toplevel()
    win.geometry('250x80')
    win.title(title)
    subwin = Frame(win)
    Label(win, text=message).pack()
    Label(win,pady=5)
    Label(win, text='what would you like to do ?').pack()
    subwin.pack(pady=5)
    Button(subwin, text='continue' , command=nxtround).grid(column=1, padx=5, row=2)
    Button(subwin, text='restart', command=newgame).grid(column=2, padx=5, row=2)
    Button(subwin, text='Quit', command=closefn).grid(column=3, padx = 5,row=2)


def wincheck():  # checks winner
    for i in ['X', 'O']:
        if b1['text'] == b2['text'] == b3['text'] == i or b4['text'] == b5['text'] == b6['text'] == i or b7['text'] == \
                b8['text'] == b9['text'] == i:
            messageBox('Winner',"!!Player " + i + ' WINS!!' ,i)
            for w in [b1,b2,b3,b4,b5,b6,b7,b8,b9] :
                w.configure(state="disabled")
            winflag = True
            return  winflag
        elif b1['text'] == b4['text'] == b7['text'] == i or b2['text'] == b5['text'] == b8['text'] == i or b3['text'] == \
                b6['text'] == b9['text'] == i:
            messageBox('Winner', "!!Player " + i + ' WINS!!',i)
            for w in [b1,b2,b3,b4,b5,b6,b7,b8,b9] :
                w.configure(state="disabled")
            winflag = True
            return  winflag
        elif b1['text'] == b5['text'] == b9['text'] == i or b3['text'] == b5['text'] == b7['text'] == i:
            messageBox('Winner', "!!Player " + i + ' WINS!!',i)
            for w in [b1,b2,b3,b4,b5,b6,b7,b8,b9] :
                w.configure(state="disabled")
            winflag = True
            return winflag


def butupdate(b):  # update screen and turn
    global p, c, winflag
    valid(b)
    if p == "x" and b['text'] == '':
        b.config(text='X')
        turn.config(text='PLAYER O')
        p = 'o'
        c += 1
        wincheck()
        drawcheck(c, winflag)
        return p, c
    elif p == 'o' and b['text'] == '':
        b.config(text='O')
        turn.config(text='PLAYER X')
        p = 'x'
        c += 1
        wincheck()
        drawcheck(c, winflag)
        return p, c


def drawcheck(c, winflag):  # check draw
    if c == 9 and winflag == False:
        messageBox('tie','its a tie :(',None)


def valid(b):  # check valid turn
    if b['text'] != '':
        messagebox.showwarning(title="invalid move!!", message='play another tile')

print(c,winflag)

root = Tk()
root.title('tic tac toe')

frame2 = Frame(root, pady=10, padx=10)
frame1 = Frame(frame2, highlightbackground="black", highlightthickness=2, pady=10, padx=10)
score = Label(frame2, text='X:O  ' + str(scrx) + ':' + str(scro) , font=('ink free', 20, 'bold'))
turn = Label(frame2, text="PLAYER X", font=('ink free', 20, 'bold'))
b1 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b1))
b2 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b2))
b3 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b3))
b4 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b4))
b5 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b5))
b6 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b6))
b7 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b7))
b8 = Button(frame1, text='', font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b8))
b9 = Button(frame1, text='',font=('ink free', 20, 'bold'), height=1, width=3, command=lambda: butupdate(b9))

frame2.pack()
score.pack()
turn.pack()
frame1.pack()

b1.grid(column=0, row=5)
b2.grid(column=1, row=5)
b3.grid(column=2, row=5)
b4.grid(column=0, row=6)
b5.grid(column=1, row=6)
b6.grid(column=2, row=6)
b7.grid(column=0, row=7)
b8.grid(column=1, row=7)
b9.grid(column=2, row=7)

root.mainloop()
