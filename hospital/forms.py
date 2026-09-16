from django import forms
from .models import Appointment, Doctor
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

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user