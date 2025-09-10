from django.urls import path
from . import views

app_name = 'browser_extension'

urlpatterns = [
    # Core browser extension functionality
    path('check-url/', views.browser_check_url, name='check_url'),
    path('settings/', views.browser_settings, name='settings'),
    
    # Session management
    path('start-session/', views.browser_start_session, name='start_session'),
    path('sessions/<uuid:session_id>/end/', views.browser_end_session, name='end_session'),
    
    # Blocked sites management
    path('blocked-sites/', views.browser_blocked_sites, name='blocked_sites'),
    path('override/', views.browser_override_block, name='override_block'),
    
    # Statistics
    path('stats/', views.browser_protection_stats, name='protection_stats'),
]