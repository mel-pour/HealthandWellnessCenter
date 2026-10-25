class CustomerController:
    def __init__(self, customer_service):
        self.customer_service = customer_service

    def create_customer(
        self, customer_id, name, social_id, age,
        gender, phone_number, balance
    ):
        try:
            customer = self.customer_service.create_customer(
                customer_id,
                name,
                social_id,
                age,
                gender,
                phone_number,
                balance
            )

            return True, "Customer created successfully.", customer

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_customer(self, customer_id):
        try:
            customer = self.customer_service.get_customer(customer_id)

            return True, "Customer found successfully.", customer

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_all_customers(self):
        try:
            customers = self.customer_service.get_all_customers()

            return True, "Customers retrieved successfully.", customers

        except Exception:
            return False, "Could not retrieve customers.", None

    def get_customer_info(self, customer_id):
        try:
            info = self.customer_service.get_customer_info(customer_id)

            return True, "Customer information retrieved successfully.", info

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def add_balance(self, customer_id, amount):
        try:
            self.customer_service.add_balance(customer_id, amount)

            customer = self.customer_service.get_customer(customer_id)

            return True, "Balance added successfully.", customer

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def has_enough_balance(self, customer_id, amount):
        try:
            enough_balance = self.customer_service.has_enough_balance(
                customer_id, amount
            )

            if enough_balance:
                return True, "Sufficient balance.", True

            return True, "Insufficient account balance.", False

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def deduct_balance(self, customer_id, amount):
        try:
            self.customer_service.deduct_balance(customer_id, amount)

            customer = self.customer_service.get_customer(customer_id)

            return True, "Balance deducted successfully.", customer

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def refund(self, customer_id, amount):
        try:
            self.customer_service.refund(customer_id, amount)

            customer = self.customer_service.get_customer(customer_id)

            return True, "Refund processed successfully.", customer

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None