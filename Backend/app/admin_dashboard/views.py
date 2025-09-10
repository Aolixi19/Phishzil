# admin_dashboard/views.py
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q, Sum
from .models import SystemSettings, AdminLog, OrganizationManagement, ComplianceReport
from .serializers import (
    SystemSettingsSerializer, AdminLogSerializer, UserManagementSerializer,
    OrganizationManagementSerializer, ComplianceReportSerializer, SystemOverviewSerializer
)

def log_admin_action(user, action_type, description, request, result='SUCCESS', additional_data=None):
    """Helper function to log admin actions"""
    AdminLog.objects.create(
        admin_user=user,
        action_type=action_type,
        action_description=description,
        ip_address=request.META.get('REMOTE_ADDR', ''),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        result=result,
        additional_data=additional_data or {}
    )

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_system_overview(request):
    """
    Get system-wide overview for admin dashboard
    
    GET /api/admin/overview
    """
    try:
        serializer = SystemOverviewSerializer()
        overview_data = serializer.to_representation(None)
        
        log_admin_action(
            request.user,
            'SECURITY_AUDIT',
            'Accessed system overview dashboard',
            request
        )
        
        return Response(overview_data)
        
    except Exception as e:
        log_admin_action(
            request.user,
            'SECURITY_AUDIT',
            f'Failed to access system overview: {str(e)}',
            request,
            result='FAILURE'
        )
        return Response(
            {'error': f'Failed to generate overview: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAdminUser])
def manage_users(request):
    """
    List or manage users (admin only)
    
    GET /api/admin/users?search=username&is_active=true
    POST /api/admin/users/{id}/action
    """
    if request.method == 'GET':
        try:
            queryset = User.objects.all()
            
            # Apply filters
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(username__icontains=search) |
                    Q(email__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )
            
            is_active = request.query_params.get('is_active')
            if is_active is not None:
                queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
            # Pagination
            limit = int(request.query_params.get('limit', 50))
            offset = int(request.query_params.get('offset', 0))
            
            total_count = queryset.count()
            users = queryset.order_by('-date_joined')[offset:offset + limit]
            
            serializer = UserManagementSerializer(users, many=True)
            
            log_admin_action(
                request.user,
                'USER_MANAGEMENT',
                f'Viewed user list (total: {total_count})',
                request
            )
            
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
                {'error': f'Failed to retrieve users: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        try:
            user_id = request.data.get('user_id')
            action = request.data.get('action')  # activate, deactivate, reset_password
            
            user = get_object_or_404(User, id=user_id)
            
            if action == 'activate':
                user.is_active = True
                user.save()
                message = f'User {user.username} activated'
            elif action == 'deactivate':
                user.is_active = False
                user.save()
                message = f'User {user.username} deactivated'
            elif action == 'reset_password':
                # Generate temporary password and send email
                import secrets
                temp_password = secrets.token_urlsafe(12)
                user.set_password(temp_password)
                user.save()
                message = f'Password reset for user {user.username}'
                # Here you would send the temp password via email
            else:
                return Response(
                    {'error': 'Invalid action'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            log_admin_action(
                request.user,
                'USER_MANAGEMENT',
                message,
                request,
                additional_data={'target_user': user.username, 'action': action}
            )
            
            return Response({
                'message': message,
                'user': UserManagementSerializer(user).data
            })
            
        except Exception as e:
            log_admin_action(
                request.user,
                'USER_MANAGEMENT',
                f'Failed user action: {str(e)}',
                request,
                result='FAILURE'
            )
            return Response(
                {'error': f'Failed to perform action: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'POST', 'PUT'])
@permission_classes([permissions.IsAdminUser])
def system_settings(request):
    """
    Manage system settings
    
    GET /api/admin/settings
    POST /api/admin/settings
    PUT /api/admin/settings/{key}
    """
    if request.method == 'GET':
        try:
            settings = SystemSettings.objects.all()
            
            # Filter public settings for non-superusers
            if not request.user.is_superuser:
                settings = settings.filter(is_public=True)
            
            serializer = SystemSettingsSerializer(settings, many=True)
            
            return Response({
                'settings': serializer.data,
                'total_count': settings.count()
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve settings: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        try:
            serializer = SystemSettingsSerializer(data=request.data)
            if serializer.is_valid():
                setting = serializer.save(updated_by=request.user)
                
                log_admin_action(
                    request.user,
                    'SYSTEM_SETTINGS',
                    f'Created setting: {setting.setting_key}',
                    request,
                    additional_data={'setting_key': setting.setting_key}
                )
                
                return Response(
                    SystemSettingsSerializer(setting).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Failed to create setting: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'PUT':
        try:
            setting_key = request.data.get('setting_key')
            setting = get_object_or_404(SystemSettings, setting_key=setting_key)
            
            serializer = SystemSettingsSerializer(
                setting,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                
                log_admin_action(
                    request.user,
                    'SYSTEM_SETTINGS',
                    f'Updated setting: {setting.setting_key}',
                    request,
                    additional_data={'setting_key': setting.setting_key}
                )
                
                return Response(serializer.data)
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Failed to update setting: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_logs(request):
    """
    Get admin activity logs
    
    GET /api/admin/logs?action_type=USER_MANAGEMENT&limit=100
    """
    try:
        logs = AdminLog.objects.all()
        
        # Apply filters
        action_type = request.query_params.get('action_type')
        if action_type:
            logs = logs.filter(action_type=action_type)
        
        admin_user = request.query_params.get('admin_user')
        if admin_user:
            logs = logs.filter(admin_user__username=admin_user)
        
        result_filter = request.query_params.get('result')
        if result_filter:
            logs = logs.filter(result=result_filter)
        
        date_from = request.query_params.get('date_from')
        if date_from:
            logs = logs.filter(timestamp__gte=date_from)
        
        # Pagination
        limit = int(request.query_params.get('limit', 100))
        offset = int(request.query_params.get('offset', 0))
        
        total_count = logs.count()
        logs = logs.order_by('-timestamp')[offset:offset + limit]
        
        serializer = AdminLogSerializer(logs, many=True)
        
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
            {'error': f'Failed to retrieve logs: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def generate_compliance_report(request):
    """
    Generate compliance report
    
    POST /api/admin/compliance-report
    {
        "report_type": "SECURITY_AUDIT",
        "period_start": "2025-01-01T00:00:00Z",
        "period_end": "2025-01-31T23:59:59Z",
        "organization_id": "uuid"
    }
    """
    try:
        report_type = request.data.get('report_type')
        period_start = request.data.get('period_start')
        period_end = request.data.get('period_end')
        organization_id = request.data.get('organization_id')
        
        # Generate report data based on type
        from ..Phishing_Detection.models import ThreatDetectionResult
        from ..threat_protection.models import DisarmedLink, QuarantinedFile

        
        if report_type == 'SECURITY_AUDIT':
            report_data = {
                'total_detections': ThreatDetectionResult.objects.filter(
                    created_at__range=[period_start, period_end]
                ).count(),
                'malicious_detections': ThreatDetectionResult.objects.filter(
                    created_at__range=[period_start, period_end],
                    is_malicious=True
                ).count(),
                'links_disarmed': DisarmedLink.objects.filter(
                    disarm_timestamp__range=[period_start, period_end]
                ).count(),
                'files_quarantined': QuarantinedFile.objects.filter(
                    quarantine_timestamp__range=[period_start, period_end]
                ).count()
            }
        elif report_type == 'THREAT_SUMMARY':
            threat_types = ThreatDetectionResult.objects.filter(
                created_at__range=[period_start, period_end],
                is_malicious=True
            ).values('threat_types').annotate(count=Count('id'))
            
            report_data = {
                'threat_breakdown': list(threat_types),
                'total_threats': sum(item['count'] for item in threat_types)
            }
        else:
            report_data = {'message': 'Report type not implemented yet'}
        
        # Create report record
        organization = None
        if organization_id:
            organization = get_object_or_404(OrganizationManagement, id=organization_id)
        
        report = ComplianceReport.objects.create(
            organization=organization,
            report_type=report_type,
            period_start=period_start,
            period_end=period_end,
            generated_by=request.user,
            report_data=report_data
        )
        
        log_admin_action(
            request.user,
            'COMPLIANCE_REPORT',
            f'Generated {report_type} report for period {period_start} to {period_end}',
            request,
            additional_data={'report_id': str(report.id)}
        )
        
        return Response(
            ComplianceReportSerializer(report).data,
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAdminUser])
def organization_management(request):
    """
    Manage organizations
    
    GET /api/admin/organizations
    POST /api/admin/organizations
    """
    if request.method == 'GET':
        try:
            organizations = OrganizationManagement.objects.all()
            
            # Apply filters
            org_type = request.query_params.get('organization_type')
            if org_type:
                organizations = organizations.filter(organization_type=org_type)
            
            is_active = request.query_params.get('is_active')
            if is_active is not None:
                organizations = organizations.filter(is_active=is_active.lower() == 'true')
            
            serializer = OrganizationManagementSerializer(organizations, many=True)
            
            return Response({
                'organizations': serializer.data,
                'total_count': organizations.count()
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve organizations: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        try:
            serializer = OrganizationManagementSerializer(data=request.data)
            if serializer.is_valid():
                organization = serializer.save()
                
                log_admin_action(
                    request.user,
                    'USER_MANAGEMENT',
                    f'Created organization: {organization.name}',
                    request,
                    additional_data={'organization_id': str(organization.id)}
                )
                
                return Response(
                    OrganizationManagementSerializer(organization).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Failed to create organization: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )