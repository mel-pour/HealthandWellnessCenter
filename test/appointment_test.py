from model.appointment import Appointment
from datetime import date, time

# ==============================================================================================================
a_d= date (2026,10,20)
a_t= time (20,30,)

apointment1 = Appointment(70001,10001,50001,a_d,a_t,50,"pending")

print(apointment1)

# pass
# ==============================================================================================================
