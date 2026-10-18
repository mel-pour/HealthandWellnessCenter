from validation.validation import *

class Appointment:
    def __init__(
        self,
        appointment_id,
        customer_id,
        offering_id,
        appointment_date,
        start_time,
        price_paid,
        status="pending"
    ):
        self.appointment_id = appointment_id
        self.customer_id = customer_id
        self.offering_id = offering_id
        self.appointment_date = appointment_date
        self.start_time = start_time
        self.price_paid = price_paid
        self.status = status

    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, value):
        appointment_id_validator(value)
        self.__appointment_id = value

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        customer_id_validator(value)
        if value <= 0:
            raise ValueError("Customer ID must be positive.")
        self.__customer_id = value

    @property
    def offering_id(self):
        return self.__offering_id

    @offering_id.setter
    def offering_id(self, value):
        offering_id_validator(value)
        self.__offering_id = value

    @property
    def appointment_date(self):
        return self.__appointment_date

    @appointment_date.setter
    def appointment_date(self, value):
        appointment_date_validator(value)
        self.__appointment_date = value

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        start_time_validator(value)
        self.__start_time = value

    @property
    def price_paid(self):
        return self.__price_paid

    @price_paid.setter
    def price_paid(self, value):
        price_validator(value)
        self.__price_paid = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        appointment_status_validator(value)
        self.__status = value

    def get_info(self):
        return (
            f"Appointment ID: {self.appointment_id}, "
            f"Customer ID: {self.customer_id}, "
            f"Offering ID: {self.offering_id}, "
            f"Date: {self.appointment_date}, "
            f"Time: {self.start_time.strftime('%H:%M')}, "
            f"Status: {self.status}, "
            f"Price: {self.price_paid:.2f}"
        )

    def book(self):
        if self.status != "pending":
            raise ValueError("Only a pending appointment can be booked.")

        self.status = "booked"

    def calculate_cancellation_fee(self):
        return round(self.price_paid * 0.20, 2)

    def cancel(self):
        if self.status != "booked":
            raise ValueError("Only a booked appointment can be cancelled.")
        fee = self.calculate_cancellation_fee()
        refund = round(self.price_paid - fee, 2)
        self.status = "cancelled"
        return fee, refund

    def __repr__(self):
        return (f"Appointment(\n, appointment_id= {self.appointment_id}\n"
                f", customer_id= {self.customer_id}\n"
                f", offering_id= {self.offering_id}\n"
                f", appointment_date= {self.appointment_date}\n"
                f", start_time= {self.start_time}\n"
                f", price_paid= {self.price_paid}\n"
                f", status= {self.status}")

