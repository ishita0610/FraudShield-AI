from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import random
from .models import OTPVerification


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'accounts/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, f'Account created successfully! Welcome, {username}. Please log in.')
        return redirect('accounts:login')

    return render(request, 'accounts/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please enter username and password.')
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate OTP
            otp_code = str(random.randint(100000, 999999))

            otp_obj, _ = OTPVerification.objects.get_or_create(user=user)
            otp_obj.otp_code = otp_code
            otp_obj.is_verified = False
            otp_obj.save()

            # Store user id in session for OTP step
            request.session['pre_auth_user_id'] = user.id
            request.session['pre_auth_username'] = user.username

            # Print OTP to terminal
            print(f"\n{'='*50}")
            print(f"🔐 OTP FOR USER: {user.username}")
            print(f"   OTP CODE: {otp_code}")
            print(f"{'='*50}\n")

            messages.info(request, f'OTP sent! Check your terminal for the code.')
            return redirect('accounts:verify_otp')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def verify_otp_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    pre_auth_user_id = request.session.get('pre_auth_user_id')
    if not pre_auth_user_id:
        messages.error(request, 'Please log in first.')
        return redirect('accounts:login')

    username = request.session.get('pre_auth_username', '')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()

        try:
            user = User.objects.get(id=pre_auth_user_id)
            otp_obj = OTPVerification.objects.get(user=user)

            if otp_obj.is_expired():
                messages.error(request, 'OTP has expired. Please log in again.')
                del request.session['pre_auth_user_id']
                return redirect('accounts:login')

            if otp_obj.otp_code == entered_otp:
                otp_obj.is_verified = True
                otp_obj.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['pre_auth_user_id']
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Incorrect OTP. Please try again.')

        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            messages.error(request, 'Session error. Please log in again.')
            return redirect('accounts:login')

    return render(request, 'accounts/verify_otp.html', {'username': username})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')
