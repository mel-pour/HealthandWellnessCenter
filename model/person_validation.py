import re

specialty_list = ["massage", "facial", "manicure", "lifeguard", "gym coach", "facility supervision", "reception",
                  "management", "office work"]


def person_id_validator(person_id):
    if not isinstance(person_id, int):
        raise ValueError("Invalid Person ID !!!")
    return person_id


def name_validator(name):
    if not isinstance(name, str) or not re.match(r"^[a-zA-Z\s]{3,50}$", name):
        raise ValueError("Invalid Name !!!")
    return name


def family_validator(family):
    if not isinstance(family, str) or not re.match(r"^[a-zA-Z\s]{3,50}$", family):
        raise ValueError("Invalid Family !!!")
    return family


def social_id_validator(social_id):
    if not isinstance(social_id, str) or not re.match(r"^(\d{10}|\d{3}-\d{6}-\d)$", social_id):
        raise ValueError("Invalid Social_id !!!")
    return social_id


def age_validator(age):
    if not isinstance(age, int) or not (5 <= int(age) <= 80):
        raise ValueError(" Age Not Authorized !!!")
    return age


def gender_validator(gender):
    if not isinstance(gender, str) or not re.match("(male|female)", gender):
        raise ValueError("Enter A Correct Gender (male/female) !!!")
    return gender


def phone_number_validator(phone_number):
    if not isinstance(phone_number, str) or not re.match(r"^(\d{11}|\+98\d{10})$", phone_number):
        raise ValueError("Enter A Correct Phone Number !!!")
    return phone_number


def employees_role_validator(role):
    if not isinstance(role, str) or not re.match("(instructor|service_provider|facility_staff|administration)", role):
        raise ValueError("Enter A Correct Role !!!")
    return role


# def employees_specialty_validator(specialty):
#     if not isinstance(specialty, str) or not re.match(f"({"|".join(specialty_list)})", specialty):
#         raise ValueError("Enter A Correct Specialty !!!")
#     return specialty


def employees_salary_validator(salary):
    if not isinstance(salary, int) or not (3000 <= int(salary) <= 10000):
        raise ValueError(" Salary Must BE In Authorized Range!!!")
    return salary