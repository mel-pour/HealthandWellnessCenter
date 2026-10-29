import tkinter as tk
from tkinter import messagebox


class CustomerView:
    def __init__(self, root, customer_controller, back_callback):
        self.root = root
        self.customer_controller = customer_controller
        self.back_callback = back_callback

        self.main_frame = tk.Frame(self.root, padx=20, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            self.main_frame,
            text="Customer View",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Customer search
        search_frame = tk.Frame(self.main_frame)
        search_frame.pack(fill="x", pady=10)

        tk.Label(
            search_frame,
            text="Customer ID:",
            font=("Arial", 11)
        ).pack(side="left", padx=(0, 10))

        self.customer_id_entry = tk.Entry(search_frame, width=15)
        self.customer_id_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Search Customer",
            command=self.search_customer
        ).pack(side="left", padx=10)

        # Customer information
        self.info_frame = tk.LabelFrame(
            self.main_frame,
            text="Customer Information",
            padx=15,
            pady=15
        )
        self.info_frame.pack(fill="x", pady=10)

        self.name_label = self.create_info_row("Name:")
        self.age_label = self.create_info_row("Age:")
        self.gender_label = self.create_info_row("Gender:")
        self.phone_label = self.create_info_row("Phone:")
        self.balance_label = self.create_info_row("Account Balance:")

        # Buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Add Balance",
            width=15,
            command=self.add_balance
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Create Customer",
            width=15,
            command=self.show_create_customer
        ).pack(side="left", padx=5)

        tk.Button(
            self.main_frame,
            text="Back to Main Menu",
            command=self.back_callback
        ).pack(pady=10)

        self.current_customer_id = None

    def create_info_row(self, label_text):
        """Create one row for displaying customer information."""
        row = tk.Frame(self.info_frame)
        row.pack(fill="x", pady=4)

        tk.Label(
            row,
            text=label_text,
            width=18,
            anchor="w",
            font=("Arial", 10, "bold")
        ).pack(side="left")

        value_label = tk.Label(
            row,
            text="-",
            anchor="w",
            font=("Arial", 10)
        )
        value_label.pack(side="left")

        return value_label

    def search_customer(self):
        customer_id_text = self.customer_id_entry.get().strip()

        if not customer_id_text:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a customer ID."
            )
            return

        try:
            customer_id = int(customer_id_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Customer ID must be a number."
            )
            return

        success, message, customer = (
            self.customer_controller.get_customer(customer_id)
        )

        if not success:
            self.clear_customer_info()
            self.current_customer_id = None
            messagebox.showerror("Customer Search", message)
            return

        self.current_customer_id = customer.customer_id

        self.name_label.config(text=customer.name)
        self.age_label.config(text=str(customer.age))
        self.gender_label.config(text=customer.gender)
        self.phone_label.config(text=customer.phone_number)
        self.balance_label.config(text=f"{customer.balance:.2f}")

    def clear_customer_info(self):
        self.name_label.config(text="-")
        self.age_label.config(text="-")
        self.gender_label.config(text="-")
        self.phone_label.config(text="-")
        self.balance_label.config(text="-")

    def add_balance(self):
        messagebox.showinfo(
            "Coming Soon",
            "We'll implement the Add Balance form in the next step."
        )

    def show_create_customer(self):
        messagebox.showinfo(
            "Coming Soon",
            "We'll implement the Create Customer form in the next step."
        )