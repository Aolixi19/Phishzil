// TODO Implement this library.
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class PhishzilAlertsScreen extends StatelessWidget {
  const PhishzilAlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Threat Alerts', style: GoogleFonts.poppins()),
      ),
      body: Center(
        child: Text(
          'This page will display phishing threat alerts.',
          style: GoogleFonts.poppins(fontSize: 16),
        ),
      ),
    );
  }
}
