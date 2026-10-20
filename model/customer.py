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

    def __repr__(self):
        return (f"Customer(\n, customer_id= {self.customer_id}\n"
                f", name= {self.name}\n"
                f", social_id= {self.social_id}\n"
                f", age= {self.age}\n"
                f", gender= {self.gender}\n"
                f", phone_number= {self.phone_number}\n"
                f", balance= {self.balance}")
