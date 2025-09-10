from rest_framework import serializers
from .models import (
    DisarmedLink, NotificationPreferences, QuarantinedFile, RealTimeSession, 
    ProtectionRule, ProtectionLog
)
from Phishing_Detection.models import ThreatDetectionResult

from Phishing_Detection.utils import analyze_security_threat
import hashlib
import time
from django.utils import timezone


class LinkDisarmSerializer(serializers.Serializer):
    """Serializer for disarming malicious links"""
    url = serializers.URLField(required=True)
    disarm_method = serializers.ChoiceField(
        choices=[choice[0] for choice in DisarmedLink.DISARM_METHODS],
        default='BLOCK'
    )
    context = serializers.CharField(required=False, default='manual')
    source_content = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        user = self.context['request'].user
        
        # First, analyze the URL for threats
        analysis = analyze_security_threat(
            url=validated_data['url'],
            context=validated_data.get('context', 'manual')
        )
        
        # Create threat detection result
        threat_result = ThreatDetectionResult.objects.create(
            detection_type='URL',
            analyzed_url=validated_data['url'],
            analyzed_text=validated_data.get('source_content'),
            is_malicious=analysis.is_malicious,
            threat_level=analysis.threat_level,
            confidence_score=analysis.confidence_score,
            threat_types=analysis.threat_types,
            indicators=analysis.indicators,
            recommended_action=analysis.recommended_action,
            analysis_details=analysis.details,
            context=validated_data.get('context'),
            user=user
        )
        
        # Create safe replacement based on method
        disarm_method = validated_data.get('disarm_method', 'BLOCK')
        
        if disarm_method == 'BLOCK':
            safe_replacement = f"[BLOCKED: Malicious link detected - {analysis.threat_level} threat]"
        elif disarm_method == 'PLACEHOLDER':
            safe_replacement = f"[LINK REMOVED: Click to view details]"
        elif disarm_method == 'SANITIZE':
            safe_replacement = f"hxxp://{validated_data['url'].replace('http://', '').replace('https://', '')}"
        elif disarm_method == 'PREVIEW':
            safe_replacement = f"[SAFE PREVIEW: {validated_data['url'][:30]}...]"
        else:
            safe_replacement = f"[DISARMED: {validated_data['url'][:30]}...]"
        
        # Create disarmed link record
        disarmed_link = DisarmedLink.objects.create(
            original_url=validated_data['url'],
            safe_replacement=safe_replacement,
            disarm_method=disarm_method,
            disarm_reason=f"Threat level: {analysis.threat_level}, Confidence: {analysis.confidence_score:.0%}",
            threat_detection=threat_result,
            user=user
        )
        
        # Log the action
        ProtectionLog.objects.create(
            user=user,
            action_type='LINK_DISARMED',
            description=f"Disarmed {disarm_method}: {validated_data['url']}",
            disarmed_link=disarmed_link,
            source_data=validated_data,
            result_data={
                'safe_replacement': safe_replacement,
                'threat_level': analysis.threat_level,
                'confidence': analysis.confidence_score
            }
        )
        
        return disarmed_link


