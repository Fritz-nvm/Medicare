from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login

from .forms import PatientSignUpForm, SpecialistSignUpForm
from .models import User


# Create your views here.
def homepage(request):
    return render(request, 'starter-page.html')

def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')


class SignUpView(TemplateView):
    template_name = "registration/signup.html"

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = "registration/patient_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "patient"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # Log the user in.
        login(self.request, user)
        # Redirect to a success page or home page
        # return redirect("home") # Replace "home" with your actual home page URL name
        return redirect(reverse_lazy("core_app:patient_dashboard")) # Or redirect to login for now

class SpecialistSignUpView(CreateView):
    model = User
    form_class = SpecialistSignUpForm
    template_name = "registration/specialist_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "specialist"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # Log the user in.
        login(self.request, user)
        # Redirect to a success page or home page
        # return redirect("home") # Replace "home" with your actual home page URL name
        return redirect(reverse_lazy("login")) # Or redirect to login for now

# Add other views like login, logout, profile views later

