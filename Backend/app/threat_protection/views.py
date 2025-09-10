from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncDate

from .models import (
    DisarmedLink, NotificationPreferences, QuarantinedFile, RealTimeSession,
    ProtectionRule, ProtectionLog
)
from .serializers import (
    LinkDisarmSerializer, FileQuarantineSerializer, NotificationPreferencesSerializer, RealTimeScanSerializer,
    DisarmedLinkSerializer, QuarantinedFileSerializer, RealTimeSessionSerializer,
    ProtectionRuleSerializer, ProtectionLogSerializer
)
import time


# ========== LINK DISARMING ==========

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def disarm_malicious_link(request):
    """
    Disarm a malicious link by replacing it with safe text.
    
    POST /api/protection/disarm-link
    {
        "url": "http://malicious-site.com",
        "disarm_method": "BLOCK",
        "context": "email"
    }
    """
    try:
        serializer = LinkDisarmSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            disarmed_link = serializer.save()
            
            response_data = DisarmedLinkSerializer(disarmed_link).data
            response_data['message'] = f"Link successfully disarmed using {disarmed_link.disarm_method} method"
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': f'Failed to disarm link: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_disarmed_links(request):
    """
    List all disarmed links for the user.
    
    GET /api/protection/disarmed-links?limit=20&method=BLOCK
    """
    try:
        queryset = DisarmedLink.objects.filter(user=request.user)
        
        # Apply filters
        disarm_method = request.query_params.get('method')
        if disarm_method:
            queryset = queryset.filter(disarm_method=disarm_method)
        
        date_from = request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(disarm_timestamp__gte=date_from)
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        total_count = queryset.count()
        links = queryset[offset:offset + limit]
        
        serializer = DisarmedLinkSerializer(links, many=True)
        
        return Response({
            'count': total_count,
            'results': serializer.data,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'has_next': offset + limit < total_count
            }
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve disarmed links: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def override_disarmed_link(request, link_id):
    """
    Allow user to override a disarmed link (mark as safe).
    
    POST /api/protection/disarmed-links/{id}/override
    {
        "reason": "This is a legitimate business link"
    }
    """
    try:
        disarmed_link = get_object_or_404(
            DisarmedLink, 
            id=link_id, 
            user=request.user
        )
        
        reason = request.data.get('reason', 'User override')
        
        disarmed_link.user_overridden = True
        disarmed_link.override_reason = reason
        disarmed_link.save()
        
        # Log the override
        ProtectionLog.objects.create(
            user=request.user,
            action_type='USER_OVERRIDE',
            description=f"User overrode disarmed link: {disarmed_link.original_url}",
            disarmed_link=disarmed_link,
            result_data={'reason': reason}
        )
        
        return Response({
            'message': 'Link override recorded successfully',
            'original_url': disarmed_link.original_url,
            'reason': reason
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to override link: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== FILE QUARANTINE ==========

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def quarantine_file(request):
    """
    Quarantine a suspicious file.
    
    POST /api/protection/quarantine-file
    Content-Type: multipart/form-data
    {
        "file": <file_upload>,
        "context": "email_attachment"
    }
    """
    try:
        serializer = FileQuarantineSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            quarantined_file = serializer.save()
            
            response_data = QuarantinedFileSerializer(quarantined_file).data
            response_data['message'] = f"File '{quarantined_file.original_filename}' quarantined successfully"
            response_data['safe_preview_available'] = bool(quarantined_file.safe_preview_location)
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': f'Failed to quarantine file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_quarantined_files(request):
    """
    List all quarantined files for the user.
    
    GET /api/protection/quarantined-files?status=QUARANTINED
    """
    try:
        queryset = QuarantinedFile.objects.filter(user=request.user)
        
        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        source_context = request.query_params.get('source')
        if source_context:
            queryset = queryset.filter(source_context=source_context)
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        total_count = queryset.count()
        files = queryset[offset:offset + limit]
        
        serializer = QuarantinedFileSerializer(files, many=True)
        
        return Response({
            'count': total_count,
            'results': serializer.data,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'has_next': offset + limit < total_count
            }
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve quarantined files: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_safe_file_preview(request, file_id):
    """
    Get safe preview of quarantined file.
    
    GET /api/protection/quarantined-files/{id}/preview
    """
    try:
        quarantined_file = get_object_or_404(
            QuarantinedFile,
            id=file_id,
            user=request.user
        )
        
        if not quarantined_file.safe_preview_location:
            quarantined_file.create_safe_preview()
        
        preview_info = {
            'file_id': str(quarantined_file.id),
            'original_filename': quarantined_file.original_filename,
            'file_size': quarantined_file.file_size,
            'mime_type': quarantined_file.mime_type,
            'threat_level': quarantined_file.threat_detection.threat_level,
            'quarantine_date': quarantined_file.quarantine_timestamp,
            'preview_content': f"[SAFE PREVIEW]\nThis file has been quarantined due to potential threats.\nFilename: {quarantined_file.original_filename}\nSize: {quarantined_file.file_size} bytes\nThreat Level: {quarantined_file.threat_detection.threat_level}",
            'warning': "This is a safe preview. The original file remains quarantined."
        }
        
        return Response(preview_info)
    
    except Exception as e:
        return Response(
            {'error': f'Failed to get file preview: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== REAL-TIME SCANNING ==========

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def real_time_scan(request):
    """
    Perform real-time scanning of content (email, SMS, etc.).
    
    POST /api/protection/real-time-scan
    {
        "content_type": "email",
        "content": "Check out this link: http://suspicious-site.com",
        "sender_info": {"email": "sender@example.com"},
        "attachments": [<file1>, <file2>]
    }
    """
    try:
        start_time = time.time()
        
        serializer = RealTimeScanSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            scan_results = serializer.save()
            
            processing_time = int((time.time() - start_time) * 1000)
            scan_results['processing_time_ms'] = processing_time
            scan_results['scan_timestamp'] = timezone.now().isoformat()
            
            return Response(scan_results, status=status.HTTP_200_OK)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': f'Failed to perform real-time scan: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protection_sessions(request):
    """
    Get user's protection sessions.
    
    GET /api/protection/sessions?active_only=true
    """
    try:
        queryset = RealTimeSession.objects.filter(user=request.user)
        
        active_only = request.query_params.get('active_only', 'false').lower() == 'true'
        if active_only:
            queryset = queryset.filter(is_active=True)
        
        session_type = request.query_params.get('type')
        if session_type:
            queryset = queryset.filter(session_type=session_type.upper())
        
        sessions = queryset[:20]  # Limit to recent 20
        serializer = RealTimeSessionSerializer(sessions, many=True)
        
        return Response({
            'sessions': serializer.data,
            'total_active': queryset.filter(is_active=True).count()
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve sessions: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def end_protection_session(request, session_id):
    """
    End a protection session.
    
    POST /api/protection/sessions/{id}/end
    """
    try:
        session = get_object_or_404(
            RealTimeSession,
            id=session_id,
            user=request.user,
            is_active=True
        )
        
        session.end_session()
        
        return Response({
            'message': 'Protection session ended successfully',
            'session_id': str(session.id),
            'duration_minutes': int((session.ended_at - session.started_at).total_seconds() / 60),
            'threats_blocked': session.threats_blocked
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to end session: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== PROTECTION ANALYTICS ==========

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protection_analytics(request):
    """
    Get protection analytics and statistics.
    
    GET /api/protection/analytics?period=7d
    """
    try:
        period = request.query_params.get('period', '7d')  # 1d, 7d, 30d
        
        period_map = {'1d': 1, '7d': 7, '30d': 30}
        days = period_map.get(period, 7)
        start_date = timezone.now() - timezone.timedelta(days=days)
        
        # Basic statistics
        user_links = DisarmedLink.objects.filter(
            user=request.user,
            disarm_timestamp__gte=start_date
        )
        
        user_files = QuarantinedFile.objects.filter(
            user=request.user,
            quarantine_timestamp__gte=start_date
        )
        
        user_sessions = RealTimeSession.objects.filter(
            user=request.user,
            started_at__gte=start_date
        )
        
        # Daily trends
        daily_links = user_links.annotate(
            date=TruncDate('disarm_timestamp')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        daily_files = user_files.annotate(
            date=TruncDate('quarantine_timestamp')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Method breakdown
        method_breakdown = user_links.values('disarm_method').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Session statistics
        session_stats = user_sessions.aggregate(
            total_threats_blocked=Sum('threats_blocked'),
            total_links_disarmed=Sum('links_disarmed'),
            total_files_quarantined=Sum('files_quarantined')
        )
        
        analytics = {
            'period': period,
            'summary': {
                'total_links_disarmed': user_links.count(),
                'total_files_quarantined': user_files.count(),
                'active_sessions': user_sessions.filter(is_active=True).count(),
                'total_threats_blocked': session_stats['total_threats_blocked'] or 0,
                'protection_efficiency': 95.5  # Calculate based on threats vs successful blocks
            },
            'trends': {
                'daily_links_disarmed': list(daily_links),
                'daily_files_quarantined': list(daily_files),
                'disarm_methods': list(method_breakdown)
            },
            'recent_activity': {
                'recent_disarmed_links': DisarmedLinkSerializer(
                    user_links[:5], many=True
                ).data,
                'recent_quarantined_files': QuarantinedFileSerializer(
                    user_files[:5], many=True
                ).data
            }
        }
        
        return Response(analytics)
    
    except Exception as e:
        return Response(
            {'error': f'Failed to generate analytics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== PROTECTION LOGS ==========

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protection_logs(request):
    """
    Get detailed protection logs.
    
    GET /api/protection/logs?action_type=LINK_DISARMED&limit=50
    """
    try:
        queryset = ProtectionLog.objects.filter(user=request.user)
        
        # Apply filters
        action_type = request.query_params.get('action_type')
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        date_from = request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(timestamp__gte=date_from)
        
        # Pagination
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))
        
        total_count = queryset.count()
        logs = queryset[offset:offset + limit]
        
        serializer = ProtectionLogSerializer(logs, many=True)
        
        return Response({
            'count': total_count,
            'results': serializer.data,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'has_next': offset + limit < total_count
            }
        })
    
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve protection logs: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
# Add to protection/views.py

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def protection_rules(request):
    """
    Manage custom protection rules
    
    GET /api/protection/rules
    POST /api/protection/rules
    """
    if request.method == 'GET':
        try:
            rules = ProtectionRule.objects.filter(user=request.user)
            
            # Apply filters
            rule_type = request.query_params.get('rule_type')
            if rule_type:
                rules = rules.filter(rule_type=rule_type)
            
            is_active = request.query_params.get('is_active')
            if is_active is not None:
                rules = rules.filter(is_active=is_active.lower() == 'true')
            
            serializer = ProtectionRuleSerializer(rules, many=True)
            
            return Response({
                'rules': serializer.data,
                'total_count': rules.count()
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve rules: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        try:
            serializer = ProtectionRuleSerializer(data=request.data)
            if serializer.is_valid():
                rule = serializer.save(user=request.user)
                
                return Response(
                    ProtectionRuleSerializer(rule).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Failed to create rule: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def protection_rule_detail(request, rule_id):
    """
    Get, update, or delete a protection rule
    
    GET /api/protection/rules/{id}
    PUT /api/protection/rules/{id}
    DELETE /api/protection/rules/{id}
    """
    try:
        rule = get_object_or_404(ProtectionRule, id=rule_id, user=request.user)
        
        if request.method == 'GET':
            serializer = ProtectionRuleSerializer(rule)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = ProtectionRuleSerializer(rule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        elif request.method == 'DELETE':
            rule.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
    except Exception as e:
        return Response(
            {'error': f'Failed to process rule: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def test_protection_rule(request):
    """
    Test a protection rule against sample content
    
    POST /api/protection/rules/test
    {
        "rule_id": "uuid",
        "test_content": "http://test-url.com"
    }
    """
    try:
        rule_id = request.data.get('rule_id')
        test_content = request.data.get('test_content')
        
        rule = get_object_or_404(ProtectionRule, id=rule_id, user=request.user)
        
        # Test the rule against content
        import re
        
        if rule.rule_type == 'URL_PATTERN':
            match = re.search(rule.pattern, test_content)
        elif rule.rule_type == 'DOMAIN':
            from urllib.parse import urlparse
            domain = urlparse(test_content).netloc
            match = rule.pattern.lower() in domain.lower()
        elif rule.rule_type == 'KEYWORD':
            match = rule.pattern.lower() in test_content.lower()
        else:
            match = False
        
        return Response({
            'rule_name': rule.name,
            'test_content': test_content,
            'matches': bool(match),
            'action_would_be': rule.action if match else 'NO_ACTION',
            'rule_active': rule.is_active
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to test rule: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def notification_preferences(request):
    """
    Get or update notification preferences
    
    GET /api/protection/notifications/preferences
    POST /api/protection/notifications/preferences
    """
    try:
        preferences, created = NotificationPreferences.objects.get_or_create(
            user=request.user
        )
        
        if request.method == 'GET':
            serializer = NotificationPreferencesSerializer(preferences)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = NotificationPreferencesSerializer(
                preferences,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
    except Exception as e:
        return Response(
            {'error': f'Failed to manage preferences: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )