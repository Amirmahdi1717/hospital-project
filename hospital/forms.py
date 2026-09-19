from django import forms
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from .models import Appointment, Doctor, MedicalRecord
from django.contrib.auth.models import User


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            "doctor",
            "date",
            "time",
        ]

        labels = {
            "doctor": "پزشک",
            "date": "تاریخ نوبت",
            "time": "ساعت نوبت",
        }

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "time": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")

        if date and date < timezone.localdate():
            raise forms.ValidationError(
                "امکان ثبت نوبت برای تاریخ گذشته وجود ندارد."
            )

        return date

    def clean(self):
        cleaned_data = super().clean()

        doctor = cleaned_data.get("doctor")
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if doctor and date and time:
            conflict = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=time,
                status__in=["pending", "confirmed"],
            )

            if self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)

            if conflict.exists():
                raise forms.ValidationError(
                    "این پزشک در این تاریخ و ساعت قبلاً نوبت دارد. "
                    "لطفاً تاریخ یا ساعت دیگری انتخاب کنید."
                )

        return cleaned_data


class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor

        fields = [
            "name",
            "specialty",
            "phone",
        ]

        labels = {
            "name": "نام پزشک",
            "specialty": "تخصص پزشک",
            "phone": "شماره تماس",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "نام پزشک را وارد کنید"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "شماره تماس پزشک را وارد کنید"
                }
            ),
        }





class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور را وارد کنید"
            }
        )
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور را دوباره وارد کنید"
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
        ]

        labels = {
            "username": "نام کاربری",
            "first_name": "نام",
            "last_name": "نام خانوادگی",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "نام کاربری را وارد کنید"
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "نام خود را وارد کنید"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "نام خانوادگی را وارد کنید"
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError(
                "رمزهای عبور یکسان نیستند."
            )

        if password:
            temp_user = User(
                username=cleaned_data.get("username", ""),
                first_name=cleaned_data.get("first_name", ""),
                last_name=cleaned_data.get("last_name", ""),
            )

            try:
                validate_password(password, user=temp_user)
            except forms.ValidationError as error:
                self.add_error("password", error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user


class MedicalRecordForm(forms.ModelForm):

    class Meta:
        model = MedicalRecord

        fields = [
            "doctor",
            "visit_date",
            "diagnosis",
            "prescription",
            "notes",
        ]

        labels = {
            "doctor": "پزشک معالج",
            "visit_date": "تاریخ ویزیت",
            "diagnosis": "بیماری / تشخیص",
            "prescription": "نسخه",
            "notes": "توضیحات پزشک",
        }

        widgets = {
            "visit_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "diagnosis": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "مثلاً سرماخوردگی، فشار خون بالا..."
                }
            ),

            "prescription": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "داروها و دوز مصرفی (اختیاری)"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "توضیحات تکمیلی پزشک (اختیاری)"
                }
            ),
        }