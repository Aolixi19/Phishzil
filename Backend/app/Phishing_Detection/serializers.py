# serializers.py
from rest_framework import serializers
from .models import ThreatDetectionResult, ThreatDatabase, Alert, SafeBrowsingWarning, ThreatDatabase, ThreatFeed, UserReport,AlertNotification
from .utils import analyze_security_threat
import hashlib
import time
from django.utils import timezone
import requests
import json

class URLDetectionSerializer(serializers.Serializer):
    """Serializer for URL phishing detection"""
    url = serializers.URLField(required=True)
    context = serializers.ChoiceField(
        choices=['email', 'sms', 'chat', 'web', 'browser'],
        required=False,
        default='web'
    )
    message_content = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Optional message content containing the URL"
    )
    sender_email = serializers.EmailField(required=False, allow_blank=True)
    sender_domain = serializers.CharField(required=False, allow_blank=True)
    user_agent = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        start_time = time.time()
        
        # Prepare sender info if provided
        sender_info = {}
        if validated_data.get('sender_email'):
            sender_info['email'] = validated_data['sender_email']
            sender_info['domain'] = validated_data['sender_email'].split('@')[1]
        if validated_data.get('sender_domain'):
            sender_info['domain'] = validated_data['sender_domain']
        
        # Run comprehensive analysis
        analysis = analyze_security_threat(
            url=validated_data['url'],
            message_content=validated_data.get('message_content'),
            sender_info=sender_info if sender_info else None,
            context=validated_data.get('context', 'web')
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Save result to database
        result = ThreatDetectionResult.objects.create(
            detection_type='URL',
            analyzed_url=validated_data['url'],
            analyzed_text=validated_data.get('message_content'),
            is_malicious=analysis.is_malicious,
            threat_level=analysis.threat_level,
            confidence_score=analysis.confidence_score,
            threat_types=analysis.threat_types,
            indicators=analysis.indicators,
            recommended_action=analysis.recommended_action,
            analysis_details=analysis.details,
            processing_time_ms=processing_time,
            context=validated_data.get('context'),
            user_agent=validated_data.get('user_agent'),
            user=self.context['request'].user if self.context['request'].user.is_authenticated else None
        )
        
        return result


class TextDetectionSerializer(serializers.Serializer):
    """Serializer for text/message phishing detection"""
    text_content = serializers.CharField(required=True)
    context = serializers.ChoiceField(
        choices=['email', 'sms', 'chat', 'message'],
        required=False,
        default='message'
    )
    sender_email = serializers.EmailField(required=False, allow_blank=True)
    sender_domain = serializers.CharField(required=False, allow_blank=True)
    sender_display_name = serializers.CharField(required=False, allow_blank=True)
    subject = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        start_time = time.time()
        
        # Prepare sender info
        sender_info = {}
        if validated_data.get('sender_email'):
            sender_info['email'] = validated_data['sender_email']
            sender_info['domain'] = validated_data['sender_email'].split('@')[1]
        if validated_data.get('sender_domain'):
            sender_info['domain'] = validated_data['sender_domain']
        if validated_data.get('sender_display_name'):
            sender_info['display_name'] = validated_data['sender_display_name']
        
        # Combine subject and content for analysis
        full_content = validated_data['text_content']
        if validated_data.get('subject'):
            full_content = f"Subject: {validated_data['subject']}\n\n{full_content}"
        
        # Run comprehensive analysis
        analysis = analyze_security_threat(
            message_content=full_content,
            sender_info=sender_info if sender_info else None,
            context=validated_data.get('context', 'message')
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Save result
        result = ThreatDetectionResult.objects.create(
            detection_type='TEXT',
            analyzed_text=full_content,
            is_malicious=analysis.is_malicious,
            threat_level=analysis.threat_level,
            confidence_score=analysis.confidence_score,
            threat_types=analysis.threat_types,
            indicators=analysis.indicators,
            recommended_action=analysis.recommended_action,
            analysis_details=analysis.details,
            processing_time_ms=processing_time,
            context=validated_data.get('context'),
            user=self.context['request'].user if self.context['request'].user.is_authenticated else None
        )
        
        return result
    

class FileDetectionSerializer(serializers.Serializer):
    """Serializer for file phishing/malware detection"""
    file = serializers.FileField(required=False)
    file_name = serializers.CharField(required=False)
    file_hash = serializers.CharField(required=False, max_length=64)
    file_size = serializers.IntegerField(required=False)
    context = serializers.ChoiceField(
        choices=['email', 'download', 'upload', 'attachment'],
        required=False,
        default='attachment'
    )
    sender_email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('file') and not data.get('file_hash'):
            raise serializers.ValidationError(
                "Either 'file' or 'file_hash' must be provided"
            )
        return data

    def create(self, validated_data):
        start_time = time.time()
        
        file_content = None
        file_name = validated_data.get('file_name', 'unknown')
        file_hash = validated_data.get('file_hash')
        file_size = validated_data.get('file_size')
        
        # Handle file upload
        if validated_data.get('file'):
            uploaded_file = validated_data['file']
            file_content = uploaded_file.read()
            file_name = uploaded_file.name
            file_size = uploaded_file.size
            
            # Calculate hash if not provided
            if not file_hash:
                file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Check threat database first for known hashes
        known_threat = None
        if file_hash:
            known_threat = ThreatDatabase.objects.filter(
                threat_type='HASH',
                value=file_hash,
                is_active=True
            ).first()
        
        # Run comprehensive analysis
        if file_content:
            analysis = analyze_security_threat(
                file_content=file_content,
                context=validated_data.get('context', 'attachment')
            )
        else:
            # Hash-only analysis (limited)
            if known_threat:
                analysis = type('ThreatAssessment', (), {
                    'is_malicious': True,
                    'threat_level': known_threat.severity,
                    'confidence_score': 0.95,
                    'threat_types': ['KNOWN_MALICIOUS_HASH'],
                    'indicators': [f'Hash matches known threat: {known_threat.description}'],
                    'recommended_action': 'BLOCK_IMMEDIATELY',
                    'details': {'database_match': True}
                })()
            else:
                analysis = type('ThreatAssessment', (), {
                    'is_malicious': False,
                    'threat_level': 'LOW',
                    'confidence_score': 0.1,
                    'threat_types': [],
                    'indicators': ['Hash not found in threat database'],
                    'recommended_action': 'ALLOW_WITH_MONITORING',
                    'details': {'hash_only_analysis': True}
                })()
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Save result
        result = ThreatDetectionResult.objects.create(
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
            processing_time_ms=processing_time,
            context=validated_data.get('context'),
            user=self.context['request'].user if self.context['request'].user.is_authenticated else None
        )
        
        return result


class ThreatDetectionResultSerializer(serializers.ModelSerializer):
    """Serializer for threat detection results output"""
    
    class Meta:
        model = ThreatDetectionResult
        fields = [
            'id', 'detection_type', 'is_malicious', 'threat_level',
            'confidence_score', 'threat_types', 'indicators', 
            'recommended_action', 'analysis_details', 'processing_time_ms',
            'created_at'
        ]
        read_only_fields = fields
        
class AlertSerializer(serializers.ModelSerializer):
    """Serializer for security alerts"""
    
    class Meta:
        model = Alert
        fields = [
            'id', 'alert_type', 'severity', 'status', 'title', 'description',
            'threat_details', 'source_url', 'source_file', 'user_override',
            'override_reason', 'created_at', 'acknowledged_at', 'resolved_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'acknowledged_at', 'resolved_at'
        ]


class AlertOverrideSerializer(serializers.Serializer):
    """Serializer for user alert overrides"""
    action = serializers.ChoiceField(choices=[
        ('mark_safe', 'Mark as Safe'),
        ('mark_unsafe', 'Mark as Unsafe'),
        ('acknowledge', 'Acknowledge'),
        ('resolve', 'Resolve')
    ])
    reason = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        action = validated_data['action']
        reason = validated_data.get('reason', '')
        
        if action == 'mark_safe':
            instance.status = 'FALSE_POSITIVE'
            instance.user_override = True
            instance.override_reason = reason
            instance.override_timestamp = timezone.now()
        elif action == 'mark_unsafe':
            instance.status = 'ACTIVE'
            instance.user_override = False
        elif action == 'acknowledge':
            instance.status = 'ACKNOWLEDGED'
            instance.acknowledged_at = timezone.now()
        elif action == 'resolve':
            instance.status = 'RESOLVED'
            instance.resolved_at = timezone.now()
        
        instance.save()
        return instance
    
# serializers.py - Add these new serializers

class BulkAlertActionSerializer(serializers.Serializer):
    """Serializer for bulk alert operations"""
    alert_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        max_length=100,
        help_text="List of alert IDs to process"
    )
    action = serializers.ChoiceField(choices=[
        ('mark_read', 'Mark as Read'),
        ('mark_unread', 'Mark as Unread'),
        ('acknowledge', 'Acknowledge All'),
        ('resolve', 'Resolve All'),
        ('delete', 'Delete All'),
        ('archive', 'Archive All'),
    ])
    reason = serializers.CharField(required=False, allow_blank=True)

    def validate_alert_ids(self, value):
        # Verify all alerts belong to the requesting user
        user = self.context['request'].user
        existing_alerts = Alert.objects.filter(
            id__in=value, 
            user=user
        ).values_list('id', flat=True)
        
        if len(existing_alerts) != len(value):
            invalid_ids = set(value) - set(existing_alerts)
            raise serializers.ValidationError(
                f"Invalid alert IDs: {list(invalid_ids)}"
            )
        return value

    def create(self, validated_data):
        alert_ids = validated_data['alert_ids']
        action = validated_data['action']
        reason = validated_data.get('reason', '')
        user = self.context['request'].user
        
        alerts = Alert.objects.filter(id__in=alert_ids, user=user)
        updated_count = 0
        
        for alert in alerts:
            if action == 'mark_read':
                alert.is_read = True
            elif action == 'mark_unread':
                alert.is_read = False
            elif action == 'acknowledge':
                alert.status = 'ACKNOWLEDGED'
                alert.acknowledged_at = timezone.now()
                alert.is_read = True
            elif action == 'resolve':
                alert.status = 'RESOLVED'
                alert.resolved_at = timezone.now()
                alert.is_read = True
            elif action == 'archive':
                alert.status = 'ARCHIVED'
                alert.is_read = True
            elif action == 'delete':
                alert.delete()
                updated_count += 1
                continue
            
            if reason:
                alert.override_reason = reason
                alert.override_timestamp = timezone.now()
            
            alert.save()
            updated_count += 1
        
        return {
            'action': action,
            'processed_count': updated_count,
            'total_requested': len(alert_ids)
        }


class AlertSearchSerializer(serializers.Serializer):
    """Advanced alert search serializer"""
    search_query = serializers.CharField(required=False, allow_blank=True)
    alert_types = serializers.ListField(
        child=serializers.ChoiceField(choices=[choice[0] for choice in Alert.ALERT_TYPES]),
        required=False
    )
    severities = serializers.ListField(
        child=serializers.ChoiceField(choices=[choice[0] for choice in Alert.SEVERITY_LEVELS]),
        required=False
    )
    statuses = serializers.ListField(
        child=serializers.ChoiceField(choices=[choice[0] for choice in Alert.STATUS_CHOICES]),
        required=False
    )
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    is_read = serializers.BooleanField(required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    priority_min = serializers.IntegerField(min_value=1, max_value=5, required=False)
    priority_max = serializers.IntegerField(min_value=1, max_value=5, required=False)


class EnhancedAlertSerializer(serializers.ModelSerializer):
    """Enhanced alert serializer with new fields"""
    related_alerts_count = serializers.SerializerMethodField()
    notification_status = serializers.SerializerMethodField()
    time_since_created = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = [
            'id', 'alert_type', 'severity', 'status', 'title', 'description',
            'threat_details', 'source_url', 'source_file', 'user_override',
            'override_reason', 'created_at', 'acknowledged_at', 'resolved_at',
            # New fields
            'priority', 'tags', 'is_read', 'expires_at', 'auto_created',
            'escalation_level', 'notification_sent', 'notification_sent_at',
            'related_alerts_count', 'notification_status', 'time_since_created'
        ]
        read_only_fields = [
            'id', 'created_at', 'acknowledged_at', 'resolved_at',
            'related_alerts_count', 'notification_status', 'time_since_created'
        ]
    
    def get_related_alerts_count(self, obj):
        return obj.related_alerts.count()
    
    def get_notification_status(self, obj):
        if not obj.notification_sent:
            return 'not_sent'
        return 'sent'
    
    def get_time_since_created(self, obj):
        from django.utils.timesince import timesince
        return timesince(obj.created_at)


class AlertNotificationSerializer(serializers.ModelSerializer):
    """Serializer for alert notifications"""
    
    class Meta:
        model = AlertNotification
        fields = [
            'id', 'notification_type', 'recipient', 'status',
            'sent_at', 'delivered_at', 'read_at', 'error_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SafeBrowsingWarningSerializer(serializers.ModelSerializer):
    """Serializer for safe browsing warnings"""
    
    class Meta:
        model = SafeBrowsingWarning
        fields = [
            'id', 'original_url', 'warning_type', 'threat_details',
            'user_proceeded', 'proceed_timestamp', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'proceed_timestamp']


class ThreatDatabaseSerializer(serializers.ModelSerializer):
    """Serializer for threat database entries"""
    source_feed_name = serializers.CharField(source='source_feed.name', read_only=True)
    
    class Meta:
        model = ThreatDatabase
        fields = [
            'id', 'threat_type', 'value', 'severity', 'description',
            'source', 'source_feed_name', 'tags', 'first_seen', 'last_seen',
            'confidence_score', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ThreatFeedSerializer(serializers.ModelSerializer):
    """Serializer for threat feeds"""
    
    class Meta:
        model = ThreatFeed
        fields = [
            'id', 'name', 'feed_type', 'url', 'is_active',
            'last_updated', 'update_frequency', 'total_threats',
            'new_threats_count', 'created_at'
        ]
        read_only_fields = [
            'id', 'last_updated', 'total_threats', 'new_threats_count', 'created_at'
        ]


class ThreatImportSerializer(serializers.Serializer):
    """Serializer for importing threat feeds"""
    feed_id = serializers.UUIDField(required=True)
    force_update = serializers.BooleanField(default=False)
    
    def validate_feed_id(self, value):
        try:
            feed = ThreatFeed.objects.get(id=value, is_active=True)
            return value
        except ThreatFeed.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive threat feed")
    
    def create(self, validated_data):
        feed = ThreatFeed.objects.get(id=validated_data['feed_id'])
        force_update = validated_data.get('force_update', False)
        
        # Import threats from feed
        import_result = self._import_from_feed(feed, force_update)
        
        return {
            'feed': feed,
            'import_result': import_result
        }
    
    def _import_from_feed(self, feed, force_update=False):
        """Import threats from external feed"""
        try:
            if feed.feed_type == 'PHISHTANK':
                return self._import_phishtank(feed, force_update)
            elif feed.feed_type == 'OPENPHISH':
                return self._import_openphish(feed, force_update)
            else:
                return {'error': f'Unsupported feed type: {feed.feed_type}'}
        except Exception as e:
            return {'error': str(e)}
    
    def _import_phishtank(self, feed, force_update):
        """Import from PhishTank API"""
        headers = {}
        if feed.api_key:
            headers['User-Agent'] = f'phishtank-api/{feed.api_key}'
        
        response = requests.get(feed.url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        imported_count = 0
        updated_count = 0
        
        for entry in data:
            if entry.get('verified') == 'yes':
                url = entry.get('url')
                phish_id = entry.get('phish_id')
                
                threat, created = ThreatDatabase.objects.get_or_create(
                    threat_type='URL',
                    value=url,
                    defaults={
                        'severity': 'HIGH',
                        'description': f'PhishTank verified phishing URL',
                        'source_feed': feed,
                        'source': 'PhishTank',
                        'external_id': str(phish_id),
                        'confidence_score': 0.9,
                        'first_seen': timezone.now(),
                    }
                )
                
                if created:
                    imported_count += 1
                elif force_update:
                    threat.last_seen = timezone.now()
                    threat.save()
                    updated_count += 1
        
        # Update feed statistics
        feed.last_updated = timezone.now()
        feed.new_threats_count = imported_count
        feed.total_threats = ThreatDatabase.objects.filter(source_feed=feed).count()
        feed.save()
        
        return {
            'imported': imported_count,
            'updated': updated_count,
            'total': feed.total_threats
        }
    
    def _import_openphish(self, feed, force_update):
        """Import from OpenPhish feed"""
        response = requests.get(feed.url, timeout=30)
        response.raise_for_status()
        
        urls = response.text.strip().split('\n')
        imported_count = 0
        
        for url in urls:
            if url.strip():
                threat, created = ThreatDatabase.objects.get_or_create(
                    threat_type='URL',
                    value=url.strip(),
                    defaults={
                        'severity': 'HIGH',
                        'description': 'OpenPhish detected phishing URL',
                        'source_feed': feed,
                        'source': 'OpenPhish',
                        'confidence_score': 0.85,
                        'first_seen': timezone.now(),
                    }
                )
                
                if created:
                    imported_count += 1
        
        # Update feed statistics
        feed.last_updated = timezone.now()
        feed.new_threats_count = imported_count
        feed.total_threats = ThreatDatabase.objects.filter(source_feed=feed).count()
        feed.save()
        
        return {
            'imported': imported_count,
            'total': feed.total_threats
        }


class UserReportSerializer(serializers.ModelSerializer):
    """Serializer for user threat reports"""
    
    class Meta:
        model = UserReport
        fields = [
            'id', 'report_type', 'status', 'suspicious_url', 'suspicious_email',
            'file_name', 'file_hash', 'content_description', 'source_context',
            'threat_indicators', 'screenshots', 'automated_analysis',
            'manual_review_notes', 'created_at', 'reviewed_at', 'resolved_at'
        ]
        read_only_fields = [
            'id', 'status', 'automated_analysis', 'manual_review_notes',
            'created_at', 'reviewed_at', 'resolved_at'
        ]
    
    def create(self, validated_data):
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        
        # Run automated analysis if URL provided
        if validated_data.get('suspicious_url'):
            from .utils import analyze_security_threat
            analysis = analyze_security_threat(url=validated_data['suspicious_url'])
            validated_data['automated_analysis'] = {
                'is_malicious': analysis.is_malicious,
                'threat_level': analysis.threat_level,
                'confidence_score': analysis.confidence_score,
                'threat_types': analysis.threat_types,
                'indicators': analysis.indicators
            }
        
        return super().create(validated_data)


class UserReportDetailSerializer(UserReportSerializer):
    """Detailed serializer for user reports with additional fields"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta(UserReportSerializer.Meta):
        fields = UserReportSerializer.Meta.fields + ['user_email']