
import tkinter as tk
from tkinter import ttk

from customer_view import CustomerView
from appointment_view import AppointmentView


class WellnessCenterApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Wellness Center Management System")
        self.root.geometry("700x450")
        self.root.minsize(600, 400)

        self.create_widgets()

    def create_widgets(self):
        # Main title
        title = ttk.Label(
            self.root,
            text="Wellness Center Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(45, 15))

        # Welcome message
        welcome = ttk.Label(
            self.root,
            text="Choose the section you want to access:",
            font=("Arial", 12)
        )
        welcome.pack(pady=10)

        # Main menu frame
        button_frame = ttk.Frame(self.root, padding=20)
        button_frame.pack(expand=True)

        # Customer View button
        customer_button = ttk.Button(
            button_frame,
            text="Customer View",
            command=self.open_customer_view,
            width=30
        )
        customer_button.pack(pady=15, ipady=20)

        # Appointment View button
        appointment_button = ttk.Button(
            button_frame,
            text="Appointment View",
            command=self.open_appointment_view,
            width=30
        )
        appointment_button.pack(pady=15, ipady=20)

    def open_customer_view(self):
        customer_window = tk.Toplevel(self.root)
        CustomerView(customer_window)

    def open_appointment_view(self):
        appointment_window = tk.Toplevel(self.root)
        AppointmentView(appointment_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = WellnessCenterApp(root)
    root.mainloop()
