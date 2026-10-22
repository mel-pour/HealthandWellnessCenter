from decimal import Decimal, ROUND_HALF_UP

from models.customer import Customer


class CustomerService:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    @staticmethod
    def to_decimal(amount):
        return Decimal(str(amount)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    def create_customer(self, customer_id, name, social_id, age, gender, phone_number, balance):
        customer = Customer(customer_id, name, social_id, age, gender, phone_number, balance)

        self.customer_repository.add(customer)
        return customer

    def get_customer(self, customer_id):
        customer = self.customer_repository.find_by_id(customer_id)

        if customer is None:
            raise ValueError("Customer not found.")

        return customer

    def get_all_customers(self):
        return self.customer_repository.get_all()

    def get_customer_info(self, customer_id):
        customer = self.get_customer(customer_id)

        return (
            f"ID: {customer.customer_id}\n"
            f"Name: {customer.name}\n"
            f"Social ID: {customer.social_id}\n"
            f"Phone: {customer.phone_number}"
        )

    def add_balance(self, customer_id, amount):
        customer = self.get_customer(customer_id)
        amount = self.to_decimal(amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        customer.balance = self.to_decimal(customer.balance) + amount
        self.customer_repository.update(customer)

    def has_enough_balance(self, customer_id, amount):
        customer = self.get_customer(customer_id)
        amount = self.to_decimal(amount)

        return self.to_decimal(customer.balance) >= amount

    def deduct_balance(self, customer_id, amount):
        customer = self.get_customer(customer_id)
        amount = self.to_decimal(amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if not self.has_enough_balance(customer_id, amount):
            raise ValueError("Insufficient account balance.")

        customer.balance = self.to_decimal(customer.balance) - amount
        self.customer_repository.update(customer)

    def refund(self, customer_id, amount):
        customer = self.get_customer(customer_id)
        amount = self.to_decimal(amount)

        if amount < 0:
            raise ValueError("Refund cannot be negative.")

        customer.balance = self.to_decimal(customer.balance) + amount
        self.customer_repository.update(customer)

    def purchase_offering(self, customer_id, offering):
        if self.has_enough_balance(customer_id, offering.price):
            self.deduct_balance(customer_id, offering.price)
            return True

        return False
