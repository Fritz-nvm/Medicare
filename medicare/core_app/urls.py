from django.urls import path, include
from .views import SignUpView, homepage

app_name='core_app'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('signup/', SignUpView.as_view(), name ='signup' )
   
]
