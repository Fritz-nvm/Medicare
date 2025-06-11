from django.urls import path, include
from .views import SignUpView, homepage, PatientSignUpView, SpecialistSignUpView, DashboardView, patients, profile, view_info
from django.conf import settings
from django.conf.urls.static import static


app_name='core_app'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('signup/', SignUpView.as_view(), name ='signup'),
    path('patient-signup/', PatientSignUpView.as_view(), name ='patient_signup'),
    path('specialist-signup/', SpecialistSignUpView.as_view(), name ='specialist_signup'),

    #dashboard urls 

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('patient/', patients, name='patients'),
    path('profile/', profile, name='profile'),

    path('view-information/', view_info, name='specialist_information'),
   
]
if settings.DEBUG:  # Only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
