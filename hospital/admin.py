from django.contrib import admin
from .models import Doctor, Appointment, Department, Specialty, MedicalRecord


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
    )

    list_filter = (
        "department",
    )

    search_fields = (
        "name",
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "specialty",
        "phone",
    )

    list_filter = (
        "specialty__department",
        "specialty",
    )

    search_fields = (
        "name",
        "specialty__name",
    )


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "visit_date",
    )

    list_filter = (
        "doctor",
        "visit_date",
    )

    search_fields = (
        "patient__username",
        "patient__first_name",
        "patient__last_name",
        "diagnosis",
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