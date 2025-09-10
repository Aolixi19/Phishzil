# urls.py - Complete URL configuration without router

from django.urls import path
from . import views

urlpatterns = [
    # Phishing Detection Endpoints
    path('url', views.detect_url, name='detect_url'),
    path('text', views.detect_text, name='detect_text'), 
    path('file', views.detect_file, name='detect_file'),
    path('stats', views.detection_stats, name='detection_stats'),
    
    # Alerts & Safe Browsing Endpoints
    path('alerts/', views.get_alerts, name='get_alerts'),
    path('alerts/<uuid:alert_id>/override/', views.override_alert, name='override_alert'),
    path('alerts/safe-browsing/', views.create_safe_browsing_warning, name='safe_browsing_warning'),
    path('alerts/bulk/', views.bulk_alert_actions, name='bulk_alert_actions'),
    path('alerts/search/', views.search_alerts, name='search_alerts'),
    path('alerts/auto-create/', views.create_alert_from_detection, name='auto_create_alert'),
    path('alerts/cleanup/', views.cleanup_old_alerts, name='cleanup_alerts'),
    path('alerts/analytics/', views.alert_analytics, name='alert_analytics'),
    
    # Threat Database Endpoints
    path('threats/', views.threat_list, name='threat_list'),
    path('threats/<int:pk>/', views.threat_detail, name='threat_detail'),
    path('threats/import/', views.import_threat_feed, name='import_threat_feed'),
    path('threats/feeds/', views.threat_feed_status, name='threat_feed_status'),
    
    # User Reports Endpoints
    path('reports/', views.report_list_create, name='report_list_create'),
    path('reports/<uuid:pk>/', views.report_detail, name='report_detail'),
    path('reports/summary/', views.report_summary, name='report_summary'),
    
    
]