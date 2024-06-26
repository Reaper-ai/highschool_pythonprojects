from tkinter import *

font = ('Digital-7', 20)
txt = ''

# update screen
def insert(x):
    global txt
    txt = txt + x
    equation.set(txt)

# clear the screen
def allclear():
    global txt
    txt = ''
    equation.set('')

# show result
def evaluate():
    try:
        result = eval(txt)
        equation.set(result)
    except SyntaxError:
        equation.set('      SYNTAX  ERROR')
    except ZeroDivisionError:
        equation.set('   ZERO DIVISION ERROR')

# delete character
def back():
    global txt
    txt = txt[:-1]
    equation.set(txt)


root = Tk()
root.title('Calculator')

outframe = Frame(root, height=250, width=250, padx=5, pady=5, bg='black')
frame = Frame(outframe, padx=5, pady=5, bg='dimgrey')

equation = StringVar()
e = Entry(frame, width=19, font=font, bg='lime', textvariable=equation)

# button initialize
b1 = Button(frame, text="1", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('1'))
b2 = Button(frame, text="2", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('2'))
b3 = Button(frame, text="3", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('3'))

b4 = Button(frame, text="4", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('4'))
b5 = Button(frame, text="5", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('5'))
b6 = Button(frame, text="6", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('6'))

b7 = Button(frame, text="7", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('7'))
b8 = Button(frame, text="8", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('8'))
b9 = Button(frame, text="9", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('9'))
b0 = Button(frame, text="0", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('0'))

b_add = Button(frame, text="+", height=1, width=3, font=font, bg="lightgrey", command=lambda: insert('+'))
b_sub = Button(frame, text="-", height=1, width=3, font=font, bg="lightgrey", command=lambda: insert('-'))
b_pro = Button(frame, text="*", height=1, width=3, font=font, bg="lightgrey", command=lambda: insert('*'))
b_div = Button(frame, text="/", height=1, width=3, font=font, bg="lightgrey", command=lambda: insert('/'))

b_eql = Button(frame, text="=", height=1, width=11, font=font, bg="royalblue", command=evaluate)
b_clr = Button(frame, text="AC", height=3, width=3, font=font, bg="wheat", command=allclear)
b_bsp = Button(frame, text="C", height=3, width=3, font=font, bg="snow", command=back)
b_exp = Button(frame, text="^", height=1, width=3, font=font, bg="lightgrey", command=lambda: insert('**'))
b_bro = Button(frame, text="(", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('('))
b_brc = Button(frame, text=")", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert(')'))
b_dec = Button(frame, text=".", height=1, width=3, font=font, bg="floralwhite", command=lambda: insert('.'))

outframe.pack()
frame.pack()

e.grid(row=1, columnspan=5, column=1, pady=5, padx=0)

# button display
b1.grid(column=1, row=5, padx=1)
b2.grid(column=2, row=5, padx=1)
b3.grid(column=3, row=5, padx=1)

b4.grid(column=1, row=4, padx=1)
b5.grid(column=2, row=4, padx=1)
b6.grid(column=3, row=4, padx=1)

b7.grid(column=1, row=3, padx=1)
b8.grid(column=2, row=3, padx=1)
b9.grid(column=3, row=3, padx=1)
b0.grid(column=2, row=6, padx=1)

b_add.grid(column=4, row=5, padx=1)
b_sub.grid(column=4, row=4, padx=1)
b_pro.grid(column=4, row=3, padx=1)
b_div.grid(column=4, row=2, padx=1)
b_exp.grid(column=3, row=2, padx=1)

b_bro.grid(column=1, row=2, padx=1)
b_brc.grid(column=2, row=2, padx=1)
b_dec.grid(column=1, row=6, padx=1)

b_eql.grid(column=3, row=6, columnspan=3, pady=2, padx=1)
b_clr.grid(column=5, row=2, rowspan=2, pady=1)
b_bsp.grid(column=5, row=4, rowspan=2, pady=1)

# main loop
root.mainloop()
