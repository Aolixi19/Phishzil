# admin_dashboard/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SystemSettings, AdminLog, OrganizationManagement, ComplianceReport
from ..Phishing_Detection.models import ThreatDetectionResult
from ..threat_protection.models import DisarmedLink, QuarantinedFile

class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSettings
        fields = ['id', 'setting_key', 'setting_value', 'setting_type', 'description',
                 'is_public', 'created_at', 'updated_at', 'updated_by']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AdminLogSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin_user.username', read_only=True)
    
    class Meta:
        model = AdminLog
        fields = ['id', 'admin_user', 'admin_username', 'action_type', 'action_description',
                 'target_object_type', 'target_object_id', 'ip_address', 'result',
                 'additional_data', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class UserManagementSerializer(serializers.ModelSerializer):
    threat_count = serializers.SerializerMethodField()
    last_activity = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active',
                 'date_joined', 'last_login', 'threat_count', 'last_activity']
        read_only_fields = ['id', 'date_joined', 'threat_count', 'last_activity']
    
    def get_threat_count(self, obj):
        return ThreatDetectionResult.objects.filter(user=obj, is_malicious=True).count()
    
    def get_last_activity(self, obj):
        # Get most recent detection or protection activity
        from django.utils import timezone
        recent_detection = ThreatDetectionResult.objects.filter(user=obj).first()
        recent_protection = DisarmedLink.objects.filter(user=obj).first()
        
        if recent_detection and recent_protection:
            return max(recent_detection.created_at, recent_protection.disarm_timestamp)
        elif recent_detection:
            return recent_detection.created_at
        elif recent_protection:
            return recent_protection.disarm_timestamp
        return None

class OrganizationManagementSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    admin_username = serializers.CharField(source='admin_user.username', read_only=True)
    
    class Meta:
        model = OrganizationManagement
        fields = ['id', 'name', 'organization_type', 'admin_user', 'admin_username',
                 'is_active', 'subscription_plan', 'max_users', 'member_count',
                 'created_at', 'settings']
        read_only_fields = ['id', 'created_at', 'member_count']
    
    def get_member_count(self, obj):
        return obj.members.filter(organizationmembership__is_active=True).count()

class ComplianceReportSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    generated_by_username = serializers.CharField(source='generated_by.username', read_only=True)
    
    class Meta:
        model = ComplianceReport
        fields = ['id', 'organization', 'organization_name', 'report_type',
                 'period_start', 'period_end', 'generated_by', 'generated_by_username',
                 'report_data', 'file_path', 'generated_at', 'is_exported']
        read_only_fields = ['id', 'generated_at']

class SystemOverviewSerializer(serializers.Serializer):
    def to_representation(self, instance):
        from django.utils import timezone
        from django.db.models import Count, Q
        
        # Calculate system-wide statistics
        total_users = User.objects.count()
        active_users_24h = User.objects.filter(
            last_login__gte=timezone.now() - timezone.timedelta(days=1)
        ).count()
        
        total_detections = ThreatDetectionResult.objects.count()
        malicious_detections = ThreatDetectionResult.objects.filter(is_malicious=True).count()
        
        total_links_disarmed = DisarmedLink.objects.count()
        total_files_quarantined = QuarantinedFile.objects.count()
        
        # Recent activity
        recent_threats = ThreatDetectionResult.objects.filter(
            is_malicious=True,
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        ).count()
        
        return {
            'users': {
                'total': total_users,
                'active_24h': active_users_24h,
                'new_registrations_24h': User.objects.filter(
                    date_joined__gte=timezone.now() - timezone.timedelta(days=1)
                ).count()
            },
            'detections': {
                'total': total_detections,
                'malicious': malicious_detections,
                'detection_rate': (malicious_detections / total_detections * 100) if total_detections > 0 else 0
            },
            'protection': {
                'links_disarmed': total_links_disarmed,
                'files_quarantined': total_files_quarantined,
                'total_threats_blocked': total_links_disarmed + total_files_quarantined
            },
            'recent_activity': {
                'threats_24h': recent_threats,
                'protection_effectiveness': 95.5,  # Calculate based on real data
                'system_uptime': 99.8
            }
        }