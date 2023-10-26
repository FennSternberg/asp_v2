from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget
import re

class LocationChoiceField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        super(LocationChoiceField, self).__init__(*args, **kwargs)
        distinct_locations = sorted(list(set(UserProfile.objects.values_list('location', flat=True))))
        self.choices = [(location, location) for location in distinct_locations]

    def validate(self, value):
        # Custom validation for location
        if not value:  # Check if empty
            raise forms.ValidationError("Invalid input: This field cannot be empty.")
        
        if len(value) < 3:  # Minimum length check
            raise forms.ValidationError("Invalid input: Location name must be at least 3 characters long.")

        if len(value) > 50:  # Maximum length check
            raise forms.ValidationError("Invalid input: Location name must be no more than 50 characters long.")
        
        # Alphabetic characters and forward slashes are allowed
        if not re.match(r'^[a-zA-Z/ ]+$', value):
            raise forms.ValidationError("Invalid input: Location name must contain only alphabetic characters and/or forward slashes.")


    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    location = LocationChoiceField(
        widget=Select2Widget(attrs={'class': 'form-control'}),
        required=True
    )
   
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email','required':'true'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name','required':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name','required':'true'}),
        }
        
    def clean_password2(self):
        # Check if both passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1:
            raise forms.ValidationError('Invalid input: Please enter a password')
        if not password2:
            raise forms.ValidationError('Invalid input: Please confirm your password')
        if password1 != password2:
            raise forms.ValidationError('Invalid input: Passwords don\'t match.')
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@amcor.com'):
            raise forms.ValidationError('Invalid input: Please use a valid @amcor.com email address.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Invalid input: There is already an account for this email')
        return email
    
    def clean_first_name(self):
        firstname = self.cleaned_data.get('first_name')
        if not firstname:
            raise forms.ValidationError('Invalid input: First Name cannot be empty.')
        if not re.match(r'^[a-zA-Z/ ]+$', firstname):
            raise forms.ValidationError("Invalid input: First Name must contain only alphabetic characters and/or forward slashes.")
        return firstname
    
    def clean_last_name(self):
        lastname = self.cleaned_data.get('last_name')
        if not lastname:
            raise forms.ValidationError('Invalid input: Last Name cannot be empty.')
        if not re.match(r'^[a-zA-Z/ ]+$', lastname):
            raise forms.ValidationError("Invalid input: Last Name must contain only alphabetic characters and/or forward slashes.")
        return lastname

    def save(self, commit=True):
        # Use the email as the username
        self.cleaned_data['username'] = self.cleaned_data['email']
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Create the user profile with default usergroup and provided location
            profile = UserProfile(user=user, usergroup='regular', location=self.cleaned_data['location'])
            profile.save()
        return user

class UpdateUserForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': 'true'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': 'true'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@amcor.com'):
            raise forms.ValidationError('Invalid input: Please use a valid @amcor.com email address.')
        return email
    
    def clean_first_name(self):
        firstname = self.cleaned_data.get('first_name')
        if not firstname:
            raise forms.ValidationError('Invalid input: First Name cannot be empty.')
        if not re.match(r'^[a-zA-Z/ ]+$', firstname):
            raise forms.ValidationError("Invalid input: First Name must contain only alphabetic characters and/or forward slashes.")
        return firstname
    
    def clean_last_name(self):
        lastname = self.cleaned_data.get('last_name')
        if not lastname:
            raise forms.ValidationError('Invalid input: Last Name cannot be empty.')
        if not re.match(r'^[a-zA-Z/ ]+$', lastname):
            raise forms.ValidationError("Invalid input: Last Name must contain only alphabetic characters and/or forward slashes.")
        return lastname

class UpdateUserProfileForm(forms.ModelForm):
    location = LocationChoiceField(
        widget=Select2Widget(attrs={'class': 'form-control','required':'true'}),
        required=True
    )
    class Meta:
        model = UserProfile
        fields = ['location']