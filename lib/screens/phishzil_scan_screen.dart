import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../utils/phishzil_constants.dart';

class PhishzilScanScreen extends StatelessWidget {
  const PhishzilScanScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: PhishzilColors.safeColor,
        iconTheme: IconThemeData(color: Colors.lightBlue),
        title: const Text('Start Scan'),
        centerTitle: true,
        foregroundColor: Colors.lightBlue,
      ),
      backgroundColor: PhishzilColors.safeColor,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.qr_code_scanner, size: 80, color: Colors.grey[700]),
            const SizedBox(height: 20),
            Text(
              'Scan a suspicious link or file',
              style: GoogleFonts.poppins(fontSize: 18),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // TODO: Implement scan logic
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: PhishzilColors.primary,
                foregroundColor: Colors.green,
                padding: const EdgeInsets.symmetric(
                  horizontal: 32,
                  vertical: 12,
                ),
              ),
              child: Text(
                'Start Scanning',
                style: GoogleFonts.poppins(fontSize: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
