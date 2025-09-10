from django.db import models
from django.contrib.auth.models import User
import uuid

class SystemSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    setting_key = models.CharField(max_length=255, unique=True)
    setting_value = models.TextField()
    setting_type = models.CharField(max_length=50, choices=[
        ('STRING', 'String'),
        ('INTEGER', 'Integer'),
        ('BOOLEAN', 'Boolean'),
        ('JSON', 'JSON'),
        ('FLOAT', 'Float')
    ])
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)  # Can regular users see this?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'system_settings'

class AdminLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100, choices=[
        ('USER_MANAGEMENT', 'User Management'),
        ('SYSTEM_SETTINGS', 'System Settings'),
        ('THREAT_DATABASE', 'Threat Database'),
        ('COMPLIANCE_REPORT', 'Compliance Report'),
        ('BULK_OPERATION', 'Bulk Operation'),
        ('SECURITY_AUDIT', 'Security Audit')
    ])
    action_description = models.TextField()
    target_object_type = models.CharField(max_length=100, blank=True)
    target_object_id = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    result = models.CharField(max_length=50, choices=[
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
        ('PARTIAL', 'Partial Success')
    ])
    additional_data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'admin_logs'

class OrganizationManagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=50, choices=[
        ('ENTERPRISE', 'Enterprise'),
        ('GOVERNMENT', 'Government'),
        ('EDUCATIONAL', 'Educational'),
        ('FAMILY', 'Family'),
        ('PERSONAL', 'Personal')
    ])
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_orgs')
    members = models.ManyToManyField(User, through='OrganizationMembership')
    is_active = models.BooleanField(default=True)
    subscription_plan = models.CharField(max_length=50, default='BASIC')
    max_users = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    settings = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'organization_management'

class OrganizationMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationManagement, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('MEMBER', 'Member'),
        ('VIEWER', 'Viewer')
    ])
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'organization_memberships'
        unique_together = ['user', 'organization']

class ComplianceReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(OrganizationManagement, on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=50, choices=[
        ('SECURITY_AUDIT', 'Security Audit'),
        ('THREAT_SUMMARY', 'Threat Summary'),
        ('USER_ACTIVITY', 'User Activity'),
        ('COMPLIANCE_CHECK', 'Compliance Check')
    ])
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_data = models.JSONField()
    file_path = models.CharField(max_length=500, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_exported = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'compliance_reports'