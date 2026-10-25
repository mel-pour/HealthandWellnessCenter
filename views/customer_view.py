from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from utils.component import *



def save():
    pass



win = Tk("customer page")
win.geometry("500x500")
win.title("login page")

# customer_id
customer_id = LabelAndEntry(win, text="Customer_Id :", x=20, y=20)
# name
name = LabelAndEntry(win, text="Name :", x=20, y=60)
# family
family = LabelAndEntry(win, text="family :", x=20, y=100, dtype=IntVar)
# social_id
social_id = LabelAndEntry(win, text="social_id :", x=20, y=140)
# age
age = LabelAndEntry(win, text="age :", x=20, y=180, dtype=IntVar)
# gender
gender = LabelAndEntry(win, text="gender :", x=20, y=220)
# phone_number
phone_number = LabelAndEntry(win, text="phone_number :", x=20, y=260)
# balance
balance = LabelAndEntry(win, text="balance :", x=20, y=300)
# role = LabelAndEntry(win, text="Role :", x=20, y=340)
# Label(win, text="Role :").place(x=20, y=340)
# listbox = tkinter.Listbox(win)
# listbox.place(x=120, y=340, width=125, height=55)
# listbox.insert(1, "customer")
# listbox.insert(2, "employee")
# listbox.insert(3, "administrator")
# role = listbox.get(listbox.curselection())

Button(win, text="Sign up", width=7).place(x=60, y=430)
Button(win, text="Log in", width=7).place(x=180, y=430)

win.mainloop()
