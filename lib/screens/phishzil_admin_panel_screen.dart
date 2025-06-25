import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../utils/phishzil_constants.dart';

class PhishzilAdminScreen extends StatelessWidget {
  const PhishzilAdminScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> logs = [
      {
        'user': 'Abihu',
        'action': 'Deleted phishing report #1023',
        'time': 'Today, 9:45 AM',
      },
      {
        'user': 'SecurityBot',
        'action': 'Flagged suspicious link from scan #3421',
        'time': 'Yesterday, 3:10 PM',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: PhishzilColors.primary,
        title: const Text('Admin Panel'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'System Logs',
              style: GoogleFonts.poppins(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            Expanded(
              child: ListView.separated(
                itemCount: logs.length,
                separatorBuilder: (_, __) => const SizedBox(height: 12),
                itemBuilder: (context, index) {
                  final log = logs[index];
                  return Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.grey[50],
                      border: Border.all(color: Colors.grey[300]!),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          log['user'] ?? '',
                          style: GoogleFonts.poppins(
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          log['action'] ?? '',
                          style: GoogleFonts.poppins(fontSize: 14),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          log['time'] ?? '',
                          style: GoogleFonts.poppins(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
