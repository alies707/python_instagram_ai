# Python Instagram AI

یک داشبورد Python برای اتصال امن به Instagram Graph API و تحلیل اولیه عملکرد محتوا.

## امکانات نسخه فعلی

- دریافت اطلاعات اکانت Professional
- نمایش تعداد دنبال‌کننده، دنبال‌شونده و محتوا
- نمایش آخرین پست‌ها
- محاسبه نرخ تعامل بر اساس لایک و کامنت
- تحلیل طول کپشن و ارائه پیشنهاد اولیه
- استفاده از API رسمی Meta به جای دریافت نام کاربری و رمز عبور

## نصب

```bash
git clone https://github.com/alies707/python_instagram_ai.git
cd python_instagram_ai
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

سپس آدرس زیر را باز کنید:

```text
http://127.0.0.1:5000
```

## تنظیم Meta

در فایل `.env` این مقادیر را وارد کنید:

```env
INSTAGRAM_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
INSTAGRAM_ACCOUNT_ID=YOUR_INSTAGRAM_ACCOUNT_ID
META_GRAPH_API_VERSION=v25.0
FLASK_SECRET_KEY=YOUR_RANDOM_SECRET
```

توکن را داخل GitHub commit نکنید. برای همین `.env` در `.gitignore` قرار گرفته است، چون بشر هنوز هم عاشق منتشر کردن Secret روی اینترنت است.

## ساختار پروژه

```text
python_instagram_ai/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── services/
│   └── instagram.py
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   └── analysis.html
└── static/
    └── style.css
```

## محدودیت مهم

این پروژه برای اکانت‌های Instagram Professional و دسترسی‌های مجاز Meta طراحی شده است. قابلیت‌های قابل استفاده به مجوزهای App، نوع اکانت و نسخه API بستگی دارند.
