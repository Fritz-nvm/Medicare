# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, PatientProfile, SpecialistProfile, Specialty, Message, Hospital
from django.core.exceptions import ValidationError




class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = SpecialistProfile
        fields = ['profile_picture']



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
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.filter(verified=True), required=False, label="Hospital/Clinic Affiliation (if applicable)")
    specialist_id = forms.CharField(required=False, max_length=20, label="Personal Specialist ID", 
    help_text="Minimum 8 characters required", widget=forms.TextInput(attrs={'placeholder': 'SP-XXXX-XXXX' })
    )


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super().clean()
        hospital = cleaned_data.get('hospital')
        specialist_id = cleaned_data.get('specialist_id')

        if not hospital and not specialist_id:
            raise ValidationError(
                "You must provide either a hospital affiliation or specialist ID"
            )
        
        if hospital and specialist_id:
            raise ValidationError(
                "Please provide either hospital affiliation OR specialist ID, not both"
            )
        
        return cleaned_data
   
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
                specialist_id=self.cleaned_data['specialist_id'],
                hospital=self.cleaned_data['hospital'],
                qualifications=self.cleaned_data['qualifications'],
                experience_years=self.cleaned_data['experience_years']
            )

       
        return user



# Add the SpecialistSearchForm for searching specialists
class SpecialistSearchForm(forms.Form):
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(), 
        required=False,
        empty_label="All Specialties"
    )
    name = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        specialty = cleaned_data.get('specialty')
        name = cleaned_data.get('name')
        
        # Ensure at least one search parameter is provided
        if not specialty and not name:
            raise forms.ValidationError("Please provide at least one search parameter")
        
        return cleaned_data

# Add the MessageForm for sending messages
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
