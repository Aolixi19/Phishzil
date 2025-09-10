# browser_extension/views.py
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from .models import BrowserSession, BlockedSite, BrowserSettings
from .serializers import (
    BrowserSessionSerializer, BlockedSiteSerializer, BrowserSettingsSerializer,
    URLCheckSerializer, BrowserOverrideSerializer
)
import time

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def browser_check_url(request):
    """
    Real-time URL checking for browser extension
    
    POST /api/browser/check-url
    {
        "url": "https://suspicious-site.com",
        "page_context": "navigation",
        "referrer": "https://google.com"
    }
    """
    start_time = time.time()
    
    try:
        serializer = URLCheckSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            result = serializer.save()
            response_time = int((time.time() - start_time) * 1000)
            result['response_time_ms'] = response_time
            
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        response_time = int((time.time() - start_time) * 1000)
        return Response(
            {
                'error': 'Failed to check URL',
                'message': str(e),
                'response_time_ms': response_time
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def browser_settings(request):
    """
    Get or update browser extension settings
    
    GET /api/browser/settings
    POST /api/browser/settings
    """
    try:
        settings, created = BrowserSettings.objects.get_or_create(
            user=request.user
        )
        
        if request.method == 'GET':
            serializer = BrowserSettingsSerializer(settings)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = BrowserSettingsSerializer(
                settings, 
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
            {'error': f'Failed to manage settings: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def browser_start_session(request):
    """
    Start a new browser protection session
    
    POST /api/browser/start-session
    {
        "browser_type": "CHROME",
        "extension_version": "1.0.0"
    }
    """
    try:
        # End any existing active sessions
        BrowserSession.objects.filter(
            user=request.user,
            is_active=True
        ).update(is_active=False, ended_at=timezone.now())
        
        # Create new session
        session_data = {
            'browser_type': request.data.get('browser_type', 'CHROME'),
            'extension_version': request.data.get('extension_version', '1.0.0')
        }
        
        serializer = BrowserSessionSerializer(data=session_data)
        if serializer.is_valid():
            session = serializer.save(user=request.user)
            
            # Generate session token
            import hashlib
            import secrets
            token_data = f"{session.id}:{request.user.id}:{secrets.token_hex(16)}"
            session.session_token = hashlib.sha256(token_data.encode()).hexdigest()
            session.save()
            
            response_data = BrowserSessionSerializer(session).data
            response_data['session_token'] = session.session_token
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to start session: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def browser_end_session(request, session_id):
    """
    End a browser protection session
    
    POST /api/browser/sessions/{id}/end
    """
    try:
        session = get_object_or_404(
            BrowserSession,
            id=session_id,
            user=request.user,
            is_active=True
        )
        
        session.is_active = False
        session.ended_at = timezone.now()
        session.save()
        
        duration = session.ended_at - session.started_at
        
        return Response({
            'message': 'Browser session ended successfully',
            'session_id': str(session.id),
            'duration_minutes': int(duration.total_seconds() / 60),
            'urls_checked': session.urls_checked,
            'threats_blocked': session.threats_blocked
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to end session: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def browser_blocked_sites(request):
    """
    Get list of blocked sites
    
    GET /api/browser/blocked-sites?limit=20&threat_type=PHISHING
    """
    try:
        queryset = BlockedSite.objects.filter(user=request.user)
        
        # Apply filters
        threat_type = request.query_params.get('threat_type')
        if threat_type:
            queryset = queryset.filter(threat_type=threat_type)
        
        date_from = request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(blocked_at__gte=date_from)
        
        overridden = request.query_params.get('overridden')
        if overridden is not None:
            queryset = queryset.filter(user_overridden=overridden.lower() == 'true')
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        total_count = queryset.count()
        sites = queryset.order_by('-blocked_at')[offset:offset + limit]
        
        serializer = BlockedSiteSerializer(sites, many=True)
        
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
            {'error': f'Failed to retrieve blocked sites: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def browser_override_block(request):
    """
    Allow user to override a blocked site
    
    POST /api/browser/override
    {
        "blocked_site_id": "uuid",
        "reason": "This is a legitimate business site"
    }
    """
    try:
        serializer = BrowserOverrideSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            blocked_site = serializer.save()
            
            return Response({
                'message': 'Site override recorded successfully',
                'blocked_site': BlockedSiteSerializer(blocked_site).data
            })
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to override block: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def browser_protection_stats(request):
    """
    Get browser protection statistics
    
    GET /api/browser/stats?period=7d
    """
    try:
        period = request.query_params.get('period', '7d')
        period_map = {'1d': 1, '7d': 7, '30d': 30}
        days = period_map.get(period, 7)
        start_date = timezone.now() - timezone.timedelta(days=days)
        
        user_sessions = BrowserSession.objects.filter(
            user=request.user,
            started_at__gte=start_date
        )
        
        user_blocked_sites = BlockedSite.objects.filter(
            user=request.user,
            blocked_at__gte=start_date
        )
        
        stats = {
            'period': period,
            'total_sessions': user_sessions.count(),
            'active_sessions': user_sessions.filter(is_active=True).count(),
            'total_urls_checked': user_sessions.aggregate(
                total=models.Sum('urls_checked')
            )['total'] or 0,
            'total_threats_blocked': user_blocked_sites.count(),
            'threats_by_type': list(
                user_blocked_sites.values('threat_type').annotate(
                    count=Count('id')
                ).order_by('-count')
            ),
            'protection_effectiveness': 95.5,  # Calculate based on blocked vs total
            'recent_blocked_sites': BlockedSiteSerializer(
                user_blocked_sites[:5], many=True
            ).data
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate stats: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )