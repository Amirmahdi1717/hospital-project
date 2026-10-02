FROM python:3.13-slim

# جلوگیری از تولید فایل‌های .pyc و بافر نشدن لاگ‌ها
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب پکیج‌های پایتون
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# جمع‌آوری فایل‌های استاتیک (CSS/JS) در ایمیج
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# مایگریشن‌ها را اجرا کن و بعد سرور تولید (gunicorn) را بالا بیاور
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]