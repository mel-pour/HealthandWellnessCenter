from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from models.customer import Customer
from utils.logger import get_logger

logger = get_logger(__name__)


class CustomerService:
    def __init__(self, customer_data_access):
        self.customer_data_access = customer_data_access

    @staticmethod
    def to_decimal(amount):
        try:
            if isinstance(amount, bool):
                raise ValueError("Amount must be a valid number.")

            result = Decimal(str(amount))

            if not result.is_finite():
                raise ValueError("Amount must be a finite number.")

            return result.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError("Amount must be a valid monetary value.") from error

    def _save_customer(self, customer):
        if not self.customer_data_access.update(customer):
            logger.error(
                "Failed to update customer ID %s.",
                customer.customer_id
            )
            raise ValueError("Failed to update customer.")

    def create_customer(
            self, customer_id, name, social_id, age, gender, phone_number, balance):
        customer = Customer(customer_id, name, social_id, age, gender, phone_number, balance)

        self.customer_data_access.add(customer)

        logger.info(
            "Customer created successfully. ID: %s",
            customer.customer_id
        )

        return customer

    def get_customer(self, customer_id):
        customer = self.customer_data_access.find_by_id(customer_id)

        if customer is None:
            logger.warning(
                "Customer not found. ID: %s",
                customer_id
            )
            raise ValueError("Customer not found.")

        return customer

    def get_all_customers(self):
        return self.customer_data_access.get_all()

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
        self._save_customer(customer)

        logger.info(
            "Balance added successfully for customer ID %s.",
            customer_id
        )

    def has_enough_balance(self, customer_id, amount):
        customer = self.get_customer(customer_id)
        amount = self.to_decimal(amount)

        if amount < 0:
            raise ValueError("Amount cannot be negative.")

        return self.to_decimal(customer.balance) >= amount

    def deduct_balance(self, customer_id, amount):
        customer = self.get_customer(customer_id)
        amount = self.to_decimal(amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if self.to_decimal(customer.balance) < amount:
            raise ValueError("Insufficient account balance.")

        customer.balance = self.to_decimal(customer.balance) - amount
        self._save_customer(customer)

        logger.info(
            "Balance deducted successfully for customer ID %s.",
            customer_id
        )

    def refund(self, customer_id, amount):
        customer = self.get_customer(customer_id)
        amount = self.to_decimal(amount)

        if amount < 0:
            raise ValueError("Refund cannot be negative.")

        customer.balance = self.to_decimal(customer.balance) + amount
        self._save_customer(customer)

        logger.info(
            "Refund processed successfully for customer ID %s.",
            customer_id
        )

    def purchase_offering(self, customer_id, offering):
        amount = self.to_decimal(offering.price)

        if self.has_enough_balance(customer_id, amount):
            self.deduct_balance(customer_id, amount)

            logger.info(
                "Offering purchased by customer ID %s.",
                customer_id
            )

            return True

        logger.warning(
            "Purchase declined due to insufficient balance. "
            "Customer ID: %s",
            customer_id
        )

        return False
