from django.contrib import admin
from .models import User, UserAccount

admin.site.register(User)
admin.site.register(UserAccount)