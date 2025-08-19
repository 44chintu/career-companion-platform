from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from .forms import ProfileExtraForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.templatetags.static import static
from .ai_agent import categorize_skills

def index(request):
    return render(request, 'dashboard/index.html')
# @login_required
def skill_cloud(request):
    profile = request.user.profile
    raw = profile.skills or ""                       # e.g. "Python, Django, SQL"
    skills = [s.strip() for s in raw.split(",") if s.strip()]

    # Use the free rule-based agent to categorize
    categorized_skills = categorize_skills(skills)

    # Compute total items to decide empty state
    total_count = sum(cnt for pairs in categorized_skills.values() for _, cnt in pairs)

    # Icon map (use CDN + your static icons)
    skill_icons = {
        "python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        "java": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
        "django": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg",
        "javascript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
        "typescript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
        "html": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
        "css": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg",
        "sql": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
        "mysql": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
        "postgresql": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg",
        "mongodb": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg",
        "react": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
        "angular": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/angularjs/angularjs-original.svg",
        "vue": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg",
        "flask": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg",
        "fastapi": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg",
        "selenium": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg",
        "docker": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
        "kubernetes": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kubernetes/kubernetes-plain.svg",
        "git": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
        "aws": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg",
        "azure": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/azure/azure-original.svg",
        "gcp": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/googlecloud/googlecloud-original.svg",
        # custom local svgs
        "power automate": static("dashboard/icons/power-automate.svg"),
    }

    context = {
        "categorized_skills": categorized_skills,
        "skill_icons": skill_icons,
        "total_count": total_count,
    }
    return render(request, "dashboard/skill_cloud.html", context)

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