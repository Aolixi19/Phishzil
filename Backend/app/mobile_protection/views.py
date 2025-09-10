# mobile_protection/views.py
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from .models import MobileDevice, SMSContent, NotificationContent, MobileAlert, MobileSettings
from .serializers import (
    MobileDeviceSerializer, SMSContentSerializer, NotificationContentSerializer,
    MobileAlertSerializer, MobileSettingsSerializer, MobileScanRequestSerializer
)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_mobile_device(request):
    """
    Register a new mobile device
    
    POST /api/mobile/register
    {
        "device_id": "unique_device_id",
        "device_type": "ANDROID",
        "device_name": "Samsung Galaxy S21",
        "app_version": "1.0.0",
        "push_token": "fcm_token_here"
    }
    """
    try:
        # Check if device already exists
        device_id = request.data.get('device_id')
        existing_device = MobileDevice.objects.filter(
            device_id=device_id,
            user=request.user
        ).first()
        
        if existing_device:
            # Update existing device
            serializer = MobileDeviceSerializer(
                existing_device,
                data=request.data,
                partial=True
            )
        else:
            # Create new device
            serializer = MobileDeviceSerializer(data=request.data)
        
        if serializer.is_valid():
            device = serializer.save(user=request.user)
            
            # Create default settings
            MobileSettings.objects.get_or_create(device=device)
            
            return Response(
                MobileDeviceSerializer(device).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to register device: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mobile_scan_content(request):
    """
    Scan mobile content for threats
    
    POST /api/mobile/scan
    {
        "device_id": "unique_device_id",
        "content_type": "sms",
        "content": "URGENT: Your account has been suspended...",
        "sender": "+1234567890"
    }
    """
    try:
        device_id = request.data.get('device_id')
        device = get_object_or_404(
            MobileDevice,
            device_id=device_id,
            user=request.user
        )
        
        serializer = MobileScanRequestSerializer(
            data=request.data,
            context={'device': device}
        )
        
        if serializer.is_valid():
            result = serializer.save()
            
            return Response({
                'scan_result': result,
                'device_id': device_id,
                'timestamp': timezone.now().isoformat()
            })
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to scan content: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mobile_alerts(request):
    """
    Get mobile alerts for user's devices
    
    GET /api/mobile/alerts?device_id=uuid&severity=HIGH
    """
    try:
        user_devices = MobileDevice.objects.filter(user=request.user)
        alerts = MobileAlert.objects.filter(device__in=user_devices)
        
        # Apply filters
        device_id = request.query_params.get('device_id')
        if device_id:
            alerts = alerts.filter(device__device_id=device_id)
        
        severity = request.query_params.get('severity')
        if severity:
            alerts = alerts.filter(severity=severity)
        
        alert_type = request.query_params.get('alert_type')
        if alert_type:
            alerts = alerts.filter(alert_type=alert_type)
        
        unacknowledged_only = request.query_params.get('unacknowledged_only', 'false')
        if unacknowledged_only.lower() == 'true':
            alerts = alerts.filter(acknowledged_at__isnull=True)
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        total_count = alerts.count()
        alerts = alerts.order_by('-created_at')[offset:offset + limit]
        
        serializer = MobileAlertSerializer(alerts, many=True)
        
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
            {'error': f'Failed to retrieve alerts: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def acknowledge_mobile_alert(request, alert_id):
    """
    Acknowledge a mobile alert
    
    POST /api/mobile/alerts/{id}/acknowledge
    """
    try:
        user_devices = MobileDevice.objects.filter(user=request.user)
        alert = get_object_or_404(
            MobileAlert,
            id=alert_id,
            device__in=user_devices
        )
        
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        return Response({
            'message': 'Alert acknowledged successfully',
            'alert': MobileAlertSerializer(alert).data
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to acknowledge alert: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def mobile_device_settings(request, device_id):
    """
    Get or update mobile device settings
    
    GET /api/mobile/devices/{id}/settings
    POST /api/mobile/devices/{id}/settings
    """
    try:
        device = get_object_or_404(
            MobileDevice,
            device_id=device_id,
            user=request.user
        )
        
        settings, created = MobileSettings.objects.get_or_create(device=device)
        
        if request.method == 'GET':
            serializer = MobileSettingsSerializer(settings)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = MobileSettingsSerializer(
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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mobile_protection_dashboard(request):
    """
    Get mobile protection dashboard data
    
    GET /api/mobile/dashboard?period=7d
    """
    try:
        period = request.query_params.get('period', '7d')
        period_map = {'1d': 1, '7d': 7, '30d': 30}
        days = period_map.get(period, 7)
        start_date = timezone.now() - timezone.timedelta(days=days)
        
        user_devices = MobileDevice.objects.filter(user=request.user)
        
        # SMS statistics
        sms_threats = SMSContent.objects.filter(
            device__in=user_devices,
            analyzed_at__gte=start_date,
            is_threat=True
        )
        
        # Notification statistics
        notification_threats = NotificationContent.objects.filter(
            device__in=user_devices,
            analyzed_at__gte=start_date,
            is_threat=True
        )
        
        # Alert statistics
        alerts = MobileAlert.objects.filter(
            device__in=user_devices,
            created_at__gte=start_date
        )
        
        dashboard_data = {
            'period': period,
            'devices': {
                'total': user_devices.count(),
                'active': user_devices.filter(is_active=True).count(),
                'devices': MobileDeviceSerializer(user_devices, many=True).data
            },
            'threats': {
                'sms_threats': sms_threats.count(),
                'notification_threats': notification_threats.count(),
                'total_threats': sms_threats.count() + notification_threats.count(),
                'threat_breakdown': list(
                    alerts.values('alert_type').annotate(
                        count=Count('id')
                    ).order_by('-count')
                )
            },
            'alerts': {
                'total': alerts.count(),
                'unacknowledged': alerts.filter(acknowledged_at__isnull=True).count(),
                'by_severity': list(
                    alerts.values('severity').annotate(
                        count=Count('id')
                    ).order_by('-count')
                )
            },
            'recent_activity': {
                'recent_sms_threats': SMSContentSerializer(
                    sms_threats[:5], many=True
                ).data,
                'recent_alerts': MobileAlertSerializer(
                    alerts[:5], many=True
                ).data
            }
        }
        
        return Response(dashboard_data)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate dashboard: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_push_notification(request):
    """
    Send push notification to user's devices
    
    POST /api/mobile/push-notification
    {
        "device_ids": ["device1", "device2"],
        "title": "Security Alert",
        "message": "Threat detected",
        "alert_id": "uuid"
    }
    """
    try:
        device_ids = request.data.get('device_ids', [])
        title = request.data.get('title')
        message = request.data.get('message')
        alert_id = request.data.get('alert_id')
        
        if not device_ids:
            # Send to all user devices
            devices = MobileDevice.objects.filter(
                user=request.user,
                is_active=True,
                push_token__isnull=False
            ).exclude(push_token='')
        else:
            devices = MobileDevice.objects.filter(
                user=request.user,
                device_id__in=device_ids,
                is_active=True,
                push_token__isnull=False
            )
        
        # Here you would integrate with actual push notification service
        # (Firebase Cloud Messaging, Apple Push Notification Service, etc.)
        
        sent_count = 0
        for device in devices:
            try:
                # Simulate push notification sending
                # push_service.send_notification(device.push_token, title, message)
                sent_count += 1
            except Exception as e:
                print(f"Failed to send push to device {device.device_id}: {str(e)}")
        
        return Response({
            'message': f'Push notifications sent to {sent_count} devices',
            'sent_count': sent_count,
            'total_devices': devices.count()
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to send push notifications: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )