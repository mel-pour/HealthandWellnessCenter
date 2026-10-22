from validation.validation import *

from offering import Offering


class HealthcareCenter:
    def __init__(self, center_id, name, center_address, center_phone_number, offerings=None):
        self.center_id = center_id
        self.name = name
        self.center_address = center_address
        self.center_phone_number = center_phone_number
        if offerings is None:
            self.offerings = []
        else:
            self.offerings = offerings

    @property
    def center_id(self):
        return self.__center_id

    @center_id.setter
    def center_id(self, value):
        center_id_validator(value)
        self.__center_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = required_text_validator(value, "Center name")

    @property
    def center_address(self):
        return self.__center_address

    @center_address.setter
    def center_address(self, value):
        self.__center_address = required_text_validator(value, "Address")

    @property
    def center_phone_number(self):
        return self.__center_phone_number

    @center_phone_number.setter
    def center_phone_number(self, value):
        center_phone_number_validator(value)
        self.__center_phone_number = value


    def get_info(self):
        return (
            f"Center ID: {self.center_id}, "
            f"Name: {self.name}, "
            f"Address: {self.center_address}, "
            f"Phone: {self.center_phone_number}"
        )



    def __repr__(self):
        return (f"HealthcareCenter(\n, center_id= {self.center_id}\n"
                f", name= {self.name}\n"
                f", center_address= {self.center_address}\n"
                f", center_phone_number= {self.center_phone_number}\n")
