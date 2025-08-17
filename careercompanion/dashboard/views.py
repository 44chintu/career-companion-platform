from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from .forms import ProfileExtraForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login


def index(request):
    return render(request, 'dashboard/index.html')
# @login_required
def skill_cloud(request):
    return render(request, 'dashboard/skill_cloud.html')
@login_required
def dashboardPage(request):
    profile = request.user.profile
    skills_list = profile.get_skills_list()
    goals_list = profile.get_learning_goals_list()
    projects_list = profile.get_projects_list()
    return render(request, 'dashboard/dashboardPage.html', {
        'profile': profile,
        'skills_count': len(skills_list),
        'learning_goals_count': len(goals_list),
        'projects_count': len(projects_list),
    })

def logout(request):
    return render(request, 'dashboard/index.html')

# @login_required
def progress_tracker(request):
    return render(request, 'dashboard/progress_tracker.html')

# @login_required
def timeline(request):
    return render(request, 'dashboard/timeLineView.html')

# @login_required
def resume_generator(request):
    return render(request, 'dashboard/resumeGenerator.html')

# @login_required
def learning_hub(request):
    return render(request, 'dashboard/learningHub.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        email_error = None
        password_error = None

        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            email_error = 'No account found with this email.'
        else:
            user = authenticate(request, username=user_obj.username, password=password)
            if not user:
                password_error = 'Incorrect password.'
            else:
                login(request, user)
                return redirect('dashboardPage')

        return render(request, 'dashboard/login.html', {
            'email_error': email_error,
            'password_error': password_error
        })
    return render(request, 'dashboard/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # Auto-login after signup
            return redirect('login')  # Go to profile page
    else:
        form = SignUpForm()
    
    return render(request, 'dashboard/signup.html', {'form': form})

def profile(request):
    profile = request.user.profile
    skills_list = profile.get_skills_list()
    goals_list = profile.get_learning_goals_list()
    completion = profile.completion_percentage()
    projects_list = profile.get_projects_list()
    return render(request, 'dashboard/profile.html', {
        'profile': profile,
        'skills_count': len(skills_list),
        'learning_goals_count': len(goals_list),
        'completion': completion,
        'projects_count': len(projects_list),
    })


def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    profile = request.user.profile
    completion = profile.completion_percentage()

    return render(request, 'dashboard/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'completion': completion,
    })