from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class ThreatFeed(models.Model):
    """External threat intelligence feeds"""
    FEED_TYPES = [
        ('PHISHTANK', 'PhishTank'),
        ('OPENPHISH', 'OpenPhish'),
        ('URLVOID', 'URLVoid'),
        ('VIRUSTOTAL', 'VirusTotal'),
        ('CUSTOM', 'Custom Feed'),
    ]
    
    name = models.CharField(max_length=100)
    feed_type = models.CharField(max_length=20, choices=FEED_TYPES)
    url = models.URLField()
    api_key = models.CharField(max_length=255, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    update_frequency = models.IntegerField(default=3600)  # seconds
    
    total_threats = models.IntegerField(default=0)
    new_threats_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['feed_type', 'is_active']),
            models.Index(fields=['last_updated']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.feed_type})"


class ThreatDatabase(models.Model):
    """Database of known threats for quick lookup"""
    THREAT_TYPES = [
        ('URL', 'Malicious URL'),
        ('DOMAIN', 'Malicious Domain'),
        ('HASH', 'File Hash'),
        ('PATTERN', 'Content Pattern'),
        ('IP', 'Malicious IP'),
        ('EMAIL', 'Known Phishing Email'),
    ]
    
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'), 
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ]
    
    threat_type = models.CharField(max_length=20, choices=THREAT_TYPES)
    value = models.TextField()  # URL, domain, hash, or pattern
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField(blank=True)
    
    # Source tracking
    source_feed = models.ForeignKey(ThreatFeed, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=100, blank=True)  # Threat intelligence source
    external_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Metadata
    tags = models.JSONField(default=list)
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    confidence_score = models.FloatField(default=0.8)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['threat_type', 'value']
        indexes = [
            models.Index(fields=['threat_type', 'value']),
            models.Index(fields=['severity', 'is_active']),
            models.Index(fields=['source_feed', 'updated_at']),
            models.Index(fields=['is_active', 'threat_type']),
        ]

    def __str__(self):
        return f"{self.threat_type}: {self.value[:50]}"


class ThreatDetectionResult(models.Model):
    """Store results of threat detection analysis"""
    DETECTION_TYPES = [
        ('URL', 'URL Detection'),
        ('TEXT', 'Text/Message Detection'),
        ('FILE', 'File Detection'),
    ]
    
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'), 
        ('CRITICAL', 'Critical')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detection_type = models.CharField(max_length=10, choices=DETECTION_TYPES)
    
    # Input data
    analyzed_url = models.URLField(blank=True, null=True)
    analyzed_text = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_hash = models.CharField(max_length=64, blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    
    # Analysis results
    is_malicious = models.BooleanField()
    threat_level = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    confidence_score = models.FloatField()  # 0.0 to 1.0
    threat_types = models.JSONField(default=list)  # List of detected threat types
    indicators = models.JSONField(default=list)    # List of threat indicators
    recommended_action = models.CharField(max_length=50)
    
    # Analysis details
    analysis_details = models.JSONField(default=dict)
    processing_time_ms = models.IntegerField(blank=True, null=True)
    
    # Context and metadata
    context = models.CharField(max_length=20, blank=True, null=True)  # email, sms, chat, web
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_malicious', 'threat_level']),
            models.Index(fields=['detection_type', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['file_hash']),
            models.Index(fields=['confidence_score']),
        ]

    def __str__(self):
        return f"{self.detection_type} - {self.threat_level} ({self.confidence_score:.2f})"


class DetectionLog(models.Model):
    """Log all detection attempts for monitoring and analytics"""
    detection_result = models.ForeignKey(ThreatDetectionResult, on_delete=models.CASCADE, related_name='logs')
    endpoint = models.CharField(max_length=50)
    request_data_hash = models.CharField(max_length=64)  # Hash of request data for deduplication
    response_time_ms = models.IntegerField()
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endpoint', 'created_at']),
            models.Index(fields=['request_data_hash']),
        ]

    def __str__(self):
        return f"{self.endpoint} - {self.response_time_ms}ms"


