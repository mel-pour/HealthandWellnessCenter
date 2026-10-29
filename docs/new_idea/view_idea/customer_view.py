import tkinter as tk
from tkinter import messagebox


class CustomerView:
    def __init__(self, root, customer_controller, back_callback):
        self.root = root
        self.customer_controller = customer_controller
        self.back_callback = back_callback

        self.main_frame = tk.Frame(self.root, padx=30, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            self.main_frame,
            text="Customer View",
            font=("Arial", 20, "bold")
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
        self.info_frame.pack(fill="x", pady=20)

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























#
# import tkinter as tk
# from tkinter import ttk, messagebox
# from decimal import Decimal, InvalidOperation
#
#
# class CustomerView:
#
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Wellness Center - Customer Management")
#         self.root.geometry("850x600")
#
#         # Temporary data for testing the View
#         self.customers = []
#         self.next_customer_id = 1
#
#         self.create_widgets()
#
#     def create_widgets(self):
#
#         # Main title
#         title = ttk.Label(
#             self.root,
#             text="Customer Management",
#             font=("Arial", 20, "bold")
#         )
#         title.pack(pady=15)
#
#         # Form
#         form_frame = ttk.LabelFrame(
#             self.root,
#             text="Create New Customer",
#             padding=15
#         )
#         form_frame.pack(fill="x", padx=20, pady=10)
#
#         # Variables
#         self.name_var = tk.StringVar()
#         self.family_var = tk.StringVar()
#         self.social_id_var = tk.StringVar()
#         self.phone_var = tk.StringVar()
#         self.balance_var = tk.StringVar(value="0.00")
#
#         # Customer ID
#         ttk.Label(
#             form_frame,
#             text="Customer ID:"
#         ).grid(row=0, column=0, sticky="w", padx=5, pady=8)
#
#         ttk.Label(
#             form_frame,
#             text="Auto-generated"
#         ).grid(row=0, column=1, sticky="w", padx=5, pady=8)
#
#         # Name
#         ttk.Label(
#             form_frame,
#             text="Name:"
#         ).grid(row=1, column=0, sticky="w", padx=5, pady=8)
#
#         ttk.Entry(
#             form_frame,
#             textvariable=self.name_var,
#             width=35
#         ).grid(row=1, column=1, sticky="w", padx=5, pady=8)
#
#         # Family
#         ttk.Label(
#             form_frame,
#             text="Family:"
#         ).grid(row=1, column=2, sticky="w", padx=5, pady=8)
#
#         ttk.Entry(
#             form_frame,
#             textvariable=self.family_var,
#             width=35
#         ).grid(row=1, column=3, sticky="w", padx=5, pady=8)
#
#         # Social ID
#         ttk.Label(
#             form_frame,
#             text="Social ID:"
#         ).grid(row=2, column=0, sticky="w", padx=5, pady=8)
#
#         ttk.Entry(
#             form_frame,
#             textvariable=self.social_id_var,
#             width=35
#         ).grid(row=2, column=1, sticky="w", padx=5, pady=8)
#
#         # Phone
#         ttk.Label(
#             form_frame,
#             text="Phone Number:"
#         ).grid(row=2, column=2, sticky="w", padx=5, pady=8)
#
#         ttk.Entry(
#             form_frame,
#             textvariable=self.phone_var,
#             width=35
#         ).grid(row=2, column=3, sticky="w", padx=5, pady=8)
#
#         # Initial balance
#         ttk.Label(
#             form_frame,
#             text="Initial Balance (€):"
#         ).grid(row=3, column=0, sticky="w", padx=5, pady=8)
#
#         ttk.Entry(
#             form_frame,
#             textvariable=self.balance_var,
#             width=35
#         ).grid(row=3, column=1, sticky="w", padx=5, pady=8)
#
#         # Buttons
#         button_frame = ttk.Frame(form_frame)
#         button_frame.grid(
#             row=5,
#             column=0,
#             columnspan=2,
#             pady=15
#         )
#
#         ttk.Button(
#             button_frame,
#             text="Create Customer",
#             command=self.create_customer
#         ).pack(side="left", padx=5)
#
#         ttk.Button(
#             button_frame,
#             text="Clear Fields",
#             command=self.clear_fields
#         ).pack(side="left", padx=5)
#
#         # Customer list
#         list_frame = ttk.LabelFrame(
#             self.root,
#             text="Customer List",
#             padding=10
#         )
#         list_frame.pack(
#             fill="both",
#             expand=True,
#             padx=20,
#             pady=10
#         )
#
#         columns = (
#             "id",
#             "name",
#             "family",
#             "social_id",
#             "phone",
#             "balance"
#         )
#
#         self.customer_table = ttk.Treeview(
#             list_frame,
#             columns=columns,
#             show="headings",
#             height=8
#         )
#
#         self.customer_table.heading("id", text="Customer ID")
#         self.customer_table.heading("name", text="Name")
#         self.customer_table.heading("family", text="Family")
#         self.customer_table.heading("social_id", text="Social ID")
#         self.customer_table.heading("phone", text="Phone")
#         self.customer_table.heading("balance", text="Balance (€)")
#
#         self.customer_table.column("id", width=90)
#         self.customer_table.column("name", width=150)
#         self.customer_table.column("family", width=150)
#         self.customer_table.column("social_id", width=130)
#         self.customer_table.column("phone", width=130)
#         self.customer_table.column("balance", width=110)
#
#         self.customer_table.pack(
#             fill="both",
#             expand=True
#         )
#
#     def create_customer(self):
#
#         name = self.name_var.get().strip()
#         family = self.family_var.get().strip()
#         social_id = self.social_id_var.get().strip()
#         phone = self.phone_var.get().strip()
#
#         # Validate text fields
#         if not name or not social_id or not phone:
#             messagebox.showwarning(
#                 "Missing Information",
#                 "Please fill in the name, social ID, and phone."
#             )
#             return
#
#         # Validate initial balance
#         try:
#             balance = Decimal(self.balance_var.get().strip())
#
#             if not balance.is_finite() or balance < 0:
#                 raise InvalidOperation
#
#         except (InvalidOperation, ValueError):
#             messagebox.showerror(
#                 "Invalid Balance",
#                 "Please enter a valid balance of zero or more."
#             )
#             return
#
#         # Create temporary customer record
#         customer = {
#             "id": self.next_customer_id,
#             "name": name,
#             "family": family,
#             "social_id": social_id,
#             "phone": phone,
#             "balance": balance
#         }
#
#         self.customers.append(customer)
#
#         # Display customer in the table
#         self.customer_table.insert(
#             "",
#             "end",
#             values=(
#                 customer["id"],
#                 customer["name"],
#                 customer["family"],
#                 customer["social_id"],
#                 customer["phone"],
#                 f'{customer["balance"]:.2f}'
#             )
#         )
#
#         self.next_customer_id += 1
#
#         messagebox.showinfo(
#             "Success",
#             f"Customer {name} created successfully!"
#         )
#
#         self.clear_fields()
#
#     def clear_fields(self):
#
#         self.name_var.set("")
#         self.family_var.set("")
#         self.social_id_var.set("")
#         self.phone_var.set("")
#         self.balance_var.set("0.00")
#
#
# if __name__ == "__main__":
#
#     root = tk.Tk()
#     app = CustomerView(root)
#     root.mainloop()
