from django.urls import path
from . import views

app_name = 'mobile_protection'

urlpatterns = [
    # Device management
    path('register/', views.register_mobile_device, name='register_device'),
    path('devices/<str:device_id>/settings/', views.mobile_device_settings, name='device_settings'),
    
    # Content scanning
    path('scan/', views.mobile_scan_content, name='scan_content'),
    
    # Alerts
    path('alerts/', views.mobile_alerts, name='alerts'),
    path('alerts/<uuid:alert_id>/acknowledge/', views.acknowledge_mobile_alert, name='acknowledge_alert'),
    
    # Dashboard
    path('dashboard/', views.mobile_protection_dashboard, name='dashboard'),
    
    # Push notifications
    path('push-notification/', views.send_push_notification, name='push_notification'),
]