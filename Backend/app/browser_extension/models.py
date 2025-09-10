from django.db import models
import uuid

from user.models import User

class BrowserSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    browser_type = models.CharField(max_length=20, choices=[
        ('CHROME', 'Chrome'),
        ('FIREFOX', 'Firefox'),
        ('EDGE', 'Edge'),
        ('SAFARI', 'Safari')
    ])
    extension_version = models.CharField(max_length=20)
    session_token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    urls_checked = models.PositiveIntegerField(default=0)
    threats_blocked = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'browser_sessions'

class BlockedSite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(BrowserSession, on_delete=models.CASCADE, null=True)
    url = models.URLField(max_length=2000)
    domain = models.CharField(max_length=255)
    threat_type = models.CharField(max_length=50, choices=[
        ('PHISHING', 'Phishing'),
        ('MALWARE', 'Malware'),
        ('SUSPICIOUS', 'Suspicious'),
        ('BLACKLISTED', 'Blacklisted')
    ])
    confidence_score = models.FloatField()
    blocked_at = models.DateTimeField(auto_now_add=True)
    user_overridden = models.BooleanField(default=False)
    override_reason = models.TextField(blank=True)
    page_context = models.CharField(max_length=100, default='navigation')

    class Meta:
        db_table = 'blocked_sites'

class BrowserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    protection_level = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('MAXIMUM', 'Maximum')
    ], default='HIGH')
    block_suspicious_downloads = models.BooleanField(default=True)
    warn_on_phishing_sites = models.BooleanField(default=True)
    auto_quarantine_files = models.BooleanField(default=True)
    show_domain_warnings = models.BooleanField(default=True)
    enable_safe_browsing = models.BooleanField(default=True)
    whitelist_domains = models.JSONField(default=list)
    blacklist_domains = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'browser_settings'