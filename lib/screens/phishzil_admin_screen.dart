// TODO Implement this library.
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class PhishzilAdminScreen extends StatelessWidget {
  const PhishzilAdminScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Admin Panel', style: GoogleFonts.poppins())),
      body: Center(
        child: Text(
          'This is the admin screen. Admin tools and settings will be added here.',
          style: GoogleFonts.poppins(fontSize: 16),
        ),
      ),
    );
  }
}
