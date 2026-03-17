# Srisangeethajewels - Jewelry Management System

A comprehensive Django-based jewelry management system for managing gold and silver jewelry items with dynamic pricing, customer management, and order processing.

## Features

### Customer Features
- **Home Page**: Browse all jewelry items with filtering (All, Gold, Silver)
- **Item Display**: View item name, photo, weight, and current price
- **Shopping Cart**: Add items to cart and manage cart items
- **Order Booking**: Place orders with address and cash on delivery option
- **User Registration**: Register with name, mobile (unique), email (unique)
- **Email Verification**: Email verification required before login
- **Login**: Login with email or mobile number
- **Password Reset**: Reset password via email verification

### Admin Features
- **Rate Management**: Set daily gold and silver rates per gram
- **Automatic Price Calculation**: Item prices automatically calculated based on weight × per-gram rate
- **Item Management**: Add items with name, photo, weight, and type (gold/silver)
- **Customer Management**: View, activate/deactivate, and delete customers
- **Decimal Weight Support**: Supports decimal weights (e.g., 1.6 grams)

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Image Handling**: Pillow

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Database Configuration

1. Create a MySQL database:
```sql
CREATE DATABASE srisangeethajewels_db;
```

2. Update database settings in `srisangeethajewels/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'srisangeethajewels_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. This account will have access to the admin panel.

### Step 5: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
srisangeethajewels/
├── manage.py
├── requirements.txt
├── srisangeethajewels/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── jewels/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templatetags/
│       ├── __init__.py
│       └── custom_filters.py
├── templates/
│   ├── base.html
│   └── jewels/
│       ├── home.html
│       ├── about.html
│       ├── login.html
│       ├── register.html
│       ├── cart.html
│       ├── checkout.html
│       ├── admin_dashboard.html
│       ├── manage_rates.html
│       ├── manage_items.html
│       ├── manage_customers.html
│       └── password_reset_*.html
├── static/
│   └── css/
│       └── style.css
└── media/
    └── items/  (created automatically for uploaded images)
```

## Usage Guide

### For Customers

1. **Registration**: 
   - Go to Register page
   - Fill in name, username, email, mobile number, and password
   - Check email for verification link
   - Click verification link to activate account

2. **Login**:
   - Use email or mobile number to login
   - Enter password

3. **Shopping**:
   - Browse items on home page
   - Filter by All, Gold, or Silver
   - Click "Add to Cart" on desired items
   - View cart and proceed to checkout
   - Enter delivery address and place order

### For Admin

1. **Access Admin Panel**:
   - Login with superuser credentials
   - Navigate to Admin Dashboard

2. **Manage Rates**:
   - Go to "Manage Rates"
   - Select type (Gold/Silver)
   - Enter per-gram rate
   - Click "Update Rate"
   - All items of that type will automatically update their prices

3. **Add Items**:
   - Go to "Manage Items"
   - Fill in item name, upload image, enter weight (supports decimals like 1.6)
   - Select type (Gold/Silver)
   - Price is automatically calculated based on current rate
   - Click "Add Item"

4. **Manage Customers**:
   - Go to "Manage Customers"
   - View all registered customers
   - Activate/Deactivate customers
   - Delete customers if needed

## Key Features Explained

### Dynamic Pricing System
- Admin sets daily per-gram rates for gold and silver
- When an item is added, its price is automatically calculated: `price = weight × per_gram_rate`
- Supports decimal weights (e.g., 1.6 grams)
- When rates are updated, all active items of that type automatically recalculate their prices

### Email Verification
- Users must verify their email before logging in
- Verification link is sent to registered email
- Token-based verification system

### Cart & Order System
- Items can be added to cart
- Cart persists across sessions
- Checkout requires delivery address
- Orders are placed with cash on delivery option

## Configuration

### Email Settings (Production)

Update `settings.py` for production email:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## About Section Details

- **Shop Name**: Srisangeethajewels
- **Owner**: Jagdesh
- **Mobile**: +91 9999999999
- **Email**: shop@srisangeethajewels.com
- **Location**: [Google Maps Link](https://maps.app.goo.gl/fAJVicNgcYptguMY7)

## Troubleshooting

1. **MySQL Connection Error**: 
   - Ensure MySQL server is running
   - Check database credentials in settings.py
   - Verify database exists

2. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT in settings.py

3. **Email Not Sending**:
   - For development, emails are printed to console
   - For production, configure SMTP settings

4. **Image Upload Issues**:
   - Ensure MEDIA_ROOT and MEDIA_URL are configured
   - Check file permissions on media directory

## License

This project is created for Srisangeethajewels jewelry shop.

## Support

For issues or questions, contact: shop@srisangeethajewels.com
