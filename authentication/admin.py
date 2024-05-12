from django.contrib import admin
from .models import User, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'date_joined']
    list_filter = ['date_joined', 'is_superuser', 'is_staff']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
