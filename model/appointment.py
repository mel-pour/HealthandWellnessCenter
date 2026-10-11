

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


