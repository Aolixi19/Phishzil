from django.urls import path
from . import views

app_name = 'threat_protection'

urlpatterns = [
    # Link Disarming
    path('disarm-link/', views.disarm_malicious_link, name='disarm_link'),
    path('disarmed-links/', views.list_disarmed_links, name='list_disarmed_links'),
    path('disarmed-links/<uuid:link_id>/override/', views.override_disarmed_link, name='override_disarmed_link'),
    
    # File Quarantine
    path('quarantine-file/', views.quarantine_file, name='quarantine_file'),
    path('quarantined-files/', views.list_quarantined_files, name='list_quarantined_files'),
    path('quarantined-files/<uuid:file_id>/preview/', views.get_safe_file_preview, name='safe_file_preview'),
    
    # Real-time Protection
    path('real-time-scan/', views.real_time_scan, name='real_time_scan'),
    path('sessions/', views.protection_sessions, name='protection_sessions'),
    path('sessions/<uuid:session_id>/end/', views.end_protection_session, name='end_protection_session'),
    
    # Analytics & Logs
    path('analytics/', views.protection_analytics, name='protection_analytics'),
    path('logs/', views.protection_logs, name='protection_logs'),
    
    # Protection rules
    path('rules/', views.protection_rules, name='protection_rules'),
    path('rules/<uuid:rule_id>/', views.protection_rule_detail, name='protection_rule_detail'),
    path('rules/test/', views.test_protection_rule, name='test_protection_rule'),
    
    # Notifications
    path('notifications/preferences/', views.notification_preferences, name='notification_preferences'),

]