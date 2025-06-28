import 'package:flutter/material.dart';

// Screens
import '../screens/phishzil_home_screen.dart';
import '../screens/phishzil_scan_screen.dart';
import '../screens/phishzil_history_screen.dart';
import '../screens/phishzil_alerts_screen.dart';
import '../screens/phishzil_admin_screen.dart';
import '../screens/phishzil_settings_screen.dart';
import '../screens/phish_login_screen.dart';
import '../screens/phish_signup_screen.dart';
import '../screens/phishzil_password_reset_screen.dart';
import '../screens/phishzil_splash_page.dart';
import '../screens/phishzil_terms_page.dart';

class PhishZilRouteGenerator {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/splash':
        return MaterialPageRoute(builder: (_) => const PhishzilSplashPage());
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
      case '/login':
        return MaterialPageRoute(builder: (_) => const PhishzilLoginPage());
      case '/signup':
        return MaterialPageRoute(builder: (_) => const PhishzilSignUpPage());
      case '/reset':
        return MaterialPageRoute(
          builder: (_) => const PhishzilPasswordResetScreen(),
        );
      case '/verify-email':
        return MaterialPageRoute(builder: (_) => const PhishzilSignUpPage());
      case '/settings':
        return MaterialPageRoute(
          builder: (_) => const PhishzilSettingsScreen(),
        );
      case '/terms':
        return MaterialPageRoute(builder: (_) => const PhishzilTermsPage());
      default:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(
              child: Text(
                '404 - Page Not Found',
                style: TextStyle(fontSize: 18, color: Colors.red),
              ),
            ),
          ),
        );
    }
  }
}
