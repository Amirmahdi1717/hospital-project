from django.shortcuts import render, redirect
from .models import Doctor, Appointment
from .forms import AppointmentForm , DoctorForm , RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib import messages


def home(request):
    doctors = Doctor.objects.all()

    return render(request, "home.html", {
        "doctors": doctors
    })



@login_required(login_url="/login/")
def appointment(request):

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            new_appointment = form.save(commit=False)

            new_appointment.patient = request.user

            new_appointment.patient_name = (
                request.user.get_full_name()
                or request.user.username
            )

            new_appointment.save()

            return redirect("home")

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointment.html",
        {"form": form}
    )


@staff_member_required(login_url="/login/")
def delete_appointment(request, appointment_id):

    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.delete()

    return redirect("appointments")


@staff_member_required(login_url="/login/")
def dashboard(request):
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all().order_by("-date", "-time")

    patients = Appointment.objects.values("patient").distinct()

    pending_count = appointments.filter(status="pending").count()
    confirmed_count = appointments.filter(status="confirmed").count()
    cancelled_count = appointments.filter(status="cancelled").count()
    completed_count = appointments.filter(status="completed").count()

    return render(request, "dashboard.html", {
        "doctors": doctors,
        "appointments": appointments,
        "patients": patients,

        "pending_count": pending_count,
        "confirmed_count": confirmed_count,
        "cancelled_count": cancelled_count,
        "completed_count": completed_count,
    })


@staff_member_required(login_url="/login/")
def update_appointment_status(request, appointment_id):
    if request.method == "POST":
        appointment = Appointment.objects.filter(
            id=appointment_id
        ).first()

        if appointment:
            new_status = request.POST.get("status")

            valid_statuses = [
                "pending",
                "confirmed",
                "cancelled",
                "completed",
            ]

            if new_status in valid_statuses:
                appointment.status = new_status
                appointment.save()

    return redirect("dashboard")


@staff_member_required(login_url="/login/")
def add_doctor(request):

    if request.method == "POST":
        form = DoctorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = DoctorForm()

    return render(request, "add_doctor.html", {
        "form": form
    })



@staff_member_required(login_url="/login/")
def edit_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = DoctorForm(instance=doctor)

    return render(request, "edit_doctor.html", {
        "form": form,
        "doctor": doctor
    })


@staff_member_required(login_url="/login/")
def delete_doctor(request, doctor_id):
    if request.method == "POST":
        doctor = Doctor.objects.get(id=doctor_id)
        doctor.delete()

    return redirect("dashboard")


def doctor_detail(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)

    return render(request, "doctor_detail.html", {
        "doctor": doctor
    })

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:
        form = RegisterForm()

    return render(request,"register.html",{"form": form})

@login_required(login_url="/login/")
def appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-date", "-time")

    return render(
        request,
        "appointments.html",
        {
            "appointments": appointments
        }
    )


@login_required(login_url="/login/")
def my_appointments(request):

    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-date", "-time")

    return render(
        request,
        "my_appointments.html",
        {
            "appointments": appointments
        }
    )


@login_required(login_url="/login/")
def cancel_appointment(request, appointment_id):

    if request.method == "POST":

        appointment = Appointment.objects.filter(
            id=appointment_id,
            patient=request.user
        ).first()

        if appointment:
            appointment.delete()

    return redirect("my_appointments")


@login_required(login_url="/login/")
def profile(request):
    return render(request, "profile.html")

@login_required(login_url="/login/")
def edit_profile(request):

    if request.method == "POST":

        user = request.user

        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")

        user.save()

        return redirect("profile")

    return render(request, "edit_profile.html")