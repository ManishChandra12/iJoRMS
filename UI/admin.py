from django.contrib import admin

from . models import Applicant, Job, JobApplicant
# Register your models here.

admin.site.register(Applicant)
admin.site.register(Job)
admin.site.register(JobApplicant)