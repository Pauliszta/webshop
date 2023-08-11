from django.contrib import admin
from .models import UserBase

# Register your models here.


class UserBaseAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'is_active', 'email', 'is_staff', 'created', 'updated']
    list_filter = ['created', 'updated']
    list_editable = ['is_active']


admin.site.register(UserBase, UserBaseAdmin)
