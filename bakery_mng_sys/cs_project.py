from datetime import datetime
from tkinter import StringVar, CENTER
from CTkTable import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="your password here!",
	database="bakery_management")

mycursor = mydb.cursor()

root = ctk.CTk()
root.title('CS project 2023-24')
root.geometry('560x430')
font = ('Times New Roman', 20,)
fontb = ('Helvetica', 20, 'italic')

ctk.set_appearance_mode("Dark")
tabview = ctk.CTkTabview(root, height=400, width=600)

tab_1 = tabview.add("main")
tab_2 = tabview.add("admin")
tab_3 = tabview.add("customer")
tab_4 = tabview.add("staff")
mycursor = mydb.cursor()

# authenticates admin user
def auth(username, password, loginframe):
	USERNAME = 'admin'
	PASSWORD = '1234'
	ud = username.get()
	pd = password.get()
	if ud != USERNAME:
		messagebox.showwarning(title='invalid username!', message='the username did not match, try again')
	elif pd != PASSWORD:
		messagebox.showwarning(title='invalid password!', message='the password did not match, try again')
	else:
		loginframe.destroy()
		nav()

# open admin tab and login
def admin_login():
	tabview.set('admin')
	loginframe = ctk.CTkFrame(tab_2, height=200, width=500)
	username = ctk.CTkEntry(loginframe, placeholder_text='USERNAME', height=30, width=300)
	password = ctk.CTkEntry(loginframe, placeholder_text='PASSSWORD', height=30, width=300)
	lb = ctk.CTkButton(loginframe, text='Login', command=lambda: auth(username, password, loginframe))
	bb = ctk.CTkButton(loginframe, text='Back', command=lambda: (tabview.set('main'), loginframe.destroy()), hover_color='red',fg_color='tomato')
	loginframe.pack()
	username.pack(padx=10, pady=10)
	password.pack(padx=10, pady=10)
	lb.pack(padx=10, pady=10)
	bb.pack(padx=10, pady=10)

# display invoice table
def showInvoices():
	mycursor5 = mydb.cursor()
	frame_out = ctk.CTkFrame(tab_2, height=400, width=500)
	frame1 = ctk.CTkScrollableFrame(frame_out, height=200, width=500)
	mycursor5.execute('SELECT Cname, Contact, DateOfOrder, TotalPatreon FROM invoices')
	t_lst = list(mycursor5.fetchall())
	t_lst.insert(0, ('CustomerName', 'Contact', 'DateOfOrder','TotalPatreon',))

	row = len(t_lst)
	table = CTkTable(master=frame1, row=row, column=4, values=t_lst)
	SSbtn = ctk.CTkButton(frame_out, text='Show Invoices', command=lambda: (frame_out.destroy(), showSales(), root.geometry('560x430')))
	bb = ctk.CTkButton(frame_out, text='Back', command=lambda: (frame_out.destroy(), nav(),),
					   fg_color='tomato', hover_color='red')
	frame_out.pack()
	frame1.place(x=0, y=0, )
	table.pack()
	SSbtn.place(x=40, y=250)
	bb.place(x=240, y=250)

# display sales table
def showSales():
	mycursor5 = mydb.cursor()
	frame_out = ctk.CTkFrame(tab_2, height=400, width=520)
	frame1 = ctk.CTkScrollableFrame(frame_out, height=200, width=520)
	mycursor5.execute('SELECT * FROM sales')
	t_lst = list(mycursor5.fetchall())
	t_lst.insert(0, ('Sno', 'Item', 'UnitsSold', 'TotalPrice', 'StockLeft'))
	row = len(t_lst)
	table = CTkTable(master=frame1, row=row, column=5, values=t_lst, width=100)
	SIbtn = ctk.CTkButton(frame_out, text='Show Invoices', command=lambda: (frame_out.destroy(), showInvoices()))
	bb = ctk.CTkButton(frame_out, text='Back', command=lambda: (frame_out.destroy(), nav()),
					   fg_color='tomato', hover_color='red')
	frame_out.pack()
	frame1.place(x=0, y=0,)
	table.pack()
	SIbtn.place(x=40, y=300)
	bb.place(x=240, y=300)


# add staff to staff table in database and updates the display table
def add_staff(empCode, empName, joindate, arg_post, arg_salary, arg_shift):
	mycursor10 = mydb.cursor()
	val = staff_table.get()
	val = val[1:]
	code = empCode.get()
	name = empName.get()
	date = joindate.get()
	post = arg_post.get()
	salary = arg_salary.get()
	shift = arg_shift.get()

	all_codes = [i[0] for i in val]

	try:
		datetime.strptime(date, ('%Y-%m-%d'))
	except ValueError:
		messagebox.showerror(title='error', message='invalid date format')
		return

	if code in all_codes:
		messagebox.showerror(title='error', message='empCode already taken')
		return
	elif not salary.isdigit():
		messagebox.showerror(title='error', message='Salary should be an integer')
		return
	else:
		salary = int(salary)
		values = (code, name, date, post, salary, shift)
		staff_table.add_row(index=1, values=values)
		sql = 'INSERT INTO staff VALUES (%s, %s, %s, %s, %s, %s)'
		mycursor10.execute(sql, values)
		mydb.commit()

# deletes staff to menu table in database and updates the display table
def del_staff(val):
	mycur0 = mydb.cursor()
	if val['row'] != 0:
		response = messagebox.askyesno(title='Remove Staff', message=f'Are You sure you want\n to delete {val["value"]} from the menu?')
		if response:
			key = staff_table.get_value(val['row'], 0)
			staff_table.delete_row(val['row'])
			mycur0.execute(f'DELETE FROM staff WHERE EmpID = "{key}" ')
			mydb.commit()
		else:
			return

# updates  staff database and table
def edit_staff(empCode, empName, joindate, arg_post, arg_salary, arg_shift):
	mycursor11 = mydb.cursor()
	code = empCode.get()
	name = empName.get()
	date = joindate.get()
	post = arg_post.get()
	salary = arg_salary.get()
	shift = arg_shift.get()

	try:
		datetime.strptime(date, ('%Y-%m-%d'))
	except ValueError:
		messagebox.showerror(title='error', message='invalid date format')
		return

	if not salary.isdigit():
		messagebox.showerror(title='error', message='Salary should be an integer')
		return
	else:
		salary = int(salary)
		values = (name, date, post, salary, shift)
		sql = f"UPDATE staff SET Ename = %s,  JoinDate = %s, Post = %s, Salary = %s , Shift = %s  WHERE EmpID ='{code}' "
		mycursor11.execute(sql, values)
		mydb.commit()
		mycursor12 = mydb.cursor()
		mycursor12.execute('SELECT * FROM staff')
		temp_val = mycursor12.fetchall()
		staff_table.update_values(temp_val)

# displays staff table
def etable():
	global staff_table
	root.geometry('700x430')
	frame_out = ctk.CTkFrame(tab_2, height=500, width=640)
	frame_in = ctk.CTkScrollableFrame(frame_out, height=200, width=640)
	frame_wrapper = ctk.CTkFrame(frame_out, height=50, width=640)
	mycur6 = mydb.cursor()
	mycur6.execute('SELECT * FROM staff')
	val = mycur6.fetchall()

	empCode = ctk.CTkEntry(frame_wrapper, placeholder_text='emp code', width=100)
	empName = ctk.CTkEntry(frame_wrapper, placeholder_text='name', width=100)
	joindate = ctk.CTkEntry(frame_wrapper, placeholder_text='join', width=100)
	post = ctk.CTkEntry(frame_wrapper, placeholder_text='post', width=100)
	salary = ctk.CTkEntry(frame_wrapper, placeholder_text='salary', width=100)
	shift = ctk.CTkEntry(frame_wrapper, placeholder_text='shift', width=100)
	add = ctk.CTkButton(frame_out, text='Add Staff', fg_color='grey', hover_color='silver', command=lambda: add_staff(empCode, empName, joindate, post,
							salary, shift))

	val.insert(0, ('EmpCode', 'EmpName', 'JoinDate', 'Post', 'Salary', 'Shift'))
	T_length = len(val)
	staff_table = CTkTable(master=frame_in, row=T_length, column=6, values=val, width=100, command=del_staff)
	EDbtn = ctk.CTkButton(frame_out, text='Edit Staff', command=lambda: edit_staff(empCode, empName, joindate, post, salary, shift))
	bb = ctk.CTkButton(frame_out, text='Back', command=lambda: (frame_out.destroy(), nav(), root.geometry('560x430')),
					   fg_color='tomato', hover_color='red')



	frame_out.pack()
	frame_in.place(x=1, y=10)
	frame_wrapper.place(x=1, y=250)
	staff_table.pack()
	empCode.grid(row=1, column=1, padx=1)
	empName.grid(row=1, column=2,  padx=1)
	joindate.grid(row=1, column=3, padx=1)
	post.grid(row=1, column=4, padx=1)
	salary.grid(row=1, column=5, padx=1)
	shift.grid(row=1, column=6, padx=1)
	EDbtn.place(x=10, y=300)
	add.place(x=180, y=300)
	bb.place(x=350, y=300)



# add items to menu table in database and updates the display table
def add_item(itemCode, itemName, itemPrice, itemStock):
	mycursor8 = mydb.cursor()
	val = menu_table.get()
	val= val[1:]
	code = itemCode.get()
	name = itemName.get()
	price = itemPrice.get()
	stock = itemStock.get()
	all_codes = [i[0] for i in val]
	all_names = [i[1] for i in val]
	if code in all_codes:
		messagebox.showerror(title='error', message='ItemCode already taken')
		return
	elif name in all_names:
		messagebox.showerror(title='error', message='ItemName already present')
		return
	elif not price.isdigit():
		messagebox.showerror(title='error', message='Price should be an integer')
		return
	elif stock not in ['y', 'n']:
		messagebox.showerror(title='error', message='value should be either "y" or "n"')
		return
	else:
		price = int(price)
		values = (code, name, price, stock)
		menu_table.add_row(index=1, values=values)
		sql = 'INSERT INTO menu VALUES (%s, %s, %s, %s)'
		mycursor8.execute(sql, values)
		mydb.commit()

# deletes items to menu table in database and updates the display table
def del_item(val):
	mycur3 = mydb.cursor()
	if val['row'] != 0:
		response = messagebox.askyesno(title='Remove Item', message=f'Are You sure you want\n to delete {val["value"]} from the menu?')
		if response:
			key = menu_table.get_value(val['row'], 1)
			menu_table.delete_row(val['row'])
			mycur3.execute(f'DELETE FROM menu WHERE Item = "{key}" ')
			mydb.commit()
		else:
			return

# updates  menu database and table
def update_script(option, temp1, temp2, temp3):
	values = [temp1.get(), temp2.get(), temp3.get()]
	key = option.get()
	temp_lest = menu_table.get()
	for i in temp_lest:
		if key == i[1]:
			temp_lest = i
			break

	if not bool(values[0]):
		values[0] = temp_lest[1]
	elif not bool(values[1]):
		values[1] = temp_lest[2]
	elif not bool(values[2]):
		values[2] = temp_lest[3]


	print(values)
	print(temp_lest)
	mycursor9 = mydb.cursor()
	sql = f"UPDATE menu SET Item = %s, Price = %s, InStock = %s  WHERE Item = '{key}'"
	mycursor9.execute(sql, values)
	mydb.commit()
	mycursor9 = mydb.cursor()
	mycursor9.execute('SELECT * FROM menu')
	val = mycursor9.fetchall()
	menu_table.update_values(val)

# provide prompt for database update
def edit_item():
	window = ctk.CTkToplevel()
	window.geometry('440x500')

	winFrame = ctk.CTkFrame(window, height=480, width=420)
	label1 = ctk.CTkLabel(winFrame, text='Select Key: ')
	ITMenu = ctk.CTkOptionMenu(winFrame, values=[i[1] for i in menu_table.get()[1:]], )
	itemName = ctk.CTkEntry(winFrame, placeholder_text='Item Name', width=200, height=30)
	itemPrice = ctk.CTkEntry(winFrame, placeholder_text='Price', width=200, height=30)
	itemStock = ctk.CTkEntry(winFrame, placeholder_text='Stock', width=200, height=30)
	update = ctk.CTkButton(winFrame, text='Update Table', command=lambda: update_script(ITMenu, itemName, itemPrice, itemStock ))
	exitbtn = ctk.CTkButton(winFrame, text='Back', command=lambda: window.destroy(),
							hover_color='red', fg_color='tomato')
	label2 = ctk.CTkLabel(winFrame, text='leave the field empty to retain original value')

	winFrame.place(x=10, y=10)

	label1.place(x=10, y=10)
	ITMenu.place(x=120, y=10)
	itemName.place(x=10, y=50)
	itemPrice.place(x=10, y=100)
	itemStock.place(x=10, y=150)
	update.place(x=10, y=250)
	exitbtn.place(x=250, y=250)
	label2.place(x=10, y=300)
	window.mainloop()

# displays menu table
def mtable():
	global menu_table
	frame_out = ctk.CTkFrame(tab_2, height=500, width=510)
	frame_in = ctk.CTkScrollableFrame(frame_out, height=200, width=500)
	frame_wrapper = ctk.CTkFrame(frame_out, height=50, width=500)
	mycur2 = mydb.cursor()
	mycur2.execute('SELECT * FROM menu')
	val = mycur2.fetchall()

	itemCode = ctk.CTkEntry(frame_wrapper, placeholder_text=max([i[0] for i in val]) + 1, width=49)
	itemName = ctk.CTkEntry(frame_wrapper, placeholder_text='item', width=150)
	itemPrice = ctk.CTkEntry(frame_wrapper, placeholder_text='price', width=100)
	itemStock = ctk.CTkEntry(frame_wrapper, placeholder_text='stock', width=50)
	add = ctk.CTkButton(frame_wrapper, text='Add Item', fg_color='silver', hover_color='grey', width=100, command=lambda: add_item(itemCode, itemName, itemPrice, itemStock))

	val.insert(0, ('ItemCode', 'ItemName', 'Price', 'InStock'))
	T_length = len(val)
	menu_table = CTkTable(master=frame_in, row=T_length, column=4, values=val, width=125, command=del_item)
	EDbtn = ctk.CTkButton(frame_out, text='Edit item', command=edit_item)
	bb = ctk.CTkButton(frame_out, text='Back', command=lambda: (frame_out.destroy(), nav()),
					   fg_color='tomato', hover_color='red')



	frame_out.pack()
	frame_in.place(x=10, y=10)
	frame_wrapper.place(x=0, y=250)
	menu_table.pack()
	itemCode.grid(row=1, column=1, padx=1)
	itemName.grid(row=1, column=2,  padx=1)
	itemPrice.grid(row=1, column=3, padx=1)
	itemStock.grid(row=1, column=4, padx=1)
	add.grid(row=1, column=5)

	EDbtn.place(x=10, y=300)
	bb.place(x=210, y=300)


# open and display admin navigation
def nav():
	navbar = ctk.CTkFrame(tab_2, height=200, width=500)
	menu = ctk.CTkButton(navbar, text='Menu', height=50, font=(None, 20), command=lambda: (mtable(), navbar.destroy()))
	sales = ctk.CTkButton(navbar, text='Sales', height=50, font=(None, 20), command=lambda: (showSales(), navbar.destroy()))
	employee = ctk.CTkButton(navbar, text='Employee', height=50, font=(None, 20),
							 command=lambda: (etable(), navbar.destroy()))
	back = ctk.CTkButton(navbar, text='Back', height=50, font=(None, 20), fg_color='tomato', hover_color='red',
						 command=lambda: (tabview.set('main'), navbar.destroy()))

	navbar.pack()
	menu.place(x=110, y=20, )
	sales.place(x=270, y=20)
	employee.place(x=110, y=90)
	back.place(x=270, y=90)

# add items to cart
def add_cart(item, qt, list, val):
	itemName = item.get()
	qtOrdered = qt.get()
	for i in val:
		if i[1] == itemName:
			itemPrice = i[2]

	t_price = itemPrice*int(qtOrdered)

	list.add_row(index=1, values=(itemName, qtOrdered, t_price))

# remove item from cart
def remove_item(val):
	if val['row'] != 0:
		response = messagebox.askyesno(title='Remove Item', message=f'Are You sure you want\n to remove {val["value"]} from the cart?')
		if response:
			orDtable.delete_row(val['row'])
		else:
			return

# update  window
def checkout(Cname, Ccontact):
	mycursor3 = mydb.cursor()
	sql = 'INSERT INTO invoices VALUES (%s, %s, %s, %s, %s)'
	ordDate = datetime.today().strftime('%Y-%m-%d')
	lst = orDtable.get()
	lst = lst[1:]

	t_price = [i[2] for i in lst]
	values = (Cname.get(), Ccontact.get(), str(lst), ordDate, sum(t_price))
	mycursor3.execute(sql, values)
	mydb.commit()
	messagebox.showinfo(title='Thank You', message='Thank you for yor patreon, hope to see you again')
	tabview.set('main')

	mycursor4 = mydb.cursor()
	for i in lst:
		i = list(i)
		sql2 = f'UPDATE sales SET UnitSold = UnitSold+%s , TotalEarnings = TotalEarnings+%s ,StockLeft=StockLeft-%s WHERE Item = "{i[0]}" '
		salesup = [i[1], i[2], int(i[1])]
		mycursor4.execute(sql2, salesup)
		mydb.commit()


