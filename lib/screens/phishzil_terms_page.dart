import 'package:flutter/material.dart';

class PhishzilTermsPage extends StatelessWidget {
  const PhishzilTermsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text("Terms & Conditions"),
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(
          "Here are the Terms & Conditions for using the PhishZil app. "
          "By signing up, you agree to comply with our terms, privacy policy, "
          "and security guidelines. (Add your real content here.)",
          style: const TextStyle(color: Colors.white70, fontSize: 15),
        ),
      ),
    );
  }
}
