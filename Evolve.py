#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import E, END, LEFT, N, RIGHT, TOP, W, ttk ,filedialog,messagebox,colorchooser
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont
import re
import io
import random
import copy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

start_window_size = (1500,700)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='Evolve\chromedriver_win32\chromedriver.exe',chrome_options=options)

class Application(tk.Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.pack()
		r = requests.get("https://www.nicovideo.jp/user/733434")
		soup = BeautifulSoup(r.text,"html.parser")
		find_start = r'まふろさんのユーザーページです。'
		find_end = r'" property="og:description"'
		check = re.findall(rf'{find_start}(.*){find_end}',str(soup))
		if check[0] != "DQN":
			print("公開停止中")
		else:
			self.canvas_w = start_window_size[0]
			self.canvas_h = start_window_size[1]

			self.card_w = 124
			self.card_h = int(self.card_w * 1.4)
			self.size = (self.card_w,self.card_h)
			self.size_2 = (self.card_w,self.card_w)

			master.geometry(f"{self.canvas_w}x{self.canvas_h}")
			master.title("Main Window")

			self.font_path = 'Evolve\img\Molot.ttf'
			self.font_size = 65
			self.font = ImageFont.truetype(self.font_path,self.font_size)
			self.font_reader = ImageFont.truetype(self.font_path,100)
			self.font_stat = ImageFont.truetype(self.font_path,50)
			self.font_count = ImageFont.truetype(self.font_path,30)

			self.font2 = ("",30,"bold")
			self.font_color = "lime"

			men = tk.Menu(master)
			master.config(menu=men)
			setting_menu = tk.Menu(men,tearoff=0)
			token = tk.Menu(men,tearoff=0)
			counter = tk.Menu(men,tearoff=0)
			men.add_cascade(label='設定', menu=setting_menu)
			men.add_cascade(label='トークン', menu=token)
			men.add_cascade(label="カウンター",menu=counter)

			self.color = "#004C2D"
			self.ura = Image.open("Evolve\img\card.png").resize(self.size)

			setting_menu.add_command(label='デッキコード入力',command=lambda:self.deck_entry())
			setting_menu.add_command(label="ローカル保存",command=lambda:self.local_save())
			setting_menu.add_command(label="ローカル読み込み",command=lambda:self.local_entry())
			setting_menu.add_command(label="開始",command=lambda:self.start())

			counter.add_command(label="指定攻撃",command=lambda:self.counter("指定攻撃"))
			counter.add_command(label="守護",command=lambda:self.counter("守護"))
			counter.add_command(label="必殺",command=lambda:self.counter("必殺"))
			counter.add_command(label="オーラ",command=lambda:self.counter("オーラ"))
			counter.add_command(label="ドレイン",command=lambda:self.counter("ドレイン"))
			counter.add_command(label="威圧",command=lambda:self.counter("威圧"))
			counter.add_command(label="カウンター",command=lambda:self.counter("カウンター"))

			elf = tk.Menu(token,tearoff=0)
			elf.add_command(label="フェアリー",command=lambda:self.token("フェアリー"))
			elf.add_command(label="薔薇の一撃",command=lambda:self.token("薔薇の一撃"))
			elf.add_command(label="フェアリーウィスプ",command=lambda:self.token("フェアリーウィスプ"))
			elf.add_command(label="クリスタリア・イヴ",command=lambda:self.token("クリスタリア・イヴ"))
			royal = tk.Menu(token,tearoff=0)
			royal.add_command(label="ナイト",command=lambda:self.token("ナイト"))
			royal.add_command(label="スティールナイト",command=lambda:self.token("スティールナイト"))
			royal.add_command(label="乙姫お守り隊",command=lambda:self.token("乙姫お守り隊"))
			royal.add_command(label="ヴァイキング",command=lambda:self.token("ヴァイキング"))
			royal.add_command(label="シールドガーディアン",command=lambda:self.token("シールドガーディアン"))
			royal.add_command(label="レオニダスの遺志",command=lambda:self.token("レオニダスの遺志"))
			wicth = tk.Menu(token,tearoff=0)
			wicth.add_command(label="攻撃型ゴーレム",command=lambda:self.token("攻撃型ゴーレム"))
			wicth.add_command(label="防御型ゴーレム",command=lambda:self.token("防御型ゴーレム"))
			wicth.add_command(label="大地の魔片",command=lambda:self.token("大地の魔片"))
			wicth.add_command(label="マジカルポーン",command=lambda:self.token("マジカルポーン"))
			dragon = tk.Menu(token,tearoff=0)
			dragon.add_command(label="ドラゴン",command=lambda:self.token("ドラゴン"))
			dragon.add_command(label="オルカ",command=lambda:self.token("オルカ"))
			dragon.add_command(label="ヘルフレイムドラゴン",command=lambda:self.token("ヘルフレイムドラゴン",))
			dragon.add_command(label="ドラゴウェポン",command=lambda:self.token("ドラゴウェポン"))
			nightmare = tk.Menu(token,tearoff=0)
			nightmare.add_command(label="ゴースト",command=lambda:self.token("ゴースト"))
			nightmare.add_command(label="フォレストバット",command=lambda:self.token("フォレストバット"))
			nightmare.add_command(label="ミミ",command=lambda:self.token("ミミ"))
			nightmare.add_command(label="ココ",command=lambda:self.token("ココ"))
			bishop = tk.Menu(token,tearoff=0)
			bishop.add_command(label="ホーリーファルコン",command=lambda:self.token("ホーリーファルコン"))
			bishop.add_command(label="ホーリータイガー",command=lambda:self.token("ホーリータイガー"))
			bishop.add_command(label="うたかたの月",command=lambda:self.token("うたかたの月"))

			token.add_cascade(label="エルフ",menu=elf)
			token.add_cascade(label="ロイヤル",menu=royal)
			token.add_cascade(label="ウィッチ",menu=wicth)
			token.add_cascade(label="ドラゴン",menu=dragon)
			token.add_cascade(label="ナイトメア",menu=nightmare)
			token.add_cascade(label="ビショップ",menu=bishop)

			self.canvas = tk.Canvas(self,width=self.canvas_w,height=self.canvas_h,bg=self.color)
			self.canvas.pack()
			self.bind_canvas("main")

			self.reader = None
			self.main_deck_data = []
			self.evo_deck_data = []
			self.start_flag = 0
			self.pp_var = 1
			self.max_var = 1
			self.ep_var = 0
			self.hand_window = None

	def deck_entry(self):
		deck_entry_window = tk.Toplevel()
		deck_entry_window.geometry("300x100")
		deck_entry_window.title("reg")

		self.deck_entry_box = tk.Entry(deck_entry_window,width=40)
		self.deck_entry_box.grid(row=0,column=0,pady=5,padx=20)

		#
		# self.deck_entry_box.insert(0,"53UP0")
		#

		paste_btn = tk.Button(deck_entry_window,text="貼り付け",command=lambda:paste())
		paste_btn.grid(row=1,column=0,pady=5)

		deck_entry_btn = tk.Button(deck_entry_window,text="Get!!",command=lambda:get())
		deck_entry_btn.grid(row=2,column=0,pady=5)

		def paste():
			clip = deck_entry_window.clipboard_get()
			self.deck_entry_box.insert(0,clip)

		def get():
			self.main_deck_data = []
			self.evo_deck_data = []
			count = 0
			reader_size = (self.size[0]*2,self.size[1]*2)
			big_size = (self.size[0]*3,self.size[1]*3)
			driver.get(f"https://decklog.bushiroad.com/view/{self.deck_entry_box.get()}")
			time.sleep(3)
			html = driver.page_source.encode('utf-8')
			soup = BeautifulSoup(html, "html.parser")
			data = soup.find_all(class_ = "deckview")
			data = data[0]
			data_list = data.find_all(class_ = "row")

			reader = re.findall(r'data-src="(.*)" id=',str(data_list[0]))[0]
			image = Image.open(io.BytesIO(requests.get(reader).content))
			self.reader_img = image.resize(reader_size)

			main_deck = data_list[1].find_all(class_ = "card-item col-xl-2 col-lg-3 col-sm-4 col-6")
			n = 0
			for i in main_deck:
				num = re.findall(r'<span class="num">(.*)</span>',str(i))[0]
				card = re.findall(r'data-src="(.*)" id=',str(i))[0]
				name = re.findall(r'"card-ctrl card-detail" title="(.*) :',str(i))[0]
				image = Image.open(io.BytesIO(requests.get(card).content))
				image = image.resize(big_size)

				r = requests.get(f"https://shadowverse-evolve.com/cardlist/?cardno={name}")
				soup = BeautifulSoup(r.text,"html.parser")
				found = soup.find('div', class_='status')
				hp = re.findall(r'体力</span>([0-9]*)</span>',str(found))
				if hp == []:
					hp = None
				else:
					hp = hp[0]
				atk = re.findall(r'攻撃力</span>([0-9]*)</span>',str(found))
				if atk == []:
					atk = None
				else:
					atk = atk[0]
				stat = [hp,atk]

				for i in range(int(num)):
					n = n + 1
					if n < 10:
						id = f"id_0{n}"
					else:
						id = f"id_{n}"
					self.main_deck_data.append([image,stat,id])
					count = count +1
					print(f"メインデッキ {count}枚目")

			if len(data_list) == 3:
				count = 0
				self.evo_deck_data = []
				evo_deck = data_list[2].find_all(class_ = "card-item col-xl-2 col-lg-3 col-sm-4 col-6")
				for i in evo_deck:
					num = re.findall(r'<span class="num">(.*)</span>',str(i))[0]
					card = re.findall(r'data-src="(.*)" id=',str(i))[0]
					name = re.findall(r'"card-ctrl card-detail" title="(.*) :',str(i))[0]
					image = Image.open(io.BytesIO(requests.get(card).content))
					image = image.resize(big_size)

					r = requests.get(f"https://shadowverse-evolve.com/cardlist/?cardno={name}")
					soup = BeautifulSoup(r.text,"html.parser")
					found = soup.find('div', class_='status')
					hp = re.findall(r'体力</span>([0-9]*)</span>',str(found))
					if hp == []:
						hp = None
					else:
						hp = hp[0]
					atk = re.findall(r'攻撃力</span>([0-9]*)</span>',str(found))
					if atk == []:
						atk = None
					else:
						atk = atk[0]
					stat = [hp,atk]

					for i in range(int(num)):
						n = n + 1
						if n < 10:
							id = f"id_0{n}"
						else:
							id = f"id_{n}"
						self.evo_deck_data.append([image,stat,id])
						count = count +1
						print(f"エボルヴデッキ {count}枚目")

			deck_entry_window.destroy()
			messagebox.showinfo("info","デッキ読み込み完了")

	def local_save(self):
		filename = None
		filename = filedialog.asksaveasfilename(title='デッキ保存',defaultextension='.npy',filetypes=[("Python NumPy Files", ".npy")],initialdir = "Evolve/deck/")
		if filename != None:
			data = [self.reader_img,self.main_deck_data,self.evo_deck_data]
			np.save(filename,data)

	def local_entry(self):
		filename = None
		filename = filedialog.askopenfilename(title = 'デッキ読み込み',initialdir = "Evolve/deck/",filetypes=[("Python NumPy Files", ".npy")])
		if filename != None:
			data = np.load(filename,allow_pickle='TRUE')
			data = data.tolist()
			self.reader_img = data[0]
			self.main_deck_data = data[1]
			self.evo_deck_data = data[2]
			messagebox.showinfo("info","デッキ読み込み完了")

	def pp_counter(self,num):
		img = Image.open("Evolve\img\pp.png").resize((self.size_2))
		draw = ImageDraw.Draw(img)
		x,y = draw.textsize(str(num),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_w/2-y/2-5)),str(num),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		return img

	def max_counter(self,num):
		img = Image.open("Evolve\img\max.png").resize((self.size_2))
		draw = ImageDraw.Draw(img)
		x,y = draw.textsize(str(num),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_w/2-y/2-5)),str(num),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		return img

	def ep_counter(self,num):
		img = Image.open("Evolve\img\ep.png").resize((self.size_2))
		draw = ImageDraw.Draw(img)
		x,y = draw.textsize(str(num),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_w/2-y/2-5)),str(num),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		return img

	def token(self,name):
		big_size = (self.size[0]*3,self.size[1]*3)
		self.num = self.num +1
		if name == "ヴァイキング":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP01/bp01_t06.png").content))
			stat = [3,2]
		if name == "うたかたの月":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t08.png").content))
			stat = [None,None]
		if name == "乙姫お守り隊":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP01/bp01_t04.png").content))
			stat = [1,2]
		if name == "オルカ":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t05.png").content))
			stat = [2,2]
		if name == "クリスタリア・イヴ":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t01.png").content))
			stat = [4,4]
		if name == "ゴースト":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD05/SD05-T01.png").content))
			stat = [1,1]
		if name == "攻撃型ゴーレム":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD03/SD03-T01.png").content))
			stat = [3,2]
		if name == "ココ":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP01/bp01_t13.png").content))
			stat = [None,None]
		if name == "シールドガーディアン":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t02.png").content))
			stat = [1,1]
		if name == "スティールナイト":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD02/SD02-T02.png").content))
			stat = [2,2]
		if name == "大地の魔片":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t15.png").content))
			stat = [None,None]
		if name == "ドラゴウェポン":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t07.png").content))
			stat = [None,None]
		if name == "ドラゴン":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP01/bp01_t11.png").content))
			stat = [5,5]
		if name == "ナイト":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD02/SD02-T01.png").content))
			stat = [1,1]
		if name == "薔薇の一撃":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP01/bp01_t01.png").content))
			stat = [None,None]
		if name == "フェアリーウィスプ":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP01/bp01_t02.png").content))
			stat = [1,1]
		if name == "フェアリー":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD01/SD01-T01.png").content))
			stat = [1,1]
		if name == "フォレストバット":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD05/SD05-T02.png").content))
			stat = [1,1]
		if name == "ヘルフレイムドラゴン":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t06.png").content))
			stat = [4,3]
		if name == "ホーリータイガー":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD06/SD06-T02.png").content))
			stat = [4,4]
		if name == "ホーリーファルコン":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD06/SD06-T01.png").content))
			stat = [2,2]
		if name == "防御型ゴーレム":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/SD03/SD03-T02.png").content))
			stat = [2,3]
		if name == "マジカルポーン":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t04.png").content))
			stat = [2,1]
		if name == "ミミ":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP01/bp01_t12.png").content))
			stat = [None,None]
		if name == "レオニダスの遺志":
			img = Image.open(io.BytesIO(requests.get("https://shadowverse-evolve.com/wordpress/wp-content/images/cardlist/BP02/bp02_t03.png").content))
			stat = [None,None]
		img = img.resize(big_size)
		big_image = ImageTk.PhotoImage(img)
		image = ImageTk.PhotoImage(img.resize(self.size))
		data = 	(image,big_image,stat,f"id_{self.num}","token")
		self.field.append(data)
		self.all_card.append([img,stat,f"id_{self.num}","token"])
		if data[2] != [None,None]:
			img = Image.new("RGBA",self.size,(0, 0, 0,0))
			draw = ImageDraw.Draw(img)
			x,y = draw.textsize(str(data[2][0]),self.font_stat)
			draw.text((0,self.card_h-y-3),str(data[2][0]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
			_x,_y = draw.textsize(str(data[2][1]),self.font_stat)
			draw.text((self.card_w - _x,self.card_h-_y-3),str(data[2][1]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
			img = ImageTk.PhotoImage(img)

			self.stat_img[data[3]] = img
			self.stat_data[data[3]] = data[2]
			self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=data[0],tag=(data[3],"token"))
			self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[data[3]],tag=(data[3],"stat","token"))
			self.card_count += 1
		else:
			self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=data[0],tag=(data[3],"token"))
			self.card_count += 1
		self.num = self.num +1

	def counter(self,name):
		if name == "カウンター":
			img = Image.open("Evolve/img/blank.png").resize((40,40))
			self.stat_data[f"id_{self.num}"] = 0
			draw = ImageDraw.Draw(img)
			x,y = draw.textsize(str(self.stat_data[f"id_{self.num}"]),self.font_count)
			draw.text((20,20),str(self.stat_data[f"id_{self.num}"]),font=self.font_count,fill="white",stroke_width=2,stroke_fill='black',anchor="mm")
			img = ImageTk.PhotoImage(img)
			self.stat_img[f"id_{self.num}"] = img
			self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[f"id_{self.num}"],tag=(f"id_{self.num}","counter_num"))
			self.card_count += 1
			self.num = self.num +1
		else:
			img = Image.open(f"Evolve\img\{name}.png").resize((40,40))
			img = ImageTk.PhotoImage(img)
			self.stat_img[f"id_{self.num}"] = img
			self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[f"id_{self.num}"],tag=(f"id_{self.num}","counter"))
			self.card_count += 1
			self.num = self.num +1

	def start(self):
		self.canvas.delete("all")
		self.num = 0
		self.start_flag = 1
		self.field = []
		self.hand = []
		self.deck = []
		self.deck_view = 0
		self.evo_deck = []
		self.evo_deck_view = 0
		self.graveyard = []
		self.graveyard_view = 0
		self.banished = []
		self.banished_view = 0
		self.temp = []
		self.temp_view = 0
		self.shuffle_flag = 0
		self.dice_var = 1

		self.reader_hp = 20
		self.card_count = 0
		self.deck_window = None
		self.evo_deck_window = None
		self.graveyard_window = None
		self.banished_window = None
		self.temp_window = None
		self.big_window = None

		self.del_card = None
		self.stat_img = {}
		self.stat_data = {}

		self.canvas.delete("system_pp")
		pp = self.pp_counter(self.pp_var)
		self.pp = ImageTk.PhotoImage(pp)
		self.canvas.create_image(self.canvas_w - self.card_w*1.6,self.canvas_h - 60,image=self.pp,tag="system_pp")

		self.canvas.delete("system_max")
		max = self.max_counter(self.max_var)
		self.max = ImageTk.PhotoImage(max)
		self.canvas.create_image(self.canvas_w - self.card_w/2,self.canvas_h - 60,image=self.max,tag="system_max")

		self.canvas.delete("system_ep")
		ep = self.ep_counter(self.ep_var)
		self.ep = ImageTk.PhotoImage(ep)
		self.canvas.create_image(self.canvas_w - self.card_w*2.7,self.canvas_h - 60,image=self.ep,tag="system_ep")

		self.canvas.delete("system_reader")
		self.reader = ImageTk.PhotoImage(self.reader_img)
		self.canvas.create_image(self.canvas_w - self.size[0]*2-16,self.size[1]+16,image=self.reader,tag="system_reader")

		img = Image.new("RGBA",(self.size[0]*2,self.size[1]*2),(0, 0, 0,0))
		draw = ImageDraw.Draw(img)
		x,y = draw.textsize(str(self.reader_hp),self.font_reader)
		draw.text((self.card_w*2-x,self.card_h*2-y-3),str(self.reader_hp),font=self.font_reader,fill="#00FF00",stroke_width=5,stroke_fill='black')
		img = ImageTk.PhotoImage(img)
		self.reader_hp_img = img
		self.canvas.create_image(self.canvas_w - self.size[0]*2-16,self.size[1]+16,image=self.reader_hp_img,tag="system_reader_hp")

		self.re_img = Image.open("Evolve/img/re.png").resize((self.card_w-20,self.card_w-20))
		self.re_img_angle = ImageTk.PhotoImage(self.re_img)
		self.canvas.create_image(self.canvas_w - self.card_w*1.5,self.card_h/2,image=self.re_img_angle,tag="system_re")

		self.dice = Image.open("Evolve/img/dice.png").resize((self.card_w-20,self.card_w-20))
		self.dice_img = ImageTk.PhotoImage(self.dice)
		self.canvas.create_image(self.canvas_w - self.card_w*2.7,100 + self.card_h*2 + 20 + 20,image=self.dice_img,tag="system_dice")

		if self.hand_window != None:
			self.hand_window.destroy()

		mas_x = self.winfo_x()
		mas_y = self.winfo_y()
		mas_h = self.winfo_height()
		self.hand_window = tk.Toplevel()
		self.hand_window.geometry(f"1200x{self.card_h}+{mas_x}+{mas_y + mas_h}")
		self.hand_window.title("Hand")
		self.hand_canvas = tk.Canvas(self.hand_window,width=2400,height=self.card_h,bg=self.color)
		self.hand_canvas.pack()
		self.bind_canvas("hand")

		self.h_menu = tk.Menu(self.hand_canvas,tearoff=0)
		self.h_menu.add_command(label="デッキに戻す",command=lambda:self.hand_deck())
		self.h_menu.add_command(label="すべてデッキに戻す",command=lambda:self.hand_deck_all())

		for i in self.main_deck_data:
			self.num = self.num +1
			p = copy.copy(i)
			image = p[0]
			big_image = ImageTk.PhotoImage(image)
			image = ImageTk.PhotoImage(image.resize(self.size))
			self.deck.append((image,big_image,p[1],p[2]))

		for i in self.evo_deck_data:
			self.num = self.num +1
			p = copy.copy(i)
			image = p[0]
			big_image = ImageTk.PhotoImage(image)
			image = ImageTk.PhotoImage(image.resize(self.size))
			self.evo_deck.append((image,big_image,p[1],p[2]))

		self.all_card = self.main_deck_data + self.evo_deck_data

		random.shuffle(self.deck)

		for i in range(4):
			self.hand.append(self.deck[0])
			self.deck.remove(self.deck[0])

		self.update()

	def update(self):
		if self.deck_window != None:
			if len(self.deck) == 0:
				self.deck_window.destroy()
				self.deck_window = None
				self.deck_view = 0
			else:
				deck_width = 0
				deck_width2 = 0
				deck_width3 = 0
				self.deck_canvas.delete("all")
				for i in range(len(self.deck)):
					if i < 13:
						self.deck_canvas.create_image(self.card_w/2 + deck_width,self.card_h/2,image=self.deck[i][0],tag=self.deck[i][3])
						deck_width = deck_width + self.card_w / 2
					elif i < 26:
						self.deck_canvas.create_image(self.card_w/2 + deck_width2,self.card_h/2+self.card_h,image=self.deck[i][0],tag=self.deck[i][3])
						deck_width2 = deck_width2 + self.card_w / 2
					else:
						self.deck_canvas.create_image(self.card_w/2 + deck_width3,self.card_h/2+self.card_h*2,image=self.deck[i][0],tag=self.deck[i][3])
						deck_width3 = deck_width3 + self.card_w / 2
		self.canvas.delete("system_deck")
		if self.deck_view == 1:
			deck_img = Image.open("Evolve\img/deck_2.png").resize((self.size))
		else:
			deck_img = Image.open("Evolve\img/deck.png").resize((self.size))
		ura = self.ura.copy()
		ura.paste(deck_img,mask=deck_img)
		draw = ImageDraw.Draw(ura)
		x,y = draw.textsize(str(len(self.deck)),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_h/2-y/2)),str(len(self.deck)),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		self.deck_img = ImageTk.PhotoImage(ura)
		self.canvas.create_image(self.canvas_w - self.card_w/2,100,image=self.deck_img,tag="system_deck")

		if self.evo_deck_window != None:
			if len(self.evo_deck) == 0:
				self.evo_deck_window.destroy()
				self.evo_deck_window = None
				self.evo_deck_view = 0
			else:
				evo_deck_width = 0
				evo_deck_width2 = 0
				self.evo_deck_canvas.delete("all")
				for i in range(len(self.evo_deck)):
					if i < 13:
						self.evo_deck_canvas.create_image(self.card_w/2 + evo_deck_width,self.card_h/2,image=self.evo_deck[i][0],tag=self.evo_deck[i][3])
						evo_deck_width = evo_deck_width + self.card_w / 2
					elif i < 26:
						self.evo_deck_canvas.create_image(self.card_w/2 + evo_deck_width2,self.card_h/2+self.card_h,image=self.evo_deck[i][0],tag=self.evo_deck[i][3])
						evo_deck_width2 = evo_deck_width2 + self.card_w / 2
		self.canvas.delete("system_evo_deck")
		if self.evo_deck_view == 1:
			evo_deck_img = Image.open("Evolve\img\evo_deck_2.png").resize((self.size))
		else:
			evo_deck_img = Image.open("Evolve\img\evo_deck.png").resize((self.size))
		ura = self.ura.copy()
		ura.paste(evo_deck_img,mask=evo_deck_img)
		draw = ImageDraw.Draw(ura)
		x,y = draw.textsize(str(len(self.evo_deck)),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_h/2-y/2)),str(len(self.evo_deck)),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		self.evo_deck_img = ImageTk.PhotoImage(ura)
		self.canvas.create_image(self.card_w/2,self.canvas_h - self.card_h/2,image=self.evo_deck_img,tag="system_evo_deck")

		if self.hand_window != None:
			self.hand_canvas.delete("all")
			hand_width = 0
			for i in range(len(self.hand)):
				self.hand_canvas.create_image(self.card_w/2 + hand_width,self.card_h/2,image=self.hand[i][0],tag=self.hand[i][3])
				hand_width = hand_width + self.card_w / 2
		self.canvas.delete("system_hand")
		hand_img = Image.open("Evolve\img\Hand.png").resize((self.size))
		ura = self.ura.copy()
		ura.paste(hand_img,mask=hand_img)
		draw = ImageDraw.Draw(ura)
		x,y = draw.textsize(str(len(self.hand)),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_h/2-y/2)),str(len(self.hand)),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		self.hand_img = ImageTk.PhotoImage(ura)
		self.canvas.create_image(self.canvas_w - self.card_w*1.6,100 + self.card_h*2 + 20 + 20,image=self.hand_img,tag="system_hand")

		if self.temp_window != None:
			if len(self.temp) == 0:
				self.temp_window.destroy()
				self.temp_window = None
				self.temp_view = 0
			else:
				temp_width = 0
				temp_width2 = 0
				self.temp_canvas.delete("all")
				for i in range(len(self.temp)):
					if i < 13:
						self.temp_canvas.create_image(self.card_w/2 + temp_width,self.card_h/2,image=self.temp[i][0],tag=self.temp[i][3])
						temp_width = temp_width + self.card_w / 2
					elif i < 26:
						self.temp_canvas.create_image(self.card_w/2 + temp_width2,self.card_h/2+self.card_h,image=self.temp[i][0],tag=self.temp[i][3])
						temp_width2 = temp_width2 + self.card_w / 2
		self.canvas.delete("system_temp")
		if self.temp_view == 1:
			temp_img = Image.open("Evolve\img/temp_2.png").resize((self.size))
		else:
			temp_img = Image.open("Evolve\img/temp.png").resize((self.size))
		ura = self.ura.copy()
		ura.paste(temp_img,mask=temp_img)
		draw = ImageDraw.Draw(ura)
		x,y = draw.textsize(str(len(self.temp)),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_h/2-y/2)),str(len(self.temp)),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		self.temp_img = ImageTk.PhotoImage(ura)
		self.canvas.create_image(self.canvas_w - self.card_w/2,100 + self.card_h + 20,image=self.temp_img,tag="system_temp")

		if self.graveyard_window != None:
			if len(self.graveyard) == 0:
				self.graveyard_window.destroy()
				self.graveyard_window = None
				self.graveyard_view = 0
			else:
				graveyard_width = 0
				graveyard_width2 = 0
				self.graveyard_canvas.delete("all")
				for i in range(len(self.graveyard)):
					if i < 18:
						self.graveyard_canvas.create_image(self.card_w/2 + graveyard_width,self.card_h/2,image=self.graveyard[i][0],tag=self.graveyard[i][3])
						graveyard_width = graveyard_width + self.card_w / 2
					elif i < 36:
						self.graveyard_canvas.create_image(self.card_w/2 + graveyard_width2,self.card_h/2+self.card_h,image=self.graveyard[i][0],tag=self.graveyard[i][3])
						graveyard_width2 = graveyard_width2 + self.card_w / 2
		self.canvas.delete("system_graveyard")
		if self.graveyard_view == 1:
			graveyard_img = Image.open("Evolve\img\graveyard_2.png").resize((self.size))
		else:
			graveyard_img = Image.open("Evolve\img\graveyard.png").resize((self.size))
		ura = self.ura.copy()
		ura.paste(graveyard_img,mask=graveyard_img)
		draw = ImageDraw.Draw(ura)
		x,y = draw.textsize(str(len(self.graveyard)),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_h/2-y/2)),str(len(self.graveyard)),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		self.graveyard_img = ImageTk.PhotoImage(ura)
		self.canvas.create_image(self.canvas_w - self.card_w/2,100 + self.card_h*2 + 20 + 20,image=self.graveyard_img,tag="system_graveyard")

		if self.banished_window != None:
			if len(self.banished) == 0:
				self.banished_window.destroy()
				self.banished_window = None
				self.banished_view = 0
			else:
				banished_width = 0
				banished_width2 = 0
				self.banished_canvas.delete("all")
				for i in range(len(self.banished)):
					if i < 18:
						self.banished_canvas.create_image(self.card_w/2 + banished_width,self.card_h/2,image=self.banished[i][0],tag=self.banished[i][3])
						banished_width = banished_width + self.card_w / 2
					elif i < 36:
						self.banished_canvas.create_image(self.card_w/2 + banished_width2,self.card_h/2+self.card_h,image=self.banished[i][0],tag=self.banished[i][3])
						banished_width2 = banished_width2 + self.card_w / 2
		self.canvas.delete("system_banished")
		if self.banished_view == 1:
			banished_img = Image.open("Evolve\img/banished_2.png").resize((self.size))
		else:
			banished_img = Image.open("Evolve\img/banished.png").resize((self.size))
		ura = self.ura.copy()
		ura.paste(banished_img,mask=banished_img)
		draw = ImageDraw.Draw(ura)
		x,y = draw.textsize(str(len(self.banished)),self.font)
		draw.text((int(self.card_w/2-x/2),int(self.card_h/2-y/2)),str(len(self.banished)),font=self.font,fill="white",stroke_width=3,stroke_fill='black')
		self.banished_img = ImageTk.PhotoImage(ura)
		self.canvas.create_image(self.card_w*2.8,self.canvas_h - self.card_h/2,image=self.banished_img,tag="system_banished")

	def spin(self,event):
		if self.start_flag != 0:
			closest_ids = self.canvas.find_closest(event.x, event.y)
			self.move_id = self.canvas.gettags(closest_ids[0])
			x1,y1,x2,y2 = self.canvas.bbox(self.move_id[0])
			if self.move_id[-1] == "current":
				if "system_pp" == self.move_id[0]:
					self.canvas.delete("system_pp")
					if event.delta > 0:
						self.pp_var = self.pp_var + 1
					else:
						self.pp_var = self.pp_var - 1
					pp = self.pp_counter(self.pp_var)
					self.pp = ImageTk.PhotoImage(pp)
					self.canvas.create_image(self.canvas_w - self.card_w*1.6,self.canvas_h - 60,image=self.pp,tag="system_pp")

				elif "system_max" == self.move_id[0]:
					self.canvas.delete("system_max")
					if event.delta > 0:
						self.max_var = self.max_var + 1
					else:
						self.max_var = self.max_var - 1
					max = self.max_counter(self.max_var)
					self.max = ImageTk.PhotoImage(max)
					self.canvas.create_image(self.canvas_w - self.card_w/2,self.canvas_h - 60,image=self.max,tag="system_max")

				elif "system_ep" == self.move_id[0]:
					self.canvas.delete("system_ep")
					if event.delta > 0:
						self.ep_var = self.ep_var + 1
					else:
						self.ep_var = self.ep_var - 1
					ep = self.ep_counter(self.ep_var)
					self.ep = ImageTk.PhotoImage(ep)
					self.canvas.create_image(self.canvas_w - self.card_w*2.7,self.canvas_h - 60,image=self.ep,tag="system_ep")

				elif "counter_num" == self.move_id[1]:
					x1,y1,x2,y2 = self.canvas.bbox(self.move_id[0])
					self.canvas.delete(self.move_id)
					if event.delta > 0:
						self.stat_data[self.move_id[0]] = int(self.stat_data[self.move_id[0]]) +1
					else:
						self.stat_data[self.move_id[0]] = int(self.stat_data[self.move_id[0]]) -1
					img = Image.open("Evolve/img/blank.png").resize((40,40))
					draw = ImageDraw.Draw(img)
					x,y = draw.textsize(str(self.stat_data[self.move_id[0]]),self.font_count)
					draw.text((20,20),str(self.stat_data[self.move_id[0]]),font=self.font_count,fill="white",stroke_width=2,stroke_fill='black',anchor="mm")
					img = ImageTk.PhotoImage(img)
					self.stat_img[self.move_id[0]] = img
					self.canvas.create_image((x1+x2)/2,(y1+y2)/2,image=self.stat_img[self.move_id[0]],tag=(self.move_id[0],"counter_num"))

				elif "system_reader_hp" == self.move_id[0]:
					self.canvas.delete("system_reader_hp")
					if event.delta > 0:
						self.reader_hp = self.reader_hp +1
					else:
						self.reader_hp = self.reader_hp -1
					img = Image.new("RGBA",(self.size[0]*2,self.size[1]*2),(0, 0, 0,0))
					draw = ImageDraw.Draw(img)
					x,y = draw.textsize(str(self.reader_hp),self.font_reader)
					draw.text((self.card_w*2-x,self.card_h*2-y-3),str(self.reader_hp),font=self.font_reader,fill="#00FF00",stroke_width=5,stroke_fill='black')
					img = ImageTk.PhotoImage(img)
					self.reader_hp_img = img
					self.canvas.create_image(self.canvas_w - self.size[0]*2-16,self.size[1]+16,image=self.reader_hp_img,tag="system_reader_hp")

				elif "stat" == self.move_id[1]:
					self.canvas.lift(self.move_id[0])
					m = (x1 + x2)/2
					if self.move_id[-2] == "yoko":
						x1,y1,x2,y2 = self.canvas.bbox(self.move_id[0])
						n = (y1 + y2)/2
						if event.delta > 0:
							if event.y < n:
								self.stat_data[self.move_id[0]][0] = int(self.stat_data[self.move_id[0]][0])+1
							else:
								self.stat_data[self.move_id[0]][1] = int(self.stat_data[self.move_id[0]][1])+1
						else:
							if event.y < n:
								self.stat_data[self.move_id[0]][0] = int(self.stat_data[self.move_id[0]][0])-1
							else:
								self.stat_data[self.move_id[0]][1] = int(self.stat_data[self.move_id[0]][1])-1
					else:
						if event.delta > 0:
							if event.x > m:
								self.stat_data[self.move_id[0]][0] = int(self.stat_data[self.move_id[0]][0])+1
							else:
								self.stat_data[self.move_id[0]][1] = int(self.stat_data[self.move_id[0]][1])+1
						else:
							if event.x > m:
								self.stat_data[self.move_id[0]][0] = int(self.stat_data[self.move_id[0]][0])-1
							else:
								self.stat_data[self.move_id[0]][1] = int(self.stat_data[self.move_id[0]][1])-1
					self.canvas.delete(self.move_id)
					img = Image.new("RGBA",self.size,(0, 0, 0,0))
					draw = ImageDraw.Draw(img)
					x,y = draw.textsize(str(self.stat_data[self.move_id[0]][1]),self.font_stat)
					draw.text((0,self.card_h-y-3),str(self.stat_data[self.move_id[0]][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
					_x,_y = draw.textsize(str(self.stat_data[self.move_id[0]][0]),self.font_stat)
					draw.text((self.card_w - _x,self.card_h-_y-3),str(self.stat_data[self.move_id[0]][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
					if self.move_id[-2] == "yoko":
						img = img.rotate(90,expand=True)
						img = ImageTk.PhotoImage(img)
					else:
						img = ImageTk.PhotoImage(img)

					self.stat_img[self.move_id[0]] = img
					self.stat_data[self.move_id[0]] = [self.stat_data[self.move_id[0]][0],self.stat_data[self.move_id[0]][1]]
					if self.move_id[-2] == "yoko":
						self.canvas.create_image((x1+x2)/2-1,(y1+y2)/2-1,image=self.stat_img[self.move_id[0]],tag=(self.move_id[0],"stat","yoko"))
					else:
						self.canvas.create_image((x1+x2)/2,(y1+y2)/2-1,image=self.stat_img[self.move_id[0]],tag=(self.move_id[0],"stat"))

	def click(self,event,canvas):
		if canvas == "main":
			closest_ids = self.canvas.find_closest(event.x, event.y)
			self.move_id = self.canvas.gettags(closest_ids[0])
			pos = self.canvas.bbox(self.move_id[0])
			if len(self.move_id) > 1:
				if not "counter" in self.move_id[1]:
					self.canvas.addtag_enclosed("move",pos[0]+1,pos[1]+1,pos[2]-1,pos[3]-1)
					self.canvas.addtag_withtag("move",self.move_id[0])
				else:
					self.canvas.addtag_withtag("move",self.move_id[0])
			self.x = event.x
			self.y = event.y
			self.card_count = 0
			self.canvas.delete(self.del_card)
			self.canvas.delete("system_log")
			self.canvas.lift(self.move_id[0])
			self.canvas.lift("system_reader")
			self.canvas.lift("system_reader_hp")
			self.canvas.lift("system_deck")
			self.canvas.lift("system_banished")
			self.canvas.lift("system_graveyard")
			self.canvas.lift("system_evo_deck")
			self.canvas.lift("system_hand")
			self.canvas.lift("system_temp")
			self.canvas.lift("system_pp")
			self.canvas.lift("system_max")
			self.canvas.lift("counter")
			self.canvas.lift("counter_num")
			self.canvas.lift("system_ep")
			self.canvas.lift("system_re")
			self.canvas.lift("system_dice")

			if self.move_id[-1] == "current":
				for i in self.field:
					if i[3] == self.move_id[0]:
						self.canvas.create_image(self.card_w*1.5,self.card_h*1.5,image=i[1],tag=i[3]+"big")
						self.del_card = i[3]+"big"
			else:
				self.canvas.delete(self.del_card)

			if self.move_id == ("system_deck","current"):
				self.hand.append(self.deck[0])
				self.deck.remove(self.deck[0])
				self.update()

			elif self.move_id == ("system_temp","current"):
				self.temp.append(self.deck[0])
				self.deck.remove(self.deck[0])
				self.update()

			elif self.move_id == ("system_re","current"):
				self.deck_shuffle()

			elif self.move_id == ("system_dice","current"):
				self.dice_count = 0
				self.dice_roll()

		elif canvas == "hand":
			closest_ids = self.hand_canvas.find_closest(event.x, event.y)
			ids = self.hand_canvas.gettags(closest_ids[0])

			if ids[-1] == "current":
				self.hand_canvas.delete(ids[0])
				for i in self.hand:
					if i[3] == ids[0]:
						self.field.append(i)
						if i[2] != [None,None]:
							img = Image.new("RGBA",self.size,(0, 0, 0,0))
							draw = ImageDraw.Draw(img)
							x,y = draw.textsize(str(i[2][1]),self.font_stat)
							draw.text((0,self.card_h-y-3),str(i[2][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
							_x,_y = draw.textsize(str(i[2][0]),self.font_stat)
							draw.text((self.card_w - _x,self.card_h-_y-3),str(i[2][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
							img = ImageTk.PhotoImage(img)

							self.stat_img[i[3]] = img
							self.stat_data[i[3]] = i[2]
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[i[3]],tag=(i[3],"stat"))
							self.card_count += 1
						else:
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.card_count += 1
						self.hand.remove(i)
				self.update()

		elif canvas == "deck":
			closest_ids = self.deck_canvas.find_closest(event.x, event.y)
			ids = self.deck_canvas.gettags(closest_ids[0])

			if ids[-1] == "current":
				self.deck_canvas.delete(ids[0])
				for i in self.deck:
					if i[3] == ids[0]:
						self.field.append(i)
						if i[2] != [None,None]:
							img = Image.new("RGBA",self.size,(0, 0, 0,0))
							draw = ImageDraw.Draw(img)
							x,y = draw.textsize(str(i[2][1]),self.font_stat)
							draw.text((0,self.card_h-y-3),str(i[2][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
							_x,_y = draw.textsize(str(i[2][0]),self.font_stat)
							draw.text((self.card_w - _x,self.card_h-_y-3),str(i[2][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
							img = ImageTk.PhotoImage(img)

							self.stat_img[i[3]] = img
							self.stat_data[i[3]] = i[2]
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[i[3]],tag=(i[3],"stat"))
							self.card_count += 1
						else:
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.card_count += 1
						self.deck.remove(i)
				self.update()

		elif canvas == "evo_deck":
			closest_ids = self.evo_deck_canvas.find_closest(event.x, event.y)
			ids = self.evo_deck_canvas.gettags(closest_ids[0])

			if ids[-1] == "current":
				self.evo_deck_canvas.delete(ids[0])
				for i in self.evo_deck:
					if i[3] == ids[0]:
						self.field.append(i)
						if i[2] != [None,None]:
							img = Image.new("RGBA",self.size,(0, 0, 0,0))
							draw = ImageDraw.Draw(img)
							x,y = draw.textsize(str(i[2][1]),self.font_stat)
							draw.text((0,self.card_h-y-3),str(i[2][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
							_x,_y = draw.textsize(str(i[2][0]),self.font_stat)
							draw.text((self.card_w - _x,self.card_h-_y-3),str(i[2][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
							img = ImageTk.PhotoImage(img)

							self.stat_img[i[3]] = img
							self.stat_data[i[3]] = i[2]
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[i[3]],tag=(i[3],"stat"))
							self.card_count += 1
						else:
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.card_count += 1
						self.evo_deck.remove(i)
				self.update()

		elif canvas == "temp":
			closest_ids = self.temp_canvas.find_closest(event.x, event.y)
			ids = self.temp_canvas.gettags(closest_ids[0])

			if ids[-1] == "current":
				self.temp_canvas.delete(ids[0])
				for i in self.temp:
					if i[3] == ids[0]:
						self.field.append(i)
						if i[2] != [None,None]:
							img = Image.new("RGBA",self.size,(0, 0, 0,0))
							draw = ImageDraw.Draw(img)
							x,y = draw.textsize(str(i[2][1]),self.font_stat)
							draw.text((0,self.card_h-y-3),str(i[2][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
							_x,_y = draw.textsize(str(i[2][0]),self.font_stat)
							draw.text((self.card_w - _x,self.card_h-_y-3),str(i[2][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
							img = ImageTk.PhotoImage(img)

							self.stat_img[i[3]] = img
							self.stat_data[i[3]] = i[2]
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[i[3]],tag=(i[3],"stat"))
							self.card_count += 1
						else:
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.card_count += 1
						self.temp.remove(i)
				self.update()

		elif canvas == "graveyard":
			closest_ids = self.graveyard_canvas.find_closest(event.x, event.y)
			ids = self.graveyard_canvas.gettags(closest_ids[0])

			if ids[-1] == "current":
				self.graveyard_canvas.delete(ids[0])
				for i in self.graveyard:
					if i[3] == ids[0]:
						self.field.append(i)
						if i[2] != [None,None]:
							img = Image.new("RGBA",self.size,(0, 0, 0,0))
							draw = ImageDraw.Draw(img)
							x,y = draw.textsize(str(i[2][1]),self.font_stat)
							draw.text((0,self.card_h-y-3),str(i[2][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
							_x,_y = draw.textsize(str(i[2][0]),self.font_stat)
							draw.text((self.card_w - _x,self.card_h-_y-3),str(i[2][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
							img = ImageTk.PhotoImage(img)

							self.stat_img[i[3]] = img
							self.stat_data[i[3]] = i[2]
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[i[3]],tag=(i[3],"stat"))
							self.card_count += 1
						else:
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.card_count += 1
						self.graveyard.remove(i)
				self.update()

		elif canvas == "banished":
			closest_ids = self.banished_canvas.find_closest(event.x, event.y)
			ids = self.banished_canvas.gettags(closest_ids[0])

			if ids[-1] == "current":
				self.banished_canvas.delete(ids[0])
				for i in self.banished:
					if i[3] == ids[0]:
						self.field.append(i)
						if i[2] != [None,None]:
							img = Image.new("RGBA",self.size,(0, 0, 0,0))
							draw = ImageDraw.Draw(img)
							x,y = draw.textsize(str(i[2][1]),self.font_stat)
							draw.text((0,self.card_h-y-3),str(i[2][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
							_x,_y = draw.textsize(str(i[2][0]),self.font_stat)
							draw.text((self.card_w - _x,self.card_h-_y-3),str(i[2][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
							img = ImageTk.PhotoImage(img)

							self.stat_img[i[3]] = img
							self.stat_data[i[3]] = i[2]
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=self.stat_img[i[3]],tag=(i[3],"stat"))
							self.card_count += 1
						else:
							self.canvas.create_image(self.canvas_w/2+self.card_w/2*self.card_count,self.canvas_h - self.card_h,image=i[0],tag=i[3])
							self.card_count += 1
						self.banished.remove(i)
				self.update()

	def field_drag(self,event):
		if self.move_id[-1] != "current" or self.move_id[-1] == "current" and self.move_id[-2] == "system_bg":
				self.canvas.delete("rect")
				self.canvas.create_rectangle(self.x,self.y,event.x,event.y,outline="red",tag="rect")
		if self.move_id[-1] == "current" and not "big" in self.move_id[0] and not "system" in self.move_id[0]:
			self.canvas.move("move",event.x - self.x,event.y - self.y)
			self.x = event.x
			self.y = event.y

	def field_release(self,event):
		#長方形を消す
		self.canvas.delete("rect")
		#canvas内の全図形のID取得,
		# all = self.canvas.find_all()
		tag_list = list(self.canvas.find_all())
		lll = []
		#moveタグで同時に移動したカードのIDを取得して重複削除する
		for i in tag_list:
			a = self.canvas.gettags(i)
			y = list(a)
			for i in y:
				if i == "move":
					lll.append(a[0])
		lll = list(set(lll))

		self.canvas.dtag("move","move")
		if self.move_id[-1] != "current" or self.move_id[-1] == "current" and self.move_id[-2] == "system_bg":
			self.canvas.addtag_overlapping("move",self.x,self.y,event.x,event.y)
			self.canvas.dtag("system_deck","move")
			self.canvas.dtag("system_evo_deck","move")
			self.canvas.dtag("system_hand","move")
			self.canvas.dtag("system_graveyard","move")
			self.canvas.dtag("system_reader","move")
			self.canvas.dtag("system_pp","move")
			self.canvas.dtag("system_max","move")
			self.canvas.dtag("system_ep","move")
			self.canvas.dtag("system_temp","move")
			self.canvas.dtag("system_banished","move")
			self.canvas.dtag("system_reader_hp","move")
			self.canvas.dtag("system_re","move")
			self.canvas.dtag("system_dice","move")

		closest_ids = self.canvas.find_closest(event.x, event.y)
		ids = self.canvas.gettags(closest_ids[0])
		if ids[-1] == "current":
			if lll == []:
				lll.append(self.move_id[0])
			if ids[0] == "system_graveyard":
				for l in lll:
					for i in self.field:
						if i[3] == l:
							pos = self.canvas.bbox(i[3])
							cards = list(self.canvas.find_enclosed(pos[0],pos[1],pos[2],pos[3]))
							if i[-1] == "token":
								self.field.remove(i)
								self.canvas.delete(i[3])
							else:
								if "yoko" in self.canvas.gettags(l):
									self.field.remove(i)
									for r in self.all_card:
										if r[2] == l:
											image = ImageTk.PhotoImage(r[0].resize(self.size))
											i = (image,i[1],i[2],i[3])
											self.graveyard.append(i)
								else:
									self.graveyard.append(i)
									self.field.remove(i)
							for i in cards:
								tag = self.canvas.gettags(i)
								if "counter" in tag or "counter_num" in tag:
									self.canvas.delete(tag[0])
								elif "token" in tag:
									self.canvas.delete(tag[0])
							self.canvas.delete(l)
							self.update()

			elif ids[0] == "system_temp":
				for l in lll:
					for i in self.field:
						if i[3] == l:
							pos = self.canvas.bbox(i[3])
							cards = list(self.canvas.find_enclosed(pos[0],pos[1],pos[2],pos[3]))
							if i[-1] == "token":
								self.field.remove(i)
								self.canvas.delete(i[3])
							else:
								if "yoko" in self.canvas.gettags(l):
									self.field.remove(i)
									for r in self.all_card:
										if r[2] == l:
											image = ImageTk.PhotoImage(r[0].resize(self.size))
											i = (image,i[1],i[2],i[3])
											self.temp.append(i)
								else:
									self.temp.append(i)
									self.field.remove(i)
							for i in cards:
								tag = self.canvas.gettags(i)
								if "counter" in tag or "counter_num" in tag:
									self.canvas.delete(tag[0])
								elif "token" in tag:
									self.canvas.delete(tag[0])
							self.canvas.delete(l)
							self.update()

			elif ids[0] == "system_banished":
				for l in lll:
					for i in self.field:
						if i[3] == l:
							pos = self.canvas.bbox(i[3])
							cards = list(self.canvas.find_enclosed(pos[0],pos[1],pos[2],pos[3]))
							if i[-1] == "token":
								self.field.remove(i)
								self.canvas.delete(i[3])
							else:
								if "yoko" in self.canvas.gettags(l):
									self.field.remove(i)
									for r in self.all_card:
										if r[2] == l:
											image = ImageTk.PhotoImage(r[0].resize(self.size))
											i = (image,i[1],i[2],i[3])
											self.banished.append(i)
								else:
									self.banished.append(i)
									self.field.remove(i)
							for i in cards:
								tag = self.canvas.gettags(i)
								if "counter" in tag or "counter_num" in tag:
									self.canvas.delete(tag[0])
								elif "token" in tag:
									self.canvas.delete(tag[0])
							self.canvas.delete(l)
							self.update()

			elif ids[0] == "system_hand":
				for l in lll:
					for i in self.field:
						if i[3] == l:
							pos = self.canvas.bbox(i[3])
							cards = list(self.canvas.find_enclosed(pos[0],pos[1],pos[2],pos[3]))
							if i[-1] == "token":
								self.field.remove(i)
								self.canvas.delete(i[3])
							else:
								if "yoko" in self.canvas.gettags(l):
									self.field.remove(i)
									for r in self.all_card:
										if r[2] == l:
											image = ImageTk.PhotoImage(r[0].resize(self.size))
											i = (image,i[1],i[2],i[3])
											self.hand.append(i)
								else:
									self.hand.append(i)
									self.field.remove(i)
							for i in cards:
								tag = self.canvas.gettags(i)
								if "counter" in tag or "counter_num" in tag:
									self.canvas.delete(tag[0])
								elif "token" in tag:
									self.canvas.delete(tag[0])
							self.canvas.delete(l)
							self.update()

			elif ids[0] == "system_deck":
				for l in lll:
					for i in self.field:
						if i[3] == l:
							pos = self.canvas.bbox(i[3])
							cards = list(self.canvas.find_enclosed(pos[0],pos[1],pos[2],pos[3]))
							if i[-1] == "token":
								self.field.remove(i)
								self.canvas.delete(i[3])
							else:
								if "yoko" in self.canvas.gettags(l):
									self.field.remove(i)
									for r in self.all_card:
										if r[2] == l:
											image = ImageTk.PhotoImage(r[0].resize(self.size))
											i = (image,i[1],i[2],i[3])
											self.deck.append(i)
								else:
									self.deck.append(i)
									self.field.remove(i)
							for i in cards:
								tag = self.canvas.gettags(i)
								if "counter" in tag or "counter_num" in tag:
									self.canvas.delete(tag[0])
								elif "token" in tag:
									self.canvas.delete(tag[0])
							self.canvas.delete(l)
							self.update()

			elif ids[0] == "system_evo_deck":
				for l in lll:
					for i in self.field:
						if i[3] == l:
							pos = self.canvas.bbox(i[3])
							cards = list(self.canvas.find_enclosed(pos[0],pos[1],pos[2],pos[3]))
							if i[-1] == "token":
								self.field.remove(i)
								self.canvas.delete(i[3])
							else:
								if "yoko" in self.canvas.gettags(l):
									self.field.remove(i)
									for r in self.all_card:
										if r[2] == l:
											image = ImageTk.PhotoImage(r[0].resize(self.size))
											i = (image,i[1],i[2],i[3])
											self.evo_deck.append(i)
								else:
									self.evo_deck.append(i)
									self.field.remove(i)
							for i in cards:
								tag = self.canvas.gettags(i)
								if "counter" in tag or "counter_num" in tag:
									self.canvas.delete(tag[0])
								elif "token" in tag:
									self.canvas.delete(tag[0])
							self.canvas.delete(l)
							self.update()

	def yoko(self,event):
		closest_ids = self.canvas.find_closest(event.x, event.y)
		self.move_id = self.canvas.gettags(closest_ids[0])
		x1,y1,x2,y2 = self.canvas.bbox(self.move_id[0])
		for i in self.field:
			if i[3] == self.move_id[0]:
				for u in self.all_card:
					if u[2] == self.move_id[0]:
						self.field.remove(i)
						self.canvas.delete(self.move_id[0])
						p = copy.copy(u)
						image = p[0].resize(self.size)
						big_image = ImageTk.PhotoImage(p[0])
						if self.move_id[-2] != "yoko":
							image = image.rotate(90,expand=True)
						image = ImageTk.PhotoImage(image)
						if u[-1] == "token":
							tpl = (image,big_image,p[1],p[2],"token")
						else:
							tpl = (image,big_image,p[1],p[2])
						self.field.append(tpl)
						for y in self.field:
							if y[3] == self.move_id[0]:
								if self.move_id[-2] != "yoko":
									if "token" in self.move_id:
										self.canvas.create_image((x1+x2)/2,(y1+y2)/2,image=y[0],tag=(y[3],"token","yoko"))
									else:
										self.canvas.create_image((x1+x2)/2,(y1+y2)/2,image=y[0],tag=(y[3],"yoko"))
								else:
									if "token" in self.move_id:
										self.canvas.create_image((x1+x2)/2,(y1+y2)/2,image=y[0],tag=(y[3],"token"))
									else:
										self.canvas.create_image((x1+x2)/2,(y1+y2)/2,image=y[0],tag=(y[3]))
						if p[1] != [None,None]:
							img = Image.new("RGBA",self.size,(0, 0, 0,0))
							draw = ImageDraw.Draw(img)
							x,y = draw.textsize(str(self.stat_data[self.move_id[0]][1]),self.font_stat)
							draw.text((0,self.card_h-y-3),str(self.stat_data[self.move_id[0]][1]),font=self.font_stat,fill="blue",stroke_width=2,stroke_fill='black')
							_x,_y = draw.textsize(str(self.stat_data[self.move_id[0]][0]),self.font_stat)
							draw.text((self.card_w - _x,self.card_h-_y-3),str(self.stat_data[self.move_id[0]][0]),font=self.font_stat,fill="red",stroke_width=2,stroke_fill='black')
							if self.move_id[-2] != "yoko":
								img = img.rotate(90,expand=True)
							img = ImageTk.PhotoImage(img)

							self.stat_img[self.move_id[0]] = img
							self.stat_data[self.move_id[0]] = [self.stat_data[self.move_id[0]][0],self.stat_data[self.move_id[0]][1]]
							if self.move_id[-2] != "yoko":
								if "token" in self.move_id:
									self.canvas.create_image((x1+x2)/2,(y1+y2)/2-1,image=self.stat_img[self.move_id[0]],tag=(self.move_id[0],"stat","token","yoko"))
								else:
									self.canvas.create_image((x1+x2)/2,(y1+y2)/2-1,image=self.stat_img[self.move_id[0]],tag=(self.move_id[0],"stat","yoko"))
							else:
								if "token" in self.move_id:
									self.canvas.create_image((x1+x2)/2,(y1+y2)/2-1,image=self.stat_img[self.move_id[0]],tag=(self.move_id[0],"stat","token"))
								else:
									self.canvas.create_image((x1+x2)/2,(y1+y2)/2-1,image=self.stat_img[self.move_id[0]],tag=(self.move_id[0],"stat"))
		self.canvas.lift("counter")
		self.canvas.lift("counter_num")

		if self.move_id[-1] == "current":
			for i in self.field:
				if i[3] == self.move_id[0]:
					self.canvas.create_image(self.card_w*1.5,self.card_h*1.5,image=i[1],tag=i[3]+"big")
					self.del_card = i[3]+"big"
		else:
			self.canvas.delete(self.del_card)

		if self.move_id == ("system_deck","current"):
			self.hand.append(self.deck[0])
			self.deck.remove(self.deck[0])
			self.update()

		if self.move_id == ("system_temp","current"):
			self.temp.append(self.deck[0])
			self.deck.remove(self.deck[0])
			self.update()

	def right_click(self,event,canvas):
		if canvas == "main":
			closest_ids = self.canvas.find_closest(event.x, event.y)
			self.move_id = self.canvas.gettags(closest_ids[0])

			if self.move_id == ("system_deck","current"):
				if self.deck_window != None:
					self.deck_window.destroy()
					self.deck_window = None
				self.deck_view = 1
				self.deck_window = tk.Toplevel()
				self.deck_window.geometry(f"{self.card_w*7}x{self.card_h*3}")
				self.deck_window.title("deck")
				self.deck_canvas = tk.Canvas(self.deck_window,width=self.card_w*7,height=self.card_h*3,bg=self.color)
				self.bind_canvas("deck")
				self.deck_canvas.pack()
				self.deck_window.protocol("WM_DELETE_WINDOW",lambda:self.deck_shuffle())
				deck_width = 0
				deck_width2 = 0
				deck_width3 = 0
				for i in range(len(self.deck)):
					if i < 13:
						self.deck_canvas.create_image(self.card_w/2 + deck_width,self.card_h/2,image=self.deck[i][0],tag=self.deck[i][3])
						deck_width = deck_width + self.card_w / 2
					elif i < 26:
						self.deck_canvas.create_image(self.card_w/2 + deck_width2,self.card_h/2+self.card_h,image=self.deck[i][0],tag=self.deck[i][3])
						deck_width2 = deck_width2 + self.card_w / 2
					else:
						self.deck_canvas.create_image(self.card_w/2 + deck_width3,self.card_h/2+self.card_h*2,image=self.deck[i][0],tag=self.deck[i][3])
						deck_width3 = deck_width3 + self.card_w / 2
				self.update()

			elif self.move_id == ("system_evo_deck","current"):
				if self.evo_deck_window != None:
					self.evo_deck_window.destroy()
					self.evo_deck_window = None
				self.evo_deck_view = 1
				self.evo_deck_window = tk.Toplevel()
				self.evo_deck_window.geometry(f"{self.card_w*7}x{self.card_h*2}")
				self.evo_deck_window.title("evo_deck")
				self.evo_deck_canvas = tk.Canvas(self.evo_deck_window,width=self.card_w*7,height=self.card_h*2,bg=self.color)
				self.bind_canvas("evo_deck")
				self.evo_deck_canvas.pack()
				self.evo_deck_window.protocol("WM_DELETE_WINDOW",lambda:self.close("evo_deck"))
				evo_deck_width = 0
				evo_deck_width2 = 0
				for i in range(len(self.evo_deck)):
					if i < 13:
						self.evo_deck_canvas.create_image(self.card_w/2 + evo_deck_width,self.card_h/2,image=self.evo_deck[i][0],tag=self.evo_deck[i][3])
						evo_deck_width = evo_deck_width + self.card_w / 2
					elif i < 26:
						self.evo_deck_canvas.create_image(self.card_w/2 + evo_deck_width2,self.card_h/2+self.card_h,image=self.evo_deck[i][0],tag=self.evo_deck[i][3])
						evo_deck_width2 = evo_deck_width2 + self.card_w / 2
				self.update()

			elif self.move_id == ("system_graveyard","current"):
				if self.graveyard_window != None:
					self.graveyard_window.destroy()
					self.graveyard_window = None
				self.graveyard_view = 1
				self.graveyard_window = tk.Toplevel()
				self.graveyard_window.geometry(f"{self.card_w*7}x{self.card_h*2}")
				self.graveyard_window.title("graveyard")
				self.graveyard_canvas = tk.Canvas(self.graveyard_window,width=self.card_w*7,height=self.card_h*2,bg=self.color)
				self.bind_canvas("graveyard")
				self.graveyard_canvas.pack()
				self.graveyard_window.protocol("WM_DELETE_WINDOW",lambda:self.close("graveyard"))
				graveyard_width = 0
				graveyard_width2 = 0
				for i in range(len(self.graveyard)):
					if i < 13:
						self.graveyard_canvas.create_image(self.card_w/2 + graveyard_width,self.card_h/2,image=self.graveyard[i][0],tag=self.graveyard[i][3])
						graveyard_width = graveyard_width + self.card_w / 2
					elif i < 26:
						self.graveyard_canvas.create_image(self.card_w/2 + graveyard_width2,self.card_h/2+self.card_h,image=self.graveyard[i][0],tag=self.graveyard[i][3])
						graveyard_width2 = graveyard_width2 + self.card_w / 2
				self.update()

			elif self.move_id == ("system_banished","current"):
				if self.banished_window != None:
					self.banished_window.destroy()
					self.banished_window = None
				self.banished_view = 1
				self.banished_window = tk.Toplevel()
				self.banished_window.geometry(f"{self.card_w*7}x{self.card_h*2}")
				self.banished_window.title("banished")
				self.banished_canvas = tk.Canvas(self.banished_window,width=self.card_w*7,height=self.card_h*2,bg=self.color)
				self.bind_canvas("banished")
				self.banished_canvas.pack()
				self.banished_window.protocol("WM_DELETE_WINDOW",lambda:self.close("banished"))
				banished_width = 0
				banished_width2 = 0
				for i in range(len(self.banished)):
					if i < 13:
						self.banished_canvas.create_image(self.card_w/2 + banished_width,self.card_h/2,image=self.banished[i][0],tag=self.banished[i][3])
						banished_width = banished_width + self.card_w / 2
					elif i < 26:
						self.banished_canvas.create_image(self.card_w/2 + banished_width2,self.card_h/2+self.card_h,image=self.banished[i][0],tag=self.banished[i][3])
						banished_width2 = banished_width2 + self.card_w / 2
				self.update()

			elif self.move_id == ("system_temp","current"):
				if self.temp_window != None:
					self.temp_window.destroy()
					self.temp_window = None
				self.temp_view = 1
				self.temp_window = tk.Toplevel()
				self.temp_window.geometry(f"{self.card_w*7}x{self.card_h*2}")
				self.temp_window.title("temp")
				self.temp_canvas = tk.Canvas(self.temp_window,width=self.card_w*7,height=self.card_h*2,bg=self.color)
				self.bind_canvas("temp")
				self.temp_canvas.pack()
				self.temp_window.protocol("WM_DELETE_WINDOW",lambda:self.close("temp"))
				temp_width = 0
				temp_width2 = 0
				for i in range(len(self.temp)):
					if i < 13:
						self.temp_canvas.create_image(self.card_w/2 + temp_width,self.card_h/2,image=self.temp[i][0],tag=self.temp[i][3])
						temp_width = temp_width + self.card_w / 2
					elif i < 26:
						self.temp_canvas.create_image(self.card_w/2 + temp_width2,self.card_h/2+self.card_h,image=self.temp[i][0],tag=self.temp[i][3])
						temp_width2 = temp_width2 + self.card_w / 2

				self.update()

			elif self.move_id == ("system_hand","current"):
				if self.hand_window != None:
					self.hand_window.destroy()
					self.hand_window = None
				mas_x = self.winfo_x()
				mas_y = self.winfo_y()
				mas_h = self.winfo_height()
				self.hand_window = tk.Toplevel()
				self.hand_window.geometry(f"1200x{self.card_h}+{mas_x}+{mas_y + mas_h}")
				self.hand_window.title("Hand")
				self.hand_canvas = tk.Canvas(self.hand_window,width=2400,height=self.card_h,bg=self.color)
				self.bind_canvas("hand")
				self.hand_canvas.pack()
				self.hand_canvas.delete("all")
				hand_width = 0
				for i in range(len(self.hand)):
					self.hand_canvas.create_image(self.card_w/2 + hand_width,self.card_h/2,image=self.hand[i][0],tag=self.hand[i][3])
					hand_width = hand_width + self.card_w / 2
				self.update()

			elif "token" in self.move_id or "counter" in self.move_id or "counter_num" in self.move_id:
				self.p_menu = tk.Menu(self.canvas,tearoff=0)
				self.p_menu.add_command(label="消去",command=lambda:self.delete())
				self.p_menu.post(event.x_root, event.y_root)

			elif self.move_id[-1] == "current" and not "system" in self.move_id[0]:
				self.p_menu = tk.Menu(self.canvas,tearoff=0)
				self.p_menu.add_command(label="デッキの 上 に置く",command=lambda:self.card_move("main","deck","up"))
				self.p_menu.add_command(label="デッキの 下 に戻す",command=lambda:self.card_move("main","deck","down"))
				self.p_menu.post(event.x_root, event.y_root)

			else:
				#範囲外に行ったカードをWindow内に戻す処理
				tag_list = list(self.canvas.find_all())
				for id in tag_list: # 全オブジェクトを列挙
					tag = self.canvas.itemcget(id,'tags') # タグ名を取得
					coord = self.canvas.coords(tag)
					if coord != [] and not "system" in tag and not "big" in tag:
						if coord[0] < self.card_w /2:
							self.canvas.move(tag,coord[0]*-1 + self.card_w/2,0)
						if coord[0] > 1200 - self.card_w /2:
							self.canvas.move(tag,1200-coord[0]-self.card_w*1.5,0)
						if coord[1] < self.card_h /2:
							self.canvas.move(tag,0,coord[1]*-1 + self.card_h/2)
						if coord[1] > 700 - self.card_h /2:
							self.canvas.move(tag,0,700-coord[1]-self.card_h)

		elif canvas == "hand":
			closest_ids = self.hand_canvas.find_closest(event.x, event.y)
			self.move_id = self.hand_canvas.gettags(closest_ids[0])
			self.p_menu = tk.Menu(self.canvas,tearoff=0)
			self.p_menu.add_command(label="大きい画像表示",command=lambda:self.big_img())
			self.p_menu.add_command(label="デッキの 上 に戻す",command=lambda:self.card_move("hand","deck","up"))
			self.p_menu.add_command(label="デッキの 下 に戻す",command=lambda:self.card_move("hand","deck","down"))
			self.p_menu.add_command(label="ランダムに1枚捨てる",command=lambda:self.card_move("hand","graveyard","random"))
			self.p_menu.post(event.x_root, event.y_root)

		elif canvas == "deck":
			closest_ids = self.deck_canvas.find_closest(event.x, event.y)
			self.move_id = self.deck_canvas.gettags(closest_ids[0])
			self.p_menu = tk.Menu(self.canvas,tearoff=0)
			self.p_menu.add_command(label="Handに入れる",command=lambda:self.card_move("deck","hand","down"))
			self.p_menu.add_command(label="Temporaryに入れる",command=lambda:self.card_move("deck","temp","down"))
			self.p_menu.add_command(label="大きい画像表示",command=lambda:self.big_img())
			self.p_menu.post(event.x_root, event.y_root)

		elif canvas == "evo_deck":
			closest_ids = self.evo_deck_canvas.find_closest(event.x, event.y)
			self.move_id = self.evo_deck_canvas.gettags(closest_ids[0])
			self.p_menu = tk.Menu(self.canvas,tearoff=0)
			self.p_menu.add_command(label="大きい画像表示",command=lambda:self.big_img())
			self.p_menu.post(event.x_root, event.y_root)

		elif canvas == "temp":
			closest_ids = self.temp_canvas.find_closest(event.x, event.y)
			self.move_id = self.temp_canvas.gettags(closest_ids[0])
			self.p_menu = tk.Menu(self.canvas,tearoff=0)
			self.p_menu.add_command(label="デッキの 上 に戻す",command=lambda:self.card_move("temp","deck","up"))
			self.p_menu.add_command(label="デッキの 下 に戻す",command=lambda:self.card_move("temp","deck","down"))
			self.p_menu.add_command(label="大きい画像表示",command=lambda:self.big_img())
			self.p_menu.post(event.x_root, event.y_root)

		elif canvas == "graveyard":
			closest_ids = self.graveyard_canvas.find_closest(event.x, event.y)
			self.move_id = self.graveyard_canvas.gettags(closest_ids[0])
			self.p_menu = tk.Menu(self.canvas,tearoff=0)
			self.p_menu.add_command(label="大きい画像表示",command=lambda:self.big_img())
			self.p_menu.post(event.x_root, event.y_root)

		elif canvas == "banished":
			closest_ids = self.banished_canvas.find_closest(event.x, event.y)
			self.move_id = self.banished_canvas.gettags(closest_ids[0])
			self.p_menu = tk.Menu(self.canvas,tearoff=0)
			self.p_menu.add_command(label="大きい画像表示",command=lambda:self.big_img())
			self.p_menu.post(event.x_root, event.y_root)

	def card_move(self,name,name2,post):
		if name == "deck":
			pool = self.deck
		elif name == "temp":
			pool = self.temp
		elif name == "hand":
			pool = self.hand
		elif name == "main":
			pool = self.field

		if name2 == "deck":
			pool2 = self.deck
		elif name2 == "temp":
			pool2 = self.temp
		elif name2 == "hand":
			pool2 = self.hand
		elif name2 == "main":
			pool2 = self.field
		elif name2 == "graveyard":
			pool2 = self.graveyard

		if post == "down":
			for i in pool:
				if i[3] == self.move_id[0]:
					pool2.append(i)
					pool.remove(i)
					self.update()
					if name == "main":
						self.canvas.delete(self.move_id[0])
		elif post == "up":
			for i in pool:
				if i[3] == self.move_id[0]:
					pool2.insert(0,i)
					pool.remove(i)
					self.update()
					if name == "main":
						self.canvas.delete(self.move_id[0])
		if post == "random":
			temp_pool = pool.copy()
			random.shuffle(temp_pool)
			pool2.append(temp_pool[0])
			pool.remove(temp_pool[0])
			self.update()
			self.log("ランダムに1枚捨てる")
		if name2 == "deck":
			if post == "up":
				self.log("カードをデッキの 上 に置く")
			elif post == "down":
				self.log("カードをデッキの 下 に戻す")

	def deck_shuffle(self):
		if self.shuffle_flag == 0:
			self.shuffle_flag = 1
			random.shuffle(self.deck)
			if self.deck_window != None:
				self.deck_window.destroy()
				self.deck_window = None
			self.deck_view = 0
			self.angle = 0
			self.roll()
		else:
			pass
		self.update()

	def dice_roll(self):
		self.canvas.delete("system_dice")
		dice = self.dice.copy()
		dice_list = [1,2,3,4,5,6]
		random.shuffle(dice_list)
		self.dice_var = dice_list[0]
		draw = ImageDraw.Draw(dice)
		x,y = dice.size
		draw.text((x/2,y/2),str(self.dice_var),font=self.font,fill="white",stroke_width=2,stroke_fill='black',anchor="mm")
		self.dice_img = ImageTk.PhotoImage(dice)
		self.canvas.create_image(self.canvas_w - self.card_w*2.7,100 + self.card_h*2 + 20 + 20,image=self.dice_img,tag="system_dice")
		if self.dice_count < 20:
			self.dice_count = self.dice_count + 1
			self.afff = self.master.after(32,lambda:self.dice_roll())
		else:
			self.master.after_cancel(self.afff)

	def roll(self):
		self.angle = self.angle + 3
		self.canvas.delete("system_re")
		re_img = Image.open("Evolve/img/re.png").resize((self.card_w-20,self.card_w-20))
		re_img = re_img.rotate(self.angle)
		self.re_img_angle = ImageTk.PhotoImage(re_img)
		self.canvas.create_image(self.canvas_w - self.card_w*1.5,self.card_h/2,image=self.re_img_angle,tag="system_re")
		if self.angle >= 360:
			self.shuffle_flag = 0
			self.master.after_cancel(self.aff)
		else:
			self.aff = self.master.after(8,lambda:self.roll())

	def close(self,name):
		if name == "evo_deck":
			if self.evo_deck_window != None:
				self.evo_deck_window.destroy()
			self.evo_deck_window = None
			self.evo_deck_view = 0
		elif name == "graveyard":
			if self.graveyard_window != None:
				self.graveyard_window.destroy()
			self.graveyard_window = None
			self.graveyard_view = 0
		elif name == "banished":
			if self.banished_window != None:
				self.banished_window.destroy()
			self.banished_window = None
			self.banished_view = 0
		elif name == "temp":
			if self.temp_window != None:
				self.temp_window.destroy()
			self.temp_window = None
			self.temp_view = 0
		elif name == "big":
			if self.big_window != None:
				self.big_window.destroy()
				self.big_window = None
		self.update()

	def delete(self):
		self.canvas.delete(self.move_id[0])

	def big_img(self):
		if self.big_window != None:
			self.big_window.destroy()
			self.big_window = None
		self.big_window = tk.Toplevel()
		self.big_window.geometry(f"{self.size[0]*3}x{self.size[1]*3}")
		self.big_window.title("Card")
		self.big_canvas = tk.Canvas(self.big_window,width=self.size[0]*3,height=self.size[1]*3,bg=self.color)
		self.big_canvas.pack()
		self.big_window.protocol("WM_DELETE_WINDOW",lambda:self.close("big"))
		if self.move_id[-1] == "current":
			for i in self.all_card:
				if i[2] == self.move_id[0]:
					self.image_ = ImageTk.PhotoImage(i[0])
					self.big_canvas.create_image(self.size[0]*3/2,self.size[1]*3/2,image=self.image_,tag=i[2])

	def bind_canvas(self,canvas):
		if canvas == "main":
			self.canvas.bind("<MouseWheel>",lambda e:self.spin(e))
			self.canvas.bind("<Button-1>",lambda e:self.click(e,"main"))
			self.canvas.bind("<Button1-Motion>",lambda e:self.field_drag(e))
			self.canvas.bind("<ButtonRelease-1>",lambda e:self.field_release(e))
			self.canvas.bind("<Button-3>",lambda e:self.right_click(e,"main"))
			self.canvas.bind("<Double-Button-1>", lambda e:self.yoko(e))

		elif canvas == "hand":
			self.hand_canvas.bind("<Button-1>",lambda e:self.click(e,"hand"))
			self.hand_canvas.bind("<Button-3>",lambda e:self.right_click(e,"hand"))

		elif canvas == "deck":
			self.deck_canvas.bind("<Button-1>",lambda e:self.click(e,"deck"))
			self.deck_canvas.bind("<Button-3>",lambda e:self.right_click(e,"deck"))

		elif canvas == "evo_deck":
			self.evo_deck_canvas.bind("<Button-1>",lambda e:self.click(e,"evo_deck"))
			self.evo_deck_canvas.bind("<Button-3>",lambda e:self.right_click(e,"evo_deck"))

		elif canvas == "temp":
			self.temp_canvas.bind("<Button-1>",lambda e:self.click(e,"temp"))
			self.temp_canvas.bind("<Button-3>",lambda e:self.right_click(e,"temp"))

		elif canvas == "graveyard":
			self.graveyard_canvas.bind("<Button-1>",lambda e:self.click(e,"graveyard"))
			self.graveyard_canvas.bind("<Button-3>",lambda e:self.right_click(e,"graveyard"))

		elif canvas == "banished":
			self.banished_canvas.bind("<Button-1>",lambda e:self.click(e,"banished"))
			self.banished_canvas.bind("<Button-3>",lambda e:self.right_click(e,"banished"))

	def log(self,word):
		self.canvas.delete("system_log")
		self.canvas.create_text(self.canvas_w/2,0,text=word,anchor="n",font=self.font2,fill=self.font_color,tag="system_log")

def main():
	win = tk.Tk()
	app = Application(master = win)
	app.mainloop()

if __name__ == "__main__":
    main()


