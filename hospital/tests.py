from django.test import TestCase

import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Appointment, Doctor, Specialty


class AppointmentFlowTests(TestCase):

    def setUp(self):
        self.specialty = Specialty.objects.create(name="قلب و عروق")

        self.doctor = Doctor.objects.create(
            name="دکتر تستی",
            specialty=self.specialty,
            phone="09120000000",
        )

        self.patient = User.objects.create_user(
            username="patient1",
            password="StrongPass!2024",
        )

        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="StrongPass!2024",
            is_staff=True,
        )

        self.tomorrow = (
            datetime.date.today() + datetime.timedelta(days=1)
        )

    def _book_appointment(self, user, date, time="10:00"):
        self.client.force_login(user)

        return self.client.post(
            reverse("appointment"),
            {
                "doctor": self.doctor.id,
                "date": date,
                "time": time,
            },
        )

    def test_patient_can_book_appointment(self):
        response = self._book_appointment(self.patient, self.tomorrow)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 1)

        appointment = Appointment.objects.first()
        self.assertEqual(appointment.status, "pending")
        self.assertEqual(appointment.doctor, self.doctor)

    def test_cannot_book_appointment_in_the_past(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        self._book_appointment(self.patient, yesterday)

        self.assertEqual(Appointment.objects.count(), 0)

    def test_cannot_double_book_same_doctor_slot(self):
        other_patient = User.objects.create_user(
            username="patient2",
            password="StrongPass!2024",
        )

        self._book_appointment(self.patient, self.tomorrow, "11:00")
        self._book_appointment(other_patient, self.tomorrow, "11:00")

        # فقط اولین نوبت باید ثبت شده باشد
        self.assertEqual(Appointment.objects.count(), 1)

    def test_cancelled_slot_can_be_rebooked(self):
        other_patient = User.objects.create_user(
            username="patient3",
            password="StrongPass!2024",
        )

        self._book_appointment(self.patient, self.tomorrow, "12:00")

        appointment = Appointment.objects.get(
            doctor=self.doctor,
            date=self.tomorrow,
            time="12:00",
        )
        appointment.status = "cancelled"
        appointment.save()

        self._book_appointment(other_patient, self.tomorrow, "12:00")

        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(
            Appointment.objects.filter(status="pending").count(), 1
        )

    def test_patient_can_cancel_own_appointment(self):
        self._book_appointment(self.patient, self.tomorrow, "13:00")

        appointment = Appointment.objects.get(patient=self.patient)

        response = self.client.post(
            reverse("cancel_appointment", args=[appointment.id])
        )

        appointment.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(appointment.status, "cancelled")
        # نوبت باید همچنان در دیتابیس بماند، نه حذف شود
        self.assertEqual(Appointment.objects.count(), 1)

    def test_staff_can_update_appointment_status(self):
        self._book_appointment(self.patient, self.tomorrow, "14:00")

        appointment = Appointment.objects.get(patient=self.patient)

        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse(
                "update_appointment_status",
                args=[appointment.id],
            ),
            {"status": "confirmed"},
        )

        appointment.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(appointment.status, "confirmed")

    def test_non_staff_cannot_update_appointment_status(self):
        self._book_appointment(self.patient, self.tomorrow, "15:00")

        appointment = Appointment.objects.get(patient=self.patient)

        # کاربر معمولی (غیر ادمین) دوباره لاگین می‌کند
        self.client.force_login(self.patient)

        self.client.post(
            reverse(
                "update_appointment_status",
                args=[appointment.id],
            ),
            {"status": "confirmed"},
        )

        appointment.refresh_from_db()

        # چون staff نیست، نباید وضعیت تغییر کرده باشد
        self.assertEqual(appointment.status, "pending")
