from pyexpat.errors import messages
from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile
from .forms import SignUpForm
from django.contrib.auth import login
from .forms import *
from django.db.models import Q
def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')

        if password == confirm_password:  # Check if passwords match
            user = User.objects.create_user(
                username=email,  # Using email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Create the user profile
            Profile.objects.create(user=user, mobile=phone_number)
            login(request, user)  # Log in the user
            return redirect('profile')  # Redirect to the profile page
        else:
            return render(request, 'signup/signup.html', {'error': 'Passwords do not match'})

    return render(request, 'signup/signup.html')

# Create your views here.

def home(request):
    return render(request, template_name='Home/home.html')

def signin(request):
    return render(request, template_name='Signin/signin.html')


def signup(request):
    return render(request, template_name='signup/signup.html')

def reset(request):
    return render(request, template_name='reset/reset.html')

from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'Project/project_list.html', {'projects': projects})

from django.shortcuts import render, get_object_or_404
from .models import Project

def details(request, id):
    # Option 1: Using get_object_or_404 for cleaner code
    project = get_object_or_404(Project, pk=id)

    return render(request, 'project/details.html', {'project': project})




def featureprojectlist(request):
    projects = FeatureProject.objects.all()
    return render(request, 'Project/featureprojectlist.html', {'projects': projects})

def details_featureprojectlist(request, id):
    try:
        project = FeatureProject.objects.get(pk=id)
    except FeatureProject.DoesNotExist:
        # Handle the error gracefully, for example:
        return render(request, '404.html', {'message': 'Project not found'})  # Or redirect to another page
    return render (request,'Project/Featuredetails.html', {'project': project})

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            # If the profile does not exist, create it
            Profile.objects.get_or_create(user=user)
            return redirect('profile')  # Redirect to the profile page
        else:
            # Invalid credentials handling
            return render(request, 'SignIn/signin.html', {'error': 'Invalid credentials'})

    return render(request, 'SignIn/signin.html')

def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'profile/profile.html', {'profile': profile})
    return redirect('signin')  # Redirect to sign-in if not authenticated

def Upload_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    return render(request, 'Project/upload_project.html', {'form': form})

def update_project(request,id):
    update = Project.objects.get(pk = id)
    form = ProjectForm(instance=update)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,instance=update)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    return render(request, 'Project/update_project.html', {'form': form})

def delete_p(request,id):
    delete = Project.objects.get(pk = id)
    if request.method == 'POST':
            delete.save()
            return redirect('project_list')
    return render(request, 'Project/delete.html')



def Mamun(request):
    return render(request, template_name='Home/splash.html')

# Handle donations

def donate_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        # Ensure amount is being passed as a number (float or int)
        try:
            amount = float(request.POST.get('amount'))
            if amount > 0:
                project.collectedAmount += amount  # Add the donation amount to the current total
                project.save()  # Save the project with the updated amount
        except (ValueError, TypeError):
            # Handle invalid input, e.g., non-numeric or empty input
            pass

        # After donation, redirect to the project detail page or wherever you want
        return redirect('details', id=project.id)
    
    return redirect('details', id=project.id)  # Redirect for non-POST requests

def comment_on_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(project=project, content=content)
        return redirect('details', id=project.id)

def rate_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        stars = request.POST.get('stars')
        Rating.objects.create(project=project, stars=stars)
        return redirect('details', id=project.id)
