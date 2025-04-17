from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Nurse, Doctor, Patient
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from datetime import time
from django.utils.timezone import datetime, timedelta
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count


User = get_user_model()

def signup(request):
    if request.method == "POST":
        # Collect form data
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        place = request.POST.get('place')
        dob = request.POST.get('dob')
        user_type = request.POST.get('user_type')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                place=place,
                dob=dob,
                user_type=user_type,
            )

            # Handle user-type specific fields
            if user_type == 'Nurse':
                nurse_phone = request.POST.get('nurse_phone')
                shift = request.POST.get('shift')
                if not nurse_phone or not shift:
                    messages.error(request, "Phone number and shift are required for nurses.")
                    user.delete()
                    return redirect('signup')

                Nurse.objects.create(
                    user=user,
                    phone_number=nurse_phone,
                    shift=shift,
                )
                print("Nurse details saved.")

            elif user_type == 'Doctor':
                print(Doctor)
                doctor_phone = request.POST.get('doctor_phone')
                print(doctor_phone)
                specialization = request.POST.get('specialization')
                experience = request.POST.get('experience')
                certificate_file = request.FILES.get('certificate_file')

                if not doctor_phone or not specialization or not experience:
                    messages.error(request, "Phone number, specialization, and experience are required for doctors.")
                    user.delete()
                    return redirect('signup')

                Doctor.objects.create(
                    user=user,
                    specialization=specialization,
                    experience=experience,
                    phone_number=doctor_phone,
                    certificate_files=certificate_file
                )
                print("Doctor details saved.")

            elif user_type == 'Patient':
                patient_phone = request.POST.get('patient_phone')
                print(patient_phone)

                if not patient_phone:
                    messages.error(request, "Phone number is required for patients.")
                    user.delete()
                    return redirect('signup')

                Patient.objects.create(user=user, phone_number=patient_phone)
                print("Patient details saved.")

            messages.success(request, "Signup successful! Please log in.")
            return redirect('')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    # Render the signup form for GET requests
    return render(request, 'signup.html')




def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'Login.html')