from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Project, FeatureProject, Profile, Donation, Comment, Rating
from django.core.mail import send_mail
from django.conf import settings

# Home Page (Requires Login)
def home(request):
    # Example Models: Donation, Project, Review
    total_donors = Donation.objects.count()  # Count unique donors by email
    total_projects = Project.objects.count()  # Count all projects
    success_rating = 5  # Count all reviews

    context = {
        "total_donors": total_donors,
        "total_projects": total_projects,
        "success_rating": success_rating,
    }
    return render(request, "home/home.html", context)


# Reset Page
def reset(request):
    return render(request, 'reset/reset.html')


# Project List (All Projects)
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project/project_list.html', {'projects': projects})


# Project Details
def details(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'project/details.html', {'project': project})


# List of Featured Projects
def featureprojectlist(request):
    projects = FeatureProject.objects.all()
    return render(request, 'project/featureprojectlist.html', {'projects': projects})


# Featured Project Details
def details_featureprojectlist(request, id):
    project = get_object_or_404(FeatureProject, pk=id)
    return render(request, 'project/Featuredetails.html', {'project': project})


# Upload a New Project
@login_required(login_url='user_signin')
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            profile, _ = Profile.objects.get_or_create(user=request.user)  # Unpack the tuple
            project.profile = profile  # Assign only the Profile instance
            project.save()
            messages.success(request, "Project uploaded successfully!")
            return redirect('project_list')
        else:
            messages.error(request, "There were errors in your form. Please fix them below.")
    else:
        form = ProjectForm()

    return render(request, 'project/upload_project.html', {'form': form})


# Check if the user is an admin
def is_admin(user):
    return user.is_staff  # Checks if the user is an admin

# Update Existing Project
@login_required(login_url='user_signin')
def update_project(request, id):
    project = get_object_or_404(Project, pk=id)
    
    # Ensure user is either the project owner or an admin
    if project.owner != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to update this project.")
        return redirect('project_list')
    
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('project_list')
        else:
            messages.error(request, "There were errors in the form. Please fix them below.")
    
    return render(request, 'project/update_project.html', {'form': form})



# Delete Project
@login_required(login_url='user_signin')
def delete_p(request, id):
    project = get_object_or_404(Project, pk=id)
    
    # Ensure user is either the project owner or an admin
    if project.owner != request.user and not request.user.is_staff:
        messages.error(request, "You cannot delete another user's project.")
        return redirect('project_list')
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('project_list')
    
    return render(request, 'project/delete.html', {'project': project})

# Donate to Project
def donate_to_project(request, id):
    project = get_object_or_404(Project, id=id)
    
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            if amount > 0:
                profile = request.user.profile if request.user.is_authenticated else Profile.objects.get_or_create(user=None)[0]
                Donation.objects.create(profile=profile, amount=amount, title=f"Donation to {project.title}", project=project)
                project.collectedAmount += amount
                project.save()
                messages.success(request, "Thank you for your donation!", extra_tags="donation")
            else:
                messages.error(request, "Please enter a valid amount.", extra_tags="donation")
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered.", extra_tags="donation")
        
        return redirect('details', id=project.id)
    
    return redirect('details', id=project.id)


# Comment on Project
def comment_on_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(project=project, content=content)
            messages.success(request, "Comment added!", extra_tags="comment")
        else:
            messages.error(request, "Comment cannot be empty.", extra_tags="comment")
        return redirect('details', id=project.id)


# Rate a Project
def rate_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        try:
            stars = int(request.POST.get('stars'))
            if 1 <= stars <= 5:
                Rating.objects.create(project=project, stars=stars)
                messages.success(request, "Rating submitted successfully!", extra_tags="rating")
            else:
                messages.error(request, "Rating must be between 1 and 5.", extra_tags="rating")
        except (ValueError, TypeError):
            messages.error(request, "Invalid rating value.", extra_tags="rating")
        
        return redirect('details', id=project.id)


