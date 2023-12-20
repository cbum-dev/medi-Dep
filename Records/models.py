from django.db import models
from Accounts.models import HealthcareProvider,User
from django.utils import timezone
from django.core.exceptions import ValidationError
class Appointment(models.Model):
    # app_id = models.AutoField(primary_key=False,default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    healthcare_provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()
    is_rescheduled = models.BooleanField(default=False)
    problem = models.TextField(default="Something wrong with my health")
    
    def is_upcoming(self):
        return self.appointment_datetime > timezone.now()

    @property
    def upcoming_appointments(self):
        print(self.user,self.healthcare_provider.user)
        return Appointment.objects.filter(user=self.user, appointment_datetime__gt=timezone.now())

    # def clean(self):
    #     # Check if the user and healthcare provider are the same
    #     if self.user == self.healthcare_provider.user:
    #         raise ValidationError("User and healthcare provider cannot be the same.")


class HealthcareReport(models.Model):
    user = models.ForeignKey(User,on_delete =models.CASCADE )
    healthcare_provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment,on_delete = models.CASCADE)
    report = models.FileField()
