import tkinter as tk
from tkinter import messagebox, ttk
from decimal import Decimal, InvalidOperation



class CustomerView:
    def __init__(self, root, customer_controller, back_callback):
        self.root = root
        self.customer_controller = customer_controller
        self.back_callback = back_callback
        self.current_customer_id = None

        self.main_frame = tk.Frame(root, padx=20, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            self.main_frame,
            text="Customer View",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 12))

        # Search area
        search_frame = tk.Frame(self.main_frame)
        search_frame.pack(fill="x", pady=5)

        tk.Label(search_frame, text="Customer ID:").pack(side="left")

        self.customer_id_entry = tk.Entry(search_frame, width=12)
        self.customer_id_entry.pack(side="left", padx=8)

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_customer
        ).pack(side="left")

        # Customer information
        self.info_frame = tk.LabelFrame(
            self.main_frame,
            text="Customer Information",
            padx=10,
            pady=8
        )
        self.info_frame.pack(fill="x", pady=10)

        self.name_label = self.create_info_row("Name:")
        self.age_label = self.create_info_row("Age:")
        self.gender_label = self.create_info_row("Gender:")
        self.phone_label = self.create_info_row("Phone:")
        self.balance_label = self.create_info_row("Balance:")

        # Actions
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=8)

        tk.Button(
            button_frame,
            text="Create Customer",
            command=self.show_create_customer
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Add Balance",
            command=self.add_balance
        ).pack(side="left", padx=5)

        # Back button
        tk.Button(
            self.main_frame,
            text="Back to Main Menu",
            command=self.back_callback
        ).pack(pady=8)

    def create_info_row(self, label_text):
        row = tk.Frame(self.info_frame)
        row.pack(fill="x", pady=2)

        tk.Label(
            row,
            text=label_text,
            width=15,
            anchor="w",
            font=("Arial", 10, "bold")
        ).pack(side="left")

        value_label = tk.Label(row, text="-", anchor="w")
        value_label.pack(side="left")

        return value_label

    def search_customer(self):
        customer_id_text = self.customer_id_entry.get().strip()

        if not customer_id_text:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a customer ID.",
                parent=self.root
            )
            return

        try:
            customer_id = int(customer_id_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Customer ID must be a whole number.",
                parent=self.root
            )
            return

        success, message, customer = (
            self.customer_controller.get_customer(customer_id)
        )

        if not success:
            self.clear_customer_info()
            self.current_customer_id = None
            messagebox.showerror(
                "Customer Search",
                message,
                parent=self.root
            )
            return

        self.current_customer_id = customer.customer_id

        self.name_label.config(text=customer.name)
        self.age_label.config(text=str(customer.age))
        self.gender_label.config(text=customer.gender)
        self.phone_label.config(text=customer.phone_number)
        self.balance_label.config(text=str(customer.balance))

    def clear_customer_info(self):
        self.name_label.config(text="-")
        self.age_label.config(text="-")
        self.gender_label.config(text="-")
        self.phone_label.config(text="-")
        self.balance_label.config(text="-")

    def show_create_customer(self):
        # Open a separate window for customer creation.
        form = tk.Toplevel(self.root)
        form.title("Create Customer")
        form.geometry("400x430")
        form.resizable(False, False)
        form.transient(self.root)
        form.grab_set()

        fields = [
            ("Customer ID", "customer_id"),
            ("Name", "name"),
            ("Social ID", "social_id"),
            ("Age", "age"),
            ("Gender", "gender"),
            ("Phone Number", "phone_number"),
            ("Initial Balance", "balance"),
        ]

        entries = {}

        for row_index, (label_text, field_name) in enumerate(fields):
            tk.Label(
                form,
                text=f"{label_text}:",
                anchor="w",
                width=16
            ).grid(
                row=row_index,
                column=0,
                padx=12,
                pady=8,
                sticky="w"
            )

            if field_name == "gender":
                entry = ttk.Combobox(
                    form,
                    values=("Male", "Female"),
                    state="readonly",
                    width=22
                )
                entry.current(0)  # Default selection: Male
            else:
                entry = tk.Entry(form, width=25)

            entry.grid(
                row=row_index,
                column=1,
                padx=12,
                pady=8
            )

            entries[field_name] = entry

        # Defaults for two fields
        entries["balance"].insert(0, "0.00")

        def save_customer():
            values = {
                field_name: entry.get().strip()
                for field_name, entry in entries.items()
            }

            # Check required fields.
            required_fields = [
                "customer_id",
                "name",
                "social_id",
                "age",
                "gender",
                "phone_number",
                "balance"
            ]

            if any(not values[field] for field in required_fields):
                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields.",
                    parent=form
                )
                return

            # Convert input into the expected types.
            try:
                customer_id = int(values["customer_id"])
                age = int(values["age"])
                balance = Decimal(values["balance"])

                if not balance.is_finite():
                    raise ValueError("Balance must be a finite number.")

            except (ValueError, InvalidOperation):
                messagebox.showerror(
                    "Invalid Input",
                    "Customer ID and age must be whole numbers, "
                    "and balance must be a valid number.",
                    parent=form
                )
                return

            # Delegate creation to the controller.
            success, message, customer = (
                self.customer_controller.create_customer(
                    customer_id=customer_id,
                    name=values["name"],
                    social_id=values["social_id"],
                    age=age,
                    gender=values["gender"],
                    phone_number=values["phone_number"],
                    balance=balance
                )
            )

            if not success:
                messagebox.showerror(
                    "Customer Creation Failed",
                    message,
                    parent=form
                )
                return

            messagebox.showinfo(
                "Success",
                "Customer created successfully!",
                parent=form
            )

            # Close the form and display the newly created customer.
            form.destroy()
            self.customer_id_entry.delete(0, tk.END)
            self.customer_id_entry.insert(0, str(customer.customer_id))
            self.search_customer()

        tk.Button(
            form,
            text="Save Customer",
            command=save_customer,
            width=18
        ).grid(
            row=len(fields),
            column=0,
            columnspan=2,
            pady=18
        )

    def add_balance(self):
        # Ensure a customer has been selected.
        if self.current_customer_id is None:
            messagebox.showwarning(
                "No Customer Selected",
                "Please search for a customer first.",
                parent=self.root
            )
            return

        # Create the Add Balance window.
        form = tk.Toplevel(self.root)
        form.title("Add Balance")
        form.geometry("320x180")
        form.resizable(False, False)
        form.transient(self.root)
        form.grab_set()

        tk.Label(
            form,
            text=f"Customer ID: {self.current_customer_id}",
            font=("Arial", 11, "bold")
        ).pack(pady=(15, 10))

        tk.Label(
            form,
            text="Amount to add:"
        ).pack()

        amount_entry = tk.Entry(form, width=20)
        amount_entry.pack(pady=5)
        amount_entry.focus_set()

        def save_balance():
            amount_text = amount_entry.get().strip()

            if not amount_text:
                messagebox.showwarning(
                    "Missing Amount",
                    "Please enter an amount.",
                    parent=form
                )
                return

            try:
                amount = Decimal(amount_text)

                if not amount.is_finite():
                    raise InvalidOperation

            except (InvalidOperation, ValueError):
                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid number.",
                    parent=form
                )
                return

            success, message, customer = (
                self.customer_controller.add_balance(
                    self.current_customer_id,
                    amount
                )
            )

            if not success:
                messagebox.showerror(
                    "Balance Update Failed",
                    message,
                    parent=form
                )
                return

            messagebox.showinfo(
                "Success",
                f"Balance updated successfully!\n"
                f"New balance: {customer.balance}",
                parent=form
            )

            # Close the dialog and refresh customer information.
            form.destroy()
            self.search_customer()

        tk.Button(
            form,
            text="Add Balance",
            command=save_balance,
            width=15
        ).pack(pady=10)