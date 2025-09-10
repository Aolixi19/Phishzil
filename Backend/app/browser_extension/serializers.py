from rest_framework import serializers
from .models import BrowserSession, BlockedSite, BrowserSettings
from ..Phishing_Detection.models import ThreatDetectionResult

class BrowserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrowserSession
        fields = ['id', 'browser_type', 'extension_version', 'is_active', 
                 'started_at', 'urls_checked', 'threats_blocked']
        read_only_fields = ['id', 'started_at', 'urls_checked', 'threats_blocked']

class BlockedSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedSite
        fields = ['id', 'url', 'domain', 'threat_type', 'confidence_score',
                 'blocked_at', 'user_overridden', 'override_reason', 'page_context']
        read_only_fields = ['id', 'blocked_at']

class BrowserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrowserSettings
        fields = ['protection_level', 'block_suspicious_downloads', 'warn_on_phishing_sites',
                 'auto_quarantine_files', 'show_domain_warnings', 'enable_safe_browsing',
                 'whitelist_domains', 'blacklist_domains', 'updated_at']
        read_only_fields = ['updated_at']

class URLCheckSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2000)
    page_context = serializers.CharField(max_length=100, default='navigation')
    referrer = serializers.URLField(required=False, allow_blank=True)
    user_agent = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        from ..Phishing_Detection.utils import analyze_security_threat
        
        url = validated_data['url']
        context = validated_data['page_context']
        user = self.context['request'].user
        
        # Quick threat analysis for browser
        analyzer = analyze_security_threat()
        result = analyzer.quick_check(url, context)
        
        # Create detection result
        detection_result = ThreatDetectionResult.objects.create(
            user=user,
            detection_type='URL',
            analyzed_url=url,
            is_malicious=result['is_malicious'],
            confidence_score=result['confidence'],
            threat_level=result['threat_level'],
            threat_types=result['threat_types'],
            indicators=result['indicators']
        )
        
        # If malicious, create blocked site record
        if result['is_malicious'] and result['confidence'] > 0.7:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            
            BlockedSite.objects.create(
                user=user,
                url=url,
                domain=domain,
                threat_type=result['threat_types'][0] if result['threat_types'] else 'SUSPICIOUS',
                confidence_score=result['confidence'],
                page_context=context
            )
        
        return {
            'url': url,
            'is_safe': not result['is_malicious'],
            'confidence': result['confidence'],
            'threat_types': result['threat_types'],
            'action': 'BLOCK' if result['is_malicious'] and result['confidence'] > 0.8 else 'WARN',
            'detection_result_id': str(detection_result.id)
        }

class BrowserOverrideSerializer(serializers.Serializer):
    blocked_site_id = serializers.UUIDField()
    reason = serializers.CharField(max_length=500)

    def create(self, validated_data):
        user = self.context['request'].user
        blocked_site = BlockedSite.objects.get(
            id=validated_data['blocked_site_id'],
            user=user
        )
        
        blocked_site.user_overridden = True
        blocked_site.override_reason = validated_data['reason']
        blocked_site.save()
        
        return blocked_site