from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import *

# Home Page (Requires Login)

def home(request):
    return render(request, template_name="home/home.html")

# Reset Page
def reset(request):
    return render(request, template_name='reset/reset.html')

# List All Projects
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project/project_list.html', {'projects': projects})

# Project Details
def details(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'project/details.html', {'project': project})

# List Featured Projects
def featureprojectlist(request):
    projects = FeatureProject.objects.all()
    return render(request, 'project/featureprojectlist.html', {'projects': projects})

# Featured Project Details
def details_featureprojectlist(request, id):
    project = get_object_or_404(FeatureProject, pk=id)
    return render(request, 'project/Featuredetails.html', {'project': project})


# Upload a New Project
def upload_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project uploaded successfully!")
            return redirect('project_list')
    return render(request, 'project/upload_project.html', {'form': form})

# Update Existing Project
def update_project(request, id):
    update = get_object_or_404(Project, pk=id)
    form = ProjectForm(instance=update)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('project_list')
    return render(request, 'project/update_project.html', {'form': form})

# Delete Project
def delete_p(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('project_list')
    return render(request, 'project/delete.html')

# Donate to a Project
def donate_to_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            if amount > 0:
                project.collectedAmount += amount
                project.save()
                messages.success(request, "Thank you for your donation!")
            else:
                messages.error(request, "Please enter a valid amount.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered.")
        return redirect('details', id=project.id)
    return redirect('details', id=project.id)

# Comment on a Project
def comment_on_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(project=project, content=content)
            messages.success(request, "Comment added!")
        else:
            messages.error(request, "Comment cannot be empty.")
        return redirect('details', id=project.id)

# Rate a Project
def rate_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        try:
            stars = int(request.POST.get('stars'))
            if 1 <= stars <= 5:
                Rating.objects.create(project=project, stars=stars)
                messages.success(request, "Rating submitted successfully!")
            else:
                messages.error(request, "Rating must be between 1 and 5.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid rating value.")
        return redirect('details', id=project.id)

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debug: Print the submitted data
        print(f"Username: {username}, Password: {password}")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in and remember them if the checkbox is checked
            auth_login(request, user)
            
            # Optionally, handle "Remember me"
            if 'rememberMe' in request.POST:
                request.session.set_expiry(1209600)  # Keep session for two weeks

            messages.success(request, f"Welcome, {username}!")
            # return redirect('home')  # Redirect to home page
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('signin')  # Redirect back to the sign-in page if failed

    return render(request, "SignIn/signin.html")

# User Sign-Up
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if the passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Create the user
        User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email, password=password1)
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('signin')
    
    return render(request, "signup/signup.html")


def thanks(request):
    return render(request, "Home/thank_you.html")