import threading 
from time import sleep
from pygame import mixer
from typing import Tuple
import ttkbootstrap as tb
from tkinter import filedialog
mixer.init()
class Music(tb.Window):
  def __init__(self):
    super().__init__(themename='vapor')
    self.geometry('400x250')
    self.resizable(False , False)
    self.title('boombBox')
    self.iconbitmap(r'icons\boombbox.ico')
    self.flag = True
    self.volume_status = 10
    self.mp3()
    self.bind('<MouseWheel>' , self.set_music_volume) 
  def mp3(self):
    self.main_frame = tb.Frame(self)
    self.main_frame.pack(expand=True , fill='both')
    self.main_frame.columnconfigure((0,1,2,3,4) , weight=1 , uniform='a')
    self.main_frame.rowconfigure((0,1,2,3,4,5) , weight=1 , uniform='a')

    self.lbl = tb.Label(self.main_frame ,width=100)
    self.lbl.grid(row=0 ,column=0 , columnspan = 4)

    self.volume = tb.Scale(self.main_frame , from_=0 , to=100)
    self.volume.grid(row=4 , column=3 ,sticky='ewns' ,padx=5)
    self.volume.set(self.volume_status)
    mixer.music.set_volume(0.1)
    self.volume.configure(command=self.music_volume)

    self.play_btn  = tb.Button(self.main_frame , text='Play')
    self.next_btn  = tb.Button(self.main_frame , text='Next')
    self.last_bnt  = tb.Button(self.main_frame , text='Last')
    self.brows_bnt = tb.Button(self.main_frame, text='📁')
    self.stop_btn  = tb.Button(self.main_frame , text='||')
    
    self.brows_bnt.grid(row=4 , column=0)
    self.last_bnt.grid(row=5 , column=0 ,sticky='ew')
    self.stop_btn.grid(row=5 , column=1 , columnspan=2 , sticky='ew' ,padx=10)
    self.next_btn.grid(row=5 , column=3 , sticky='ew')
    self.play_btn.grid(row=4 , column=1 , sticky='ew' ,columnspan=2 , padx=10)

    self.int_var =  tb.IntVar()
    self.next_var = tb.BooleanVar()
    self.last_var = tb.BooleanVar()
    self.brows_bnt.configure(command=self.openfile)
    self.play_btn.configure(command= lambda : self.int_var.set(1))
    self.stop_btn.configure(command=self.pause_)


  
  def openfile(self):
    self.int_var.set(0)
    self.path = filedialog.askopenfilename(initialdir=r'D:\fun\musics',filetypes=[('mp3 files' , "*.mp3")],multiple=1)
    self.play_music()



    
  def play_music(self):
    self.int_var.set(1)
    self.next_btn.configure(command = lambda : self.next_var.set(True))
    self.last_bnt.configure(command = lambda : self.last_var.set(True))
    self.flag = True
    while True:
        curent_mp3 = 0
        pointer = 0
        if self.int_var.get() == 1:
          th = threading.Thread(target=self.music_list , args=(curent_mp3 , pointer))
          th.start()
          break
        else:
          break



  def pause_(self):
    if self.flag:
      self.flag = False
      self.stop_btn.configure(text='\\>')
    else:
      self.flag = True
      self.stop_btn.configure(text='||')

  def music_volume(self , e):
    volume = self.volume.get() / 100
    mixer.music.set_volume(volume)

  def set_music_volume(self , e):
    if e.delta > 0:
      self.volume_status +=2
      if self.volume_status >=100:
        self.volume_status = 100
    else:
      self.volume_status -=2
      if self.volume_status <= 0 :
        self.volume_status = 0
        
    self.volume.set(self.volume_status)
    volume = self.volume.get() / 100
    mixer.music.set_volume(volume)


  def music_list(self , curent_mp3 , pointer):
    for pointer in range(len(self.path)):
      if self.int_var.get() == 0:
        break 
      if curent_mp3 < 0:
        curent_mp3 +=len(self.path)
      curent_mp3 +=1 
      if curent_mp3 >=len(self.path):
        curent_mp3 = 0
      pointer = curent_mp3
      mixer.music.load(self.path[pointer])
      mixer.music.play()
      music_name = self.path[pointer].split('/')
      self.lbl.configure(text =f'{music_name[-1]}')
      while mixer.music.get_busy():
          if self.int_var.get() == 0:
            break
          sleep(1)
          while self.flag == False:
              mixer.music.pause()

          if self.flag == True:
            mixer.music.unpause()           

          if self.last_var.get():
            self.last_var.set(False)
            pointer = pointer-1
            if pointer<=-len(self.path): 
              pointer = 0
            curent_mp3 = pointer
            mixer.music.load(self.path[pointer])
            mixer.music.play()
            music_name = self.path[pointer].split('/')
            self.lbl.configure(text =f'{music_name[-1]}')

          if self.next_var.get():
            self.next_var.set(False)
            pointer = pointer + 1
            if pointer >= len(self.path):
              pointer = 0
            curent_mp3 = pointer
            mixer.music.load(self.path[pointer])
            mixer.music.play()
            music_name = self.path[pointer].split('/')
            self.lbl.configure(text =f'{music_name[-1]}')
          
          if mixer.music.get_busy() == False :
            self.next_var.set(False)
            break



Music().mainloop()




