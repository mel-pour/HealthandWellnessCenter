
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP


class AppointmentView:

    def __init__(self, root):
        self.root = root
        self.root.title("Wellness Center - Appointment Management")
        self.root.geometry("1000x700")

        # Temporary sample customers
        self.customers = {
            1001: {
                "name": "John Smith",
                "balance": Decimal("100.00")
            },
            1002: {
                "name": "Sarah Jones",
                "balance": Decimal("65.00")
            }
        }

        # Temporary sample offerings
        self.offerings = {
            1: {
                "name": "Massage",
                "type": "Service",
                "price": Decimal("50.00"),
                "duration": 60
            },
            2: {
                "name": "Facial",
                "type": "Service",
                "price": Decimal("35.00"),
                "duration": 30
            },
            3: {
                "name": "Gym Access",
                "type": "Facility",
                "price": Decimal("15.00"),
                "duration": None
            },
            4: {
                "name": "Pool and Sauna",
                "type": "Facility",
                "price": Decimal("25.00"),
                "duration": None
            }
        }

        # Temporary sample appointments
        self.appointments = [
            {
                "id": 1,
                "customer_id": 1001,
                "offering_id": 1,
                "date": "2026-10-20",
                "time": "14:00",
                "price_paid": Decimal("50.00"),
                "status": "Booked"
            },
            {
                "id": 2,
                "customer_id": 1001,
                "offering_id": 2,
                "date": "2026-10-22",
                "time": "11:00",
                "price_paid": Decimal("35.00"),
                "status": "Booked"
            },
            {
                "id": 3,
                "customer_id": 1002,
                "offering_id": 2,
                "date": "2026-10-21",
                "time": "10:00",
                "price_paid": Decimal("35.00"),
                "status": "Booked"
            }
        ]

        self.next_appointment_id = 4
        self.selected_customer_id = None
        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self.root,
            text="Appointment Management",
            font=("Arial", 20, "bold")
        ).pack(pady=12)

        # Customer search
        search_frame = ttk.LabelFrame(
            self.root,
            text="Find Customer",
            padding=12
        )
        search_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            search_frame,
            text="Customer ID:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.customer_id_var = tk.StringVar()

        ttk.Entry(
            search_frame,
            textvariable=self.customer_id_var,
            width=18
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            search_frame,
            text="Find Customer",
            command=self.find_customer
        ).grid(row=0, column=2, padx=10, pady=5)

        # Customer information
        info_frame = ttk.LabelFrame(
            self.root,
            text="Customer Information",
            padding=12
        )
        info_frame.pack(fill="x", padx=20, pady=5)

        self.name_label = ttk.Label(
            info_frame,
            text="Customer: Not selected"
        )
        self.name_label.grid(row=0, column=0, padx=10, sticky="w")

        self.balance_label = ttk.Label(
            info_frame,
            text="Balance: —",
            font=("Arial", 11, "bold")
        )
        self.balance_label.grid(row=0, column=1, padx=20, sticky="w")

        # Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.current_tab = ttk.Frame(self.tabs, padding=10)
        self.new_tab = ttk.Frame(self.tabs, padding=10)

        self.tabs.add(
            self.current_tab,
            text="Current Appointments"
        )
        self.tabs.add(
            self.new_tab,
            text="New Appointment"
        )

        self.create_current_appointments_tab()
        self.create_new_appointment_tab()

    # --------------------------------------------------
    # CURRENT APPOINTMENTS TAB
    # --------------------------------------------------

    def create_current_appointments_tab(self):

        columns = (
            "id", "offering", "date",
            "time", "price", "status"
        )

        self.appointment_table = ttk.Treeview(
            self.current_tab,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=12
        )

        headings = {
            "id": "Appointment ID",
            "offering": "Offering",
            "date": "Date",
            "time": "Time",
            "price": "Original Price (€)",
            "status": "Status"
        }

        for column in columns:
            self.appointment_table.heading(
                column, text=headings[column]
            )
            self.appointment_table.column(column, width=130)

        self.appointment_table.pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            self.current_tab,
            text="Cancel Selected Appointment",
            command=self.cancel_appointment
        ).pack(anchor="w", pady=12)

    # --------------------------------------------------
    # NEW APPOINTMENT TAB
    # --------------------------------------------------

    def create_new_appointment_tab(self):

        form = ttk.LabelFrame(
            self.new_tab,
            text="Book a New Appointment",
            padding=15
        )
        form.pack(fill="x", pady=10)

        ttk.Label(
            form,
            text="Offering:"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=8)

        self.offering_var = tk.StringVar()

        self.offering_combo = ttk.Combobox(
            form,
            textvariable=self.offering_var,
            state="readonly",
            width=35
        )
        self.offering_combo.grid(
            row=0, column=1, sticky="w", padx=5, pady=8
        )
        self.offering_combo.bind(
            "<<ComboboxSelected>>",
            self.update_price_preview
        )

        self.offering_options = {}

        for offering_id, offering in self.offerings.items():
            label = (
                f'{offering["name"]} '
                f'(€{offering["price"]:.2f})'
            )
            self.offering_options[label] = offering_id

        self.offering_combo["values"] = list(
            self.offering_options.keys()
        )

        if self.offering_options:
            self.offering_combo.current(0)

        ttk.Label(
            form,
            text="Date (YYYY-MM-DD):"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=8)

        self.date_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.date_var,
            width=38
        ).grid(row=1, column=1, sticky="w", padx=5, pady=8)

        ttk.Label(
            form,
            text="Start Time (HH:MM):"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=8)

        self.time_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.time_var,
            width=38
        ).grid(row=2, column=1, sticky="w", padx=5, pady=8)

        self.price_label = ttk.Label(
            form,
            text="Price: —"
        )
        self.price_label.grid(
            row=3, column=0, columnspan=2,
            sticky="w", padx=5, pady=8
        )

        self.remaining_label = ttk.Label(
            form,
            text="Balance after booking: —"
        )
        self.remaining_label.grid(
            row=4, column=0, columnspan=2,
            sticky="w", padx=5, pady=8
        )

        ttk.Button(
            form,
            text="Book Appointment",
            command=self.book_appointment
        ).grid(
            row=5, column=0, columnspan=2, pady=15
        )

        self.update_price_preview()

    def update_price_preview(self, event=None):

        label = self.offering_var.get()

        if label not in self.offering_options:
            return

        offering_id = self.offering_options[label]
        price = self.offerings[offering_id]["price"]

        self.price_label.config(
            text=f"Selected offering price: €{price:.2f}"
        )

        if self.selected_customer_id is None:
            self.remaining_label.config(
                text="Find a customer to check their balance."
            )
            return

        balance = self.customers[
            self.selected_customer_id
        ]["balance"]

        if balance >= price:
            remaining = balance - price
            self.remaining_label.config(
                text=f"Balance after booking: €{remaining:.2f}"
            )
        else:
            shortfall = price - balance
            self.remaining_label.config(
                text=f"Insufficient balance: €{shortfall:.2f} more needed"
            )

    # --------------------------------------------------
    # FIND CUSTOMER
    # --------------------------------------------------

    def find_customer(self):

        text_id = self.customer_id_var.get().strip()

        try:
            customer_id = int(text_id)
        except ValueError:
            messagebox.showerror(
                "Invalid ID",
                "Enter a valid numeric customer ID."
            )
            return

        if customer_id not in self.customers:
            self.selected_customer_id = None

            self.name_label.config(text="Customer: Not found")
            self.balance_label.config(text="Balance: —")

            self.appointment_table.delete(
                *self.appointment_table.get_children()
            )

            self.update_price_preview()

            messagebox.showwarning(
                "Customer Not Found",
                "No customer exists with that ID."
            )
            return

        self.selected_customer_id = customer_id
        customer = self.customers[customer_id]

        self.name_label.config(
            text=f'Customer: {customer["name"]} (ID: {customer_id})'
        )

        self.update_balance()
        self.load_customer_appointments()
        self.update_price_preview()

    def update_balance(self):

        if self.selected_customer_id is None:
            return

        balance = self.customers[
            self.selected_customer_id
        ]["balance"]

        self.balance_label.config(
            text=f"Account Balance: €{balance:.2f}"
        )

    def load_customer_appointments(self):

        self.appointment_table.delete(
            *self.appointment_table.get_children()
        )

        for appointment in self.appointments:

            if (
                appointment["customer_id"]
                != self.selected_customer_id
            ):
                continue

            offering = self.offerings[
                appointment["offering_id"]
            ]

            self.appointment_table.insert(
                "",
                "end",
                iid=str(appointment["id"]),
                values=(
                    appointment["id"],
                    offering["name"],
                    appointment["date"],
                    appointment["time"],
                    f'{appointment["price_paid"]:.2f}',
                    appointment["status"]
                )
            )

    # --------------------------------------------------
    # BOOK APPOINTMENT
    # --------------------------------------------------

    def book_appointment(self):

        if self.selected_customer_id is None:
            messagebox.showwarning(
                "No Customer",
                "Find a customer before booking an appointment."
            )
            return

        offering_label = self.offering_var.get()

        if offering_label not in self.offering_options:
            messagebox.showwarning(
                "No Offering",
                "Please select an offering."
            )
            return

        try:
            appointment_date = datetime.strptime(
                self.date_var.get().strip(),
                "%Y-%m-%d"
            ).date()

            appointment_time = datetime.strptime(
                self.time_var.get().strip(),
                "%H:%M"
            ).time()

        except ValueError:
            messagebox.showerror(
                "Invalid Date or Time",
                "Use YYYY-MM-DD for date and HH:MM for time."
            )
            return

        appointment_datetime = datetime.combine(
            appointment_date, appointment_time
        )

        if appointment_datetime <= datetime.now():
            messagebox.showerror(
                "Invalid Appointment",
                "Please choose a future date and time."
            )
            return

        customer_id = self.selected_customer_id
        customer = self.customers[customer_id]

        offering_id = self.offering_options[offering_label]
        offering = self.offerings[offering_id]
        price = offering["price"]

        if customer["balance"] < price:
            messagebox.showerror(
                "Insufficient Balance",
                f'Price: €{price:.2f}\n'
                f'Available balance: €{customer["balance"]:.2f}'
            )
            return

        # Determine appointment duration.
        # Facility access uses a 60-minute slot in this prototype.
        duration = offering["duration"] or 60

        new_start = datetime.combine(
            appointment_date, appointment_time
        )
        new_end = new_start + timedelta(minutes=duration)

        # Prevent overlapping appointments for this customer.
        for existing in self.appointments:

            if (
                existing["customer_id"] != customer_id
                or existing["status"] != "Booked"
            ):
                continue

            existing_offering = self.offerings[
                existing["offering_id"]
            ]

            existing_duration = (
                existing_offering["duration"] or 60
            )

            existing_start = datetime.strptime(
                f'{existing["date"]} {existing["time"]}',
                "%Y-%m-%d %H:%M"
            )

            existing_end = existing_start + timedelta(
                minutes=existing_duration
            )

            if new_start < existing_end and new_end > existing_start:
                messagebox.showerror(
                    "Schedule Conflict",
                    "This customer already has an appointment "
                    "during that time."
                )
                return

        confirm = messagebox.askyesno(
            "Confirm Booking",
            f'Customer: {customer["name"]}\n'
            f'Offering: {offering["name"]}\n'
            f'Date: {appointment_date}\n'
            f'Time: {appointment_time.strftime("%H:%M")}\n'
            f'Price: €{price:.2f}\n'
            f'Balance after booking: '
            f'€{customer["balance"] - price:.2f}\n\n'
            "Confirm this booking?"
        )

        if not confirm:
            return

        # Temporary in-memory booking and payment
        customer["balance"] -= price

        appointment = {
            "id": self.next_appointment_id,
            "customer_id": customer_id,
            "offering_id": offering_id,
            "date": appointment_date.isoformat(),
            "time": appointment_time.strftime("%H:%M"),
            "price_paid": price,
            "status": "Booked"
        }

        self.appointments.append(appointment)
        self.next_appointment_id += 1

        self.load_customer_appointments()
        self.update_balance()
        self.update_price_preview()

        self.date_var.set("")
        self.time_var.set("")

        messagebox.showinfo(
            "Booking Successful",
            "Appointment booked and balance updated."
        )

        # Switch to the current appointments tab
        self.tabs.select(self.current_tab)

    # --------------------------------------------------
    # CANCEL APPOINTMENT AND REFUND
    # --------------------------------------------------

    def cancel_appointment(self):

        if self.selected_customer_id is None:
            messagebox.showwarning(
                "No Customer",
                "Find a customer first."
            )
            return

        selected = self.appointment_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Appointment Selected",
                "Select an appointment to cancel."
            )
            return

        appointment_id = int(selected[0])

        appointment = next(
            (
                item for item in self.appointments
                if item["id"] == appointment_id
                and item["customer_id"] == self.selected_customer_id
            ),
            None
        )

        if appointment is None or appointment["status"] != "Booked":
            messagebox.showwarning(
                "Cannot Cancel",
                "This appointment is not currently booked."
            )
            return

        original_price = appointment["price_paid"]

        fee = (
            original_price * Decimal("0.20")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        refund = original_price - fee

        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            f"Original price: €{original_price:.2f}\n"
            f"Cancellation fee: €{fee:.2f}\n"
            f"Refund: €{refund:.2f}\n\n"
            "Cancel this appointment?"
        )

        if not confirm:
            return

        customer = self.customers[self.selected_customer_id]

        customer["balance"] += refund
        appointment["status"] = "Cancelled"

        self.load_customer_appointments()
        self.update_balance()
        self.update_price_preview()

        messagebox.showinfo(
            "Cancellation Successful",
            f"Refund of €{refund:.2f} added to the account.\n"
            f"Cancellation fee: €{fee:.2f}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentView(root)
    root.mainloop()
