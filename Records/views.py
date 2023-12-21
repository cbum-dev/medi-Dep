from rest_framework import generics,serializers,permissions
from .models import Appointment, HealthcareReport
from .serializers import (
    AppointmentSerializer,
    BookAppSerializer,
    HealthCareRecordSerializer,
)
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail

from rest_framework.exceptions import ValidationError
class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        appointment = serializer.save()
        subject = "Appointment Confirmation"
        message = f"Your appointment with {appointment.healthcare_provider.name} on {appointment.appointment_datetime} has been booked successfully."
        from_email = "priyanshukumar2002234@gmail.com"  # Your email address
        recipient_list = "priyanshukumar20022304@gmail.com"  # User's email address
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)


class UserAppointmentsListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.user
        print(user.user)
        return Appointment.objects.filter(user=user)


class UpcomingAppointmentsView(generics.ListAPIView):
    queryset = Appointment.objects.all().order_by('-id')
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(
            user=self.request.user.user, appointment_datetime__gt=timezone.now()
        )
class UpcomingAppointmentsProviderView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        return Appointment.objects.filter(
            healthcare_provider=self.request.user.id, appointment_datetime__gt=timezone.now()
        ).order_by('appointment_datetime')


class ProviderAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        provider = self.request.user.healthcareprovider
        print(
            provider
        )  # Get the healthcare provider associated with the authenticated user
        return Appointment.objects.filter(healthcare_provider=provider).order_by('-id')

from django.conf import settings


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = BookAppSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user.user.user.user
        healthcare_provider = serializer.validated_data['healthcare_provider'].user
        # print(user,healthcare_provider,user.user)
        # Check if the user and healthcare_provider are the same CustomUser
        if user.user == healthcare_provider:
            raise serializers.ValidationError("User and healthcare provider cannot be the same.")

        # Continue with the appointment creation if the user and healthcare_provider are different
        appointment = serializer.save(user=user)

        # Send confirmation email
        subject = "Appointment Confirmation"
        message = f"Your appointment with {appointment.healthcare_provider.name} on {appointment.appointment_datetime} has been booked successfully."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)




from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentRescheduleSerializer,HealthCareCreateRecordSerializer
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
class AppointmentRescheduleView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentRescheduleSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        appointment = self.get_object()

        # Check if the user is the owner of the appointment
        if appointment.user.user != request.user:
            return Response(
                {"detail": "You are not the owner of this appointment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if appointment.is_rescheduled == True:
            return Response(
                {"error": "Appointment is already rescheduled. Make a new appointment."}
            )
        serializer = self.get_serializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)

        new_appointment_datetime = serializer.validated_data["new_appointment_datetime"]
        appointment.appointment_datetime = new_appointment_datetime
        appointment.is_rescheduled = True
        appointment.is_approved = False
        appointment.save()

        return Response({"detail": "Appointment rescheduled successfully."})



class RecordsView(generics.ListAPIView):
    # queryset = HealthcareReport.objects.all()
    serializer_class = HealthCareRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HealthcareReport.objects.filter(user=self.request.user.id)
class RecordsViewForProvider(generics.ListAPIView):
    # queryset = HealthcareReport.objects.all()
    serializer_class = HealthCareRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HealthcareReport.objects.filter(healthcare_provider=self.request.user.id)

class CreateRecordView(generics.CreateAPIView):
    queryset = HealthcareReport.objects.all()
    serializer_class = HealthCareCreateRecordSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     appointment_id = self.kwargs.get('appointment_id')
    #     appointment = get_object_or_404(Appointment, pk=appointment_id)
    #     if appointment.healthcare_provider.user.id == self.request.user.id:
    #         serializer.save(healthcare_provider = appointment.healthcare_provider,user=appointment.user, appointment=appointment)
    #     else:
    #         raise serializers.ValidationError("Only providers can create health records for their appointments.")


class IsHealthcareProvider(permissions.BasePermission):
    """
    Custom permission to check if the user is a healthcare provider.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a healthcare provider
        return request.user.is_authenticated and hasattr(request.user, 'healthcareprovider')

    def has_object_permission(self, request, view, obj):
        # Check if the user has permission to access the specific object (if needed)
        return request.user == obj.healthcare_provider.user

class ApproveAppointmentView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsHealthcareProvider]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Additional validation: Check if the healthcare provider is the owner of the appointment
        if request.user != instance.healthcare_provider.user:
            return Response({"detail": "You do not have permission to approve this appointment."}, status=status.HTTP_403_FORBIDDEN)

        instance.is_approved = True
        instance.save()

        return Response({"detail": "Appointment approved successfully."})
