from django.urls import path
from .views import register, login_view, package_detail,book_package, payment_page, confirm_payment,payment_success,payment_failure
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('packages/', views.packages, name='packages'),  # Packages page
    path('gallery/', views.gallery, name='gallery'),  # Photo Gallery page
    path('about/', views.about, name='about'),  # About Us page
    path('contact/', views.contact, name='contact'),  # Contact Us page

    path('packages/', views.browse_packages, name='browse_packages'),  # Browse available packages
    path('packages/<int:package_id>/', views.package_detail, name='package_detail'),  # Package detail

    path('packages/<int:package_id>/book/', book_package, name='book_package'),
    path('payment/<int:booking_id>/', payment_page, name='payment_page'),  # Render payment page
    path('confirm_payment/<int:booking_id>/', confirm_payment, name='confirm_payment'),

    path('packages/<int:booking_id>/payment/', views.payment_page, name='payment_page'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),

    path('vendor/create-package/', views.create_package, name='create_package'),  # Vendor creates package


    path('register/user/', views.user_registration, name='user_registration'),  # User registration
    path('register/vendor/', views.vendor_registration, name='vendor_registration'),  # Vendor registration
    path('registration-success/', views.registration_success, name='registration_success'),  # Success page



    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/package/create/', views.create_package, name='create_package'),


    path('logout/', views.logout, name='logout'),  # Logout page (for logged in users)

    path('register/', views.register, name='register'),  # Registration page

    path('admin/approve-packages/', views.admin_approve_packages, name='admin_approve_packages'),

    path('user/login/', views.user_login, name='user_login'),  # User login
    path('vendor/login/', views.vendor_login, name='vendor_login'),  # Vendor login

    path('admin/pending-packages/', views.pending_packages, name='pending_packages'),  # List of pending packages
    path('admin/approve-package/<int:pk>/', views.approve_package, name='approve_package'),  # Approve package

    path('browse-packages/', views.browse_packages, name='browse_packages'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),

]