class FileQuarantineSerializer(serializers.Serializer):
    """Serializer for quarantining malicious files"""
    file = serializers.FileField(required=False)
    file_hash = serializers.CharField(required=False, max_length=64)
    file_name = serializers.CharField(required=False)
    context = serializers.CharField(required=False, default='upload')

    def validate(self, data):
        if not data.get('file') and not data.get('file_hash'):
            raise serializers.ValidationError(
                "Either 'file' or 'file_hash' must be provided"
            )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        
        file_content = None
        file_name = validated_data.get('file_name', 'unknown')
        file_hash = validated_data.get('file_hash')
        file_size = 0
        mime_type = 'application/octet-stream'
        
        # Handle file upload
        if validated_data.get('file'):
            uploaded_file = validated_data['file']
            file_content = uploaded_file.read()
            file_name = uploaded_file.name
            file_size = uploaded_file.size
            mime_type = getattr(uploaded_file, 'content_type', 'application/octet-stream')
            
            # Calculate hash
            file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Analyze file for threats
        if file_content:
            analysis = analyze_security_threat(
                file_content=file_content,
                context=validated_data.get('context', 'upload')
            )
        else:
            # Hash-only analysis
            analysis = type('ThreatAssessment', (), {
                'is_malicious': True,  # Assume malicious if being quarantined
                'threat_level': 'HIGH',
                'confidence_score': 0.8,
                'threat_types': ['SUSPICIOUS_FILE'],
                'indicators': ['File quarantined by user request'],
                'recommended_action': 'QUARANTINE',
                'details': {'hash_only_analysis': True}
            })()
        
        # Create threat detection result
        threat_result = ThreatDetectionResult.objects.create(
            detection_type='FILE',
            file_name=file_name,
            file_hash=file_hash,
            file_size=file_size,
            is_malicious=analysis.is_malicious,
            threat_level=analysis.threat_level,
            confidence_score=analysis.confidence_score,
            threat_types=analysis.threat_types,
            indicators=analysis.indicators,
            recommended_action=analysis.recommended_action,
            analysis_details=analysis.details,
            context=validated_data.get('context'),
            user=user
        )
        
        # Create quarantine location (in real implementation, use proper file storage)
        quarantine_location = f"quarantine/{user.id}/{file_hash[:8]}/{file_name}"
        
        # Create quarantined file record
        quarantined_file = QuarantinedFile.objects.create(
            original_filename=file_name,
            file_hash=file_hash,
            file_size=file_size,
            mime_type=mime_type,
            quarantine_location=quarantine_location,
            threat_detection=threat_result,
            user=user,
            source_context=validated_data.get('context', 'upload')
        )
        
        # Create safe preview
        quarantined_file.create_safe_preview()
        
        # Log the action
        ProtectionLog.objects.create(
            user=user,
            action_type='FILE_QUARANTINED',
            description=f"Quarantined file: {file_name}",
            quarantined_file=quarantined_file,
            source_data=validated_data,
            result_data={
                'quarantine_location': quarantine_location,
                'file_size': file_size,
                'threat_level': analysis.threat_level
            }
        )
        
        return quarantined_file


class RealTimeScanSerializer(serializers.Serializer):
    """Serializer for real-time content scanning"""
    content_type = serializers.ChoiceField(choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('message', 'Message'),
        ('webpage', 'Webpage')
    ])
    content = serializers.CharField(required=True)
    sender_info = serializers.JSONField(required=False, default=dict)
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True
    )

    def create(self, validated_data):
        user = self.context['request'].user
        
        # Get or create active session
        session, created = RealTimeSession.objects.get_or_create(
            user=user,
            session_type=validated_data['content_type'].upper(),
            is_active=True,
            defaults={
                'device_info': self.context.get('device_info', {}),
                'settings': self.context.get('user_settings', {})
            }
        )
        
        scan_results = {
            'safe_content': validated_data['content'],
            'disarmed_links': [],
            'quarantined_files': [],
            'threats_found': 0,
            'actions_taken': []
        }
        
        # Scan content for threats
        analysis = analyze_security_threat(
            message_content=validated_data['content'],
            sender_info=validated_data.get('sender_info'),
            context=validated_data['content_type']
        )
        
        # Handle threats found in content
        if analysis.is_malicious:
            session.record_threat_blocked()
            scan_results['threats_found'] += 1
            scan_results['actions_taken'].append(f"Content threat detected: {analysis.threat_level}")
        
        # Scan for and disarm malicious links
        import re
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\KATEX_INLINE_OPEN\KATEX_INLINE_CLOSE,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, validated_data['content'])
        
        safe_content = validated_data['content']
        for url in urls:
            # Analyze each URL
            url_analysis = analyze_security_threat(url=url, context=validated_data['content_type'])
            
            if url_analysis.is_malicious:
                # Create disarmed link
                disarm_serializer = LinkDisarmSerializer(
                    data={
                        'url': url,
                        'disarm_method': 'BLOCK',
                        'context': validated_data['content_type'],
                        'source_content': validated_data['content']
                    },
                    context=self.context
                )
                
                if disarm_serializer.is_valid():
                    disarmed_link = disarm_serializer.save()
                    
                    # Replace in content
                    safe_content = safe_content.replace(url, disarmed_link.safe_replacement)
                    
                    scan_results['disarmed_links'].append({
                        'original_url': url,
                        'safe_replacement': disarmed_link.safe_replacement,
                        'threat_level': url_analysis.threat_level
                    })
                    
                    session.links_disarmed += 1
                    session.save()
        
        # Handle file attachments
        for attachment in validated_data.get('attachments', []):
            quarantine_serializer = FileQuarantineSerializer(
                data={
                    'file': attachment,
                    'context': f"{validated_data['content_type']}_attachment"
                },
                context=self.context
            )
            
            if quarantine_serializer.is_valid():
                quarantined_file = quarantine_serializer.save()
                
                scan_results['quarantined_files'].append({
                    'filename': quarantined_file.original_filename,
                    'threat_level': quarantined_file.threat_detection.threat_level,
                    'quarantine_id': str(quarantined_file.id)
                })
                
                session.files_quarantined += 1
                session.save()
        
        scan_results['safe_content'] = safe_content
        scan_results['session_id'] = str(session.id)
        
        return scan_results


