from typing import Tuple
from customtkinter import *
set_default_color_theme('dark-blue')

class Music(CTk):
  def __init__(self,fg_color: str | Tuple[str, str] | None = None, **kwargs):
    super().__init__(fg_color, **kwargs)
    self.geometry('500x550')
    self.title('boombBox')
    self.iconbitmap(r'icons\boombbox.ico')






Music().mainloop()





