from rest_framework import status,viewsets, permissions
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import (
    EnhancedAlertSerializer,
    URLDetectionSerializer, 
    TextDetectionSerializer, 
    FileDetectionSerializer,
    ThreatDetectionResultSerializer,AlertSerializer, AlertOverrideSerializer, SafeBrowsingWarningSerializer,
    ThreatDatabaseSerializer, ThreatFeedSerializer, ThreatImportSerializer,
    UserReportSerializer, UserReportDetailSerializer,ThreatDetectionResult,AlertSearchSerializer,BulkAlertActionSerializer,AlertNotification
)
from .models import DetectionLog,Alert, SafeBrowsingWarning, ThreatDatabase, ThreatFeed, UserReport
import hashlib
import time
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_url(request):
    """
    Analyze URL for phishing and malicious content.
    
    POST /api/detect/url
    {
        "url": "https://example.com/suspicious-link",
        "context": "email",
        "message_content": "Click here to verify your account",
        "sender_email": "noreply@suspicious-domain.com"
    }
    """
    start_time = time.time()
    
    try:
        serializer = URLDetectionSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            result = serializer.save()
            response_time = int((time.time() - start_time) * 1000)
            
            # Log the detection attempt
            DetectionLog.objects.create(
                detection_result=result,
                endpoint='detect_url',
                request_data_hash=hashlib.sha256(
                    str(request.data).encode()
                ).hexdigest(),
                response_time_ms=response_time
            )
            
            response_data = ThreatDetectionResultSerializer(result).data
            response_data['response_time_ms'] = response_time
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'errors': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        response_time = int((time.time() - start_time) * 1000)
        
        return Response(
            {
                'error': 'Internal server error during URL analysis',
                'message': str(e),
                'response_time_ms': response_time
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_text(request):
    """
    Analyze text/message content for phishing and social engineering.
    
    POST /api/detect/text
    {
        "text_content": "URGENT: Your account has been suspended...",
        "context": "email",
        "sender_email": "security@fake-bank.com",
        "subject": "Account Security Alert"
    }
    """
    start_time = time.time()
    
    try:
        serializer = TextDetectionSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            result = serializer.save()
            response_time = int((time.time() - start_time) * 1000)
            
            # Log the detection attempt
            DetectionLog.objects.create(
                detection_result=result,
                endpoint='detect_text',
                request_data_hash=hashlib.sha256(
                    str(request.data).encode()
                ).hexdigest(),
                response_time_ms=response_time
            )
            
            response_data = ThreatDetectionResultSerializer(result).data
            response_data['response_time_ms'] = response_time
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        response_time = int((time.time() - start_time) * 1000)
        
        return Response(
            {
                'error': 'Internal server error during text analysis',
                'message': str(e),
                'response_time_ms': response_time
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_file(request):
    """
    Analyze file for malicious content.
    
    POST /api/detect/file
    Content-Type: multipart/form-data
    {
        "file": <file_upload>,
        "context": "email"
    }
    
    OR
    
    {
        "file_hash": "sha256_hash_value",
        "file_name": "suspicious.exe",
        "file_size": 1024000
    }
    """
    start_time = time.time()
    
    try:
        serializer = FileDetectionSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            result = serializer.save()
            response_time = int((time.time() - start_time) * 1000)
            
            # Log the detection attempt
            request_hash = hashlib.sha256(
                (str(request.data.get('file_name', '')) + 
                 str(request.data.get('file_hash', ''))).encode()
            ).hexdigest()
            
            DetectionLog.objects.create(
                detection_result=result,
                endpoint='detect_file',
                request_data_hash=request_hash,
                response_time_ms=response_time
            )
            
            response_data = ThreatDetectionResultSerializer(result).data
            response_data['response_time_ms'] = response_time
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        response_time = int((time.time() - start_time) * 1000)
        
        return Response(
            {
                'error': 'Internal server error during file analysis', 
                'message': str(e),
                'response_time_ms': response_time
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

from django.views.decorators.cache import cache_page

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@cache_page(60 * 5)  # ✅ Correct for FBV
def detection_stats(request):
    """
    Get detection statistics for the authenticated user.
    
    GET /api/detect/stats
    """
    from django.db.models import Count, Avg
    from .models import ThreatDetectionResult
    
    user_results = ThreatDetectionResult.objects.filter(user=request.user)
    
    stats = {
        'total_detections': user_results.count(),
        'malicious_detections': user_results.filter(is_malicious=True).count(),
        'detection_breakdown': user_results.values('detection_type').annotate(
            count=Count('id')
        ),
        'threat_level_breakdown': user_results.values('threat_level').annotate(
            count=Count('id')
        ),
        'average_confidence': user_results.aggregate(
            avg_confidence=Avg('confidence_score')
        )['avg_confidence'],
        'recent_threats': ThreatDetectionResultSerializer(
            user_results.filter(is_malicious=True)[:5], many=True
        ).data
    }
    
    return Response(stats)

# ========== ALERTS & SAFE BROWSING ==========

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_alerts(request):
    """
    Get all security alerts for the logged-in user.
    
    GET /api/alerts?status=ACTIVE&severity=HIGH&limit=50
    """
    try:
        # Filter alerts by user
        alerts = Alert.objects.filter(user=request.user)
        
        # Apply filters
        status_filter = request.GET.get('status')
        if status_filter:
            alerts = alerts.filter(status=status_filter)
        
        severity_filter = request.GET.get('severity')
        if severity_filter:
            alerts = alerts.filter(severity=severity_filter)
        
        alert_type_filter = request.GET.get('alert_type')
        if alert_type_filter:
            alerts = alerts.filter(alert_type=alert_type_filter)
        
        # Pagination
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        
        total_count = alerts.count()
        alerts = alerts[offset:offset + limit]
        
        serializer = AlertSerializer(alerts, many=True)
        
        # Get summary statistics
        summary = Alert.objects.filter(user=request.user).aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='ACTIVE')),
            critical=Count('id', filter=Q(severity='CRITICAL')),
            high=Count('id', filter=Q(severity='HIGH'))
        )
        
        return Response({
            'alerts': serializer.data,
            'total_count': total_count,
            'summary': summary,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'has_next': offset + limit < total_count
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve alerts: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# views.py - Add these new enhanced alert management functions

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_alert_actions(request):
    """
    Perform bulk operations on multiple alerts.
    
    POST /api/detect/alerts/bulk
    {
        "alert_ids": ["uuid1", "uuid2", "uuid3"],
        "action": "mark_read",
        "reason": "Reviewed all alerts"
    }
    """
    try:
        serializer = BulkAlertActionSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            result = serializer.save()
            
            return Response({
                'success': True,
                'message': f"Successfully {result['action']} {result['processed_count']} alerts",
                'processed_count': result['processed_count'],
                'total_requested': result['total_requested']
            })
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to process bulk action: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_alerts(request):
    """
    Advanced alert search with multiple filters.
    
    POST /api/detect/alerts/search
    {
        "search_query": "phishing",
        "alert_types": ["PHISHING_URL"],
        "severities": ["HIGH", "CRITICAL"],
        "date_from": "2025-08-01T00:00:00Z",
        "is_read": false
    }
    """
    try:
        search_serializer = AlertSearchSerializer(data=request.data)
        
        if not search_serializer.is_valid():
            return Response(
                {'errors': search_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Start with user's alerts
        queryset = Alert.objects.filter(user=request.user)
        
        # Apply search filters
        search_data = search_serializer.validated_data
        
        if search_data.get('search_query'):
            query = search_data['search_query']
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(threat_details__icontains=query)
            )
        
        if search_data.get('alert_types'):
            queryset = queryset.filter(alert_type__in=search_data['alert_types'])
        
        if search_data.get('severities'):
            queryset = queryset.filter(severity__in=search_data['severities'])
        
        if search_data.get('statuses'):
            queryset = queryset.filter(status__in=search_data['statuses'])
        
        if search_data.get('date_from'):
            queryset = queryset.filter(created_at__gte=search_data['date_from'])
        
        if search_data.get('date_to'):
            queryset = queryset.filter(created_at__lte=search_data['date_to'])
        
        if search_data.get('is_read') is not None:
            queryset = queryset.filter(is_read=search_data['is_read'])
        
        if search_data.get('tags'):
            for tag in search_data['tags']:
                queryset = queryset.filter(tags__icontains=tag)
        
        if search_data.get('priority_min'):
            queryset = queryset.filter(priority__gte=search_data['priority_min'])
        
        if search_data.get('priority_max'):
            queryset = queryset.filter(priority__lte=search_data['priority_max'])
        
        # Pagination
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        
        total_count = queryset.count()
        alerts = queryset[offset:offset + limit]
        
        serializer = EnhancedAlertSerializer(alerts, many=True)
        
        return Response({
            'alerts': serializer.data,
            'total_count': total_count,
            'search_summary': {
                'total_found': total_count,
                'search_filters_applied': len([k for k, v in search_data.items() if v]),
                'query': search_data.get('search_query', 'None')
            },
            'pagination': {
                'limit': limit,
                'offset': offset,
                'has_next': offset + limit < total_count
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to search alerts: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_alert_from_detection(request):
    """
    Automatically create alert from threat detection result.
    
    POST /api/detect/alerts/auto-create
    {
        "detection_result_id": "uuid",
        "force_create": false
    }
    """
    try:
        detection_result_id = request.data.get('detection_result_id')
        force_create = request.data.get('force_create', False)
        
        if not detection_result_id:
            return Response(
                {'error': 'detection_result_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the detection result
        try:
            detection_result = ThreatDetectionResult.objects.get(
                id=detection_result_id,
                user=request.user
            )
        except ThreatDetectionResult.DoesNotExist:
            return Response(
                {'error': 'Detection result not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if alert already exists
        existing_alert = Alert.objects.filter(
            detection_result=detection_result
        ).first()
        
        if existing_alert and not force_create:
            return Response({
                'message': 'Alert already exists for this detection',
                'alert': EnhancedAlertSerializer(existing_alert).data
            })
        
        # Create alert based on threat level
        if detection_result.is_malicious and detection_result.confidence_score >= 0.7:
            # Determine alert type
            alert_type = 'PHISHING_URL'
            if detection_result.detection_type == 'FILE':
                alert_type = 'MALICIOUS_FILE'
            elif detection_result.detection_type == 'TEXT':
                alert_type = 'SUSPICIOUS_EMAIL'
            
            # Determine priority based on severity
            priority_map = {
                'CRITICAL': 1,
                'HIGH': 2,
                'MEDIUM': 3,
                'LOW': 4
            }
            
            alert = Alert.objects.create(
                user=request.user,
                detection_result=detection_result,
                alert_type=alert_type,
                severity=detection_result.threat_level,
                priority=priority_map.get(detection_result.threat_level, 3),
                status='ACTIVE',
                title=f"{detection_result.threat_level} Threat Detected",
                description=f"Detected {', '.join(detection_result.threat_types)} with {detection_result.confidence_score:.0%} confidence",
                threat_details={
                    'detection_type': detection_result.detection_type,
                    'confidence_score': detection_result.confidence_score,
                    'threat_types': detection_result.threat_types,
                    'indicators': detection_result.indicators,
                    'recommended_action': detection_result.recommended_action
                },
                source_url=detection_result.analyzed_url,
                source_file=detection_result.file_name,
                auto_created=True,
                tags=['auto-generated', detection_result.detection_type.lower()]
            )
            
            # Send notification if critical
            if detection_result.threat_level == 'CRITICAL':
                _send_alert_notification(alert)
            
            return Response({
                'message': 'Alert created successfully',
                'alert': EnhancedAlertSerializer(alert).data
            }, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                'message': 'Detection result does not meet alert criteria',
                'criteria': {
                    'is_malicious': detection_result.is_malicious,
                    'confidence_score': detection_result.confidence_score,
                    'required_confidence': 0.7
                }
            })
            
    except Exception as e:
        return Response(
            {'error': f'Failed to create alert: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cleanup_old_alerts(request):
    """
    Cleanup old resolved/archived alerts.
    
    POST /api/detect/alerts/cleanup
    {
        "days_old": 30,
        "statuses": ["RESOLVED", "FALSE_POSITIVE"],
        "dry_run": true
    }
    """
    try:
        days_old = int(request.data.get('days_old', 30))
        statuses = request.data.get('statuses', ['RESOLVED', 'FALSE_POSITIVE'])
        dry_run = request.data.get('dry_run', True)
        
        # Calculate cutoff date
        cutoff_date = timezone.now() - timezone.timedelta(days=days_old)
        
        # Find alerts to cleanup
        alerts_to_cleanup = Alert.objects.filter(
            user=request.user,
            status__in=statuses,
            created_at__lt=cutoff_date
        )
        
        cleanup_count = alerts_to_cleanup.count()
        
        if not dry_run:
            # Actually delete the alerts
            deleted_count, _ = alerts_to_cleanup.delete()
            
            return Response({
                'message': f'Successfully cleaned up {deleted_count} old alerts',
                'deleted_count': deleted_count,
                'criteria': {
                    'days_old': days_old,
                    'statuses': statuses,
                    'cutoff_date': cutoff_date
                }
            })
        else:
            return Response({
                'message': f'Dry run: Found {cleanup_count} alerts that would be deleted',
                'would_delete_count': cleanup_count,
                'criteria': {
                    'days_old': days_old,
                    'statuses': statuses,
                    'cutoff_date': cutoff_date
                },
                'note': 'Set dry_run=false to actually delete these alerts'
            })
            
    except Exception as e:
        return Response(
            {'error': f'Failed to cleanup alerts: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alert_analytics(request):
    """
    Enhanced alert analytics and insights.
    
    GET /api/detect/alerts/analytics?period=7d
    """
    try:
        period = request.GET.get('period', '7d')  # 1d, 7d, 30d, 90d
        
        # Calculate date range
        period_map = {
            '1d': 1,
            '7d': 7,
            '30d': 30,
            '90d': 90
        }
        
        days = period_map.get(period, 7)
        start_date = timezone.now() - timezone.timedelta(days=days)
        
        user_alerts = Alert.objects.filter(
            user=request.user,
            created_at__gte=start_date
        )
        
        # Basic statistics
        total_alerts = user_alerts.count()
        unread_alerts = user_alerts.filter(is_read=False).count()
        critical_alerts = user_alerts.filter(severity='CRITICAL').count()
        auto_created_alerts = user_alerts.filter(auto_created=True).count()
        
        # Trend analysis (alerts per day)
        from django.db.models import Count
        from django.db.models.functions import TruncDate
        
        daily_trend = user_alerts.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Alert type breakdown
        type_breakdown = user_alerts.values('alert_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Severity breakdown
        severity_breakdown = user_alerts.values('severity').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Status breakdown
        status_breakdown = user_alerts.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Response time analysis (time to acknowledge/resolve)
        response_times = []
        for alert in user_alerts.filter(acknowledged_at__isnull=False):
            response_time = (alert.acknowledged_at - alert.created_at).total_seconds() / 3600  # hours
            response_times.append(response_time)
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Top threat indicators
        all_indicators = []
        for alert in user_alerts:
            if alert.threat_details.get('indicators'):
                all_indicators.extend(alert.threat_details['indicators'])
        
        from collections import Counter
        top_indicators = Counter(all_indicators).most_common(10)
        
        return Response({
            'period': period,
            'summary': {
                'total_alerts': total_alerts,
                'unread_alerts': unread_alerts,
                'critical_alerts': critical_alerts,
                'auto_created_alerts': auto_created_alerts,
                'read_rate': (total_alerts - unread_alerts) / total_alerts * 100 if total_alerts > 0 else 0,
                'avg_response_time_hours': round(avg_response_time, 2)
            },
            'trends': {
                'daily_alerts': list(daily_trend),
                'alert_types': list(type_breakdown),
                'severities': list(severity_breakdown),
                'statuses': list(status_breakdown)
            },
            'insights': {
                'top_threat_indicators': top_indicators,
                'most_common_alert_type': type_breakdown[0]['alert_type'] if type_breakdown else None,
                'most_common_severity': severity_breakdown[0]['severity'] if severity_breakdown else None
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate analytics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _send_alert_notification(alert):
    """Helper function to send alert notifications"""
    try:
        # Create notification record
        notification = AlertNotification.objects.create(
            alert=alert,
            notification_type='IN_APP',
            recipient=alert.user.email,
            status='SENT'
        )
        
        # Update alert
        alert.notification_sent = True
        alert.notification_sent_at = timezone.now()
        alert.save()
        
        # Here you would integrate with actual notification services
        # (email, push notifications, SMS, etc.)
        
        return True
    except Exception as e:
        print(f"Failed to send notification: {str(e)}")
        return False


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def override_alert(request, alert_id):
    """
    Mark alert as safe/unsafe or change status (user override).
    
    POST /api/alerts/{id}/override
    {
        "action": "mark_safe",
        "reason": "This is a legitimate business email"
    }
    """
    try:
        alert = get_object_or_404(Alert, id=alert_id, user=request.user)
        
        serializer = AlertOverrideSerializer(data=request.data)
        if serializer.is_valid():
            updated_alert = serializer.update(alert, serializer.validated_data)
            
            response_data = AlertSerializer(updated_alert).data
            response_data['message'] = f"Alert {serializer.validated_data['action']} successfully"
            
            return Response(response_data)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to update alert: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_safe_browsing_warning(request):
    """
    Create a safe browsing warning for a detected threat.
    
    POST /api/alerts/safe-browsing
    {
        "original_url": "http://malicious-site.com",
        "warning_type": "PHISHING",
        "threat_details": {...}
    }
    """
    try:
        serializer = SafeBrowsingWarningSerializer(data=request.data)
        if serializer.is_valid():
            warning = serializer.save(user=request.user)
            
            return Response(
                SafeBrowsingWarningSerializer(warning).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to create warning: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== THREAT DATABASE INTEGRATION ==========

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threat_list(request):
    """
    List all threats with filtering and search.
    
    GET /api/detect/threats/?threat_type=URL&severity=HIGH&search=phishing
    """
    try:
        queryset = ThreatDatabase.objects.filter(is_active=True)
        
        # Apply filters
        threat_type = request.query_params.get('threat_type')
        if threat_type:
            queryset = queryset.filter(threat_type=threat_type)
        
        severity = request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        source = request.query_params.get('source')
        if source:
            queryset = queryset.filter(source__icontains=source)
        
        # Search functionality
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(value__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        total_count = queryset.count()
        threats = queryset.order_by('-updated_at')[offset:offset + limit]
        
        serializer = ThreatDatabaseSerializer(threats, many=True)
        
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
            {'error': f'Failed to retrieve threats: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threat_detail(request, pk):
    """
    Get details of a specific threat.
    
    GET /api/detect/threats/{id}/
    """
    try:
        threat = get_object_or_404(ThreatDatabase, pk=pk, is_active=True)
        serializer = ThreatDatabaseSerializer(threat)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve threat: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def import_threat_feed(request):
    """
    Import threats from external feed (admin only).
    
    POST /api/threats/import
    {
        "feed_id": "uuid-of-threat-feed",
        "force_update": false
    }
    """
    start_time = time.time()
    
    try:
        serializer = ThreatImportSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            processing_time = int((time.time() - start_time) * 1000)
            
            return Response({
                'feed_name': result['feed'].name,
                'feed_type': result['feed'].feed_type,
                'import_result': result['import_result'],
                'processing_time_ms': processing_time
            })
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        return Response(
            {
                'error': f'Failed to import threat feed: {str(e)}',
                'processing_time_ms': processing_time
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def threat_feed_status(request):
    """
    Get status of all threat feeds (admin only).
    
    GET /api/threats/feeds
    """
    try:
        feeds = ThreatFeed.objects.all()
        serializer = ThreatFeedSerializer(feeds, many=True)
        
        # Calculate overall statistics
        total_threats = ThreatDatabase.objects.filter(is_active=True).count()
        feeds_status = {
            'total_feeds': feeds.count(),
            'active_feeds': feeds.filter(is_active=True).count(),
            'total_threats': total_threats,
            'last_24h_updates': feeds.filter(
                last_updated__gte=timezone.now() - timezone.timedelta(days=1)
            ).count()
        }
        
        return Response({
            'feeds': serializer.data,
            'status': feeds_status
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve feed status: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== USER REPORTS ==========

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def report_list_create(request):
    """
    List user reports or create a new report.
    
    GET /api/detect/reports/
    POST /api/detect/reports/
    """
    if request.method == 'GET':
        try:
            # Users can only see their own reports
            queryset = UserReport.objects.filter(user=request.user)
            
            # Apply filters
            report_type = request.query_params.get('report_type')
            if report_type:
                queryset = queryset.filter(report_type=report_type)
            
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            # Pagination
            limit = int(request.query_params.get('limit', 20))
            offset = int(request.query_params.get('offset', 0))
            
            total_count = queryset.count()
            reports = queryset.order_by('-created_at')[offset:offset + limit]
            
            serializer = UserReportSerializer(reports, many=True)
            
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
                {'error': f'Failed to retrieve reports: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        try:
            serializer = UserReportSerializer(
                data=request.data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                report = serializer.save()
                
                # Create alert if automated analysis detects high risk
                automated_analysis = report.automated_analysis
                if (automated_analysis.get('is_malicious') and 
                    automated_analysis.get('confidence_score', 0) > 0.7):
                    
                    Alert.objects.create(
                        user=request.user,
                        alert_type='PHISHING_URL' if report.suspicious_url else 'SUSPICIOUS_EMAIL',
                        severity=automated_analysis.get('threat_level', 'MEDIUM'),
                        title=f"User reported threat: {report.report_type}",
                        description=f"User reported suspicious content with high confidence automated detection",
                        threat_details=automated_analysis,
                        source_url=report.suspicious_url
                    )
                
                return Response(
                    UserReportDetailSerializer(report).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Failed to create report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def report_detail(request, pk):
    """
    Get, update, or delete a specific report.
    
    GET /api/detect/reports/{id}/
    PUT /api/detect/reports/{id}/
    PATCH /api/detect/reports/{id}/
    DELETE /api/detect/reports/{id}/
    """
    try:
        report = get_object_or_404(UserReport, pk=pk, user=request.user)
        
        if request.method == 'GET':
            serializer = UserReportDetailSerializer(report)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = UserReportSerializer(
                report, 
                data=request.data, 
                partial=partial,
                context={'request': request}
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(UserReportDetailSerializer(report).data)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        elif request.method == 'DELETE':
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
    except Exception as e:
        return Response(
            {'error': f'Failed to process report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_summary(request):
    """
    Get summary of user's reports.
    
    GET /api/detect/reports/summary/
    """
    try:
        user_reports = UserReport.objects.filter(user=request.user)
        
        summary = {
            'total_reports': user_reports.count(),
            'by_type': list(user_reports.values('report_type').annotate(
                count=Count('id')
            )),
            'by_status': list(user_reports.values('status').annotate(
                count=Count('id')
            )),
            'recent_reports': UserReportSerializer(
                user_reports[:5], many=True
            ).data,
            'confirmed_threats': user_reports.filter(
                status='CONFIRMED'
            ).count()
        }
        
        return Response(summary)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate summary: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )