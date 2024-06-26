from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import json
import pytz
from tkinter import *
from ttkbootstrap.constants import *
key = 'paste your api key hare'

font =('poppins', 15, 'bold')


class Day:
	def __init__(self, tcmx, tcmn, tfmx, tfmn,  c, w, p, fname):
		self.maxtc = tcmx
		self.mintc = tcmn
		self.maxtf = tfmx
		self.mintf = tfmn
		self.fname = fname
		self.windspd = w
		self.ppt_in = p
		self.cdn = c



	def display(self):
		Label(self.fname,text='min / max ',font=('poppins', 12)).pack(padx=2, pady=2)
		Label(self.fname, text=f'{self.maxtc}/{self.mintc } \xb0C', font=font).pack(padx=2, pady=2)
		Label(self.fname, text=f'{self.maxtf}/{self.mintf} \xb0F', font=('poppins', 12)).pack(padx=2, pady=2)
		Label(self.fname, text=f'max winds {self.windspd} kmph', font=('poppins', 14)).pack(padx=2, pady=2)
		Label(self.fname, text=f'total precipitation \n   {self.ppt_in} mm').pack(padx=2, pady=2)
		Label(self.fname, text=self.cdn, font=('Helvetica', 18)).pack(padx=2, pady=2)


def getWeather(key=key):

	city = text.get()


	jsondata = requests.get('http://api.weatherapi.com/v1/current.json?key='+key+'&q='+city).json()

	#print(json.dumps(jsondata, indent=2))
	setweather(jsondata)

def setweather(jsondata):

	fn_temp_c = jsondata['current']['temp_c']
	fn_temp_f = jsondata['current']['temp_f']
	fn_wind_spd = jsondata['current']['wind_kph']
	fn_ppt_in = jsondata['current']['precip_in']
	fn_humid_var = jsondata['current']['humidity']
	fn_feelslike_c = jsondata['current']['feelslike_c']
	fn_feelslike_f = jsondata['current']['feelslike_f']
	
	location.set(jsondata['location']['name'])
	time.set(jsondata['location']['localtime'])
	condition.set(jsondata['current']['condition']['text'])
	tempe.set(f'{fn_temp_c} \xb0C/ {fn_temp_f} \xb0F')
	wind_spd.set(f'Wind: {fn_wind_spd} km/h')
	ppt_in.set( f'Precipitation: {fn_ppt_in} in' )
	humid_var.set(f'Humidity: {fn_humid_var} %')
	feelslike.set(f'feels like {fn_feelslike_c} \xb0C/ {fn_feelslike_f} \xb0F')

