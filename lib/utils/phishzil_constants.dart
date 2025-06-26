import 'package:flutter/material.dart';

class PhishzilColors {
  static const Color safeColor = Color.fromARGB(255, 8, 12, 68);
  static const Color dangerColor = Colors.red;
  static const Color warningColor = Colors.orange;
  static const Color primaryColor = Colors.lightBlue;
  static const Color textColor = Colors.black87;
  static const Color primary = Color(0xFF1E88E5); // Blue
  static const Color secondary = Color(0xFF42A5F5); // Lighter Blue
  static const Color background = Color(0xFFF5F7FA);
  static const Color card = Colors.white;
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF757575);
  static const Color warning = Color(0xFFFBC02D); // Yellow
  static const Color danger = Color(0xFFE53935); // Red
  static const Color success = Color(0xFF43A047); // Green
}

class PhishzilAssets {
  static const String shieldAnimation = 'assets/animations/shield.json';
  static const String loginLogo = 'assets/images/sh.png';
}

class PhishzilStrings {
  static const String appName = 'PhishZil';
  static const String welcomeMessage = 'Welcome, Abihu 👋';
  static const String subtitle = 'Protecting you from phishing in real-time.';
  static const String securityTipTitle = '🛡️ Security Tip:';
  static const String securityTip =
      'Never click suspicious links in unexpected emails, even if they look familiar.';
}

class PhishzilSpacing {
  static const double height = 14.0;
  static const double padding = 16.0;
  static const double cardSpacing = 10.0;
  static const double sectionSpacing = 20.0;
}