# Admin Sign-In
def admin_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and (user.is_staff or user.is_superuser):
            auth_login(request, user)
            messages.success(request, f"Welcome, Admin {username}!")
            return redirect('/admin/')  # Redirect to Django admin panel
        else:
            messages.error(request, "Invalid admin credentials. Please check your username and password.")
            return redirect('admin_signin')

    # Log out admin if they return to the sign-in page or visit non-admin pages
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        logout(request)

    return render(request, "SignIn/admin_signin.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        # Redirect to home or show an error if the user is not an admin
        return redirect('home')
    return render(request, 'profile/admin_profile.html')

# User Sign-In
def user_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if not (user.is_staff or user.is_superuser):  # Ensure user is not admin
                auth_login(request, user)
                
                # Handle "Remember Me" functionality
                if 'rememberMe' in request.POST:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Session ends when browser closes
                
                messages.success(request, f"Welcome, {username}!")
                return redirect('profile_dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, "You do not have access as a standard user.")
                return redirect('user_signin')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('user_signin')

    return render(request, "SignIn/user_signin.html")

# User Sign-Up
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phn_number = request.POST.get('phn_number')

        # Validate passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check for duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Check for duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )

        # Create or link the profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phn_number = phn_number
        profile.save()

        # Log the user in
        messages.success(request, "Account created successfully!")
        auth_login(request, user)
        return redirect('profile_dashboard')

    return render(request, "signup/signup.html")


# Profile Dashboard
@login_required
def profile_dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    projects = profile.projects.all()
    
    # Add statistics to each project
    for project in projects:
        project.donations_count = project.donations.count()
        project.donations_total = project.donations.aggregate(total=models.Sum('amount'))['total'] or 0
    
    # Fetch donations specifically related to the profile
    donations = Donation.objects.filter(profile=profile)

    return render(request, "profile/profile.html", {
        "profile": profile,
        "projects": projects,
        "donations": donations,  # Pass donations to the template
    })



@login_required
def delete_profile(request):
    if request.method == "POST":
        # Get the user's profile
        profile = request.user.profile  # Assuming a one-to-one relationship exists

        # Delete associated projects and donations if necessary
        profile.projects.all().delete()  # Delete all related projects
        Donation.objects.filter(profile=profile).delete()  # Delete related donations

        # Optionally delete the user account
        user = request.user
        user.delete()

        messages.success(request, "Your profile and account have been successfully deleted.")
        return redirect("home")  # Redirect to the homepage or another appropriate URL

    return render(request, "profile/delete_profile.html")
# User Sign-Out
def signout(request):
    if request.user.is_authenticated:
        # Check if the user is an admin (staff or superuser)
        if request.user.is_staff or request.user.is_superuser:
            # Admin user logs out
            messages.success(request, "You have been logged out successfully, Admin!")
            logout(request)  # Log out the admin
            return redirect('home')  # Redirect to home page for admin
        else:
            # Regular user logs out
            messages.success(request, "You have been logged out successfully.")
            logout(request)  # Log out the regular user
            return redirect('user_signin')  # Redirect to sign-in page for regular user
    else:
        # If the user is not authenticated, redirect to sign-in page
        return redirect('user_signin')

# Update Profile
@login_required
def update_profile(request):
    try:
        profile = request.user.profile  # Get the profile associated with the logged-in user
    except Profile.DoesNotExist:
        # If profile doesn't exist, show an error message and redirect to signup page
        messages.error(request, "Profile does not exist. Please create a profile first.")
        return redirect('signup')
    
    if request.method == "POST":
        # If the form is submitted via POST, bind the data and files (if any)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_dashboard')  # Redirect to profile dashboard
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        # If it's a GET request, pre-fill the form with the user's profile data
        form = ProfileForm(instance=profile)
    
    # Render the form in the template
    return render(request, "profile/update_profile.html", {"form": form})

# Thank You Page
def thank_you(request):
    return render(request, 'home/thank_you.html')


def search_projects(request):
    query = request.GET.get('query', '')
    projects = Project.objects.filter(title__icontains=query) | Project.objects.filter(description__icontains=query) if query else []
    return render(request, 'Home/search.html', {'projects': projects, 'query': query})

def about(request):
    return render(request, 'our_info/about.html')

def contact_us(request):
    if request.method == 'POST':
        # Fetching form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')  # Optional
        message = request.POST.get('message')

        # Simple server-side validation
        if not name or not email or not message:
            messages.error(request, "Please fill in all required fields.")
            return redirect('contact_us')  # Replace with your URL name for the contact page

        # Process form (e.g., send an email or save to database)
        try:
            # Sending an email (optional)
            subject = f"New Contact Us Message from {name}"
            email_body = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Message:\n{message}\n"
            )
            admin_email = settings.DEFAULT_CONTACT_EMAIL  # Replace with your email setting
            send_mail(subject, email_body, email, [admin_email])

            # Add success message
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect('contact_us')  # Redirect back to the contact page (or another page)

        except Exception as e:
            # Log the error and show a generic error message
            print(f"Error sending email: {e}")
            messages.error(request, "There was an issue processing your request. Please try again later.")

    return render(request, 'our_info/contact_us.html')  # Use the template you created