# # Search By Name
# name_search = StringVar()
# Label(win, text="Search Name").place(x=250, y=20)
# Entry(win, textvariable=name_search).place(x=350, y=20)


from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from utils.component import *



def save():
    pass



win = Tk("customer page")
win.geometry("500x500")
win.title("login page")

# appointment_id
appointment_id = LabelAndEntry(win, text="Appointment_Id :", x=20, y=20)
# date
date = LabelAndEntry(win, text="Date(YYYY-MM-DD) :", x=20, y=60)
# start_time
family = LabelAndEntry(win, text="Start_time(HH:MM) :", x=20, y=100, dtype=IntVar)
# status
status = LabelAndEntry(win, text="Status :", x=20, y=140)
# balance
balance = LabelAndEntry(win, text="balance :", x=20, y=180)
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
