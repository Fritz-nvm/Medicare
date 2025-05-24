# core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    """Custom User model inheriting from AbstractUser."""
    is_patient = models.BooleanField("Patient status", default=False)
    is_specialist = models.BooleanField("Specialist status", default=False)
    # Add other common fields if needed, e.g., email = models.EmailField(unique=True)
    # Ensure email is unique if used for login

    # Add related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set", # Changed related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set", # Changed related_name
        related_query_name="user",
    )

    def __str__(self):
        return self.username

class Specialty(models.Model):
    """Model representing a medical specialty."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name

class SpecialistProfile(models.Model):
    """Model storing profile information specific to Specialists."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='specialist_profile')
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True, related_name='specialists')
    # If multiple specialties are allowed:
    # specialties = models.ManyToManyField(Specialty, blank=True, related_name='specialists')
    qualifications = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Add other fields like clinic_address, contact_number, profile_picture, etc.

    def __str__(self):
        specialty_name = self.specialty.name if self.specialty else "No Specialty Assigned"
        return f"Dr. {self.user.get_full_name() or self.user.username} - {specialty_name}"

class PatientProfile(models.Model):
    """Model storing profile information specific to Patients."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='patient_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # Add other fields like medical_history_summary, insurance_details, etc.

    def __str__(self):
        return f"Patient: {self.user.get_full_name() or self.user.username}"

# Message model will be added later when implementing messaging feature
# class Message(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
#     recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
#     subject = models.CharField(max_length=255, blank=True)
#     body = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"From {self.sender} to {self.recipient} at {self.timestamp:%Y-%m-%d %H:%M}"
#
#     class Meta:
#         ordering = ['-timestamp']

