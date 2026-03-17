# Quick Setup Instructions

## 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 2. Setup MySQL Database

1. Install MySQL if not already installed
2. Create database:
```sql
CREATE DATABASE srisangeethajewels_db;
```

3. Update `srisangeethajewels/settings.py` with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'srisangeethajewels_db',
        'USER': 'root',  # Change to your MySQL username
        'PASSWORD': '',  # Change to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Create Admin User

```bash
python manage.py createsuperuser
```

Enter:
- Username
- Email
- Password

## 5. Create Media Directory

```bash
mkdir media
mkdir media/items
```

## 6. Run Server

```bash
python manage.py runserver
```

## 7. Access the Application

- Home: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- Admin Dashboard: http://127.0.0.1:8000/admin-dashboard/ (after login as admin)

## First Steps After Setup

1. **Login as Admin** using the superuser credentials
2. **Set Initial Rates**:
   - Go to Admin Dashboard → Manage Rates
   - Set Gold rate (e.g., 16000 per gram)
   - Set Silver rate (e.g., 800 per gram)
3. **Add Items**:
   - Go to Admin Dashboard → Manage Items
   - Add jewelry items with images, weight, and type
   - Prices will be calculated automatically

## Notes

- Email verification uses console backend by default (emails printed to terminal)
- For production, configure SMTP settings in `settings.py`
- Images are stored in `media/items/` directory
- Static files are served from `static/` directory
