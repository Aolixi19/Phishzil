from django.db import models
from django.conf import settings
from django.utils import timezone
from Phishing_Detection.models import ThreatDetectionResult
import uuid
import os
from django.contrib.auth.models import User


class DisarmedLink(models.Model):
    """Links that have been automatically disarmed"""
    DISARM_METHODS = [
        ('BLOCK', 'Blocked with warning'),
        ('SANITIZE', 'Sanitized URL'),
        ('REDIRECT', 'Safe redirect'),
        ('PLACEHOLDER', 'Text placeholder'),
        ('PREVIEW', 'Safe preview mode'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_url = models.URLField()
    safe_replacement = models.CharField(max_length=500)
    disarm_method = models.CharField(max_length=20, choices=DISARM_METHODS)
    disarm_reason = models.TextField()
    
    # Relationships
    threat_detection = models.ForeignKey(
        ThreatDetectionResult, 
        on_delete=models.CASCADE, 
        related_name='disarmed_links'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='disarmed_links'
    )
    
    # Metadata
    click_attempts = models.IntegerField(default=0)
    user_overridden = models.BooleanField(default=False)
    override_reason = models.TextField(blank=True, null=True)
    
    # Timestamps
    disarm_timestamp = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-disarm_timestamp']
        indexes = [
            models.Index(fields=['user', 'disarm_timestamp']),
            models.Index(fields=['original_url']),
            models.Index(fields=['disarm_method']),
        ]

    def __str__(self):
        return f"Disarmed: {self.original_url[:50]} ({self.disarm_method})"

    def record_click_attempt(self):
        """Record when user tries to access disarmed link"""
        self.click_attempts += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['click_attempts', 'last_accessed'])


class QuarantinedFile(models.Model):
    """Files quarantined due to threats"""
    QUARANTINE_STATUS = [
        ('QUARANTINED', 'Quarantined'),
        ('ANALYZING', 'Under Analysis'),
        ('SAFE', 'Marked Safe'),
        ('MALICIOUS', 'Confirmed Malicious'),
        ('DELETED', 'Permanently Deleted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64, unique=True)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    
    # Storage locations
    quarantine_location = models.CharField(max_length=500)
    safe_preview_location = models.CharField(max_length=500, blank=True, null=True)
    
    # Analysis results
    threat_detection = models.ForeignKey(
        ThreatDetectionResult, 
        on_delete=models.CASCADE,
        related_name='quarantined_files'
    )
    status = models.CharField(max_length=20, choices=QUARANTINE_STATUS, default='QUARANTINED')
    
    # User info
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='quarantined_files'
    )
    source_context = models.CharField(max_length=50)  # email, sms, download, etc.
    
    # Timestamps
    quarantine_timestamp = models.DateTimeField(auto_now_add=True)
    analysis_completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-quarantine_timestamp']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['file_hash']),
            models.Index(fields=['quarantine_timestamp']),
        ]

    def __str__(self):
        return f"Quarantined: {self.original_filename} ({self.status})"

    def create_safe_preview(self):
        """Create safe preview of quarantined file"""
        # Implementation would depend on file type
        preview_content = f"[SAFE PREVIEW]\nFilename: {self.original_filename}\nSize: {self.file_size} bytes\nType: {self.mime_type}\nThreat Level: {self.threat_detection.threat_level}"
        
        preview_filename = f"preview_{self.id}.txt"
        preview_path = os.path.join('quarantine', 'previews', preview_filename)
        
        # In real implementation, you'd write to actual storage
        self.safe_preview_location = preview_path
        self.save(update_fields=['safe_preview_location'])
        
        return preview_path


class RealTimeSession(models.Model):
    """Track real-time protection sessions"""
    SESSION_TYPES = [
        ('EMAIL', 'Email Protection'),
        ('SMS', 'SMS Protection'),
        ('BROWSER', 'Browser Protection'),
        ('MOBILE', 'Mobile App Protection'),
        ('CHAT', 'Chat/Messaging Protection'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='protection_sessions'
    )
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    
    # Session stats
    is_active = models.BooleanField(default=True)
    threats_blocked = models.IntegerField(default=0)
    links_disarmed = models.IntegerField(default=0)
    files_quarantined = models.IntegerField(default=0)
    
    # Session metadata
    device_info = models.JSONField(default=dict, blank=True)
    settings = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_type', 'started_at']),
        ]

    def __str__(self):
        return f"{self.session_type} session for {self.user.username}"

    def record_threat_blocked(self):
        """Record a threat being blocked in this session"""
        self.threats_blocked += 1
        self.last_activity = timezone.now()
        self.save(update_fields=['threats_blocked', 'last_activity'])

    def end_session(self):
        """End the protection session"""
        self.is_active = False
        self.ended_at = timezone.now()
        self.save(update_fields=['is_active', 'ended_at'])


class ProtectionRule(models.Model):
    """Custom protection rules for users/organizations"""
    RULE_TYPES = [
        ('URL_PATTERN', 'URL Pattern Blocking'),
        ('DOMAIN_WHITELIST', 'Domain Whitelist'),
        ('FILE_EXTENSION', 'File Extension Blocking'),
        ('SENDER_PATTERN', 'Sender Pattern Blocking'),
        ('CONTENT_KEYWORD', 'Content Keyword Blocking'),
    ]
    
    ACTION_TYPES = [
        ('BLOCK', 'Block completely'),
        ('WARN', 'Warn user'),
        ('QUARANTINE', 'Quarantine'),
        ('ALLOW', 'Allow'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='protection_rules'
    )
    
    name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    pattern = models.TextField()  # Regex or pattern to match
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=100)  # Lower = higher priority
    
    # Stats
    times_triggered = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['rule_type', 'priority']),
        ]

    def __str__(self):
        return f"{self.name} ({self.rule_type})"


