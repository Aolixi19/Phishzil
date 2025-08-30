import 'package:permission_handler/permission_handler.dart';

class PermissionHandlerUtil {
  /// Requests only essential permissions one by one and handles permanently denied cases
  static Future<void> requestEssentialPermissions() async {
    final permissions = [
      Permission.sms,
      Permission.storage,
      Permission.notification,
      Permission.ignoreBatteryOptimizations,
    ];

    for (final permission in permissions) {
      final status = await permission.request();

      // If the permission is permanently denied, prompt user to open app settings
      if (status.isPermanentlyDenied) {
        await openAppSettings();
        break;
      }
    }
  }

  /// Returns true if all essential permissions are granted
  static Future<bool> areEssentialPermissionsGranted() async {
    final permissions = [
      Permission.sms,
      Permission.storage,
      Permission.notification,
      Permission.ignoreBatteryOptimizations,
    ];

    final results = await Future.wait(permissions.map((p) => p.status));
    return results.every((status) => status.isGranted);
  }
}
