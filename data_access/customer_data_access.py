
from decimal import Decimal

from models.customer import Customer


class CustomerDataAccess:
    def __init__(self, storage):
        self.storage = storage

    def add(self, customer):
        data = self.storage.load()
        customers = data["customers"]

        if self.find_by_id(customer.customer_id) is not None:
            raise ValueError("Customer ID already exists.")

        customers.append({
            "customer_id": customer.customer_id,
            "name": customer.name,
            "social_id": customer.social_id,
            "age": customer.age,
            "gender": customer.gender,
            "phone_number": customer.phone_number,
            "balance": str(customer.balance)
        })

        self.storage.save(data)

    def find_by_id(self, customer_id):
        data = self.storage.load()

        for item in data["customers"]:
            if item["customer_id"] == customer_id:
                return Customer(
                    item["customer_id"],
                    item["name"],
                    item["social_id"],
                    item["age"],
                    item["gender"],
                    item["phone_number"],
                    Decimal(item["balance"])
                )

        return None

    def get_all(self):
        data = self.storage.load()
        customers = []

        for item in data["customers"]:
            customers.append(
                Customer(
                    item["customer_id"],
                    item["name"],
                    item["social_id"],
                    item["age"],
                    item["gender"],
                    item["phone_number"],
                    Decimal(item["balance"])
                )
            )

        return customers

    def update(self, customer):
        data = self.storage.load()

        for index, item in enumerate(data["customers"]):
            if item["customer_id"] == customer.customer_id:
                data["customers"][index] = {
                    "customer_id": customer.customer_id,
                    "name": customer.name,
                    "social_id": customer.social_id,
                    "age": customer.age,
                    "gender": customer.gender,
                    "phone_number": customer.phone_number,
                    "balance": str(customer.balance)
                }

                self.storage.save(data)
                return True

        return False

    def delete(self, customer_id):
        data = self.storage.load()
        customers = data["customers"]

        for index, item in enumerate(customers):
            if item["customer_id"] == customer_id:
                del customers[index]
                self.storage.save(data)
                return True

        return False
