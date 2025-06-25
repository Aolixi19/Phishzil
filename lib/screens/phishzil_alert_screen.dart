import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../utils/phishzil_constants.dart';

class PhishzilAlertsScreen extends StatelessWidget {
  const PhishzilAlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> alerts = [
      {
        'title': 'Phishing Attempt Blocked',
        'message':
            'We blocked a suspicious email trying to steal your credentials.',
        'time': '2 hours ago',
      },
      {
        'title': 'New Phishing Technique Detected',
        'message': 'A new attack using fake banking apps is trending.',
        'time': 'Yesterday',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: PhishzilColors.primary,
        title: const Text('Threat Alerts'),
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: alerts.length,
        separatorBuilder: (_, __) => const SizedBox(height: 12),
        itemBuilder: (context, index) {
          final alert = alerts[index];
          return Container(
            decoration: BoxDecoration(
              color: Colors.red.shade50,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.red.shade100),
            ),
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  alert['title'] ?? '',
                  style: GoogleFonts.poppins(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.red.shade700,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  alert['message'] ?? '',
                  style: GoogleFonts.poppins(fontSize: 14),
                ),
                const SizedBox(height: 6),
                Text(
                  alert['time'] ?? '',
                  style: GoogleFonts.poppins(fontSize: 12, color: Colors.grey),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
