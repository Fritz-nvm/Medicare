# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, PatientProfile, SpecialistProfile, Specialty

class PatientSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=10, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        user.username = self.cleaned_data['email']  # Set username to email
        if commit:
            user.save()
            PatientProfile.objects.create(user=user)
        return user

class SpecialistSignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=10, required=True)
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), required=True)
    qualifications = forms.CharField(widget=forms.Textarea, required=True)
    experience_years = forms.IntegerField(required=True, min_value=0)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

   
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_specialist = True
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            SpecialistProfile.objects.create(
                user=user,
                specialty=self.cleaned_data['specialty'],
                qualifications=self.cleaned_data['qualifications'],
                experience_years=self.cleaned_data['experience_years']
            )
        return user