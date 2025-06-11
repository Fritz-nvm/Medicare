from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Specialty, SpecialistProfile, PatientProfile, Hospital

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 
                      'is_patient', 'is_specialist', 
                      'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 
                      'first_name', 'last_name', 'phone_number'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register other models
admin.site.register(Specialty)
admin.site.register(SpecialistProfile)
admin.site.register(PatientProfile)
admin.site.register(Hospital)