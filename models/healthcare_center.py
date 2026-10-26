from validation.validation import (center_id_validator, center_name_validator, center_address_validator,
                                   center_phone_number_validator)


class HealthcareCenter:
    def __init__(
            self,
            center_id,
            name,
            center_address,
            center_phone_number,
            offerings=None
    ):
        self.center_id = center_id
        self.name = name
        self.center_address = center_address
        self.center_phone_number = center_phone_number

        if offerings is None:
            self.offerings = []
        else:
            self.offerings = list(offerings)

    # ==============================================
    # CENTER ID
    # ==============================================

    @property
    def center_id(self):
        return self.__center_id

    @center_id.setter
    def center_id(self, value):
        self.__center_id = center_id_validator(value)

    # ==============================================
    # NAME
    # ==============================================

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = center_name_validator(value)

    # ==============================================
    # ADDRESS
    # ==============================================

    @property
    def center_address(self):
        return self.__center_address

    @center_address.setter
    def center_address(self, value):
        self.__center_address = center_address_validator(value)

    # ==============================================
    # PHONE NUMBER
    # ==============================================

    @property
    def center_phone_number(self):
        return self.__center_phone_number

    @center_phone_number.setter
    def center_phone_number(self, value):
        self.__center_phone_number = center_phone_number_validator(value)

    # ==============================================
    # INFORMATION
    # ==============================================

    def get_info(self):
        return (
            f"Center ID: {self.center_id}, "
            f"Name: {self.name}, "
            f"Address: {self.center_address}, "
            f"Phone: {self.center_phone_number}"
        )

    # ==============================================
    # OBJECT REPRESENTATION
    # ==============================================

    def __repr__(self):
        return (
            f"HealthcareCenter("
            f"center_id={self.center_id}, "
            f"name={self.name!r}, "
            f"center_address={self.center_address!r}, "
            f"center_phone_number={self.center_phone_number!r}, "
            f"offerings={self.offerings!r}"
            f")"
        )
