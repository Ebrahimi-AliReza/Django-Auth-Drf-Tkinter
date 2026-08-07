# استفاده از نسخه slim برای حجم کمتر (اختیاری اما توصیه شده)
FROM python:3.12-slim

# تنظیمات محیطی برای پایتون
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعیین پوشه کاری
WORKDIR /app

# ابتدا فقط فایل نیازمندی‌ها را کپی می‌کنیم تا از کش داکر استفاده شود
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# حالا بقیه کدها را کپی می‌کنیم
COPY . /app/

# فقط شماره پورت را اکسپوز می‌کنیم
EXPOSE 8000

# دستور نهایی برای اجرای برنامه (مثال برای جنگو یا فست‌آپی)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]