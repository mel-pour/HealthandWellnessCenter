import tkinter as tk

from views.customer_view import CustomerView


class MainView:
    def __init__(self, root, customer_controller):
        self.root = root
        self.customer_controller = customer_controller

        self.root.title("Healthcare & Wellness Center")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()

        self.main_frame = tk.Frame(self.root, padx=30, pady=30)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Healthcare & Wellness Center",
            font=("Arial", 20, "bold")
        ).pack(pady=(30, 15))

        tk.Label(
            self.main_frame,
            text="Welcome! Please choose an option.",
            font=("Arial", 12)
        ).pack(pady=(0, 35))

        tk.Button(
            self.main_frame,
            text="Customer View",
            font=("Arial", 12),
            width=22,
            height=2,
            command=self.open_customer_view
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Appointment View",
            font=("Arial", 12),
            width=22,
            height=2,
            command=self.show_appointment_message
        ).pack(pady=10)

    def open_customer_view(self):
        self.clear_window()

        CustomerView(
            self.root,
            self.customer_controller,
            self.show_main_menu
        )

    def show_appointment_message(self):
        from tkinter import messagebox

        messagebox.showinfo(
            "Coming Soon",
            "We'll implement the Appointment View later."
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()