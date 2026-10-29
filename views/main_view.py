import tkinter as tk

from views.customer_view import CustomerView
from views.appointment_view import AppointmentView
from views.offering_view import OfferingView


class MainView:
    def __init__(
        self,
        root,
        customer_controller,
        appointment_controller,
        offering_service
    ):
        self.root = root
        self.customer_controller = customer_controller
        self.appointment_controller = appointment_controller
        self.offering_service = offering_service

        self.root.title("Healthcare & Wellness Center")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()

        self.root.geometry("600x500")

        self.main_frame = tk.Frame(self.root, padx=30, pady=30)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Healthcare & Wellness Center",
            font=("Arial", 20, "bold")
        ).pack(pady=(20, 15))

        tk.Label(
            self.main_frame,
            text="Welcome! Please choose an option.",
            font=("Arial", 12)
        ).pack(pady=(0, 20))

        tk.Button(
            self.main_frame,
            text="Customer View",
            font=("Arial", 12),
            width=22,
            height=2,
            command=self.open_customer_view
        ).pack(pady=6)

        tk.Button(
            self.main_frame,
            text="Appointment View",
            font=("Arial", 12),
            width=22,
            height=2,
            command=self.open_appointment_view
        ).pack(pady=6)

        tk.Button(
            self.main_frame,
            text="Offering Management",
            font=("Arial", 12),
            width=22,
            height=2,
            command=self.open_offering_view
        ).pack(pady=6)

    def open_customer_view(self):
        self.clear_window()

        CustomerView(
            self.root,
            self.customer_controller,
            self.show_main_menu
        )

    def open_appointment_view(self):
        self.clear_window()

        AppointmentView(
            self.root,
            self.appointment_controller,
            self.customer_controller,
            self.show_main_menu
        )

    def open_offering_view(self):
        self.clear_window()

        OfferingView(
            self.root,
            self.offering_service,
            self.show_main_menu
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()