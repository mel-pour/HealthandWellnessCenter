import re
from datetime import date, time
from decimal import Decimal, InvalidOperation


# ==================================================
# GENERAL VALIDATION
# ==================================================

def validate_positive_id(value, field_name="ID"):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer.")

    return value


def required_text_validator(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")

    return value.strip()


def required_name_validator(value, field_name):
    value = required_text_validator(value, field_name)

    if not re.fullmatch(r"[a-zA-Z\s]{3,50}", value):
        raise ValueError(f"{field_name} is invalid.")

    return value


def positive_decimal_validator(value, field_name, allow_zero=False):
    """
    Convert a numeric value to Decimal and validate it.

    Returns:
        Decimal: The validated value rounded to two decimal places.
    """
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a number.")

    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{field_name} must be a valid number.") from None

    if not number.is_finite():
        raise ValueError(f"{field_name} must be a finite number.")

    if allow_zero:
        if number < 0:
            raise ValueError(f"{field_name} cannot be negative.")
    elif number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")

    return number.quantize(Decimal("0.01"))


# ==================================================
# 1. CUSTOMER
# ==================================================

def customer_id_validator(value):
    return validate_positive_id(value, "Customer ID")


def customer_name_validator(value):
    return required_name_validator(value, "Customer name")


def social_id_validator(social_id):
    social_id = required_text_validator(social_id, "Social ID")

    if not re.fullmatch(r"(\d{10}|\d{3}-\d{6}-\d)", social_id):
        raise ValueError("Invalid Social ID.")

    return social_id


def age_validator(age):
    if isinstance(age, bool) or not isinstance(age, int) or not 5 <= age <= 80:
        raise ValueError("Age must be an integer between 5 and 80.")

    return age


def gender_validator(gender):
    if not isinstance(gender, str):
        raise ValueError("Gender must be male or female.")

    gender = gender.strip().lower()

    if gender not in ("male", "female"):
        raise ValueError("Gender must be male or female.")

    return gender


def phone_number_validator(phone_number):
    phone_number = required_text_validator(phone_number, "Phone number")

    if not re.fullmatch(r"(09\d{9}|\+989\d{9})", phone_number):
        raise ValueError("Enter a valid phone number.")

    return phone_number


def balance_validator(balance):
    return positive_decimal_validator(
        balance,
        "Balance",
        allow_zero=True
    )


# ==================================================
# 2. OFFERING
# ==================================================

def offering_id_validator(value):
    return validate_positive_id(value, "Offering ID")


def offering_name_validator(value):
    return required_name_validator(value, "Offering name")


def offering_type_validator(offering_type):
    if not isinstance(offering_type, str):
        raise ValueError("Offering type must be service or facility.")

    offering_type = offering_type.strip().lower()

    if offering_type not in ("service", "facility"):
        raise ValueError("Offering type must be service or facility.")

    return offering_type


def price_validator(value):
    return positive_decimal_validator(
        value,
        "Price",
        allow_zero=False
    )


def duration_validator(value):
    if value is None:
        return None

    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("Duration must be a positive number of minutes.")

    return value


def offering_duration_validator(offering_type, duration):
    offering_type = offering_type_validator(offering_type)
    duration = duration_validator(duration)

    if offering_type == "service" and duration is None:
        raise ValueError("A service must have a duration.")

    return duration


# ==================================================
# 3. APPOINTMENT
# ==================================================

def appointment_id_validator(value):
    return validate_positive_id(value, "Appointment ID")


def appointment_customer_id_validator(value):
    return validate_positive_id(value, "Customer ID")


def appointment_offering_id_validator(value):
    return validate_positive_id(value, "Offering ID")


def appointment_date_validator(value):
    if not isinstance(value, date):
        raise ValueError("Appointment date must be a valid date.")

    return value


def start_time_validator(value):
    if not isinstance(value, time):
        raise ValueError("Start time must be a valid time.")

    return value


def appointment_status_validator(status):
    if not isinstance(status, str):
        raise ValueError("Status must be pending, booked, or cancelled.")

    status = status.strip().lower()

    if status not in ("pending", "booked", "cancelled"):
        raise ValueError("Status must be pending, booked, or cancelled.")

    return status


# ==================================================
# 4. HEALTHCARE CENTER
# ==================================================

def center_id_validator(value):
    return validate_positive_id(value, "Center ID")


def center_name_validator(value):
    return required_name_validator(value, "Center name")


def center_address_validator(value):
    return required_text_validator(value, "Address")


def center_phone_number_validator(center_phone_number):
    center_phone_number = required_text_validator(
        center_phone_number,
        "Center phone number"
    )

    if not re.fullmatch(r"(0\d{10}|\+98\d{10})", center_phone_number):
        raise ValueError("Enter a valid center phone number.")

    return center_phone_number