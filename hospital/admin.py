from django.contrib import admin
from .models import Doctor, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "specialty",
        "phone",
    )

    search_fields = (
        "name",
        "specialty",
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "doctor",
        "date",
        "time",
        "status",
    )

    list_filter = (
        "status",
        "doctor",
        "date",
    )

    search_fields = (
        "patient_name",
        "doctor__name",
    )

    ordering = (
        "-date",
        "-time",
    )