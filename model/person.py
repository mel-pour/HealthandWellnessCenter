from model.person_validation import *


class Person:
    def __init__(self, person_id, name, family, social_id, age, gender, phone_number):
        self.person_id = person_id
        self.name = name
        self.family = family
        self.social_id = social_id
        self.age = age
        self.gender = gender
        self.phone_number = phone_number

    @property
    def person_id(self):
        return self.__person_id

    @person_id.setter
    def person_id(self, value):
        person_id_validator(value)
        self.__person_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        name_validator(value)
        self.__name = value

    @property
    def family(self):
        return self.__family

    @family.setter
    def family(self, value):
        family_validator(value)
        self.__family = value

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

    def get_info(self):
        pass


class Employee(Person):
    def __init__(self, person_id, name, family, social_id, age, gender, phone_number, role, specialty, salary):
        Person.__init__(person_id, name, family, social_id, age, gender, phone_number)
        self.role = role
        self.specialty = specialty
        self.salary = salary

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        employees_role_validator(value)
        self.__role = value

    @property
    def specialty(self):
        return self.__specialty

    @specialty.setter
    def specialty(self, value):
        # employees_specialty_validator()
        self.__specialty = value

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        employees_salary_validator(value)
        self.__salary = value

    def availability(self):
        pass


class Customer(Person):
    def __init__(self, person_id, name, family, social_id, age, gender, phone_number, account):
        Person.__init__(person_id, name, family, social_id, age, gender, phone_number)
        self.account = account

    def payment(self):
        pass

    def enroll_in_class(self):
        pass

    def use_facilities(self):
        pass

    def book_appointments(self):
        pass
