from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    if request.method == 'POST':
        uname = request.POST.get('email')
        pwd = request.POST.get('password')
        print(pwd)
        user = authenticate(username=uname, password=pwd)
        storage = messages.get_messages(request)
        for _ in storage:
            pass  # Iterate over messages to clear them
        if user is not None:
            auth.login(request, user)
            return  redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request,'temps/login.html')
    else:
        return render(request,'temps/login.html')

def signup(request):
    print("Hello")
    if request.method == 'POST':
        print("Hello")
        email = request.POST.get('email')
        full_name = request.POST.get('fullname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cnfpassword')

        storage = messages.get_messages(request)
        for _ in storage:
            pass  # Iterate over messages to clear them

        # Validation
        if not email or not full_name or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'temps/register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'temps/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'temps/register.html')
        print(messages)
        # Create user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name, user.last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

        user.save()

        # Log the user in

        messages.success(request, 'Account created successfully')

        return redirect('/login')  # Change 'home' to your desired redirect url after registration

    return render(request, 'temps/register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')