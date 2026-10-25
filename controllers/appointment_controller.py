class AppointmentController:
    def __init__(self, appointment_service):
        self.appointment_service = appointment_service

    def create_appointment(
        self,
        appointment_id,
        customer_id,
        offering_id,
        appointment_date,
        start_time
    ):
        try:
            appointment = self.appointment_service.create_appointment(
                appointment_id,
                customer_id,
                offering_id,
                appointment_date,
                start_time
            )

            return (
                True,
                "Appointment booked successfully.",
                appointment
            )

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