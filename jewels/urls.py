# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('about/', views.about, name='about'),
#     path('item/<int:item_id>/', views.item_detail, name='item_detail'),
#     path('register/', views.register, name='register'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('verify-otp/', views.verify_otp, name='verify_otp'),
#     path('verify-email/<str:token>/', views.verify_email, name='verify_email'),

#     # Cart and Orders
#     path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/', views.view_cart, name='view_cart'),
#     path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
#     path('checkout/', views.checkout, name='checkout'),
#     path('my-orders/', views.my_orders, name='my_orders'),

#     # Admin (only staff can access)
#     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
#     path('admin/rates/', views.manage_rates, name='manage_rates'),
#     path('admin/items/', views.manage_items, name='manage_items'),
#     path('admin/orders/', views.manage_orders, name='manage_orders'),
#     path('admin/customers/', views.manage_customers, name='manage_customers'),
#     path('admin/customers/<int:user_id>/toggle/', views.toggle_customer_status, name='toggle_customer_status'),
#     path('admin/customers/<int:user_id>/delete/', views.delete_customer, name='delete_customer'),
    
    
#     # Password Reset
#     path('password-reset/', auth_views.PasswordResetView.as_view(
#         template_name='jewels/password_reset.html',
#         email_template_name='jewels/password_reset_email.html',
#         subject_template_name='jewels/password_reset_subject.txt'
#     ), name='password_reset'),
#     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
#         template_name='jewels/password_reset_done.html'
#     ), name='password_reset_done'),
#     path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
#         template_name='jewels/password_reset_confirm.html'
#     ), name='password_reset_confirm'),
#     path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
#         template_name='jewels/password_reset_complete.html'
#     ), name='password_reset_complete'),
# ]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.LogoutView, name='logout'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),

    # 🛒 Cart
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # 📦 Orders
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # 🛠 Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/rates/', views.manage_rates, name='manage_rates'),
    path('admin/items/', views.manage_items, name='manage_items'),
    path('admin/orders/', views.manage_orders, name='manage_orders'),
    path('admin/customers/', views.manage_customers, name='manage_customers'),
    path('admin/customers/<int:user_id>/toggle/', views.toggle_customer_status, name='toggle_customer_status'),
    path('admin/customers/<int:user_id>/delete/', views.delete_customer, name='delete_customer'),


   
    # 🔐 Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='jewels/password_reset.html',
        email_template_name='jewels/password_reset_email.html',
        subject_template_name='jewels/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='jewels/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='jewels/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='jewels/password_reset_complete.html'
    ), name='password_reset_complete'),
]
