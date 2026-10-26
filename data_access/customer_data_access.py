from decimal import Decimal

from models.customer import Customer


class CustomerDataAccess:
    def __init__(self, storage):
        self.storage = storage

    def add(self, customer):
        data = self.storage.load()
        customers = data["customers"]

        # Check for duplicate customer IDs.
        if any(
            item["customer_id"] == customer.customer_id
            for item in customers
        ):
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
        return True

    def find_by_id(self, customer_id):
        data = self.storage.load()

        for item in data["customers"]:
            if item["customer_id"] == customer_id:
                return self._create_customer(item)

        return None

    def get_all(self):
        data = self.storage.load()

        return [
            self._create_customer(item)
            for item in data["customers"]
        ]

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

    @staticmethod
    def _create_customer(item):
        return Customer(
            customer_id=item["customer_id"],
            name=item["name"],
            social_id=item["social_id"],
            age=item["age"],
            gender=item["gender"],
            phone_number=item["phone_number"],
            balance=Decimal(str(item["balance"]))
        )