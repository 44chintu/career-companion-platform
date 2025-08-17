from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    PROFILE_TYPE_CHOICES = [
        ('student', 'Student'),
        ('job_seeker', 'Job Seeker'),
        ('employee', 'Employee'),
        ('freelancer', 'Freelancer'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    tagline = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.FileField(
        upload_to='cover_letters/', blank=True, null=True, verbose_name="Curriculum Vitae"
    )

    full_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    twitter_profile = models.URLField(blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)

    education = models.TextField(blank=True, null=True, help_text="Comma separated education details (important ones only)")
    bio = models.TextField(blank=True, null=True)

    profile_type = models.CharField(max_length=50, choices=PROFILE_TYPE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)

    skills = models.TextField(blank=True, null=True, help_text="Comma separated skills")
    experience = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)

    learning_goal = models.TextField(blank=True, null=True, help_text="Comma separated learning goals")
    technologies_interested = models.TextField(blank=True, null=True, help_text="Comma separated technologies of interest")
    projects = models.TextField(blank=True, null=True, help_text="Comma separated project names")
    certifications = models.TextField(blank=True, null=True, help_text="Comma separated certification names")
    achievements = models.TextField(blank=True, null=True, help_text="Comma separated achievements")
    short_term_goals = models.TextField(blank=True, null=True, help_text="Comma separated short term goals")
    long_term_goals = models.TextField(blank=True, null=True, help_text="Comma separated long term goals")

    dream_role = models.CharField(max_length=100, blank=True, null=True)
    dream_company = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # --- Helpers ---
    def get_list_from_field(self, field_value):
        if not field_value:
            return []
        return [item.strip() for item in field_value.split(",") if item.strip()]

    def get_skills_list(self):
        return self.get_list_from_field(self.skills)

    def get_learning_goals_list(self):
        return self.get_list_from_field(self.learning_goal)

    def get_projects_list(self):
        return self.get_list_from_field(self.projects)

    def get_certifications_list(self):
        return self.get_list_from_field(self.certifications)

    def get_achievements_list(self):
        return self.get_list_from_field(self.achievements)

    def get_short_term_goals_list(self):
        return self.get_list_from_field(self.short_term_goals)

    def get_long_term_goals_list(self):
        return self.get_list_from_field(self.long_term_goals)

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def completion_percentage(self):
        fields_to_check = [
            self.full_name,
            self.phone_number,
            self.date_of_birth,
            self.location,
            self.skills,
            self.experience,
            self.role,
            self.learning_goal,
            self.short_term_goals,
            self.long_term_goals,
            self.dream_role,
            self.dream_company,
            self.resume,
            self.linkedin_profile,
            self.github_profile,
            self.education,
            self.certifications,
            self.achievements,
        ]

        total_fields = len(fields_to_check)
        filled_fields = sum(1 for field in fields_to_check if field and str(field).strip())
        
        if total_fields == 0:
            return 0
        return int((filled_fields / total_fields) * 100)