class Alert(models.Model):
    """Real-time security alerts for users"""
    ALERT_TYPES = [
        ('PHISHING_URL', 'Phishing URL Detected'),
        ('MALICIOUS_FILE', 'Malicious File Detected'),
        ('SUSPICIOUS_EMAIL', 'Suspicious Email Content'),
        ('DOMAIN_SPOOFING', 'Domain Spoofing Attempt'),
        ('CREDENTIAL_HARVEST', 'Credential Harvesting Attempt'),
        ('SOCIAL_ENGINEERING', 'Social Engineering Detected'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
        ('FALSE_POSITIVE', 'False Positive'),
        ('ARCHIVED', 'Archived'),  # ✅ Added for BulkAlertActionSerializer
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='security_alerts')
    detection_result = models.OneToOneField(
        ThreatDetectionResult, 
        on_delete=models.CASCADE, 
        related_name='alert',
        null=True, blank=True
    )
    
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    threat_details = models.JSONField(default=dict)
    
    # Source information
    source_url = models.URLField(blank=True, null=True)
    source_file = models.CharField(max_length=255, blank=True, null=True)
    source_content = models.TextField(blank=True, null=True)
    
    # User actions
    user_override = models.BooleanField(default=False)
    override_reason = models.TextField(blank=True, null=True)
    override_timestamp = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    priority = models.IntegerField(default=1, help_text="1=Highest, 5=Lowest")
    tags = models.JSONField(default=list, blank=True)
    is_read = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    related_alerts = models.ManyToManyField('self', blank=True, symmetrical=False)
    auto_created = models.BooleanField(default=False)  # Was this auto-generated?
    escalation_level = models.IntegerField(default=0)  # 0=normal, 1=escalated, 2=critical
    
    # Notification tracking
    notification_sent = models.BooleanField(default=False)
    notification_sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'status', 'severity']),
            models.Index(fields=['alert_type', 'created_at']),
            models.Index(fields=['severity', 'status']),
            models.Index(fields=['is_read', 'created_at']),
            models.Index(fields=['priority', 'created_at']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['auto_created']),
            models.Index(fields=['escalation_level']),
        ]

    def __str__(self):
        return f"{self.alert_type} - {self.severity} ({self.user.username})"

    def mark_as_read(self):
        """Mark alert as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    def acknowledge(self):
        """Acknowledge the alert"""
        self.status = 'ACKNOWLEDGED'
        self.acknowledged_at = timezone.now()
        self.save(update_fields=['status', 'acknowledged_at'])

    def resolve(self, reason=None):
        """Resolve the alert"""
        self.status = 'RESOLVED'
        self.resolved_at = timezone.now()
        if reason:
            self.override_reason = reason
        self.save(update_fields=['status', 'resolved_at', 'override_reason'])

    def archive(self):
        """Archive the alert"""
        self.status = 'ARCHIVED'
        self.is_read = True
        self.save(update_fields=['status', 'is_read'])

    @property
    def is_expired(self):
        """Check if alert has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class AlertNotification(models.Model):
    """Track alert notifications sent to users"""
    NOTIFICATION_TYPES = [
        ('EMAIL', 'Email'),
        ('PUSH', 'Push Notification'),
        ('SMS', 'SMS'),
        ('IN_APP', 'In-App Notification'),
    ]
    
    DELIVERY_STATUS = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
        ('READ', 'Read by User'),
    ]
    
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    recipient = models.CharField(max_length=255)  # email, phone, device_id
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='PENDING')
    
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['alert', 'notification_type']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['recipient']),
        ]

    def __str__(self):
        return f"{self.notification_type} to {self.recipient} - {self.status}"

    def mark_as_sent(self):
        """Mark notification as sent"""
        self.status = 'SENT'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at'])

    def mark_as_delivered(self):
        """Mark notification as delivered"""
        self.status = 'DELIVERED'
        self.delivered_at = timezone.now()
        self.save(update_fields=['status', 'delivered_at'])

    def mark_as_read(self):
        """Mark notification as read by user"""
        self.status = 'READ'
        self.read_at = timezone.now()
        self.save(update_fields=['status', 'read_at'])


