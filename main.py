import eyed3 , io
from PIL import Image , ImageTk
import threading 
import ttkbootstrap as tb
from time import sleep
from pygame import mixer
from tkinter import filedialog
mixer.init()
class Music(tb.Window):
  _old_playlist= ()
  _old_img = []
  def __init__(self):
    super().__init__(themename='vapor')
    self.geometry('400x250')
    self.resizable(False , False)
    self.title('boombBox')
    self.iconbitmap(r'icons\boombbox.ico')
    self.flag = True
    self.getbusy = False
    self.volume_status = 10
    self.img_list = []
    self.mp3()
    self.bind('<MouseWheel>' , self.set_music_volume) 
  def mp3(self):
    self.main_frame = tb.Frame(self)
    self.main_frame.pack(expand=True , fill='both')
    self.main_frame.columnconfigure((0,1,2,3,4,5) , weight=1 , uniform='a')
    self.main_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10) , weight=1 , uniform='a')

    

    self.lbl = tb.Label(self.main_frame, width=100 , text='?')
    self.lbl.grid(row=8 , column=0 , columnspan = 4)

    self.image = tb.Label(self.main_frame)
    self.image.place(x=120 ,y=5)

    self.volume = tb.Scale(self.main_frame , from_=0 , to=100)
    self.volume.grid(row=6 , column=3 , rowspan=2 ,padx=5 , sticky='nsew')
    self.volume.set(self.volume_status)
    mixer.music.set_volume(0.1)
    self.volume.configure(command=self.music_volume)

    self.next_btn  = tb.Button(self.main_frame , text='Next')
    self.last_bnt  = tb.Button(self.main_frame , text='Last')
    self.brows_bnt = tb.Button(self.main_frame, text='📁')
    self.stop_btn  = tb.Button(self.main_frame , text='||')
    
    self.brows_bnt.grid(row=6 ,rowspan=2 , column=0 ,sticky='w')
    self.last_bnt.grid(row=9 , column=0 ,rowspan=2,sticky='ew')
    self.stop_btn.grid(row=9 , column=1 ,rowspan=2, columnspan=2 , sticky='ew' ,padx=10)
    self.next_btn.grid(row=9 , column=3 ,rowspan=2, sticky='ew')

    self.int_var =  tb.IntVar()
    self.next_var = tb.BooleanVar()
    self.last_var = tb.BooleanVar()
    self.brows_bnt.configure(command=self.openfile)
    self.stop_btn.configure(command=self.pause_)


  
  def openfile(self):

      self.int_var.set(0)
      self.img_list.clear()
      self.path = filedialog.askopenfilename(initialdir=r'D:\fun\musics',filetypes=[('mp3 files' , "*.mp3")],multiple=1)
      
      if len(self.path)>0:
          Music._old_img.clear()
          for musics in self.path:
            file = eyed3.load(musics)
            for i in file.tag.images:
              img = ImageTk.PhotoImage(Image.open(io.BytesIO(i.image_data)).resize(size=(150,150)))
              self.img_list.append(img)
              Music._old_img.append(img)
          Music._old_playlist = self.path
          #  passing path to the play_music but in another way
      
      elif self.getbusy and len(self.path) < 1:
        self.path = Music._old_playlist
        for i in Music._old_img:
          self.img_list.append(i)
      
      self.play_music()

    
  def play_music(self):
    self.int_var.set(1)
    self.next_btn.configure(command = lambda : self.next_var.set(True))
    self.last_bnt.configure(command = lambda : self.last_var.set(True))
    self.flag = True
    curent_mp3 = 0
    pointer = 0
    if self.int_var.get() == 1:
      th = threading.Thread(target=self.music_list , args=(curent_mp3 , pointer))
      th.start()


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
      self.image.configure(image=self.img_list[pointer])
      while mixer.music.get_busy():
          self.getbusy = True
          
          if self.int_var.get() == 0:
            break
          sleep(0.1)
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
            self.image.configure(image=self.img_list[pointer])


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
            self.image.configure(image=self.img_list[pointer])

          
          if mixer.music.get_busy() == False :
            self.next_var.set(False)
            self.getbusy = False
            break



Music().mainloop()




