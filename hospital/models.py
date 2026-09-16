from django.db import models

from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "بخش بیمارستان"
        verbose_name_plural = "بخش‌های بیمارستان"

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="specialties",
    )

    class Meta:
        verbose_name = "تخصص"
        verbose_name_plural = "تخصص‌ها"

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctors",
    )
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("confirmed", "تأیید شده"),
        ("cancelled", "لغو شده"),
        ("completed", "انجام شده"),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    patient_name = models.CharField(max_length=100)

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name}"