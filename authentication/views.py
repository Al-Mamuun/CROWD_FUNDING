from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError  # Import ValidationError
from django.core.validators import validate_email


# Create your views here.


def home(request):
    return render(request, "Home/home.html")



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone_number = request.POST['phone_number']

        # Validate passwords match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('signup')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        # Create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.phone_number = phone_number  # This assumes you have a phone_number field in User model or a custom user model
        myuser.save()

        messages.success(request, "Your account has been successfully created.")
        return redirect('signin')

    return render(request, "signup/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']  # this will be the email
        pass1 = request.POST['pass1']  # password

        # Authenticate using the email as username
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)  # Login the user
            fname = user.first_name  # Get the user's first name
            return render(request, "profile/profile.html", {'fname': fname})  # Render profile page
        
        else:
            messages.error(request, "Invalid credentials")  # Show error message
            return redirect('signin')  # Redirect back to signin

    return render(request, "SignIn/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out succesfully")
    return redirect('home')