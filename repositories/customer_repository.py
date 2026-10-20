class CustomerRepository:
    def __init__(self):
        self.__customers = {}

    def add(self, customer):
        customer_id = customer.customer_id

        if customer_id in self.__customers:
            raise ValueError("Customer ID already exists.")

        if self.find_by_social_id(customer.social_id) is not None:
            raise ValueError("A customer with this Social ID already exists.")

        self.__customers[customer_id] = customer

    def find_by_id(self, customer_id):
        return self.__customers.get(customer_id)

    def find_by_social_id(self, social_id):
        for customer in self.__customers.values():
            if customer.social_id == social_id:
                return customer

        return None

    def get_all(self):
        return list(self.__customers.values())

    def update(self, customer):
        customer_id = customer.customer_id

        if customer_id not in self.__customers:
            raise ValueError("Customer not found.")

        self.__customers[customer_id] = customer