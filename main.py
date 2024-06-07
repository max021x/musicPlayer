import threading 
from time import sleep
from pygame import mixer
from typing import Tuple
from customtkinter import *
from tkinter import filedialog
set_default_color_theme('dark-blue')
mixer.init()
class Music(CTk):
  def __init__(self,fg_color: str | Tuple[str, str] | None = None, **kwargs):
    super().__init__(fg_color, **kwargs)
    self.geometry('400x250')
    self.resizable(False , False)
    self.title('boombBox')
    self.iconbitmap(r'icons\boombbox.ico')
    self.mp3()
    self.flag = True
  def mp3(self):
    self.main_frame = CTkFrame(self)
    self.main_frame.pack(expand=True , fill='both')
    self.main_frame.columnconfigure((0,1,2,3,4) , weight=1 , uniform='a')
    self.main_frame.rowconfigure((0,1,2,3,4,5) , weight=1 , uniform='a')

    self.play_btn = CTkButton(self.main_frame , text='Play')
    self.next_btn = CTkButton(self.main_frame , text='Next')
    self.last_bnt = CTkButton(self.main_frame , text='Last')
    self.brows_bnt = CTkButton(self.main_frame, text='📁' , font=('arial',20),width=15)
    self.stop_btn = CTkButton(self.main_frame , text='Stop')
    
    self.brows_bnt.grid(row=4, column=0,sticky='e')
    self.play_btn.grid(row=5 ,column=2 , padx=10)
    self.next_btn.grid(row=5 ,column=3 , columnspan=2)
    self.last_bnt.grid(row=5 ,column=0 , columnspan=2)
    self.stop_btn.grid(row=4 , column=2)

    self.int_var = IntVar()
    self.next_var = BooleanVar()
    self.last_var = BooleanVar()
    self.brows_bnt.configure(command=self.openfile)
    self.play_btn.configure(command= lambda : self.int_var.set(1))
    self.stop_btn.configure(command=self.pause_)
  def openfile(self):
    self.path = filedialog.askopenfilename(initialdir=r'D:\fun\musics',filetypes=[('mp3 files' , "*.mp3")],multiple=1)
    self.th = threading.Thread(target=self.play_music)
    self.th.start()
    
  def play_music(self):
    self.play_btn.wait_variable(self.int_var)
    self.next_btn.configure(command = lambda : self.next_var.set(True))
    self.last_bnt.configure(command=lambda : self.last_var.set(True))
    while True:
        curent_mp3 = 0
        pointer = 0 
        for pointer in range(len(self.path)):
          if curent_mp3 < 0:
            curent_mp3 +=len(self.path)
          curent_mp3 +=1 
          if curent_mp3 >=len(self.path):
            curent_mp3 = 0
          pointer = curent_mp3
          mixer.music.load(self.path[pointer])
          mixer.music.play()
          print(pointer)
          while mixer.music.get_busy():
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
                print(pointer)

              if self.next_var.get():
                self.next_var.set(False)
                pointer = pointer + 1
                if pointer >= len(self.path):
                  pointer = 0
                curent_mp3 = pointer
                mixer.music.load(self.path[pointer])
                mixer.music.play()
                print(pointer)
              

              if mixer.music.get_busy() == False :
                self.next_var.set(False)
                break
                

  def pause_(self):
    if self.flag:
      self.flag = False
    else:
      self.flag = True
  

Music().mainloop()





