"""
URL configuration for medicare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from core_app.views import DashboardView, SpecialistSearchView, InboxView, SentMessagesView, MessageDetailView, ComposeMessageView, compose_to_specialist


urlpatterns = [
    path('admin/', admin.site.urls),
     # Include custom URLs from the core app under /auth/
    path("", include("core_app.urls")), 
    # Include Django's built-in auth URLs (login, logout, password management) under /accounts/
    path("accounts/", include("django.contrib.auth.urls")), 

    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # Add specialist search view
    path("specialists/search/", SpecialistSearchView.as_view(), name="specialist_search"),
    # Add messaging views
    path("messages/inbox/", InboxView.as_view(), name="inbox"),
    path("messages/sent/", SentMessagesView.as_view(), name="sent_messages"),
    path("messages/view/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/compose/", ComposeMessageView.as_view(), name="compose_message"),
    path("messages/compose/specialist/<int:specialist_id>/", compose_to_specialist, name="compose_to_specialist"),
   
]
