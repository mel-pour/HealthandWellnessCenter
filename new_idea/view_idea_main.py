
import tkinter as tk
from tkinter import ttk


class WellnessCenterApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Wellness Center Management System")
        self.root.geometry("900x600")
        self.root.minsize(700, 450)

        self.create_widgets()

    def create_widgets(self):

        # Main title
        title = ttk.Label(
            self.root,
            text="Wellness Center Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        # Main navigation tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Customer tab
        self.customer_tab = ttk.Frame(
            self.notebook,
            padding=20
        )

        self.notebook.add(
            self.customer_tab,
            text="Customers"
        )

        self.create_customer_overview()

        # Appointment tab
        self.appointment_tab = ttk.Frame(
            self.notebook,
            padding=20
        )

        self.notebook.add(
            self.appointment_tab,
            text="Appointments"
        )

        self.create_appointment_overview()

    def create_customer_overview(self):

        ttk.Label(
            self.customer_tab,
            text="Customer Management",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        ttk.Label(
            self.customer_tab,
            text=(
                "Create new customer accounts and manage "
                "customer information."
            ),
            wraplength=500,
            justify="center"
        ).pack(pady=10)

        ttk.Button(
            self.customer_tab,
            text="Open Customer View",
            command=self.open_customer_view
        ).pack(pady=15)

    def create_appointment_overview(self):

        ttk.Label(
            self.appointment_tab,
            text="Appointment Management",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        ttk.Label(
            self.appointment_tab,
            text=(
                "Find customers, view their appointments, "
                "book new appointments, and process cancellations."
            ),
            wraplength=500,
            justify="center"
        ).pack(pady=10)

        ttk.Button(
            self.appointment_tab,
            text="Open Appointment View",
            command=self.open_appointment_view
        ).pack(pady=15)

    def open_customer_view(self):
        self.notebook.select(self.customer_tab)

        # The existing Customer View will be connected here.

    def open_appointment_view(self):
        self.notebook.select(self.appointment_tab)

        # The existing Appointment View will be connected here.


if __name__ == "__main__":

    root = tk.Tk()
    app = WellnessCenterApp(root)
    root.mainloop()
