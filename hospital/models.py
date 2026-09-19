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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "date", "time"],
                condition=models.Q(status__in=["pending", "confirmed"]),
                name="unique_active_appointment_per_doctor_slot",
                violation_error_message=(
                    "این پزشک در این تاریخ و ساعت قبلاً نوبت دارد. "
                    "لطفاً تاریخ یا ساعت دیگری انتخاب کنید."
                ),
            )
        ]

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="medical_records",
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medical_records",
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medical_records",
    )

    visit_date = models.DateField()

    diagnosis = models.TextField(
        verbose_name="بیماری / تشخیص"
    )

    prescription = models.TextField(
        blank=True,
        verbose_name="نسخه"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="توضیحات پزشک"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "سابقه پزشکی"
        verbose_name_plural = "سوابق پزشکی"
        ordering = ["-visit_date"]

    def __str__(self):
        return f"{self.patient} - {self.visit_date}"