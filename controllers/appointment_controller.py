from datetime import datetime, date, time



class AppointmentController:
    def __init__(self, appointment_service, offering_service):
        self.appointment_service = appointment_service
        self.offering_service = offering_service

    @staticmethod
    def _parse_id(value, field_name):
        try:
            return int(value)
        except (ValueError, TypeError) as error:
            raise ValueError(
                f"{field_name} must be a valid integer."
            ) from error

    @staticmethod
    def _parse_date(value):
        if isinstance(value, date):
            return value

        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except (ValueError, TypeError, AttributeError) as error:
            raise ValueError(
                "Please enter a valid date in YYYY-MM-DD format."
            ) from error

    @staticmethod
    def _parse_time(value):
        if isinstance(value, time):
            return value

        try:
            return datetime.strptime(value.strip(), "%H:%M").time()
        except (ValueError, TypeError, AttributeError) as error:
            raise ValueError(
                "Please enter a valid time in HH:MM format, using 24-hour time."
            ) from error

    def create_appointment(
            self,
            appointment_id,
            customer_id,
            offering_id,
            appointment_date,
            start_time
    ):
        try:
            appointment_id = self._parse_id(
                appointment_id, "Appointment ID"
            )
            customer_id = self._parse_id(
                customer_id, "Customer ID"
            )
            offering_id = self._parse_id(
                offering_id, "Offering ID"
            )
            appointment_date = self._parse_date(appointment_date)
            start_time = self._parse_time(start_time)

            appointment = self.appointment_service.create_appointment(
                appointment_id,
                customer_id,
                offering_id,
                appointment_date,
                start_time
            )

            return True, "Appointment booked successfully.", appointment

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_appointment(self, appointment_id):
        try:
            appointment = self.appointment_service.get_appointment(
                appointment_id
            )

            return True, "Appointment found successfully.", appointment

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_all_appointments(self):
        try:
            appointments = (
                self.appointment_service.get_all_appointments()
            )

            return (
                True,
                "Appointments retrieved successfully.",
                appointments
            )

        except Exception:
            return False, "Could not retrieve appointments.", None

    def get_customer_appointments(self, customer_id):
        try:
            appointments = (
                self.appointment_service.get_customer_appointments(
                    customer_id
                )
            )

            return (
                True,
                "Customer appointments retrieved successfully.",
                appointments
            )

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def preview_cancellation(self, appointment_id):
        try:
            fee, refund_amount = (
                self.appointment_service.preview_cancellation(
                    appointment_id
                )
            )

            result = {
                "cancellation_fee": fee,
                "refund_amount": refund_amount
            }

            return (
                True,
                "Cancellation preview calculated successfully.",
                result
            )

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "Could not preview cancellation.", None

    def cancel_appointment(self, appointment_id):
        try:
            fee, refund_amount = (
                self.appointment_service.cancel_appointment(
                    appointment_id
                )
            )

            result = {
                "cancellation_fee": fee,
                "refund_amount": refund_amount
            }

            return (
                True,
                "Appointment cancelled successfully.",
                result
            )

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None

    def get_all_offerings(self):
        try:
            offerings = self.offering_service.get_all_offerings()
            return True, "Offerings retrieved successfully.", offerings
        except Exception:
            return False, "Could not retrieve offerings.", None

    def get_appointment_info(self, appointment_id):
        try:
            info = self.appointment_service.get_appointment_info(
                appointment_id
            )

            return (
                True,
                "Appointment information retrieved successfully.",
                info
            )

        except (ValueError, TypeError) as error:
            return False, str(error), None

        except Exception:
            return False, "An unexpected error occurred.", None