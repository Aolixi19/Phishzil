import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:top_snackbar_flutter/custom_snack_bar.dart';
import 'package:top_snackbar_flutter/top_snack_bar.dart';

import '../phishzil_auth/phishzil_auth_provider.dart';
import '../phishzil_global_widget/phishzil_button.dart';
import '../phishzil_routes/phishzil_route_name.dart';

class VerifyCodePage extends StatefulWidget {
  final String email;

  const VerifyCodePage({super.key, required this.email});

  @override
  State<VerifyCodePage> createState() => _VerifyCodePageState();
}

class _VerifyCodePageState extends State<VerifyCodePage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController codeController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  String? localError;
  bool _isResending = false;

  @override
  void initState() {
    super.initState();
    emailController.text = widget.email;
    assert(widget.email.trim().isNotEmpty, 'Email must not be empty');
    debugPrint('Verification page initialized for: ${widget.email}');
  }

  @override
  void dispose() {
    codeController.dispose();
    emailController.dispose();
    super.dispose();
  }

  Future<void> _verifyCode() async {
    if (!(_formKey.currentState?.validate() ?? false)) return;

    final authProvider = Provider.of<AuthProvider>(context, listen: false);

    try {
      final success = await authProvider.verifyCode(
        emailController.text.trim(),
        codeController.text.trim(),
      );

      if (success && mounted) {
        showTopSnackBar(
          Overlay.of(context),
          const CustomSnackBar.success(message: 'Verification successful ✅'),
        );
        context.go(RouteNames.login);
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          localError =
              'Verification failed. Please check the code and try again.';
        });
      }
      debugPrint('Verification error: $e');
    }
  }

  Future<void> resendVerificationCode() async {
    setState(() => _isResending = true);

    try {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      final success = await authProvider.resendVerificationCode(
        emailController.text.trim(),
      );

      if (success && mounted) {
        showTopSnackBar(
          Overlay.of(context),
          const CustomSnackBar.success(message: 'New verification code sent ✅'),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() => localError = 'Failed to resend code. Please try again.');
      }
      debugPrint('Resend error: $e');
    } finally {
      if (mounted) {
        setState(() => _isResending = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);

    return Scaffold(
      backgroundColor: const Color(0xFF00172B),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                const Text(
                  'Email Verification',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.lightBlueAccent,
                  ),
                ),
                const SizedBox(height: 20),

                TextFormField(
                  controller: emailController,
                  readOnly: true,
                  decoration: InputDecoration(
                    labelText: 'Email',
                    filled: true,
                    fillColor: Colors.white10,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
                const SizedBox(height: 20),

                const Text(
                  'Enter the 6-digit code sent to your email',
                  style: TextStyle(color: Colors.white70),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 30),

                TextFormField(
                  controller: codeController,
                  keyboardType: TextInputType.number,
                  maxLength: 6,
                  style: const TextStyle(
                    color: Colors.white,
                    letterSpacing: 2.0,
                    fontSize: 24,
                  ),
                  textAlign: TextAlign.center,
                  decoration: InputDecoration(
                    hintText: '••••••',
                    hintStyle: const TextStyle(
                      color: Colors.white30,
                      letterSpacing: 2.0,
                      fontSize: 24,
                    ),
                    filled: true,
                    fillColor: Colors.white10,
                    counterText: '',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    contentPadding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter the 6-digit code';
                    }
                    if (value.length != 6 ||
                        !RegExp(r'^\d{6}$').hasMatch(value)) {
                      return 'Please enter a valid 6-digit number';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                TextButton(
                  onPressed: _isResending ? null : resendVerificationCode,
                  child: _isResending
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text(
                          "Didn't receive code? Resend",
                          style: TextStyle(color: Colors.lightBlueAccent),
                        ),
                ),
                const SizedBox(height: 30),

                GradientButton(
                  onPressed: _verifyCode,
                  label: 'Verify Code',
                  isLoading: auth.isLoading,
                ),
                const SizedBox(height: 20),

                if (localError != null && localError!.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Text(
                      localError!,
                      style: const TextStyle(color: Colors.red),
                      textAlign: TextAlign.center,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