class AlertTemplate(models.Model):
    """Predefined alert templates for consistent messaging"""
    name = models.CharField(max_length=100, unique=True)
    alert_type = models.CharField(max_length=30, choices=Alert.ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=Alert.SEVERITY_LEVELS)
    
    title_template = models.CharField(max_length=200)
    description_template = models.TextField()
    
    # Template variables documentation
    available_variables = models.JSONField(
        default=list,
        help_text="List of available template variables like {url}, {confidence}, etc."
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['alert_type', 'severity']),
            models.Index(fields=['is_active']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.alert_type})"
    
    def render_alert(self, **context):
        """Render alert with dynamic content"""
        try:
            return {
                'title': self.title_template.format(**context),
                'description': self.description_template.format(**context)
            }
        except KeyError as e:
            raise ValueError(f"Missing template variable: {e}")


class SafeBrowsingWarning(models.Model):
    """Safe browsing warning pages and redirects"""
    WARNING_TYPES = [
        ('PHISHING', 'Phishing Site'),
        ('MALWARE', 'Malware Distribution'),
        ('SUSPICIOUS', 'Suspicious Content'),
        ('BLOCKED', 'Blocked Domain'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, null=True, blank=True)
    
    original_url = models.URLField()
    warning_type = models.CharField(max_length=20, choices=WARNING_TYPES)
    threat_details = models.JSONField(default=dict)
    
    # User actions
    user_proceeded = models.BooleanField(default=False)
    proceed_timestamp = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['original_url']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['warning_type']),
            models.Index(fields=['user_proceeded']),
        ]

    def __str__(self):
        return f"{self.warning_type}: {self.original_url[:50]}"

    def mark_user_proceeded(self):
        """Mark that user proceeded despite warning"""
        self.user_proceeded = True
        self.proceed_timestamp = timezone.now()
        self.save(update_fields=['user_proceeded', 'proceed_timestamp'])


class UserReport(models.Model):
    """User-submitted threat reports"""
    REPORT_TYPES = [
        ('PHISHING_URL', 'Phishing URL'),
        ('PHISHING_EMAIL', 'Phishing Email'),
        ('MALICIOUS_FILE', 'Malicious File'),
        ('SPAM', 'Spam Content'),
        ('SCAM', 'Scam/Fraud'),
        ('OTHER', 'Other Threat'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('INVESTIGATING', 'Under Investigation'),
        ('CONFIRMED', 'Confirmed Threat'),
        ('FALSE_POSITIVE', 'False Positive'),
        ('DUPLICATE', 'Duplicate Report'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_reports')
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Reported content
    suspicious_url = models.URLField(blank=True, null=True)
    suspicious_email = models.EmailField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_hash = models.CharField(max_length=64, blank=True, null=True)
    content_description = models.TextField()
    
    # Additional details
    source_context = models.CharField(max_length=50, blank=True, null=True)  # email, sms, web, etc.
    threat_indicators = models.JSONField(default=list)
    screenshots = models.JSONField(default=list)  # URLs to screenshot files
    
    # Analysis results
    automated_analysis = models.JSONField(default=dict, blank=True)
    manual_review_notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['report_type', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'reviewed_at']),
            models.Index(fields=['suspicious_url']),
        ]
    
    def __str__(self):
        return f"{self.report_type} - {self.status} ({self.user.username})"

    def mark_as_investigating(self):
        """Mark report as under investigation"""
        self.status = 'INVESTIGATING'
        self.reviewed_at = timezone.now()
        self.save(update_fields=['status', 'reviewed_at'])

    def confirm_threat(self, notes=None):
        """Confirm the report as a legitimate threat"""
        self.status = 'CONFIRMED'
        self.resolved_at = timezone.now()
        if notes:
            self.manual_review_notes = notes
        self.save(update_fields=['status', 'resolved_at', 'manual_review_notes'])

    def mark_false_positive(self, notes=None):
        """Mark report as false positive"""
        self.status = 'FALSE_POSITIVE'
        self.resolved_at = timezone.now()
        if notes:
            self.manual_review_notes = notes
        self.save(update_fields=['status', 'resolved_at', 'manual_review_notes'])