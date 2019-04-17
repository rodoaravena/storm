from django.contrib import admin
from schedule.models import Schedule, ModuleTime, UserProfile

admin.site.register(Schedule)
admin.site.register(ModuleTime)
admin.site.register(UserProfile)