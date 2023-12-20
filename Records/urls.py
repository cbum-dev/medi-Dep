from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.RecordsView.as_view(), name='records'), #done
    path('records-provider/', views.RecordsViewForProvider.as_view(), name='records-provider'), #done
    path('records/create/<int:appointment_id>/', views.CreateRecordView.as_view(), name='create-health-record'),
    path('appointments/<int:pk>/reschedule/', views.AppointmentRescheduleView.as_view(), name='reschedule-appointment'),
    path('appointments/create/',views.AppointmentCreateView.as_view(),name="Create-appointments"),
    path('appointments/provider/', views.ProviderAppointmentsView.as_view(), name='provider-appointments'),
    path('upcoming/', views.UpcomingAppointmentsView.as_view(), name='upcoming-appointments'),
    path('appointments/', views.AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('aappointments/', views.UserAppointmentsListView.as_view(), name='user-appointments'),
]
