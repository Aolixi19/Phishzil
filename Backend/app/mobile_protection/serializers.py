# mobile_protection/serializers.py
from datetime import timezone
from rest_framework import serializers
from .models import MobileDevice, SMSContent, NotificationContent, MobileAlert, MobileSettings

class MobileDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileDevice
        fields = ['id', 'device_id', 'device_type', 'device_name', 'app_version',
                 'is_active', 'last_seen', 'registered_at', 'permissions_granted']
        read_only_fields = ['id', 'last_seen', 'registered_at']

class SMSContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSContent
        fields = ['id', 'sender', 'message_content', 'received_at', 'analyzed_at',
                 'is_threat', 'threat_type', 'confidence_score', 'action_taken']
        read_only_fields = ['id', 'analyzed_at']

class NotificationContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationContent
        fields = ['id', 'app_package', 'app_name', 'title', 'content', 'received_at',
                 'analyzed_at', 'is_threat', 'threat_type', 'confidence_score', 'action_taken']
        read_only_fields = ['id', 'analyzed_at']

class MobileAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileAlert
        fields = ['id', 'alert_type', 'severity', 'title', 'message', 'threat_details',
                 'created_at', 'acknowledged_at', 'is_dismissed']
        read_only_fields = ['id', 'created_at']

class MobileSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileSettings
        fields = ['sms_protection_enabled', 'notification_scanning_enabled',
                 'auto_block_suspicious_links', 'send_push_alerts', 'scan_frequency',
                 'trusted_contacts', 'blocked_keywords']

class MobileScanRequestSerializer(serializers.Serializer):
    content_type = serializers.ChoiceField(choices=['sms', 'notification', 'link'])
    content = serializers.CharField(max_length=5000)
    sender = serializers.CharField(max_length=255, required=False)
    app_package = serializers.CharField(max_length=255, required=False)
    app_name = serializers.CharField(max_length=255, required=False)
    received_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        from ..Phishing_Detection.utils import analyze_security_threat
        
        content_type = validated_data['content_type']
        content = validated_data['content']
        device = self.context['device']
        
        analyzer = analyze_security_threat()
        result = analyzer.analyze_content(content, content_type)
        
        # Create appropriate content record
        if content_type == 'sms':
            content_record = SMSContent.objects.create(
                device=device,
                sender=validated_data.get('sender', 'Unknown'),
                message_content=content,
                received_at=validated_data.get('received_at', timezone.now()),
                is_threat=result['is_malicious'],
                threat_type=result['threat_type'],
                confidence_score=result['confidence'],
                action_taken=result['recommended_action']
            )
        elif content_type == 'notification':
            content_record = NotificationContent.objects.create(
                device=device,
                app_package=validated_data.get('app_package', ''),
                app_name=validated_data.get('app_name', ''),
                title=content[:500],  # Truncate title
                content=content,
                received_at=validated_data.get('received_at', timezone.now()),
                is_threat=result['is_malicious'],
                threat_type=result['threat_type'],
                confidence_score=result['confidence'],
                action_taken=result['recommended_action']
            )
        
        # Create alert if high threat
        if result['is_malicious'] and result['confidence'] > 0.7:
            alert_type = 'SMS_THREAT' if content_type == 'sms' else 'NOTIFICATION_THREAT'
            MobileAlert.objects.create(
                device=device,
                alert_type=alert_type,
                severity=result['threat_level'],
                title=f"Suspicious {content_type} detected",
                message=f"PhishZil detected a {result['threat_type']} threat",
                threat_details=result
            )
        
        return result