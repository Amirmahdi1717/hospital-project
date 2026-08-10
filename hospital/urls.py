from django.urls import path
from .views import *
urlpatterns = [
    path("", home, name="home"),
    path("appointment/", appointment, name="appointment"),
    path("appointments/", appointments, name="appointments"),
    path("appointments/delete/<int:appointment_id>/",delete_appointment,name="delete_appointment",),
    path("dashboard/", dashboard, name="dashboard"),
    path("doctor/add/", add_doctor, name="add_doctor"),
    path("doctor/edit/<int:doctor_id>/",edit_doctor,name="edit_doctor"),
    path("doctor/delete/<int:doctor_id>/",delete_doctor,name="delete_doctor"),
    path("doctor/<int:doctor_id>/",doctor_detail,name="doctor_detail"),
    path("register/" ,register, name="register"),
    path("my-appointments/",my_appointments,name="my_appointments"),
    path("my-appointments/cancel/<int:appointment_id>/",cancel_appointment,name="cancel_appointment"),
    

    
]