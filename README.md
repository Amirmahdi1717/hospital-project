# 🏥 Hospital Management System

یک پروژه وب برای مدیریت و ارائه خدمات یک بیمارستان که با **Django** و
**Python** توسعه داده شده است.

## 📌 معرفی پروژه

این پروژه با هدف ایجاد یک سیستم ساده و قابل توسعه برای مدیریت بخش‌های
مختلف یک بیمارستان طراحی شده است. رابط کاربری پروژه با HTML و CSS ساخته
شده و بخش‌های مختلف آن از طریق Django مدیریت می‌شوند.

## ✨ امکانات

-   🏠 صفحه اصلی (Home)
-   👤 مدیریت کاربران
-   📅 سیستم ثبت و مدیریت نوبت‌ها (Appointments)
-   📝 فرم‌های دریافت اطلاعات
-   🎨 رابط کاربری با HTML و CSS
-   📱 ساختار قابل توسعه برای صفحات مختلف بیمارستان
-   🗂️ مدیریت فایل‌های Static
-   🐍 توسعه‌یافته با Django

## 🛠️ تکنولوژی‌های استفاده‌شده

-   **Python**
-   **Django**
-   **HTML5**
-   **CSS3**
-   **SQLite**
-   **Git / GitHub**

## 📁 ساختار کلی پروژه

``` text
hospital/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── hospital/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   ├── home.html
│   ├── appointments.html
│   └── ...
│
├── static/
│   └── css/
│       └── style.css
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

> ساختار بالا نمای کلی پروژه است و ممکن است با توسعه پروژه فایل‌ها و
> پوشه‌های بیشتری به آن اضافه شوند.

## ⚙️ نصب و اجرای پروژه

### 1. دریافت پروژه

``` bash
git clone https://github.com/Amirmahdi1717/hospital-project.git
cd hospital-project
```

### 2. ساخت Virtual Environment

در Windows:

``` bash
python -m venv venv
```

فعال‌سازی:

``` bash
venv\Scripts\activate
```

در Linux / macOS:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. نصب وابستگی‌ها

اگر فایل `requirements.txt` در پروژه وجود دارد:

``` bash
pip install -r requirements.txt
```

در غیر این صورت، Django را نصب کنید:

``` bash
pip install django
```

### 4. اجرای Migration

``` bash
python manage.py migrate
```

### 5. اجرای سرور

``` bash
python manage.py runserver
```

سپس در مرورگر وارد آدرس زیر شوید:

``` text
http://127.0.0.1:8000/
```

## 🔐 نکات امنیتی

فایل‌های حساس نباید در GitHub قرار بگیرند. مواردی مانند:

``` text
.env
db.sqlite3
venv/
__pycache__/
media/
```

در `.gitignore` قرار گرفته‌اند تا در صورت نیاز توسط Git نادیده گرفته
شوند.

همچنین اطلاعات حساسی مانند `SECRET_KEY`، رمز عبور دیتابیس و API Keyها
نباید در Repository عمومی قرار بگیرند.

## 🚀 توسعه پروژه

این پروژه قابلیت توسعه در بخش‌های مختلف را دارد، از جمله:

-   مدیریت پزشکان
-   مدیریت بیماران
-   مدیریت بخش‌های بیمارستان
-   سیستم نوبت‌دهی پیشرفته
-   پنل مدیریت
-   ثبت سوابق پزشکی
-   سیستم جستجوی پزشکان
-   احراز هویت و سطح دسترسی کاربران

## 📌 وضعیت پروژه

🚧 پروژه در حال توسعه است و امکانات جدید به مرور به آن اضافه خواهند شد.

## 👨‍💻 توسعه‌دهنده

**Amirmahdi1717**

------------------------------------------------------------------------

⭐ اگر این پروژه برای شما مفید بود، می‌توانید Repository را Star کنید.
