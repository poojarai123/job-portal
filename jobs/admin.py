from django.contrib import admin
from .models import UserProfile, CandidateProfile, EmployerProfile, Job, Application

admin.site.register(UserProfile)
admin.site.register(CandidateProfile)
admin.site.register(EmployerProfile)
admin.site.register(Job)
admin.site.register(Application)
