import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../utils/phishzil_constants.dart';

class PhishzilHistoryScreen extends StatelessWidget {
  const PhishzilHistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> scanHistory = [
      {
        'title': 'Suspicious Link Detected',
        'date': 'June 22, 2025',
        'status': 'Blocked',
      },
      {'title': 'Safe File Scanned', 'date': 'June 20, 2025', 'status': 'Safe'},
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: PhishzilColors.primary,
        title: const Text('Scan History'),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: scanHistory.length,
        itemBuilder: (context, index) {
          final item = scanHistory[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            elevation: 3,
            child: ListTile(
              leading: Icon(
                item['status'] == 'Blocked'
                    ? Icons.warning
                    : Icons.check_circle,
                color: item['status'] == 'Blocked' ? Colors.red : Colors.green,
              ),
              title: Text(
                item['title'] ?? '',
                style: GoogleFonts.poppins(fontWeight: FontWeight.w500),
              ),
              subtitle: Text(item['date'] ?? ''),
              trailing: Text(
                item['status'] ?? '',
                style: GoogleFonts.poppins(),
              ),
            ),
          );
        },
      ),
    );
  }
}
