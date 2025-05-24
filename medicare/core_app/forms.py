# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, PatientProfile, SpecialistProfile, Specialty

class PatientSignUpForm(UserCreationForm):
    # Add any patient-specific fields needed during signup here
    # For example: date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            # Add other fields from User model if needed
        )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
            # Create PatientProfile upon saving the user
            PatientProfile.objects.create(user=user)
            # You could potentially populate profile fields here if they were in the form
            # patient_profile = PatientProfile.objects.create(user=user, date_of_birth=self.cleaned_data.get("date_of_birth"))
        return user

class SpecialistSignUpForm(UserCreationForm):
    # Add specialist-specific fields needed during signup here
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), required=False, empty_label="Select Specialty (Optional)")
    qualifications = forms.CharField(widget=forms.Textarea, required=False)
    experience_years = forms.IntegerField(required=False, min_value=0)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            # Add other fields from User model if needed
        )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_specialist = True
        if commit:
            user.save()
            # Create SpecialistProfile upon saving the user
            SpecialistProfile.objects.create(
                user=user,
                specialty=self.cleaned_data.get("specialty"),
                qualifications=self.cleaned_data.get("qualifications"),
                experience_years=self.cleaned_data.get("experience_years")
            )
        return user