# open cart prompt
def placeOrder(val):
	global orDtable

	window = ctk.CTkToplevel()
	window.geometry('440x500')
	winFrame = ctk.CTkFrame(window, height=480, width=420)
	items = [(i[1]) for i in val]
	items = items[1:]
	for i in items:
		if i[3] == 'n':
			items.remove(i)

	Cname = ctk.CTkEntry(winFrame, placeholder_text='your name', width=200, height=30)
	Ccontact = ctk.CTkEntry(winFrame, placeholder_text='contact info', width=200, height=30)
	label1 = ctk.CTkLabel(winFrame, text='Item :', font=font)
	ItemMenu = ctk.CTkOptionMenu(winFrame, values=items, )
	add = ctk.CTkButton(winFrame, text='Add to Cart', text_color='black', font=('Ariel', 16, 'bold'), width=120, fg_color='silver', hover_color='grey', command=lambda: add_cart(ItemMenu, QTMenu, orDtable, val))
	label2 = ctk.CTkLabel(winFrame, text='Quantity:', font=font)
	QTMenu = ctk.CTkOptionMenu(winFrame, values=['1', '2', '3', '4', '5'],)
	label3 = ctk.CTkLabel(winFrame, text='click on the item name to remove it from the list', font=('Ariel', 12, 'italic'))
	scrollBar = ctk.CTkScrollableFrame(winFrame, width=380, height=200)
	orDtable = CTkTable(master=scrollBar, row=1, column=3, values=[('Item', 'Quantity', 'NetPrice')], width=100, command=remove_item)
	ckeckout = ctk.CTkButton(winFrame, text='Place Order', command=lambda: checkout(Cname, Ccontact))
	exitbtn = ctk.CTkButton(winFrame, text='Back', command=lambda: (tabview.set('main'), window.destroy()),
					   hover_color='red', fg_color='tomato')


	winFrame.place(x=10, y=10)
	Cname.place(x=10, y=10)
	Ccontact.place(x=10, y=50)
	label1.place(x=10, y=100)
	ItemMenu.place(x=100, y=100)
	add.place(x=250, y=100)
	label2.place(x=10, y=140)
	QTMenu.place(x=100, y=140)
	label3.place(x=10, y=178)
	scrollBar.place(x=10, y=200)
	orDtable.pack()
	ckeckout.place(x=10, y=430)
	exitbtn.place(x=250, y=430)
	window.mainloop()

#check stock availability
def stockCheck():
	mycursor17 = mydb.cursor()
	mycursor17.callproc('stockCheck')
	mydb.commit()

# open menu for customer
def customer():
	tabview.set('customer')
	menu = ctk.CTkFrame(tab_3, width=400)
	stockCheck()
	title = ctk.CTkLabel(menu, text='Menu', font=('Algerian', 24))
	mycur = mydb.cursor()
	mycur.execute('SELECT * FROM menu ')
	val = mycur.fetchall()
	val.insert(0, ('ItemCode', 'ItemName', 'Price', 'InStock'))
	T_length = len(val)
	table = CTkTable(master=menu, row=T_length, column=4, values=val, width=125)
	lb = ctk.CTkButton(menu, text='Place Order', command=lambda: placeOrder(val))
	bb = ctk.CTkButton(menu, text='Back', command=lambda: (tabview.set('main'), menu.destroy(), root.geometry('560x430')),
					   hover_color='red', fg_color='tomato')
	h = str(table.winfo_reqheight() + 230)
	root.geometry(f'560x{h}')

	menu.grid(row=1, column=1)
	title.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
	table.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
	lb.grid(row=3, column=1, padx=10, pady=5,)
	bb.grid(row=3, column=2, padx=10, pady=5)

# view staff details
def viewDetail(id, emplst):
	f1 = ctk.CTkFrame(tab_4, height=400, width=500, )
	tup = []
	temp = id.get()
	for x in emplst:
		if x[0] == temp:
			tup = x
			break

	f1.place(x=260, y=170, anchor=CENTER)
	ctk.CTkLabel(f1, text='EMPID : ', font=font, ).grid(row=1, column=1, padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text=str(tup[0]), font=fontb, ).grid(row=1, column=2,  padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text='NAME : ', font=font, ).grid(row=2, column=1,  padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text=str(tup[1]), font=fontb, ).grid(row=2, column=2,  padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text='JOINDATE :', font=font, ).grid(row=3, column=1,  padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text=str(tup[2]), font=fontb, ).grid(row=3, column=2, padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text='CURRENT POST : ', font=font, ).grid(row=4, column=1, padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text=str(tup[3]), font=fontb, ).grid(row=4, column=2, padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text=' SALARY(per month) : ', font=font, ).grid(row=5, column=1, padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text=str(tup[4]), font=fontb, ).grid(row=5, column=2, padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text='SHIFT : ', font=font, ).grid(row=6, column=1, padx=10, pady=10, sticky='w')
	ctk.CTkLabel(f1, text=str(tup[5]), font=fontb, ).grid(row=6, column=2, padx=10, pady=10, sticky='w')
	ctk.CTkButton(f1, text='Back', command=lambda: (tabview.set('main'), f1.destroy()), hover_color='red', fg_color='tomato').grid(row=7, column=1, columnspan=2, padx=10, pady=10)

# sub process for authenticating staff
def check(id, name, idlst, namelst):
		edict = dict(zip(idlst, namelst))
		tid = id.get()
		tname = name.get()
		if tid in edict and edict[tid] == tname:
			return False
		else:
			return True

# authenticate staff
def eauth(name, id, frame):

	mycursor.execute("SELECT * FROM staff")
	lst = mycursor.fetchall()
	ENAME = [i[1] for i in lst]
	EMPID = [i[0] for i in lst]
	ud = name.get()
	pd = id.get()

	epid = StringVar()
	epid.set(pd)

	if pd not in EMPID:
		messagebox.showwarning(title='ERROR', message='invalid empid!')
	elif ud not in ENAME:
		messagebox.showwarning(title='ERROR', message=f'No staff with the\nname {ud} found!')
	elif check(id, name, EMPID, ENAME):
		messagebox.showwarning(title='ERROR', message=f'Name and id do not belong to same person !')
	else:
		frame.destroy()
		viewDetail(epid, lst)

# open staff tab and login
def staff():
	tabview.set('staff')
	empframe = ctk.CTkFrame(tab_4, height=200, width=500)
	ename = ctk.CTkEntry(empframe, placeholder_text='NAME', height=30, width=300)
	empid = ctk.CTkEntry(empframe, placeholder_text='EMPID', height=30, width=300)
	lb = ctk.CTkButton(empframe, text='Login', command=lambda: eauth(ename, empid, empframe))
	bb = ctk.CTkButton(empframe, text='Back', command=lambda: (tabview.set('main'), empframe.destroy()),
					   fg_color='tomato', hover_color='red')
	empframe.pack()
	empid.pack(padx=10, pady=10)
	ename.pack(padx=10, pady=10)
	lb.pack(padx=10, pady=10)
	bb.pack(padx=10, pady=10)

heading = ctk.CTkFrame(tab_1, width=500, height=100, fg_color='grey')
head = ctk.CTkLabel(heading, text='Welcome to \n Bakery Management System', font=('Algerian', 24))
buttonframe = ctk.CTkFrame(tab_1, height=100, width=500)
b1 = ctk.CTkButton(buttonframe, text="Admin", font=font, fg_color='skyblue', hover_color='darkturquoise', command=admin_login)
b2 = ctk.CTkButton(buttonframe, text="Customer", font=font, fg_color='cornflowerblue',hover_color='royalblue', command=customer )
b3 = ctk.CTkButton(buttonframe, text="Staff", font=font, fg_color='silver', hover_color='grey', command=staff)
b4 = ctk.CTkButton(buttonframe, text="EXIT", font=font, fg_color='tomato', hover_color='red')

about = ctk.CTkFrame(tab_1, height=120, width=500)
l1 = ctk.CTkLabel(about, text='About', font=('Helvetica', 12, 'bold'))
l2 = ctk.CTkLabel(about, text='Created by - Gaurav Upreti', font=('Helvetica', 12))
l3 = ctk.CTkLabel(about, text='Class - XII C ', font=('Helvetica', 12))
l4 = ctk.CTkLabel(about, text='Session - 2023-24', font=('Helvetica', 12))

tabview.pack(padx=10, pady=10)
heading.place(x=10, y=10, )
head.place(relx=0.1, rely=0.1)
buttonframe.place(x=10, y=120)
b1.place(x=100, y=10)
b2.place(x=260, y=10)
b3.place(x=100, y=50)
b4.place(x=260, y=50)
about.place(x=10, y=230)
l1.place(x=10, y=10)
l2.place(x=10, y=50)
l3.place(x=10, y=70)
l4.place(x=10, y=90)

root.mainloop()
