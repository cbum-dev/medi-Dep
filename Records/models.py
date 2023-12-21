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
    is_approved = models.BooleanField(default=False)
    
    def is_upcoming(self):
        return self.appointment_datetime > timezone.now()

    @property
    def upcoming_appointments(self):
        print(self.user,self.healthcare_provider.user)
        return Appointment.objects.filter(user=self.user, appointment_datetime__gt=timezone.now())

    def approve_appointment(self):
        # Additional validation: Only healthcare providers can approve appointments
        if isinstance(self.healthcare_provider, HealthcareProvider):
            self.is_approved = True
            self.save()
        else:
            raise ValueError("Only healthcare providers can approve appointments.")



class HealthcareReport(models.Model):
    user = models.ForeignKey(User,on_delete =models.CASCADE )
    healthcare_provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment,on_delete = models.CASCADE)
    report = models.FileField()
