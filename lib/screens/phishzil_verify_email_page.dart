import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../routers/phishzil_app_routes.dart';
import '../utils/phishzil_constants.dart';

class PhishzilVerifyEmailPage extends StatefulWidget {
  const PhishzilVerifyEmailPage({super.key});

  @override
  State<PhishzilVerifyEmailPage> createState() =>
      _PhishzilVerifyEmailPageState();
}

class _PhishzilVerifyEmailPageState extends State<PhishzilVerifyEmailPage> {
  bool _isSending = false;
  bool _checkingVerification = false;
  int _cooldown = 0;
  Timer? _timer;

  final user = FirebaseAuth.instance.currentUser;

  @override
  void initState() {
    super.initState();
    _startVerificationAutoCheck();
  }

  void _startCooldown() {
    setState(() => _cooldown = 60);
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_cooldown == 0) {
        timer.cancel();
      } else {
        setState(() => _cooldown--);
      }
    });
  }

  void _startVerificationAutoCheck() {
    Timer.periodic(const Duration(seconds: 4), (timer) async {
      await user?.reload();
      if (user?.emailVerified == true) {
        timer.cancel();
        if (!mounted) return;
        Navigator.pushReplacementNamed(context, AppRoutes.home);
      }
    });
  }

  Future<void> _resendEmailVerification() async {
    setState(() => _isSending = true);
    try {
      await user?.sendEmailVerification();
      _startCooldown();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Verification email sent. Check your inbox."),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Failed to send email: $e"),
          backgroundColor: Colors.red,
        ),
      );
    }
    setState(() => _isSending = false);
  }

  Future<void> _checkVerificationAndProceed() async {
    setState(() => _checkingVerification = true);
    await user?.reload();
    if (user?.emailVerified == true) {
      if (!mounted) return;
      Navigator.pushReplacementNamed(context, AppRoutes.home);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Email not verified yet."),
          backgroundColor: Colors.red,
        ),
      );
    }
    setState(() => _checkingVerification = false);
  }

  Future<void> _logout() async {
    await FirebaseAuth.instance.signOut();
    if (!mounted) return;
    Navigator.pushReplacementNamed(context, AppRoutes.login);
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.mark_email_unread,
                  color: Colors.amber,
                  size: 80,
                ),
                const SizedBox(height: 20),
                const Text(
                  "Verify Your Email",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 10),
                const Text(
                  "A verification link has been sent to:",
                  style: TextStyle(color: Colors.white70),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 4),
                Text(
                  user?.email ?? '',
                  style: const TextStyle(color: Colors.lightBlueAccent),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 30),
                ElevatedButton.icon(
                  icon: const Icon(Icons.refresh),
                  label: Text(
                    _isSending
                        ? "Sending..."
                        : _cooldown > 0
                        ? "Resend in $_cooldown s"
                        : "Resend Verification",
                  ),
                  onPressed: _isSending || _cooldown > 0
                      ? null
                      : _resendEmailVerification,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: PhishzilColors.secondary,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 24,
                      vertical: 12,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                ElevatedButton.icon(
                  icon: _checkingVerification
                      ? const SizedBox(
                          height: 16,
                          width: 16,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Icon(Icons.check_circle_outline),
                  label: Text(
                    _checkingVerification ? "Checking..." : "I’ve Verified",
                  ),
                  onPressed: _checkingVerification
                      ? null
                      : _checkVerificationAndProceed,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 24,
                      vertical: 12,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                TextButton.icon(
                  icon: const Icon(Icons.logout, color: Colors.redAccent),
                  label: const Text(
                    "Logout",
                    style: TextStyle(color: Colors.redAccent),
                  ),
                  onPressed: _logout,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
