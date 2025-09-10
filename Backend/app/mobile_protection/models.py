# mobile_protection/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class MobileDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=20, choices=[
        ('ANDROID', 'Android'),
        ('IOS', 'iOS')
    ])
    device_name = models.CharField(max_length=255)
    app_version = models.CharField(max_length=20)
    push_token = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    permissions_granted = models.JSONField(default=dict)  # SMS, notifications, etc.
    
    class Meta:
        db_table = 'mobile_devices'

class SMSContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(MobileDevice, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message_content = models.TextField()
    received_at = models.DateTimeField()
    analyzed_at = models.DateTimeField(auto_now_add=True)
    is_threat = models.BooleanField(default=False)
    threat_type = models.CharField(max_length=50, blank=True)
    confidence_score = models.FloatField(default=0.0)
    action_taken = models.CharField(max_length=50, default='NONE')
    user_reported = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'sms_content'

class NotificationContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(MobileDevice, on_delete=models.CASCADE)
    app_package = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    content = models.TextField()
    received_at = models.DateTimeField()
    analyzed_at = models.DateTimeField(auto_now_add=True)
    is_threat = models.BooleanField(default=False)
    threat_type = models.CharField(max_length=50, blank=True)
    confidence_score = models.FloatField(default=0.0)
    action_taken = models.CharField(max_length=50, default='NONE')
    
    class Meta:
        db_table = 'notification_content'

class MobileAlert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(MobileDevice, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, choices=[
        ('SMS_THREAT', 'SMS Threat'),
        ('APP_THREAT', 'App Threat'),
        ('NOTIFICATION_THREAT', 'Notification Threat'),
        ('MALICIOUS_LINK', 'Malicious Link')
    ])
    severity = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ])
    title = models.CharField(max_length=255)
    message = models.TextField()
    threat_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    is_dismissed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'mobile_alerts'

class MobileSettings(models.Model):
    device = models.OneToOneField(MobileDevice, on_delete=models.CASCADE)
    sms_protection_enabled = models.BooleanField(default=True)
    notification_scanning_enabled = models.BooleanField(default=True)
    auto_block_suspicious_links = models.BooleanField(default=True)
    send_push_alerts = models.BooleanField(default=True)
    scan_frequency = models.CharField(max_length=20, choices=[
        ('REAL_TIME', 'Real Time'),
        ('EVERY_HOUR', 'Every Hour'),
        ('DAILY', 'Daily')
    ], default='REAL_TIME')
    trusted_contacts = models.JSONField(default=list)
    blocked_keywords = models.JSONField(default=list)
    
    class Meta:
        db_table = 'mobile_settings'