class ProtectionLog(models.Model):
    """Detailed log of all protection actions"""
    ACTION_TYPES = [
        ('LINK_DISARMED', 'Link Disarmed'),
        ('FILE_QUARANTINED', 'File Quarantined'),
        ('THREAT_BLOCKED', 'Threat Blocked'),
        ('USER_OVERRIDE', 'User Override'),
        ('RULE_TRIGGERED', 'Protection Rule Triggered'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='protection_logs'
    )
    session = models.ForeignKey(
        RealTimeSession, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='logs'
    )
    
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.TextField()
    
    # References to related objects
    disarmed_link = models.ForeignKey(DisarmedLink, on_delete=models.SET_NULL, null=True, blank=True)
    quarantined_file = models.ForeignKey(QuarantinedFile, on_delete=models.SET_NULL, null=True, blank=True)
    protection_rule = models.ForeignKey(ProtectionRule, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional context
    source_data = models.JSONField(default=dict)
    result_data = models.JSONField(default=dict)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action_type', 'timestamp']),
            models.Index(fields=['session', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.action_type}: {self.description[:50]}"
    
# Add to protection/models.py

class ProtectionRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rule_type = models.CharField(max_length=50, choices=[
        ('URL_PATTERN', 'URL Pattern'),
        ('EMAIL_SENDER', 'Email Sender'),
        ('FILE_TYPE', 'File Type'),
        ('KEYWORD', 'Keyword'),
        ('DOMAIN', 'Domain')
    ])
    pattern = models.TextField()  # Regex or pattern to match
    action = models.CharField(max_length=50, choices=[
        ('BLOCK', 'Block'),
        ('QUARANTINE', 'Quarantine'),
        ('WARN', 'Warn'),
        ('ALLOW', 'Allow')
    ])
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=100)  # Lower = higher priority
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match_count = models.PositiveIntegerField(default=0)  # How many times rule was triggered
    
    class Meta:
        db_table = 'protection_rules'
        ordering = ['priority', 'created_at']

class NotificationPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_alerts = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_alerts = models.BooleanField(default=False)
    alert_frequency = models.CharField(max_length=20, choices=[
        ('IMMEDIATE', 'Immediate'),
        ('HOURLY', 'Hourly Digest'),
        ('DAILY', 'Daily Digest'),
        ('WEEKLY', 'Weekly Digest')
    ], default='IMMEDIATE')
    threat_level_threshold = models.CharField(max_length=20, choices=[
        ('LOW', 'Low and above'),
        ('MEDIUM', 'Medium and above'),
        ('HIGH', 'High and above'),
        ('CRITICAL', 'Critical only')
    ], default='MEDIUM')
    notification_channels = models.JSONField(default=list)  # email, push, sms, etc.
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notification_preferences'