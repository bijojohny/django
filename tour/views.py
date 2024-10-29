from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from .models import Package
from .models import Booking,Vendor
from .forms import TourPackageForm
from .models import TourPackage, Booking
from django.contrib.auth.models import User
from .forms import VendorRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def approve_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    package.approved = True  # Mark package as approved
    package.save()
    return redirect('pending_packages')  # Redirect back to the pending packages list

def pending_packages(request):
    packages = TourPackage.objects.filter(approved=False)  # Get unapproved packages
    return render(request, 'pending_packages.html', {'packages': packages})


def vendor_dashboard(request):
    vendor_packages = TourPackage.objects.filter(vendor=request.user)
    return render(request, 'vendor_dashboard.html', {'packages': vendor_packages})

def create_package(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST,request.FILES)
        image = request.FILES.get('image')  # Get image from FILES

        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user  # Assign the current vendor to the package
            package.save()
            return redirect('vendor_dashboard')  # Redirect to vendor dashboard after successful package creation
    else:
        form = TourPackageForm()

    return render(request, 'create_package.html', {'form': form})
def admin_approve_packages(request):
    packages = TourPackage.objects.filter(is_approved=False)
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        package = TourPackage.objects.get(id=package_id)
        package.is_approved = True
        package.save()
        return redirect('admin_approve_packages')
    return render(request, 'admin_approve_packages.html', {'packages': packages})


def register(request):
    return render(request, 'register.html')


def user_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('registration_success')  # Redirect to success page after registration
    return render(request, 'user_registration.html',{'form': TourPackageForm})
def vendor_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('registration_success')  # Redirect to success page after registration
    return render(request, 'vendor_registration.html', {'form': TourPackageForm})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)  # Log the user in
            return redirect('browse_packages')  # Redirect to home page after login
        else:
            error_message = "Invalid username or password."
            return render(request, 'user_login.html', {'error_message': error_message})
    return render(request, 'user_login.html')

def browse_packages(request):
    # Only show packages that have been approved by the admin
    approved_packages = TourPackage.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'browse_packages.html', {'packages': approved_packages})


def package_detail(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)  # Fetch the specific package
    return render(request, 'package_detail.html', {'package': package})


def book_package(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)

    if request.method == "POST":
        # Retrieve the number of people from the form data
        number_of_people = request.POST.get('number_of_people')
        if not number_of_people:
            messages.error(request, "Please specify the number of people.")
            return redirect('book_package', package_id=package_id)

        # Create a booking instance with the number of people
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            number_of_people=int(number_of_people),  # Ensure it's converted to int
        )
        booking.save()

        # Redirect to the payment page with the booking ID
        return redirect('payment_page', booking_id=booking.id)

    return render(request, 'book_package.html', {'package': package})

def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        payment_success = True  # Assume the payment is successful
        if payment_success:
            return redirect('payment_success')
        else:
            return redirect('payment_failure')  # Optional, or redirect to browse_packages
    return render(request, 'payment_page.html', {'booking': booking})

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failure(request):
    return render(request, 'payment_failure.html')

def confirm_payment(request, booking_id):
    if request.method == "POST":
        # Process the payment details from the form
        card_number = request.POST['card_number']
        expiry_date = request.POST['expiry_date']
        cvv = request.POST['cvv']

        # Here you would normally process the payment (this is just a placeholder)
        # Simulating payment success
        payment_success = True

        if payment_success:
            messages.success(request, "Payment successful!")
            # Optionally mark the booking as paid in the database here
            return render(request, 'payment_success.html')  # A page to show successful payment
        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('payment_page', booking_id=booking_id)  # Redirect back to payment page if payment fails

    return redirect('browse_packages')

def login_redirect(request):
    # After successful login, redirect to browse packages
    return redirect('browse_packages')

def vendor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)  # Log the vendor in
            return redirect('vendor_dashboard')  # Redirect to vendor dashboard after login
        else:
            error_message = "Invalid username or password."
            return render(request, 'vendor_login.html', {'error_message': error_message})
    return render(request, 'vendor_login.html')


def registration_success(request):
    return render(request, 'registration_success.html')

def home(request):
    return render(request, 'home.html')

def packages(request):
    return render(request, 'packages.html')






# View for Photo Gallery
def gallery(request):
    return render(request, 'gallery.html')


# View for About Us
def about(request):
    return render(request, 'about.html')

# View for Contact Us
def contact(request):
    return render(request, 'contact.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home or dashboard page
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to home page after logout


def index(request):
    return render(request,'index.html')


def add_package(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = Vendor.objects.get(user=request.user)  # Link package to the vendor
            package.is_approved = False  # Set to false initially
            package.save()
            return redirect('vendor_dashboard')  # Redirect to vendor dashboard after saving
    else:
        form = TourPackageForm()

    return render(request, 'add_package.html', {'form': form})