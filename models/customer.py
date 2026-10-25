from validation.validation import (customer_id_validator, customer_name_validator, social_id_validator, age_validator,
                                   gender_validator, phone_number_validator, balance_validator)


class Customer:
    def __init__(self, customer_id, name, social_id, age, gender, phone_number, balance):
        self.customer_id = customer_id
        self.name = name
        self.social_id = social_id
        self.age = age
        self.gender = gender
        self.phone_number = phone_number
        self.balance = balance

    # ==============================================
    # CUSTOMER ID
    # ==============================================

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = customer_id_validator(value)

    # ==============================================
    # NAME
    # ==============================================

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = customer_name_validator(value)

    # ==============================================
    # SOCIAL ID
    # ==============================================

    @property
    def social_id(self):
        return self.__social_id

    @social_id.setter
    def social_id(self, value):
        self.__social_id = social_id_validator(value)

    # ==============================================
    # AGE
    # ==============================================

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = age_validator(value)

    # ==============================================
    # GENDER
    # ==============================================

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        self.__gender = gender_validator(value)

    # ==============================================
    # PHONE NUMBER
    # ==============================================

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = phone_number_validator(value)

    # ==============================================
    # BALANCE
    # ==============================================

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        self.__balance = balance_validator(value)

    # ==============================================
    # INFORMATION
    # ==============================================

    def get_info(self):
        return (
            f"Customer ID: {self.customer_id}\n"
            f"Name: {self.name}\n"
            f"Social ID: {self.social_id}\n"
            f"Age: {self.age}\n"
            f"Gender: {self.gender}\n"
            f"Phone: {self.phone_number}\n"
            f"Balance: {self.balance:.2f}"
        )

    # ==============================================
    # OBJECT REPRESENTATION
    # ==============================================

    def __repr__(self):
        return (
            f"Customer("
            f"customer_id={self.customer_id}, "
            f"name={self.name!r}, "
            f"social_id={self.social_id!r}, "
            f"age={self.age}, "
            f"gender={self.gender!r}, "
            f"phone_number={self.phone_number!r}, "
            f"balance={self.balance!r}"
            f")"
        )
