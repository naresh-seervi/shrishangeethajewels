# Srisangeethajewels - Project Summary

## Project Overview
A complete jewelry management system built with Django, MySQL, HTML, CSS, and JavaScript. The system allows customers to browse, add to cart, and book jewelry items, while admins can manage rates, items, and customers.

## Completed Features

### ✅ Customer Features
1. **Home Page**
   - Beautiful hero section with shop name "Srisangeethajewels"
   - Three filter buttons: All, Gold, Silver
   - Displays all items by default
   - Shows item name, photo, weight, and current price
   - Current gold and silver rates displayed
   - Add to cart functionality (requires login)

2. **About Page**
   - Shop information
   - Owner name: Jagdesh
   - Contact details (mobile, email)
   - Google Maps location link
   - Information about gold and silver purchasing

3. **Registration**
   - Name, username, email (unique), mobile (unique)
   - Password with confirmation
   - Email verification required
   - Verification token sent via email

4. **Login**
   - Login with email OR mobile number
   - Password authentication
   - Email verification check
   - Redirect to admin dashboard for staff users

5. **Shopping Cart**
   - Add items to cart
   - View cart with all items
   - Remove items from cart
   - Total price calculation

6. **Checkout/Booking**
   - Delivery address input
   - Cash on delivery payment method
   - Order placement
   - Cart cleared after order

7. **Password Reset**
   - Email-based password reset
   - Token-based reset link
   - Secure password reset flow

### ✅ Admin Features
1. **Admin Dashboard**
   - Centralized admin panel
   - Quick access to all admin functions

2. **Rate Management**
   - Set daily gold rate (per gram)
   - Set daily silver rate (per gram)
   - Automatic price update for all items
   - Update existing rate for today
   - View rate history

3. **Item Management**
   - Add new items
   - Upload item images
   - Set item name, weight (supports decimals like 1.6)
   - Select type (Gold/Silver)
   - Automatic price calculation: weight × per_gram_rate
   - View all items with status

4. **Customer Management**
   - View all customers
   - See verification status
   - Activate/Deactivate customers
   - Delete customers from database

## Technical Implementation

### Database Models
1. **CustomUser**: Extended Django user with mobile, email verification
2. **Rate**: Stores daily gold/silver rates per gram
3. **Item**: Jewelry items with name, image, weight, type, auto-calculated price
4. **Cart**: User's shopping cart items
5. **Order**: Customer orders with address and payment method
6. **OrderItem**: Order line items

### Key Features
- **Dynamic Pricing**: Prices automatically calculated based on weight × current rate
- **Decimal Weight Support**: Handles weights like 1.6 grams
- **Rate Updates**: When admin updates rate, all items of that type recalculate prices
- **Email Verification**: Token-based email verification system
- **Dual Login**: Login with email or mobile number
- **Price Recalculation**: Cart and checkout recalculate prices based on latest rates

## File Structure
```
srisangeethajewels/
├── manage.py
├── requirements.txt
├── README.md
├── SETUP_INSTRUCTIONS.md
├── srisangeethajewels/
│   ├── settings.py (MySQL config)
│   ├── urls.py
│   └── ...
├── jewels/
│   ├── models.py (CustomUser, Item, Rate, Cart, Order)
│   ├── views.py (All views)
│   ├── forms.py (Registration, Login, Item, Rate forms)
│   ├── urls.py (All URL patterns)
│   ├── admin.py (Django admin config)
│   └── templatetags/ (Custom filters)
├── templates/
│   ├── base.html
│   └── jewels/ (All page templates)
├── static/
│   ├── css/style.css (Beautiful styling)
│   └── js/main.js (JavaScript enhancements)
└── media/ (Item images)
```

## Design Features
- Modern, responsive design
- Gradient backgrounds
- Smooth animations
- Card-based layouts
- Professional color scheme (blue/gold theme)
- Font Awesome icons
- Bootstrap 5 framework
- Mobile-responsive

## Setup Requirements
1. Python 3.8+
2. MySQL Server
3. Install dependencies: `pip install -r requirements.txt`
4. Create database and configure settings.py
5. Run migrations
6. Create superuser
7. Run server

## Next Steps for Deployment
1. Configure production email settings (SMTP)
2. Set DEBUG = False in settings.py
3. Set proper SECRET_KEY
4. Configure ALLOWED_HOSTS
5. Set up static file serving (nginx/Apache)
6. Configure media file serving
7. Set up SSL certificate
8. Configure database backups

## Notes
- Email verification uses console backend in development (emails printed to terminal)
- For production, configure SMTP in settings.py
- All images stored in media/items/ directory
- Static files in static/ directory
- MySQL database required

## Testing Checklist
- [ ] User registration with email verification
- [ ] Login with email and mobile
- [ ] Browse items (All, Gold, Silver filters)
- [ ] Add items to cart
- [ ] Remove items from cart
- [ ] Place order with address
- [ ] Admin: Set gold/silver rates
- [ ] Admin: Add items (verify price calculation)
- [ ] Admin: Manage customers (activate/deactivate/delete)
- [ ] Password reset functionality
- [ ] Price recalculation when rates change

## Support
For issues or questions, refer to README.md or contact: shop@srisangeethajewels.com
