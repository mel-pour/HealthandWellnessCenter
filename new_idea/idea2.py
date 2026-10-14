import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal


class WellnessCenterView:

    def __init__(self, root):
        self.root = root
        self.root.title("Wellness Center Management System")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)

        self.selected_offering = tk.StringVar()
        self.booking_date = tk.StringVar()
        self.booking_time = tk.StringVar()

        self.customer_id = 1001
        self.customer_name = "John Smith"
        self.balance = Decimal("150.00")

        self.create_widgets()

    # ---------------- CUSTOMER INFORMATION ----------------

    def create_widgets(self):

        title = ttk.Label(
            self.root,
            text="Wellness Center Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        customer_frame = ttk.LabelFrame(
            self.root,
            text="Customer Information",
            padding=15
        )
        customer_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(
            customer_frame,
            text=f"Customer ID: {self.customer_id}"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        ttk.Label(
            customer_frame,
            text=f"Name: {self.customer_name}"
        ).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.balance_label = ttk.Label(
            customer_frame,
            text=f"Account Balance: €{self.balance:.2f}",
            font=("Arial", 11, "bold")
        )
        self.balance_label.grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )

        # ---------------- MAIN CONTENT ----------------

        content_frame = ttk.Frame(self.root)
        content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)

        self.create_offerings_section(content_frame)
        self.create_booking_section(content_frame)

        # ---------------- APPOINTMENTS ----------------

        self.create_appointments_section()

        # ---------------- ACCOUNT ACTIONS ----------------

        account_frame = ttk.Frame(self.root)
        account_frame.pack(fill="x", padx=20, pady=15)

        ttk.Button(
            account_frame,
            text="Add Balance",
            command=self.add_balance
        ).pack(side="left", padx=5)

        ttk.Button(
            account_frame,
            text="Refresh",
            command=self.refresh_view
        ).pack(side="right", padx=5)

    # ---------------- AVAILABLE OFFERINGS ----------------

    def create_offerings_section(self, parent):

        frame = ttk.LabelFrame(
            parent,
            text="Available Offerings",
            padding=10
        )
        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10),
            pady=5
        )

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.offerings_tree = ttk.Treeview(
            frame,
            columns=("name", "type", "price", "duration"),
            show="headings",
            height=8,
            selectmode="browse"
        )

        self.offerings_tree.heading("name", text="Offering")
        self.offerings_tree.heading("type", text="Type")
        self.offerings_tree.heading("price", text="Price")
        self.offerings_tree.heading("duration", text="Duration")

        self.offerings_tree.column("name", width=130)
        self.offerings_tree.column("type", width=80)
        self.offerings_tree.column("price", width=80)
        self.offerings_tree.column("duration", width=80)

        self.offerings_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.offerings_tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.offerings_tree.configure(
            yscrollcommand=scrollbar.set
        )

        offerings = [
            (1, "Massage", "Service", "50.00", "60 min"),
            (2, "Facial", "Service", "35.00", "30 min"),
            (3, "Gym Access", "Facility", "15.00", "-"),
            (4, "Pool & Sauna", "Facility", "25.00", "-")
        ]

        for offering in offerings:
            offering_id, name, offering_type, price, duration = offering

            self.offerings_tree.insert(
                "",
                "end",
                iid=str(offering_id),
                values=(
                    name,
                    offering_type,
                    f"€{Decimal(price):.2f}",
                    duration
                )
            )

        ttk.Label(
            frame,
            text="Select an offering to book or purchase."
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=10
        )

    # ---------------- BOOKING SECTION ----------------

    def create_booking_section(self, parent):

        frame = ttk.LabelFrame(
            parent,
            text="Booking and Purchases",
            padding=15
        )
        frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0),
            pady=5
        )

        ttk.Label(
            frame,
            text="Appointment Date (YYYY-MM-DD):"
        ).pack(anchor="w", pady=(5, 2))

        ttk.Entry(
            frame,
            textvariable=self.booking_date
        ).pack(fill="x", pady=5)

        ttk.Label(
            frame,
            text="Start Time (HH:MM):"
        ).pack(anchor="w", pady=(10, 2))

        ttk.Entry(
            frame,
            textvariable=self.booking_time
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Book Appointment",
            command=self.book_appointment
        ).pack(fill="x", pady=(20, 5))

        ttk.Button(
            frame,
            text="Purchase Directly",
            command=self.purchase_offering
        ).pack(fill="x", pady=5)

        ttk.Label(
            frame,
            text=(
                "Services require appointments.\n"
                "Facility access can be purchased\n"
                "directly or reserved in advance."
            ),
            justify="left"
        ).pack(anchor="w", pady=15)

    # ---------------- APPOINTMENTS LIST ----------------

    def create_appointments_section(self):

        frame = ttk.LabelFrame(
            self.root,
            text="My Appointments",
            padding=10
        )
        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "id",
            "offering",
            "date",
            "time",
            "status"
        )

        self.appointments_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=5,
            selectmode="browse"
        )

        self.appointments_tree.heading("id", text="ID")
        self.appointments_tree.heading(
            "offering", text="Offering"
        )
        self.appointments_tree.heading("date", text="Date")
        self.appointments_tree.heading("time", text="Time")
        self.appointments_tree.heading("status", text="Status")

        self.appointments_tree.column("id", width=50)
        self.appointments_tree.column("offering", width=200)
        self.appointments_tree.column("date", width=150)
        self.appointments_tree.column("time", width=100)
        self.appointments_tree.column("status", width=120)

        self.appointments_tree.pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            frame,
            text="Cancel Selected Appointment",
            command=self.cancel_appointment
        ).pack(anchor="w", pady=10)

    # ---------------- BUTTON CALLBACKS ----------------

    def book_appointment(self):

        selected = self.offerings_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Offering Selected",
                "Please select an offering first."
            )
            return

        offering = self.offerings_tree.item(
            selected[0], "values"
        )

        offering_type = offering[1]

        if offering_type != "Service":
            messagebox.showinfo(
                "Facility Reservation",
                "Facility reservations will be connected "
                "to the booking controller."
            )
            return

        date = self.booking_date.get().strip()
        start_time = self.booking_time.get().strip()

        if not date or not start_time:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the appointment date and time."
            )
            return

        messagebox.showinfo(
            "Booking Request",
            f"Offering: {offering[0]}\n"
            f"Date: {date}\n"
            f"Time: {start_time}\n\n"
            "The booking controller will process this request."
        )

    def purchase_offering(self):

        selected = self.offerings_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Offering Selected",
                "Please select an offering first."
            )
            return

        offering = self.offerings_tree.item(
            selected[0], "values"
        )

        if offering[1] != "Facility":
            messagebox.showwarning(
                "Invalid Purchase",
                "Direct purchase is intended for facility access."
            )
            return

        messagebox.showinfo(
            "Purchase Request",
            f"Offering: {offering[0]}\n"
            f"Price: {offering[2]}\n\n"
            "The account controller will process this purchase."
        )

    def cancel_appointment(self):

        selected = self.appointments_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Appointment Selected",
                "Please select an appointment to cancel."
            )
            return

        appointment_id = selected[0]

        confirm = messagebox.askyesno(
            "Cancel Appointment",
            f"Cancel appointment {appointment_id}?\n"
            "The cancellation fee is 20% of the original price."
        )

        if confirm:
            messagebox.showinfo(
                "Cancellation Request",
                "The cancellation controller will verify "
                "the booking and process the 80% refund."
            )

    def add_balance(self):

        dialog = tk.Toplevel(self.root)
        dialog.title("Add Balance")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text="Amount to add (€):"
        ).pack(pady=(15, 5))

        amount_entry = ttk.Entry(dialog)
        amount_entry.pack(padx=20, fill="x")
        amount_entry.focus_set()

        def submit():

            try:
                amount = Decimal(amount_entry.get().strip())

                if not amount.is_finite() or amount <= 0:
                    raise ValueError

            except Exception:
                messagebox.showerror(
                    "Invalid Amount",
                    "Enter a valid positive amount.",
                    parent=dialog
                )
                return

            messagebox.showinfo(
                "Balance Request",
                f"Requested amount: €{amount:.2f}\n\n"
                "The account controller will process the top-up.",
                parent=dialog
            )

            dialog.destroy()

        ttk.Button(
            dialog,
            text="Submit",
            command=submit
        ).pack(pady=15)

    def refresh_view(self):
        messagebox.showinfo(
            "Refresh",
            "The controller will reload customer data, "
            "offerings, balance, and appointments."
        )


if __name__ == "__main__":

    root = tk.Tk()
    app = WellnessCenterView(root)
    root.mainloop()