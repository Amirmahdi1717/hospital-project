from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment, MedicalRecord, PatientProfile
from .forms import AppointmentForm , DoctorForm , RegisterForm, MedicalRecordForm, PatientProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib import messages


# دسترسی: عمومی — نیازی به ورود نیست
def home(request):
    query = request.GET.get("q", "").strip()

    doctors = Doctor.objects.select_related("specialty")

    if query:
        doctors = doctors.filter(
            Q(name__icontains=query)
            | Q(specialty__name__icontains=query)
        )

    return render(request, "home.html", {
        "doctors": doctors,
        "query": query,
    })



# دسترسی: فقط بیمار (کاربر لاگین‌کرده)
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

            try:
                new_appointment.save()

            except IntegrityError:
                messages.error(
                    request,
                    "این پزشک در این تاریخ و ساعت قبلاً نوبت دارد. "
                    "لطفاً تاریخ یا ساعت دیگری انتخاب کنید."
                )

                return render(
                    request,
                    "appointment.html",
                    {"form": form}
                )

            messages.success(
                request,
                "نوبت شما با موفقیت ثبت شد و در انتظار تأیید است."
            )

            return redirect("home")

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointment.html",
        {"form": form}
    )


# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def delete_appointment(request, appointment_id):

    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()

        messages.success(request, "نوبت با موفقیت حذف شد.")

    return redirect("appointments")


# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def dashboard(request):

    doctors = Doctor.objects.all()

    appointments = Appointment.objects.all().order_by(
        "-date",
        "-time"
    )

    patients = (
        User.objects
        .filter(appointment__isnull=False)
        .annotate(
            appointment_count=Count(
                "appointment",
                distinct=True
            )
        )
        .distinct()
    )

    pending_count = appointments.filter(
        status="pending"
    ).count()

    confirmed_count = appointments.filter(
        status="confirmed"
    ).count()

    cancelled_count = appointments.filter(
        status="cancelled"
    ).count()

    completed_count = appointments.filter(
        status="completed"
    ).count()

    paginator = Paginator(appointments, 10)
    page_number = request.GET.get("page")
    appointments_page = paginator.get_page(page_number)

    return render(
        request,
        "dashboard.html",
        {
            "doctors": doctors,
            "appointments": appointments_page,
            "patients": patients,

            "pending_count": pending_count,
            "confirmed_count": confirmed_count,
            "cancelled_count": cancelled_count,
            "completed_count": completed_count,
        }
    )


# دسترسی: فقط ادمین (staff)
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

                messages.success(request, "وضعیت نوبت به‌روزرسانی شد.")

    return redirect("dashboard")


# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def add_doctor(request):

    if request.method == "POST":
        form = DoctorForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "پزشک جدید با موفقیت اضافه شد.")

            return redirect("dashboard")

    else:
        form = DoctorForm()

    return render(request, "add_doctor.html", {
        "form": form
    })



# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)

        if form.is_valid():
            form.save()

            messages.success(request, "اطلاعات پزشک با موفقیت ویرایش شد.")

            return redirect("dashboard")

    else:
        form = DoctorForm(instance=doctor)

    return render(request, "edit_doctor.html", {
        "form": form,
        "doctor": doctor
    })


# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def delete_doctor(request, doctor_id):
    if request.method == "POST":
        doctor = get_object_or_404(Doctor, id=doctor_id)
        doctor.delete()

        messages.success(request, "پزشک با موفقیت حذف شد.")

    return redirect("dashboard")


# دسترسی: عمومی — نیازی به ورود نیست
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    return render(request, "doctor_detail.html", {
        "doctor": doctor
    })

# دسترسی: عمومی — نیازی به ورود نیست
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "ثبت‌نام با موفقیت انجام شد. حالا وارد حساب خود شوید."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(request,"register.html",{"form": form})

# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def appointments(request):
    all_appointments = Appointment.objects.all().select_related(
        "doctor"
    ).order_by("-date", "-time")

    paginator = Paginator(all_appointments, 10)
    page_number = request.GET.get("page")
    appointments_page = paginator.get_page(page_number)

    return render(
        request,
        "appointments.html",
        {
            "appointments": appointments_page
        }
    )


# دسترسی: فقط بیمار (کاربر لاگین‌کرده)
@login_required(login_url="/login/")
def my_appointments(request):

    all_appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-date", "-time")

    paginator = Paginator(all_appointments, 10)
    page_number = request.GET.get("page")
    appointments_page = paginator.get_page(page_number)

    return render(
        request,
        "my_appointments.html",
        {
            "appointments": appointments_page
        }
    )


# دسترسی: فقط بیمار (کاربر لاگین‌کرده)
@login_required(login_url="/login/")
def cancel_appointment(request, appointment_id):

    if request.method == "POST":

        appointment = Appointment.objects.filter(
            id=appointment_id,
            patient=request.user,
            status__in=["pending", "confirmed"],
        ).first()

        if appointment:
            appointment.status = "cancelled"
            appointment.save()

            messages.success(request, "نوبت شما با موفقیت لغو شد.")

    return redirect("my_appointments")


# دسترسی: فقط بیمار (کاربر لاگین‌کرده)
@login_required(login_url="/login/")
def profile(request):
    patient_profile, _ = PatientProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, "profile.html", {
        "patient_profile": patient_profile,
    })

# دسترسی: فقط بیمار (کاربر لاگین‌کرده)
@login_required(login_url="/login/")
def edit_profile(request):

    patient_profile, _ = PatientProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user = request.user

        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")

        user.save()

        profile_form = PatientProfileForm(
            request.POST,
            instance=patient_profile
        )

        if profile_form.is_valid():
            profile_form.save()

        messages.success(request, "پروفایل شما با موفقیت به‌روزرسانی شد.")

        return redirect("profile")

    else:
        profile_form = PatientProfileForm(instance=patient_profile)

    return render(request, "edit_profile.html", {
        "profile_form": profile_form,
    })

# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def patient_detail(request, patient_id):

    patient = get_object_or_404(User, id=patient_id)

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related(
        "doctor"
    ).order_by(
        "-date",
        "-time"
    )

    records = MedicalRecord.objects.filter(
        patient=patient
    ).select_related(
        "doctor"
    ).order_by(
        "-visit_date"
    )

    return render(
        request,
        "patient_detail.html",
        {
            "patient": patient,
            "appointments": appointments,
            "records": records,
        }
    )


# دسترسی: فقط ادمین (staff)
@staff_member_required(login_url="/login/")
def add_medical_record(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)

    if request.method == "POST":
        form = MedicalRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()

            messages.success(request, "سابقه پزشکی جدید ثبت شد.")

            return redirect("patient_detail", patient_id=patient.id)

    else:
        form = MedicalRecordForm()

    return render(
        request,
        "add_medical_record.html",
        {
            "form": form,
            "patient": patient,
        }
    )


# دسترسی: فقط بیمار (کاربر لاگین‌کرده)
@login_required(login_url="/login/")
def my_medical_records(request):
    records = MedicalRecord.objects.filter(
        patient=request.user
    ).select_related(
        "doctor"
    ).order_by(
        "-visit_date"
    )

    return render(
        request,
        "my_medical_records.html",
        {
            "records": records,
        }
    )