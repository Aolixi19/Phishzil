from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    # System overview
    path('overview/', views.admin_system_overview, name='system_overview'),
    
    # User management
    path('users/', views.manage_users, name='manage_users'),
    
    # System settings
    path('settings/', views.system_settings, name='system_settings'),
    
    # Admin logs
    path('logs/', views.admin_logs, name='admin_logs'),
    
    # Compliance reports
    path('compliance-report/', views.generate_compliance_report, name='compliance_report'),
    
    # Organization management
    path('organizations/', views.organization_management, name='organization_management'),
]