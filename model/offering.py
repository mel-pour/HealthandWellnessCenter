from validation.validation import *


class Offering:
    def __init__(self, offering_id, name, offering_type, price, duration=None):
        self.offering_id = offering_id
        self.name = name
        self.offering_type = offering_type
        self.price = price
        self.duration = duration

    @property
    def offering_id(self):
        return self.__offering_id

    @offering_id.setter
    def offering_id(self, value):
        offering_id_validator(value)
        self.__offering_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        offering_name_validator(value)
        self.__name = value

    @property
    def offering_type(self):
        return self.__offering_type

    @offering_type.setter
    def offering_type(self, value):
        offering_type_validator(value)
        self.__offering_type = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        price_validator(value)
        self.__price = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        offering_duration_validator(self.offering_type, value)
        self.__duration = value

    def get_info(self):
        return (
            f"ID: {self.offering_id}, "
            f"Name: {self.name}, "
            f"Type: {self.offering_type}, "
            f"Price: {self.price:.2f}, "
            f"Duration: {self.duration}"
        )

    def __repr__(self):
        return (f"Offering(\n, offering_id= {self.offering_id}\n"
                f", name= {self.name}\n"
                f", offering_type= {self.offering_type}\n"
                f", price= {self.price}\n"
                f", duration= {self.duration}")

