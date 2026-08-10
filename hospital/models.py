from django.db import models

from django.contrib.auth.models import User
from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    date = models.DateField()
    time = models.TimeField()
    patient = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name}"
