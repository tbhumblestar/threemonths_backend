from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(get_user_model())