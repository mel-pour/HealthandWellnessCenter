
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation


class CustomerView:

    def __init__(self, root):
        self.root = root
        self.root.title("Wellness Center - Customer Management")
        self.root.geometry("850x600")

        # Temporary data for testing the View
        self.customers = []
        self.next_customer_id = 1

        self.create_widgets()

    def create_widgets(self):

        # Main title
        title = ttk.Label(
            self.root,
            text="Customer Management",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # Form
        form_frame = ttk.LabelFrame(
            self.root,
            text="Create New Customer",
            padding=15
        )
        form_frame.pack(fill="x", padx=20, pady=10)

        # Variables
        self.name_var = tk.StringVar()
        self.social_id_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.balance_var = tk.StringVar(value="0.00")

        # Customer ID
        ttk.Label(
            form_frame,
            text="Customer ID:"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=8)

        ttk.Label(
            form_frame,
            text="Auto-generated"
        ).grid(row=0, column=1, sticky="w", padx=5, pady=8)

        # Name
        ttk.Label(
            form_frame,
            text="Full Name:"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=8)

        ttk.Entry(
            form_frame,
            textvariable=self.name_var,
            width=35
        ).grid(row=1, column=1, sticky="w", padx=5, pady=8)

        # Social ID
        ttk.Label(
            form_frame,
            text="Social ID:"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=8)

        ttk.Entry(
            form_frame,
            textvariable=self.social_id_var,
            width=35
        ).grid(row=2, column=1, sticky="w", padx=5, pady=8)

        # Phone
        ttk.Label(
            form_frame,
            text="Phone Number:"
        ).grid(row=3, column=0, sticky="w", padx=5, pady=8)

        ttk.Entry(
            form_frame,
            textvariable=self.phone_var,
            width=35
        ).grid(row=3, column=1, sticky="w", padx=5, pady=8)

        # Initial balance
        ttk.Label(
            form_frame,
            text="Initial Balance (€):"
        ).grid(row=4, column=0, sticky="w", padx=5, pady=8)

        ttk.Entry(
            form_frame,
            textvariable=self.balance_var,
            width=35
        ).grid(row=4, column=1, sticky="w", padx=5, pady=8)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=15
        )

        ttk.Button(
            button_frame,
            text="Create Customer",
            command=self.create_customer
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear Fields",
            command=self.clear_fields
        ).pack(side="left", padx=5)

        # Customer list
        list_frame = ttk.LabelFrame(
            self.root,
            text="Customer List",
            padding=10
        )
        list_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "id",
            "name",
            "social_id",
            "phone",
            "balance"
        )

        self.customer_table = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.customer_table.heading("id", text="Customer ID")
        self.customer_table.heading("name", text="Name")
        self.customer_table.heading("social_id", text="Social ID")
        self.customer_table.heading("phone", text="Phone")
        self.customer_table.heading("balance", text="Balance (€)")

        self.customer_table.column("id", width=90)
        self.customer_table.column("name", width=150)
        self.customer_table.column("social_id", width=130)
        self.customer_table.column("phone", width=130)
        self.customer_table.column("balance", width=110)

        self.customer_table.pack(
            fill="both",
            expand=True
        )

    def create_customer(self):

        name = self.name_var.get().strip()
        social_id = self.social_id_var.get().strip()
        phone = self.phone_var.get().strip()

        # Validate text fields
        if not name or not social_id or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in the name, social ID, and phone."
            )
            return

        # Validate initial balance
        try:
            balance = Decimal(self.balance_var.get().strip())

            if not balance.is_finite() or balance < 0:
                raise InvalidOperation

        except (InvalidOperation, ValueError):
            messagebox.showerror(
                "Invalid Balance",
                "Please enter a valid balance of zero or more."
            )
            return

        # Create temporary customer record
        customer = {
            "id": self.next_customer_id,
            "name": name,
            "social_id": social_id,
            "phone": phone,
            "balance": balance
        }

        self.customers.append(customer)

        # Display customer in the table
        self.customer_table.insert(
            "",
            "end",
            values=(
                customer["id"],
                customer["name"],
                customer["social_id"],
                customer["phone"],
                f'{customer["balance"]:.2f}'
            )
        )

        self.next_customer_id += 1

        messagebox.showinfo(
            "Success",
            f"Customer {name} created successfully!"
        )

        self.clear_fields()

    def clear_fields(self):

        self.name_var.set("")
        self.social_id_var.set("")
        self.phone_var.set("")
        self.balance_var.set("0.00")


if __name__ == "__main__":

    root = tk.Tk()
    app = CustomerView(root)
    root.mainloop()
