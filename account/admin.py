from django.contrib import admin

from .models import Account 

# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    fields = ('website', 'username', 'email')
    list_display = ('website', 'username', 'email')
