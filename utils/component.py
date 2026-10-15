from tkinter import *

class LabelAndEntry:
    def __init__(self, window, text, x,y,distance=120, dtype = StringVar):
        Label(window, text=text).place(x=x, y=y)
        self.__variable = dtype()
        Entry(window, textvariable=self.__variable).place(x=x+distance, y=y)

    def get(self):
        return self.__variable.get()

    def set(self,value):
        self.__variable.set(value)




__all__ = ["LabelAndEntry"]