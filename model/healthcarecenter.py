from validation.validation import *

from offering import Offering


class HealthcareCenter:
    def __init__(self, center_id, name, center_address, center_phone_number,offerings):
        self.center_id = center_id
        self.name = name
        self.center_address = center_address
        self.center_phone_number = center_phone_number
        self.offerings = []

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

    @property
    def offerings(self):
        return self.__offerings.copy()

    @offerings.setter
    def offerings(self, value):
        if not isinstance(value, list):
            raise ValueError("Offerings must be provided as a list.")

        if not all(isinstance(item, Offering) for item in value):
            raise ValueError("Every item must be an Offering object.")

        self.__offerings = value.copy()

    def get_info(self):
        return (
            f"Center ID: {self.center_id}, "
            f"Name: {self.name}, "
            f"Address: {self.center_address}, "
            f"Phone: {self.center_phone_number}"
        )

    def add_offering(self, offering):
        if not isinstance(offering, Offering):
            raise TypeError("The offering must be an Offering object.")

        if self.find_offering(offering.offering_id) is not None:
            raise ValueError("This offering ID already exists.")

        self.__offerings.append(offering)

    def find_offering(self, offering_id):
        for offering in self.__offerings:
            if offering.offering_id == offering_id:
                return offering

        return None

    def get_all_offerings(self):
        return self.offerings


    def __repr__(self):
        return (f"HealthcareCenter(\n, center_id= {self.center_id}\n"
                f", name= {self.name}\n"
                f", center_address= {self.center_address}\n"
                f", center_phone_number= {self.center_phone_number}\n")
