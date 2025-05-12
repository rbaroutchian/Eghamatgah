# از این نسخه پایتون استفاده کن
FROM python:3.11-slim

# خاموش کردن کش پایتون و فعال‌سازی خروجی‌ها
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# تنظیم پوشه کاری
WORKDIR /app

# کپی کردن فایل‌های پروژه داخل کانتینر
COPY . /app

# نصب پکیج‌ها
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# اجرای پروژه روی پورت 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
