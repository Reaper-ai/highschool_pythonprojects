from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.options import Options
from tkinter import *


def set_url():
	global url, clicked
	i = clicked.get()

	if i == 'Global':
		url =  'https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF'
	elif i == 'Japan':
		url =  'https://open.spotify.com/playlist/37i9dQZEVXbKXQ4mDTEBXq'
	elif i == 'Korea':
		url =  'https://open.spotify.com/playlist/37i9dQZEVXbNxXF4SkHj9F'
	elif i == 'India':
		url =  'https://open.spotify.com/playlist/37i9dQZEVXbLZ52XmnySJg'
	elif i == 'Usa':
		url =  'https://open.spotify.com/playlist/37i9dQZEVXbLRQDuF5jeBp'
	elif i == 'Spain':
		url =  'https://open.spotify.com/playlist/37i9dQZEVXbNFJfN1Vw8d9'
	connect(url)


def connect(url):
	global driver
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get(url)
	time.sleep(5)
	content = driver.page_source.encode('utf-8').strip()
	soup = BeautifulSoup(content, "lxml")
	find_soptify(soup)


def find_soptify(soup):
	global flist
	songRank = soup.find_all('span', class_="encore-text encore-text-body-medium", limit=10)
	songName = soup.find_all('div', class_ = "encore-text encore-text-body-medium encore-internal-color-text-base btE2c3IKaOXZ4VNAb8WQ standalone-ellipsis-one-line", limit=10)
	songArtist = soup.find_all('span', class_="encore-text encore-text-body-small encore-internal-color-text-subdued UudGCx16EmBkuFPllvss standalone-ellipsis-one-line", limit=10)

	displayinfo(flist, songRank, songName, songArtist)



def displayinfo(flist, songRank,songName,songArtist):
	x = 3
	for i in range(0,10):
		Label(flist[i], text=f'{songRank[i].text}', font=("Helvetica", 32, 'bold')).grid(row=x, column=1, rowspan=2, padx=5, pady=5, sticky='w')
		Label(flist[i], text=f' {songName[i].text}', font=('ink free',14,"bold")).grid(row=x, column=2, padx=5, pady=5, sticky='w')
		Label(flist[i], text=f' {songArtist[i].text}', font=('ink free', 12, 'italic')).grid(row=x+1, column=2, padx=5, pady=5, sticky='w')
		x +=2

'''
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

'''

root = Tk()
clicked = StringVar()
regions = ['Global', 'Japan', 'Korea', 'India', 'USA', 'Spain']

clicked.set('Global')

root.title('MUSIC')
root.geometry('400x500')

frame = Frame(root, pady=10, padx=10).grid()

f1 = Frame(root, padx=10, pady=10).grid()
f2 = Frame(root, padx=10, pady=10).grid()
f3 = Frame(root, padx=10, pady=10).grid()
f4 = Frame(root, padx=10, pady=10).grid()
f5 = Frame(root, padx=10, pady=10).grid()
f6 = Frame(root, padx=10, pady=10).grid()
f7 = Frame(root, padx=10, pady=10).grid()
f8 = Frame(root, padx=10, pady=10).grid()
f9 = Frame(root, padx=10, pady=10).grid()
f10 = Frame(root, padx=10, pady=10).grid()
flist = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]




Label(frame, text='Select region').grid(row=1, column=1)
OptionMenu(frame, clicked, *regions).grid(row=2, column=1)
Button(frame, text="check", command=set_url).grid(row=2, column=2, sticky='w')


root.mainloop()

