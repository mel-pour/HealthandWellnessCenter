import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal


class OfferingView:
    def __init__(self, root, offering_service, back_callback):
        self.root = root
        self.offering_service = offering_service
        self.back_callback = back_callback

        self.root.geometry("600x550")

        self.main_frame = tk.Frame(root, padx=20, pady=15)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Offering Management",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 15))

        # Offering ID
        self.id_entry = self.create_entry("Offering ID:")

        # Name
        self.name_entry = self.create_entry("Name:")

        # Type dropdown
        self.type_combo = self.create_dropdown(
            "Type:",
            ("service", "facility")
        )

        # Price
        self.price_entry = self.create_entry("Price:")

        # Duration
        self.duration_entry = self.create_entry(
            "Duration (minutes, optional for facilities):"
        )

        tk.Button(
            self.main_frame,
            text="Create Offering",
            command=self.create_offering
        ).pack(pady=15)

        tk.Label(
            self.main_frame,
            text="Existing Offerings",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.offerings_list = tk.Listbox(
            self.main_frame,
            height=8,
            width=65
        )
        self.offerings_list.pack(fill="both", expand=True, pady=5)

        tk.Button(
            self.main_frame,
            text="Back to Main Menu",
            command=self.back_callback
        ).pack(pady=10)

        self.load_offerings()

    def create_entry(self, label_text):
        row = tk.Frame(self.main_frame)
        row.pack(fill="x", pady=4)

        tk.Label(
            row,
            text=label_text,
            width=35,
            anchor="w"
        ).pack(side="left")

        entry = tk.Entry(row, width=25)
        entry.pack(side="left")

        return entry

    def create_dropdown(self, label_text, options):
        row = tk.Frame(self.main_frame)
        row.pack(fill="x", pady=4)

        tk.Label(
            row,
            text=label_text,
            width=35,
            anchor="w"
        ).pack(side="left")

        combo = ttk.Combobox(
            row,
            values=options,
            state="readonly",
            width=22
        )
        combo.pack(side="left")

        if options:
            combo.current(0)

        return combo

    def create_offering(self):
        try:
            # Validate Offering ID
            offering_id_text = self.id_entry.get().strip()

            if not offering_id_text:
                raise ValueError("Please enter an Offering ID.")

            offering_id = int(offering_id_text)

            # Validate name
            name = self.name_entry.get().strip()

            if not name:
                raise ValueError("Please enter an offering name.")

            # Validate offering type
            offering_type = self.type_combo.get()

            if not offering_type:
                raise ValueError("Please select an offering type.")

            # Validate price
            price = self.price_entry.get().strip()

            if not price:
                raise ValueError("Please enter the offering price.")

            # Validate duration
            duration_text = self.duration_entry.get().strip()

            if duration_text:
                try:
                    duration = int(duration_text)
                except ValueError as error:
                    raise ValueError(
                        "Duration must be a whole number of minutes."
                    ) from error
            else:
                duration = None

            # Create offering through the service layer
            offering = self.offering_service.create_offering(
                offering_id,
                name,
                offering_type,
                price,
                duration
            )

            messagebox.showinfo(
                "Success",
                f"Offering '{offering.name}' created successfully.",
                parent=self.root
            )

            self.clear_fields()
            self.load_offerings()

        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Invalid Input",
                str(error),
                parent=self.root
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not create offering:\n{error}",
                parent=self.root
            )

    def load_offerings(self):
        self.offerings_list.delete(0, tk.END)

        try:
            offerings = self.offering_service.get_all_offerings()

            for offering in offerings:
                duration = (
                    f"{offering.duration} min"
                    if offering.duration is not None
                    else "N/A"
                )

                price = Decimal(str(offering.price))

                self.offerings_list.insert(
                    tk.END,
                    f"ID: {offering.offering_id} | "
                    f"{offering.name} | "
                    f"Type: {offering.offering_type} | "
                    f"Price: ${price:.2f} | "
                    f"Duration: {duration}"
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not load offerings:\n{error}",
                parent=self.root
            )

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.type_combo.current(0)
        self.price_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)