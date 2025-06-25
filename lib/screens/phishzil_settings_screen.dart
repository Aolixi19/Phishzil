import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class PhishzilSettingsScreen extends StatelessWidget {
  const PhishzilSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Settings', style: GoogleFonts.poppins())),
      body: Center(
        child: Text(
          'Settings page content goes here.',
          style: GoogleFonts.poppins(fontSize: 16),
        ),
      ),
    );
  }
}
