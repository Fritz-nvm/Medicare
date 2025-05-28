
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_patient', False)
        extra_fields.setdefault('is_specialist', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class User(AbstractUser):
    username = None  # Completely remove username field
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=10)
    is_patient = models.BooleanField(default=False)
    is_specialist = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    # Remove the save() method override that sets username
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

