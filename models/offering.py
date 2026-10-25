from validation.validation import (offering_id_validator, offering_name_validator, offering_type_validator,
                                   price_validator, offering_duration_validator)


class Offering:
    def __init__(self, offering_id, name, offering_type, price, duration=None):
        self.offering_id = offering_id
        self.name = name
        self.offering_type = offering_type
        self.price = price
        self.duration = duration

    # ==============================================
    # OFFERING ID
    # ==============================================

    @property
    def offering_id(self):
        return self.__offering_id

    @offering_id.setter
    def offering_id(self, value):
        self.__offering_id = offering_id_validator(value)

    # ==============================================
    # NAME
    # ==============================================

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = offering_name_validator(value)

    # ==============================================
    # OFFERING TYPE
    # ==============================================

    @property
    def offering_type(self):
        return self.__offering_type

    @offering_type.setter
    def offering_type(self, value):
        self.__offering_type = offering_type_validator(value)

    # ==============================================
    # PRICE
    # ==============================================

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = price_validator(value)

    # ==============================================
    # DURATION
    # ==============================================

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = offering_duration_validator(self.offering_type, value)

    # ==============================================
    # OBJECT REPRESENTATION
    # ==============================================

    def __repr__(self):
        return (
            f"Offering("
            f"offering_id={self.offering_id}, "
            f"name={self.name!r}, "
            f"offering_type={self.offering_type!r}, "
            f"price={self.price!r}, "
            f"duration={self.duration!r}"
            f")"
        )
