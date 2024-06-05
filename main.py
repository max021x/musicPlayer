from typing import Tuple
from customtkinter import *
from tkinter.filedialog import askopenfile
from tkinter import filedialog
set_default_color_theme('dark-blue')

class Music(CTk):
  def __init__(self,fg_color: str | Tuple[str, str] | None = None, **kwargs):
    super().__init__(fg_color, **kwargs)
    self.geometry('400x250')
    self.resizable(False , False)
    self.title('boombBox')
    self.iconbitmap(r'icons\boombbox.ico')
    self.mp3()
  
  def mp3(self):
    self.main_frame = CTkFrame(self)
    self.main_frame.pack(expand=True , fill='both')
    self.main_frame.columnconfigure((0,1,2,3,4) , weight=1 , uniform='a')
    self.main_frame.rowconfigure((0,1,2,3,4,5) , weight=1 , uniform='a')

    self.play_btn = CTkButton(self.main_frame , text='Play')
    self.next_btn = CTkButton(self.main_frame , text='Next')
    self.last_bnt = CTkButton(self.main_frame , text='Last')
    self.brwos_bnt = CTkButton(self.main_frame, text='📁' , font=('arial',20),width=15)
    
    self.brwos_bnt.grid(row=4, column=0,sticky='e')
    self.play_btn.grid(row=5 ,column=2 , padx=10)
    self.next_btn.grid(row=5 ,column=3 , columnspan=2)
    self.last_bnt.grid(row=5 ,column=0 , columnspan=2)

    self.brwos_bnt.configure(command=self.openfile)
    
  def openfile(self):
    self.path = filedialog.askopenfilename(initialdir='/',filetypes=[('mp3 files' , "*.mp3")],multiple=1)
    return self.path

Music().mainloop()





