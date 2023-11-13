from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'address', 'phone_number')
    search_fields = ('user__username', 'first_name', 'last_name', 'address', 'phone_number')

admin.site.register(UserProfile, UserProfileAdmin)