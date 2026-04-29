from django.contrib import admin

# Register your models here.
from .models import User, FreelancerProfile,ClientProfile

admin.site.register(User)
admin.site.register(FreelancerProfile)
admin.site.register(ClientProfile)