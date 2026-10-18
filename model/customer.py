from validation.validation import *
from decimal import Decimal, ROUND_HALF_UP


class Customer:
    def __init__(self, customer_id, name, social_id, age, gender, phone_number, balance):
        self.customer_id = customer_id
        self.name = name
        self.social_id = social_id
        self.age = age
        self.gender = gender
        self.phone_number = phone_number
        self.balance = balance

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        customer_id_validator(value)
        self.__customer_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        customer_name_validator(value)
        self.__name = value

    @property
    def social_id(self):
        return self.__social_id

    @social_id.setter
    def social_id(self, value):
        social_id_validator(value)
        self.__social_id = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        age_validator(value)
        self.__age = value

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        gender_validator(value)
        self.__gender = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        phone_number_validator(value)
        self.__phone_number = value

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        balance_validator(value)
        self.__balance = value

    def get_info(self):
        return (
            f"ID: {self.customer_id}\n"
            f"Name: {self.name}\n"
            f"Social ID: {self.social_id}\n"
            f"Phone: {self.phone_number}"
        )

    def book_appointment(self, appointment):
        return appointment.book()

    def cancel_appointment(self, appointment):
        return appointment.cancel()


    @staticmethod
    def to_decimal(amount):
        return Decimal(str(amount)).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)


    def add_balance(self, amount):
        amount = self.to_decimal(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.balance += amount


    def has_enough_balance(self, amount):
        amount = self.to_decimal(amount)
        return self.balance >= amount


    def deduct_balance(self, amount):
        amount = self.to_decimal(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not self.has_enough_balance(amount):
            raise ValueError("Insufficient account balance.")
        self.balance -= amount

    def refund(self, amount):
        amount = self.to_decimal(amount)
        if amount < 0:
            raise ValueError("Refund cannot be negative.")
        self.balance += amount


    def purchase_offering(self, offering):
        if self.has_enough_balance(offering.price):
            self.deduct_balance(offering.price)
            return True
        return False