class DisarmedLinkSerializer(serializers.ModelSerializer):
    """Serializer for DisarmedLink model"""
    threat_level = serializers.CharField(source='threat_detection.threat_level', read_only=True)
    confidence_score = serializers.FloatField(source='threat_detection.confidence_score', read_only=True)
    
    class Meta:
        model = DisarmedLink
        fields = [
            'id', 'original_url', 'safe_replacement', 'disarm_method',
            'disarm_reason', 'click_attempts', 'user_overridden',
            'disarm_timestamp', 'threat_level', 'confidence_score'
        ]
        read_only_fields = ['id', 'disarm_timestamp', 'click_attempts']


class QuarantinedFileSerializer(serializers.ModelSerializer):
    """Serializer for QuarantinedFile model"""
    threat_level = serializers.CharField(source='threat_detection.threat_level', read_only=True)
    
    class Meta:
        model = QuarantinedFile
        fields = [
            'id', 'original_filename', 'file_hash', 'file_size', 'mime_type',
            'status', 'quarantine_timestamp', 'threat_level', 'source_context'
        ]
        read_only_fields = ['id', 'quarantine_timestamp', 'file_hash']


class RealTimeSessionSerializer(serializers.ModelSerializer):
    """Serializer for RealTimeSession model"""
    duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = RealTimeSession
        fields = [
            'id', 'session_type', 'is_active', 'threats_blocked',
            'links_disarmed', 'files_quarantined', 'started_at',
            'last_activity', 'duration_minutes'
        ]
        read_only_fields = ['id', 'started_at', 'last_activity']
    
    def get_duration_minutes(self, obj):
        if obj.ended_at:
            duration = obj.ended_at - obj.started_at
        else:
            duration = timezone.now() - obj.started_at
        return int(duration.total_seconds() / 60)


class ProtectionRuleSerializer(serializers.ModelSerializer):
    """Serializer for ProtectionRule model"""
    
    class Meta:
        model = ProtectionRule
        fields = [
            'id', 'name', 'rule_type', 'pattern', 'action',
            'is_active', 'priority', 'times_triggered',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'times_triggered', 'created_at', 'updated_at']


class ProtectionLogSerializer(serializers.ModelSerializer):
    """Serializer for ProtectionLog model"""
    
    class Meta:
        model = ProtectionLog
        fields = [
            'id', 'action_type', 'description', 'source_data',
            'result_data', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']
        

class ProtectionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectionRule
        fields = ['id', 'name', 'rule_type', 'pattern', 'action', 'is_active',
                 'priority', 'created_at', 'updated_at', 'match_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'match_count']

class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        fields = ['email_alerts', 'push_notifications', 'sms_alerts', 
                 'alert_frequency', 'threat_level_threshold', 'notification_channels',
                 'quiet_hours_start', 'quiet_hours_end']
        