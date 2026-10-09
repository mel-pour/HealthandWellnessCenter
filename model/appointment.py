

class Appointment:
    def __init__(self, appointment_id, date, start_time, status):
        self.appointment_id = appointment_id
        self.date = date
        self.start_time = start_time
        self.status = status

    @property
    def appointment_id(self):
        return self.appointment_id

    @appointment_id.setter
    def appointment_id(self, value):
        # appointment_id_validator(value)
        self.__appointment_id = value



    @property
    def date(self):
        return self.date

    @date.setter
    def date(self, value):
        # date_validator(value)
        self.__date = value


    @property
    def start_time(self):
        return self.start_time

    @start_time.setter
    def start_time(self, value):
        # start_time_validator(value)
        self.__start_time = value


    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, value):
        # status_validator(value)
        self.__status = value


    def booking(self):
        pass

    def check_balance(self):
        pass


class PrivateAppointment(Appointment):
    def __init__(self,service ,employee, appointment_id, date, start_time, status):
        Appointment.__init__(self, appointment_id, date, start_time, status)
        self.service = service
        self.employee = employee

    @property
    def service(self):
        return self.service

    @service.setter
    def service(self, value):
        # service_validator(value)
        self.__service = value

    @property
    def employee(self):
        return self.employee

    @employee.setter
    def employee(self, value):
        # employee_validator(value)
        self.__employee = value

    def booking(self):
        pass


class ClassAppointment(Appointment):
    def __init__(self,fitfess_class,appointment_id, date, start_time, status):
        Appointment.__init__(self, appointment_id, date, start_time, status)
        self.fitfess_class = fitfess_class

    @property
    def fitfess_class(self):
        return self.fitfess_class
    @fitfess_class.setter
    def fitfess_class(self, value):
        self.__fitfess_class = value

    def enroll(self):
        pass