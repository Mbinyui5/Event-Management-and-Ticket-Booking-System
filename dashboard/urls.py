from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard_view, name='admin_dashboard'),
    path('send-notification/', views.send_notification_view, name='send_notification'),
    path('export-report/', views.export_report_view, name='export_report'),
]
