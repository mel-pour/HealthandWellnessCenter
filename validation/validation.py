import re
from datetime import date, time


# ==================================================
# GENERAL VALIDATION
# ==================================================

def validate_positive_id(value, field_name="ID"):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive and a number !!!")
    return value


def required_text_validator(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()

def required_name_validator(value , field_name):
    if not isinstance(value, str) or not re.match(r"^[a-zA-Z\s]{3,50}$", value):
        raise ValueError(f"{field_name}IS Invalid !!!")
    return value

# ==================================================
# 1. CUSTOMER
# ==================================================

def customer_id_validator(value):
    return validate_positive_id(value, "Customer ID")


def customer_name_validator(value):
    return required_name_validator(value, "customer name")


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
    if not isinstance(phone_number, str) or not re.match(r"^(09\d{9}|\+989\d{9})$", phone_number):
        raise ValueError("Enter A Correct Phone Number !!!")
    return phone_number


def balance_validator(balance):
    if not isinstance(balance,int)or (int(balance) <= 0):
        raise ValueError(" Balance Can Not Be zero Or Negative !!!")
    return balance

# ==================================================
# OFFERING VALIDATION
# ==================================================

def offering_id_validator(value):
    return validate_positive_id(value, "Offering ID")


def offering_name_validator(value):
    return required_name_validator(value, "Offering name")


def offering_type_validator(offering_type):
    if not isinstance(offering_type, str) or not re.match("(service|facility)", offering_type):
        raise ValueError("Offering type must be service or facility !!!")
    return offering_type


def price_validator(value):
    if not isinstance(value, (int, float)) or value <= 0 :
        raise ValueError("Price must be a Number greater or equal to 0.")

    return round(float(value), 2)


def duration_validator(value):
    if value is None:
        return value

    if isinstance(value, int) or value <= 0:
        raise ValueError("Duration must be a positive number of minutes.")

    return value


def offering_duration_validator(offering_type, duration):
    # Validate the type and duration using their own validators.
    offering_type = offering_type_validator(offering_type)
    duration = duration_validator(duration)

    if offering_type == "service" and duration is None:
        raise ValueError("A service must have a duration.")

    return duration

# ==================================================
# APPOINTMENT VALIDATION
# ==================================================

def appointment_id_validator(value):
    return validate_positive_id(value, "Appointment ID")


def appointment_customer_id_validator(value):
    return validate_positive_id(value, "Customer ID")


def appointment_offering_id_validator(value):
    return validate_positive_id(value, "Offering ID")


def appointment_date_validator(value):
    if not isinstance(value, date) :
        raise ValueError("Appointment date must be a valid date.")
    return value


def start_time_validator(value):
    if not isinstance(value, time):
        raise ValueError("Start time must be a valid time.")
    return value


def appointment_status_validator(value):
    if not isinstance(value, str) or not re.match("(pending|booked|cancelled)", value):
                raise ValueError("Status must be pending, booked, or cancelled !!!")
    return value

# ==================================================
# HEALTHCARE CENTER VALIDATION
# ==================================================

def center_id_validator(value):
    return validate_positive_id(value, "Center ID")


def center_name_validator(value):
    return required_name_validator(value, "Center name")


def center_address_validator(value):
    return required_text_validator(value, "Address")


def center_phone_number_validator(center_phone_number):
    if not isinstance(center_phone_number, str) or not re.match(r"^(0\d{10}|\+98\d{10})$", center_phone_number):
        raise ValueError("Enter A Correct Phone Number !!!")
    return center_phone_number
