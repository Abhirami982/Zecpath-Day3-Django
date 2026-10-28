
from django.contrib import admin
from .models import Job, User, Application, Candidate, Employer

admin.site.register(Job)
admin.site.register(User)
admin.site.register(Application)
admin.site.register(Candidate)
admin.site.register(Employer)
