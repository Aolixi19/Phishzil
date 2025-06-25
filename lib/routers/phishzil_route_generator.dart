import 'package:flutter/material.dart';

import '../screens/phishzil_home_screen.dart';
import '../screens/phishzil_scan_screen.dart';
import '../screens/phishzil_history_screen.dart';
import '../screens/phishzil_alerts_screen.dart';
import '../screens/phishzil_admin_screen.dart';
import '../screens/phishzil_settings_screen.dart';

class PhishZilRouteGenerator {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const PhishzilHomeScreen());
      case '/scan':
        return MaterialPageRoute(builder: (_) => const PhishzilScanScreen());
      case '/history':
        return MaterialPageRoute(builder: (_) => const PhishzilHistoryScreen());
      case '/alerts':
        return MaterialPageRoute(builder: (_) => const PhishzilAlertsScreen());
      case '/admin':
        return MaterialPageRoute(builder: (_) => const PhishzilAdminScreen());
      case '/settings':
        return MaterialPageRoute(
          builder: (_) => const PhishzilSettingsScreen(),
        );
      default:
        return MaterialPageRoute(
          builder: (_) =>
              const Scaffold(body: Center(child: Text('404 - Page Not Found'))),
        );
    }
  }
}