def fcast(key=key):
	city = text.get()
	win = Toplevel(root)
	#win.geometry('670x250')
	win.maxsize(700, 250)
	win.minsize(650, 250)
	j = requests.get('http://api.weatherapi.com/v1/forecast.json?key='+key+'&q='+city+'&days=3').json()
	today = LabelFrame(win, text='Today', width=200, height=200)
	tomorrow = LabelFrame(win, text='Tomorrow', width=200, height=200)
	overmorrow = LabelFrame(win, text='Overmorrow', width=200, height=200)

	Today = Day(fname=today, tcmx=j["forecast"]["forecastday"][0]["day"]["maxtemp_c"],\
				tcmn=j["forecast"]["forecastday"][0]["day"]["mintemp_c"],\
				tfmx=j["forecast"]["forecastday"][0]["day"]["maxtemp_f"],\
				tfmn=j["forecast"]["forecastday"][0]["day"]["mintemp_f"],\
				w=j["forecast"]["forecastday"][0]["day"]["maxwind_kph"],\
				p=j["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],\
				c=j["forecast"]["forecastday"][0]["day"]["condition"]['text'])

	Tomorrow = Day(fname=tomorrow, tcmx=j["forecast"]["forecastday"][1]["day"]["maxtemp_c"],\
				tcmn=j["forecast"]["forecastday"][1]["day"]["mintemp_c"],\
				tfmx=j["forecast"]["forecastday"][1]["day"]["maxtemp_f"],\
				tfmn=j["forecast"]["forecastday"][1]["day"]["mintemp_f"],\
				w=j["forecast"]["forecastday"][1]["day"]["maxwind_kph"],\
				p=j["forecast"]["forecastday"][1]["day"]["totalprecip_mm"],\
				c=j["forecast"]["forecastday"][1]["day"]["condition"]['text'])

	Overmorrow = Day(fname=overmorrow, tcmx=j["forecast"]["forecastday"][2]["day"]["maxtemp_c"],\
				tcmn=j["forecast"]["forecastday"][2]["day"]["mintemp_c"],\
				tfmx=j["forecast"]["forecastday"][2]["day"]["maxtemp_f"],\
				tfmn=j["forecast"]["forecastday"][2]["day"]["mintemp_f"],\
				w=j["forecast"]["forecastday"][2]["day"]["maxwind_kph"],\
				p=j["forecast"]["forecastday"][2]["day"]["totalprecip_mm"],\
				c=j["forecast"]["forecastday"][2]["day"]["condition"]['text'])


	today.grid(row=1, column=1, padx=10, pady=10)
	tomorrow.grid(row=1, column=2, padx=10, pady=10)
	overmorrow.grid(row=1, column=3, padx=10, pady=10)
	Today.display()
	Tomorrow.display()
	Overmorrow.display()
	win.mainloop()




root = Tk()
root.geometry('500x390')
root.title('Weather')




wind_spd = StringVar()
tempe = StringVar()
ppt_in = StringVar()
humid_var = StringVar()
feelslike = StringVar()
condition = StringVar()
location = StringVar()
time = StringVar()
condition.set('-----')
tempe.set('--- \xb0C/ --- \xb0F')
wind_spd.set('Wind: --- km/h')
ppt_in.set('Precipitation: --- in')
humid_var.set('Humidity: -- %')
feelslike.set('feels like --- \xb0C/ --- \xb0F')
location.set('---------')
time.set('--.--.----.--.--')

Search_img = PhotoImage(file='searchbox.png')
Search_img = Search_img.subsample(2, 3)
simg = Label(image=Search_img)
text = Entry(root, justify='center', width=24, font=('Helvetica', 18, 'bold'), bg='#040404', fg='white')

Search_btn = PhotoImage(file='searchicon.png')
Search_btn = Search_btn.subsample(8,8)
enter = Button(root, text='', image=Search_btn, bg='#040404', fg='white', command=getWeather)

Icon_img = PhotoImage(file='icon.png')
Icon_img = Icon_img.subsample(2,2)
icon = Label(root,image=Icon_img)

frame = Frame(root, bg='#545454', width=200, height=400)
#: {a} \xb0C'
wind = Label(frame, textvariable=wind_spd, font=font)
ppt = Label(frame, textvariable=ppt_in, font=font)
h20 = Label(frame, textvariable=humid_var, font=font)

f3 = LabelFrame(root, height=200, width=200)
Location = Label(f3, textvariable=location, font=('Helvetica', 15, 'bold'))
Time = Label(f3, textvariable=time, font=('Helvetica', 15))
forcast = Button(f3, text='forecast', font=('Helvetica', 10), command=fcast)

frame2 = LabelFrame(root, text='current weather', font=('Helvetica', 13, 'italic') ,width=200, height=400)
temp = Label(frame2, textvariable=tempe, font=('Helvetica', 20, 'bold'))
fls = Label(frame2, textvariable=feelslike, font=('Helvetica', 12))
cond = Label(frame2, textvariable=condition, font=('Ariel', 18))

simg.place(x=45, y=20)
enter.place(x=390, y=26)
text.place(x=70, y=28)
icon.place(x=120, y=100)

f3.place(x=270,y=110)
Location.pack()
Time.pack()
forcast.pack()

frame.place(x=20, y=240)
wind.pack(padx=10, pady=5, anchor='w')
ppt.pack(padx=10, pady=5, anchor='w')
h20.pack(padx=10, pady=5, anchor='w')

frame2.place(x=260, y=230)
temp.pack(padx=10, pady=2)
fls.pack(padx=10, pady=2)
cond.pack(padx=10, pady=2)
root.mainloop()
