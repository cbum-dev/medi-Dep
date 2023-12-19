from django.contrib import admin
from .models import Appointment,HealthcareReport

admin.site.register(Appointment)
admin.site.register(HealthcareReport)
# Register your models here.
