from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'date_joined']
    list_filter = ['date_joined', 'is_superuser', 'is_staff']

admin.site.register(User, UserAdmin)