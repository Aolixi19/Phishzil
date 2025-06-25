// lib/themes/phishzil_app_theme.dart
import 'package:flutter/material.dart';
import 'phishzil_text_styles.dart';

class PhishZilAppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      textTheme: PhishZilTextStyles.textTheme,
    );
  }
}
