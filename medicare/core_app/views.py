from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView,DetailView, FormView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages



from .forms import PatientSignUpForm, SpecialistSignUpForm, SpecialistSearchForm, MessageForm
from .models import User, Specialty, Message


# Create your views here.
def homepage(request):
    return render(request, 'starter-page.html')

def patients(request):
    return render(request, 'patients.html')

def profile(request):
    return render(request, 'profile.html')



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
        return redirect(reverse_lazy("core_app:dashboard")) # Or redirect to login for now

class SpecialistSignUpView(CreateView):
    model = User
    form_class = SpecialistSignUpForm
    template_name = "registration/specialist_signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = "specialist"
        
        # Add dropdown options from database
        context['specialties'] = Specialty.objects.all()
        
        return context

    def form_valid(self, form):
        user = form.save()
        # Log the user in.
        login(self.request, user)
        # Redirect to a success page or home page
        # return redirect("home") # Replace "home" with your actual home page URL name
        return redirect(reverse_lazy("core_app:dashboard")) # Or redirect to login for now


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "dashboard_home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Add common dashboard data
        context['user'] = user
        
        # Add role-specific data
        if user.is_patient:
            # Patient-specific dashboard data
            context['user_type'] = 'patient'
            # Add unread message count
            context['unread_messages'] = Message.objects.filter(recipient=user, is_read=False).count()
        elif user.is_specialist:
            # Specialist-specific dashboard data
            context['user_type'] = 'specialist'
            context['specialty'] = user.specialist_profile.specialty
            # Add unread message count
            context['unread_messages'] = Message.objects.filter(recipient=user, is_read=False).count()
        
        return context


@method_decorator(login_required, name='dispatch')
class SpecialistSearchView(ListView):
    model = User
    template_name = 'specialist_search.html'
    context_object_name = 'specialists'
    paginate_by = 10  # Pagination for large result sets
    
    def get_queryset(self):
        form = SpecialistSearchForm(self.request.GET or None)
        queryset = User.objects.filter(is_specialist=True)
        
        if form.is_valid():
            specialty = form.cleaned_data.get('specialty')
            name = form.cleaned_data.get('name')
            
            if specialty:
                queryset = queryset.filter(specialist_profile__specialty=specialty)
            
            if name:
                queryset = queryset.filter(
                    Q(first_name__icontains=name) | 
                    Q(last_name__icontains=name)
                )
                
        return queryset.select_related('specialist_profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SpecialistSearchForm(self.request.GET or None)
        return context

# Messaging Views
@method_decorator(login_required, name='dispatch')
class InboxView(ListView):
    model = Message
    template_name = 'messaging/inbox.html'
    context_object_name = 'messages'
    paginate_by = 10
    
    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Message.objects.filter(recipient=self.request.user, is_read=False).count()
        return context

@method_decorator(login_required, name='dispatch')
class SentMessagesView(ListView):
    model = Message
    template_name = 'messaging/sent.html'
    context_object_name = 'messages'
    paginate_by = 10
    
    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

@method_decorator(login_required, name='dispatch')
class MessageDetailView(DetailView):
    model = Message
    template_name = 'messaging/detail.html'
    context_object_name = 'message'
    
    def get_queryset(self):
        # Ensure users can only view messages they've sent or received
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        )
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Mark as read if the current user is the recipient
        if obj.recipient == self.request.user and not obj.is_read:
            obj.mark_as_read()
        return obj

@method_decorator(login_required, name='dispatch')
class ComposeMessageView(FormView):
    form_class = MessageForm
    template_name = 'messaging/compose.html'
    success_url = reverse_lazy('sent_messages')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # If recipient_id is in GET parameters, pre-select the recipient
        recipient_id = self.request.GET.get('recipient')
        if recipient_id:
            self.recipient = get_object_or_404(User, pk=recipient_id)
        else:
            self.recipient = None
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipient'] = self.recipient
        return context
    
    def form_valid(self, form):
        recipient_id = self.request.GET.get('recipient')
        if not recipient_id:
            messages.error(self.request, "No recipient specified.")
            return self.form_invalid(form)
        
        recipient = get_object_or_404(User, pk=recipient_id)
        
        # Create the message
        message = form.save(commit=False)
        message.sender = self.request.user
        message.recipient = recipient
        message.save()
        
        messages.success(self.request, "Message sent successfully.")
        return super().form_valid(form)

@login_required
def compose_to_specialist(request, specialist_id):
    specialist = get_object_or_404(User, pk=specialist_id, is_specialist=True)
    return redirect(f"{reverse_lazy('compose_message')}?recipient={specialist_id}")
