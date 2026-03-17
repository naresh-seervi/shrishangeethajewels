import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Item, Cart, Order, OrderItem, Rate, ItemImage
from .forms import CustomUserCreationForm, LoginForm, OTPVerifyForm, ItemForm, RateForm, OrderForm





def is_admin(user):
    return user.is_authenticated and user.is_staff


def admin_required(view_func):
    """Only allow staff users; return 403 for authenticated non-staff."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to access the admin section.')
        return view_func(request, *args, **kwargs)
    return wrapper


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def home(request):
    items = Item.objects.filter(is_active=True).prefetch_related('extra_images')
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'gold':
        items = items.filter(item_type='gold')
    elif filter_type == 'silver':
        items = items.filter(item_type='silver')
    
    # Get current rates
    gold_rate = Rate.objects.filter(rate_type='gold').order_by('-date').first()
    silver_rate = Rate.objects.filter(rate_type='silver').order_by('-date').first()
    
    # Update prices for all items
    for item in items:
        item.price = item.calculate_price()
        item.save()
    
    context = {
        'items': items,
        'filter_type': filter_type,
        'gold_rate': gold_rate,
        'silver_rate': silver_rate,
    }
    return render(request, 'jewels/home.html', context)


def item_detail(request, item_id):
    """Single item page - shareable URL; opening this URL shows only this item."""
    item = get_object_or_404(Item, id=item_id, is_active=True)
    item.price = item.calculate_price()
    item.save()
    item_url = request.build_absolute_uri(request.path)
    return render(request, 'jewels/item_detail.html', {
        'item': item,
        'item_url': item_url,
        'gold_rate': Rate.objects.filter(rate_type='gold').order_by('-date').first(),
        'silver_rate': Rate.objects.filter(rate_type='silver').order_by('-date').first(),
    })



# user cancle item
@login_required
def my_orders(request):
    """User's order history - booking status in card section; orders are not deleted."""
    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set__item').order_by('-created_at')
    return render(request, 'jewels/my_orders.html', {'orders': orders})


def about(request):
    return render(request, 'jewels/about.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()
            otp = generate_otp()
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save(update_fields=['otp', 'otp_created_at'])
            send_mail(
                'Verify your email - Srisangeethajewels',
                f'Your OTP for email verification is: {otp}. It is valid for 10 minutes.',
                settings.DEFAULT_FROM_EMAIL or 'noreply@srisangeethajewels.com',
                [user.email],
                fail_silently=False,
            )
            request.session['verify_user_id'] = user.id
            messages.success(request, 'Registration successful! Check your email for the OTP.')
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'jewels/register.html', {'form': form})


def verify_otp(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('register')
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if user.otp == otp:
                # OTP valid for 10 minutes
                if user.otp_created_at and (timezone.now() - user.otp_created_at).total_seconds() < 600:
                    user.is_verified = True
                    user.otp = None
                    user.otp_created_at = None
                    user.save(update_fields=['is_verified', 'otp', 'otp_created_at'])
                    del request.session['verify_user_id']
                    messages.success(request, 'Email verified successfully! You can now login.')
                    return redirect('login')
                else:
                    messages.error(request, 'OTP has expired. Please register again to get a new OTP.')
                    return redirect('register')
            messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerifyForm()
    return render(request, 'jewels/verify_otp.html', {'form': form, 'email': user.email})


def verify_email(request, token):
    """Legacy link verification - kept for old links; prefer OTP now."""
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.is_verified = True
        user.verification_token = None
        user.save()
        messages.success(request, 'Email verified successfully! You can now login.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification token.')
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email_or_mobile = form.cleaned_data['email_or_mobile'].strip()
            password = form.cleaned_data['password']
            try:
                if '@' in email_or_mobile:
                    user = CustomUser.objects.get(email=email_or_mobile)
                else:
                    user = CustomUser.objects.get(mobile=email_or_mobile)
            except CustomUser.DoesNotExist:
                messages.error(request, 'Invalid email or mobile number.')
                return render(request, 'jewels/login.html', {'form': form})
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    if user.is_staff:
                        return redirect('admin_dashboard')
                    return redirect('home')
                else:
                    messages.error(request, 'Please verify your email (OTP) before logging in.')
            else:
                messages.error(request, 'Invalid password.')
    else:
        form = LoginForm()
    return render(request, 'jewels/login.html', {'form': form})


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id, is_active=True)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{item.name} added to cart.")
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    # Recalculate prices
    for cart_item in cart_items:
        cart_item.item.price = cart_item.item.calculate_price()
        cart_item.item.save()
    total = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'jewels/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')


@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('view_cart')
    
    for cart_item in cart_items:
        cart_item.item.price = cart_item.item.calculate_price()
        cart_item.item.save()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_amount = sum(item.item.price * item.quantity for item in cart_items)
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                address=form.cleaned_data['address'],
                payment_method='cash_on_delivery'
            )
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price
                )
            
            cart_items.delete()
            messages.success(request, 'Order placed successfully! Check your order status below.')
            return redirect('my_orders')
    else:
        form = OrderForm()
    
    total = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'jewels/checkout.html', {'cart_items': cart_items, 'total': total, 'form': form})


@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'jewels/admin_dashboard.html')


@login_required
@admin_required
def manage_rates(request):
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            from django.utils import timezone
            rate_type = form.cleaned_data['rate_type']
            per_gram_rate = form.cleaned_data['per_gram_rate']
            today = timezone.now().date()
            
            existing_rate = Rate.objects.filter(rate_type=rate_type, date=today).first()
            if existing_rate:
                existing_rate.per_gram_rate = per_gram_rate
                existing_rate.save()
                rate = existing_rate
            else:
                rate = Rate.objects.create(
                    rate_type=rate_type,
                    per_gram_rate=per_gram_rate,
                    date=today
                )
            
            items = Item.objects.filter(item_type=rate.rate_type, is_active=True)
            for item in items:
                item.price = item.weight * rate.per_gram_rate
                item.save()
            
            messages.success(request, f'{rate.rate_type.capitalize()} rate updated successfully!')
            return redirect('manage_rates')
    else:
        form = RateForm()
    
    rates = Rate.objects.all().order_by('-date')
    return render(request, 'jewels/manage_rates.html', {'form': form, 'rates': rates})


@login_required
@admin_required
def manage_items(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            item.price = item.calculate_price()
            item.save()
            for idx, f in enumerate(request.FILES.getlist('extra_images', [])):
                ItemImage.objects.create(item=item, image=f, order=idx)
            messages.success(request, 'Item added successfully!')
            return redirect('manage_items')
    else:
        form = ItemForm()
    items = Item.objects.all().order_by('-created_at').prefetch_related('extra_images')
    return render(request, 'jewels/manage_items.html', {'form': form, 'items': items})


@login_required
@admin_required
def manage_orders(request):
    orders = Order.objects.all().select_related('user').prefetch_related('orderitem_set__item').order_by('-created_at')
    return render(request, 'jewels/manage_orders.html', {'orders': orders})


@login_required
@admin_required
def manage_customers(request):
    customers = CustomUser.objects.filter(is_staff=False)
    return render(request, 'jewels/manage_customers.html', {'customers': customers})


@login_required
@admin_required
def toggle_customer_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'Customer {status} successfully.')
    return redirect('manage_customers')


@login_required
@admin_required
def delete_customer(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_staff:
        user.delete()
        messages.success(request, 'Customer deleted successfully.')
    return redirect('manage_customers')


def LogoutView(request):
    logout(request)
    return redirect('login')  