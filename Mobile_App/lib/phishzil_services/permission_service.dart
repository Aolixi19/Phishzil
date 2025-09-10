import 'package:permission_handler/permission_handler.dart';

class PermissionService {
  /// Requests all necessary permissions
  static Future<bool> requestAllPermissions() async {
    final permissions = [
      Permission.sms,
      Permission.storage,
      Permission.notification,
      Permission.ignoreBatteryOptimizations,
    ];

    // Request all permissions
    Map<Permission, PermissionStatus> statuses = await permissions.request();

    // Open app settings if any permission is permanently denied
    for (final entry in statuses.entries) {
      if (entry.value.isPermanentlyDenied) {
        await openAppSettings();
        break;
      }
    }

    // Return true only if all permissions are granted
    return statuses.values.every((status) => status.isGranted);
  }

  /// Check if all required permissions are already granted
  static Future<bool> areAllPermissionsGranted() async {
    final permissions = [
      Permission.sms,
      Permission.storage,
      Permission.notification,
      Permission.ignoreBatteryOptimizations,
    ];

    final statuses = await Future.wait(permissions.map((p) => p.status));
    return statuses.every((status) => status.isGranted);
  }
}
