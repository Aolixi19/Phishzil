// lib/features/terms/pages/terms_page.dart

import 'package:flutter/material.dart';

class TermsPage extends StatelessWidget {
  const TermsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF00172B),
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text('Terms & Conditions'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Text(
            'These are your PhishZil Terms and Conditions.\n\n'
            '1. You agree to use this app responsibly.\n'
            '2. Your data is securely handled.\n'
            '3. Do not engage in fraud or phishing.\n'
            '4. We may update these terms at any time.\n\n'
            'By using this app, you agree to be bound by these conditions.',
            style: const TextStyle(color: Colors.white70, fontSize: 16),
          ),
        ),
      ),
    );
  }
}
