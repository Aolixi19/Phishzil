// lib/themes/phishzil_text_styles.dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class PhishZilTextStyles {
  static final textTheme = TextTheme(
    displayLarge: GoogleFonts.poppins(
      fontSize: 32,
      fontWeight: FontWeight.bold,
    ),
    bodyMedium: GoogleFonts.poppins(fontSize: 16),
    labelSmall: GoogleFonts.poppins(fontSize: 12, color: Colors.grey),
  );
}
