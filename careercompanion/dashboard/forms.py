from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 'cover_photo', 'tagline', 'location',
            'resume', 'cover_letter', 'full_name', 'date_of_birth',
            'phone_number', 'linkedin_profile', 'github_profile',
            'twitter_profile', 'personal_website', 'education', 'bio',
            'profile_type', 'status', 'skills', 'experience', 'role',
            'learning_goal', 'technologies_interested', 'projects',
            'certifications', 'achievements', 'short_term_goals',
            'long_term_goals', 'dream_role', 'dream_company'
        ]

        widgets = {
            'skills': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Python, Django, React'}),
            'learning_goal': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Machine Learning, System Design'}),
            'technologies_interested': forms.Textarea(attrs={'rows': 2, 'placeholder': 'AI, Cloud, Blockchain'}),
            'projects': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Portfolio Website, Resume Builder'}),
            'certifications': forms.Textarea(attrs={'rows': 2, 'placeholder': 'AWS Certified, Data Science Certificate'}),
            'achievements': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Hackathon Winner, Published Paper'}),
            'short_term_goals': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Crack coding interviews'}),
            'long_term_goals': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Become a CTO'}),
            'dream_role': forms.TextInput(attrs={'placeholder': 'E.g. Data Scientist'}),
            'dream_company': forms.TextInput(attrs={'placeholder': 'E.g. Google'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set hashed password
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileExtraForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_type', 'status', 'skills', 'experience', 'role', 'learning_goal']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Python, Django, React'}),
            'learning_goal': forms.Textarea(attrs={'rows': 2, 'placeholder': 'AI, Cloud, Blockchain'}),
        }
