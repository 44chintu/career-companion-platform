from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('skill-cloud/', views.skill_cloud, name='skill_cloud'),
    path('progres_tracker/', views.progress_tracker, name='progress_tracker'),
    path('timeLineView/', views.timeline, name='timeLineView'),
    path('resumeGenerator/', views.resume_generator, name='resumeGenerator'),
    path('learninHub/', views.learning_hub, name='learningHub'),
    path('dashboardPage', views.dashboardPage, name='dashboardPage'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),

    # Password change URLs
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='dashboard/change_password.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='dashboard/password_change_done.html'),
         name='password_change_done'),
         path('profile/edit/', views.edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
