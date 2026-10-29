import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from decimal import Decimal


class AppointmentView:
    def __init__(
        self,
        root,
        appointment_controller,
        customer_controller,
        back_callback
    ):
        self.root = root
        self.appointment_controller = appointment_controller
        self.customer_controller = customer_controller
        self.back_callback = back_callback

        self.root.geometry("750x600")

        self.main_frame = tk.Frame(root, padx=20, pady=15)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Appointment View",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 15))

        # Customer ID
        customer_frame = tk.Frame(self.main_frame)
        customer_frame.pack(fill="x", pady=5)

        tk.Label(
            customer_frame,
            text="Customer ID:",
            width=15,
            anchor="w"
        ).pack(side="left")

        self.customer_id_entry = tk.Entry(customer_frame, width=20)
        self.customer_id_entry.pack(side="left")

        tk.Button(
            customer_frame,
            text="View Appointments",
            command=self.view_customer_appointments
        ).pack(side="left", padx=10)

        # Customer Balance
        self.balance_label = tk.Label(
            self.main_frame,
            text="Customer: -- | ID: -- | Balance: --",
            font=("Arial", 11, "bold")
        )
        self.balance_label.pack(anchor="w", pady=5)

        # Appointment ID
        appointment_frame = tk.Frame(self.main_frame)
        appointment_frame.pack(fill="x", pady=5)

        tk.Label(
            appointment_frame,
            text="Appointment ID:",
            width=15,
            anchor="w"
        ).pack(side="left")

        self.appointment_id_entry = tk.Entry(
            appointment_frame,
            width=20
        )
        self.appointment_id_entry.pack(side="left")

        # Offering dropdown
        offering_frame = tk.Frame(self.main_frame)
        offering_frame.pack(fill="x", pady=5)

        tk.Label(
            offering_frame,
            text="Offering:",
            width=15,
            anchor="w"
        ).pack(side="left")

        self.offering_combo = ttk.Combobox(
            offering_frame,
            state="readonly",
            width=40
        )
        self.offering_combo.pack(side="left")

        # Date
        date_frame = tk.Frame(self.main_frame)
        date_frame.pack(fill="x", pady=5)

        tk.Label(
            date_frame,
            text="Date (YYYY-MM-DD):",
            width=15,
            anchor="w"
        ).pack(side="left")

        self.date_entry = tk.Entry(date_frame, width=20)
        self.date_entry.pack(side="left")

        # Start time
        time_frame = tk.Frame(self.main_frame)
        time_frame.pack(fill="x", pady=5)

        tk.Label(
            time_frame,
            text="Start Time (HH:MM):",
            width=15,
            anchor="w"
        ).pack(side="left")

        self.time_entry = tk.Entry(time_frame, width=20)
        self.time_entry.pack(side="left")

        # Buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=12)

        tk.Button(
            button_frame,
            text="Book Appointment",
            command=self.book_appointment
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_booking_fields
        ).pack(side="left", padx=5)

        # Cancel Appointment
        tk.Button(
            button_frame,
            text="Cancel Appointment",
            command=self.cancel_appointment
        ).pack(side="left", padx=5)

        # Appointment results
        tk.Label(
            self.main_frame,
            text="Customer Appointments",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(10, 5))

        self.results = tk.Text(
            self.main_frame,
            height=10,
            width=85,
            state="disabled"
        )
        self.results.pack(fill="both", expand=True)

        tk.Button(
            self.main_frame,
            text="Back to Main Menu",
            command=self.back_callback
        ).pack(pady=10)

        self.offerings = []
        self.load_offerings()

    def load_offerings(self):
        try:
            # Use the service through the controller's service reference
            service = self.appointment_controller.appointment_service
            self.offerings = service.offering_service.get_all_offerings()

            display_values = [
                f"{offering.offering_id} - {offering.name} "
                f"(${Decimal(str(offering.price)):.2f}, "
                f"{offering.duration} min)"
                for offering in self.offerings
            ]

            self.offering_combo["values"] = display_values

            if display_values:
                self.offering_combo.current(0)

        except Exception as error:
            messagebox.showerror(
                "Offering Error",
                f"Could not load offerings:\n{error}",
                parent=self.root
            )

    def book_appointment(self):
        try:
            appointment_id = int(
                self.appointment_id_entry.get().strip()
            )
            customer_id = int(
                self.customer_id_entry.get().strip()
            )

            selected_index = self.offering_combo.current()

            if selected_index < 0:
                raise ValueError("Please select an offering.")

            offering = self.offerings[selected_index]

            date_text = self.date_entry.get().strip()
            time_text = self.time_entry.get().strip()

            try:
                appointment_date = datetime.strptime(
                    date_text, "%Y-%m-%d"
                ).date()
            except ValueError as error:
                raise ValueError(
                    "Please enter a valid date in YYYY-MM-DD format."
                ) from error

            try:
                start_time = datetime.strptime(
                    time_text, "%H:%M"
                ).time()
            except ValueError as error:
                raise ValueError(
                    "Please enter a valid time in HH:MM format, "
                    "using 24-hour time."
                ) from error

            success, message, appointment = (
                self.appointment_controller.create_appointment(
                    appointment_id,
                    customer_id,
                    offering.offering_id,
                    appointment_date,
                    start_time
                )
            )

            if not success:
                messagebox.showerror(
                    "Booking Failed",
                    message,
                    parent=self.root
                )
                return

            messagebox.showinfo(
                "Success",
                "Appointment booked successfully!",
                parent=self.root
            )

            self.clear_booking_fields()
            self.customer_id_entry.insert(0, str(customer_id))
            self.view_customer_appointments()

        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Invalid Input",
                str(error),
                parent=self.root
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"An unexpected error occurred:\n{error}",
                parent=self.root
            )

    def get_offering_name(self, offering_id):
        for offering in self.offerings:
            if offering.offering_id == offering_id:
                return offering.name

        return f"Unknown offering (ID: {offering_id})"

    def refresh_customer_balance(self, customer_id):
        success, message, customer = (
            self.customer_controller.get_customer(customer_id)
        )

        if not success:
            self.balance_label.config(
                text="Customer: unavailable | ID: -- | Balance: --"
            )
            return

        balance = Decimal(str(customer.balance))

        self.balance_label.config(
            text=(
                f"Customer: {customer.name} | "
                f"ID: {customer.customer_id} | "
                f"Balance: ${balance:.2f}"
            )
        )


    def view_customer_appointments(self):
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

            success, message, appointments = (
                self.appointment_controller.get_customer_appointments(
                    customer_id
                )
            )

            if not success:
                messagebox.showerror(
                    "Error",
                    message,
                    parent=self.root
                )
                return
            self.refresh_customer_balance(customer_id)

            lines = []

            for appointment in appointments:
                offering_name = self.get_offering_name(
                    appointment.offering_id
                )

                lines.append(
                    f"Appointment ID: {appointment.appointment_id}\n"
                    f"Offering: {offering_name}\n"
                    f"Date: {appointment.appointment_date}\n"
                    f"Time: {appointment.start_time.strftime('%H:%M')}\n"
                    f"Status: {appointment.status}\n"
                    f"Price: ${Decimal(str(appointment.price_paid)):.2f}\n"
                    f"{'-' * 45}"
                )

            if not lines:
                lines.append("No appointments found for this customer.")

            self.results.config(state="normal")
            self.results.delete("1.0", tk.END)
            self.results.insert("1.0", "\n".join(lines))
            self.results.config(state="disabled")

        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Invalid Input",
                str(error),
                parent=self.root
            )

    def cancel_appointment(self):
        appointment_id_text = self.appointment_id_entry.get().strip()

        if not appointment_id_text:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the appointment ID you want to cancel.",
                parent=self.root
            )
            return

        try:
            appointment_id = int(appointment_id_text)

            # Retrieve the appointment before asking for confirmation.
            success, message, appointment = (
                self.appointment_controller.get_appointment(
                    appointment_id
                )
            )

            if not success:
                messagebox.showerror(
                    "Error",
                    message,
                    parent=self.root
                )
                return

            if appointment.status != "booked":
                messagebox.showwarning(
                    "Cannot Cancel",
                    "Only booked appointments can be cancelled.",
                    parent=self.root
                )
                return

            price = Decimal(str(appointment.price_paid))
            cancellation_fee = price * Decimal("0.20")
            refund_amount = price * Decimal("0.80")

            confirmed = messagebox.askyesno(
                "Confirm Cancellation",
                f"Appointment ID: {appointment_id}\n"
                f"Original price: ${price:.2f}\n"
                f"Cancellation fee: ${cancellation_fee:.2f}\n"
                f"Refund amount: ${refund_amount:.2f}\n\n"
                "Are you sure you want to cancel this appointment?",
                parent=self.root
            )

            if not confirmed:
                return

            success, message, result = (
                self.appointment_controller.cancel_appointment(
                    appointment_id
                )
            )

            if not success:
                messagebox.showerror(
                    "Cancellation Failed",
                    message,
                    parent=self.root
                )
                return

            actual_fee = Decimal(
                str(result["cancellation_fee"])
            )
            actual_refund = Decimal(
                str(result["refund_amount"])
            )

            messagebox.showinfo(
                "Cancellation Successful",
                f"Appointment cancelled successfully.\n\n"
                f"Cancellation fee: ${actual_fee:.2f}\n"
                f"Refund: ${actual_refund:.2f}",
                parent=self.root
            )

            # Refresh the appointment list if a customer ID is entered.
            if self.customer_id_entry.get().strip():
                self.view_customer_appointments()

        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Invalid Input",
                str(error),
                parent=self.root
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not cancel the appointment:\n{error}",
                parent=self.root
            )

    def clear_booking_fields(self):
        self.appointment_id_entry.delete(0, tk.END)
        self.customer_id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.offering_combo.set("")

        # Clear the customer balance display
        self.balance_label.config(
            text="Customer: -- | ID: -- | Balance: --"
        )
        # Clear the appointment results
        self.results.config(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.config(state="disabled")