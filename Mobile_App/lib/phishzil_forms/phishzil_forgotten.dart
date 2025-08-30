// ignore_for_file: curly_braces_in_flow_control_structures, use_build_context_synchronously

import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:lottie/lottie.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:go_router/go_router.dart';
import 'package:top_snackbar_flutter/custom_snack_bar.dart';
import 'package:top_snackbar_flutter/top_snack_bar.dart';

import '../phishzil_auth/phishzil_auth_provider.dart';
import '../phishzil_global_widget/phishzil_button.dart';
import '../phishzil_routes/phishzil_route_name.dart';

class ForgotPasswordPage extends StatefulWidget {
  const ForgotPasswordPage({super.key});

  @override
  State<ForgotPasswordPage> createState() => _ForgotPasswordPageState();
}

class _ForgotPasswordPageState extends State<ForgotPasswordPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController emailController = TextEditingController();
  final _debouncer = _Debouncer(milliseconds: 500);

  bool codeSent = false;
  bool successAnimationPlayed = false;
  String? debugInfo;

  @override
  void dispose() {
    emailController.dispose();
    _debouncer.dispose();
    super.dispose();
  }

  Future<void> handleRequestResetCode() async {
    _debouncer.run(() async {
      if (!_formKey.currentState!.validate()) return;

      final email = emailController.text.trim();
      debugPrint("Attempting to send reset code to: $email");

      final authProvider = Provider.of<AuthProvider>(context, listen: false);

      try {
        setState(() => debugInfo = "Sending request to server...");

        final success = await authProvider.requestResetCode(email);

        if (!mounted) return;

        if (success) {
          debugPrint("Reset code request successful for: $email");
          setState(() {
            codeSent = true;
            debugInfo = "Server responded successfully";
          });

          await Future.delayed(const Duration(milliseconds: 300));

          if (!mounted) return;

          setState(() {
            successAnimationPlayed = true;
            debugInfo = "Navigating to reset page";
          });

          // Show success snackbar
          showTopSnackBar(
            Overlay.of(context),
            const CustomSnackBar.success(
              message: "Reset code sent successfully! Check your email",
            ),
          );

          // ✅ Fixed: Use `extra` to pass email (not pathParameters)
          context.goNamed(RouteNames.resetPassword, extra: {'email': email});
        } else {
          debugPrint("Failed to send reset code: ${authProvider.errorMessage}");
          setState(() => debugInfo = "Error: ${authProvider.errorMessage}");

          // Show error snackbar
          showTopSnackBar(
            Overlay.of(context),
            CustomSnackBar.error(
              message: authProvider.errorMessage ?? "Failed to send reset code",
            ),
          );
        }
      } catch (e) {
        debugPrint("Exception in handleRequestResetCode: $e");
        if (mounted) {
          setState(() => debugInfo = "Network error occurred");

          // Show error snackbar
          showTopSnackBar(
            Overlay.of(context),
            const CustomSnackBar.error(
              message: "Network error occurred. Please try again.",
            ),
          );
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 32.0),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 500),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                if (successAnimationPlayed)
                  Lottie.asset(
                    'assets/animations/success_check.json',
                    height: 150,
                    repeat: false,
                  ),

                if (!successAnimationPlayed) ...[
                  const Icon(
                    Icons.lock_reset,
                    color: Colors.lightBlueAccent,
                    size: 60,
                  ),
                  const SizedBox(height: 20),
                  Text(
                    'Forgot Password',
                    style: theme.textTheme.headlineSmall?.copyWith(
                      color: Colors.lightBlueAccent,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    'Enter your registered email to receive a password reset code',
                    style: TextStyle(color: Colors.redAccent),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 30),

                  /// Email input
                  Form(
                    key: _formKey,
                    child: TextFormField(
                      controller: emailController,
                      keyboardType: TextInputType.emailAddress,
                      style: const TextStyle(color: Colors.lightBlueAccent),

                      decoration: InputDecoration(
                        labelText: 'Email Address',
                        hintText: 'example@email.com',
                        hintStyle: const TextStyle(
                          color: Colors.lightBlueAccent,
                        ),
                        labelStyle: const TextStyle(
                          color: Colors.lightBlueAccent,
                        ),
                        filled: true,
                        fillColor: Colors.grey.withOpacity(0.16),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(color: Colors.lightBlueAccent),
                        ),
                        prefixIcon: const Icon(
                          Icons.email,
                          color: Colors.lightBlueAccent,
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 14,
                        ),
                      ),
                      validator: (value) {
                        if (value == null || value.trim().isEmpty) {
                          return 'Email is required';
                        }
                        if (!value.contains('@')) {
                          return 'Enter a valid email';
                        }
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(height: 30),

                  /// Submit button or loader
                  if (auth.isLoading)
                    const SpinKitFadingCircle(
                      color: Colors.lightBlueAccent,
                      size: 50,
                    )
                  else
                    GradientButton(
                      onPressed: handleRequestResetCode,
                      label: 'Send Reset Code',
                    ),

                  const SizedBox(height: 20),

                  /// Debug info
                  if (debugInfo != null)
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16.0),
                      child: Text(
                        debugInfo!,
                        style: const TextStyle(color: Colors.yellow),
                        textAlign: TextAlign.center,
                      ),
                    ),
                ],

                /// Info after code sent
                if (codeSent && !successAnimationPlayed)
                  const Padding(
                    padding: EdgeInsets.only(top: 24.0),
                    child: Text(
                      "Check your email for the reset code. Didn't receive it? Try again in a few minutes.",
                      style: TextStyle(color: Colors.greenAccent),
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

class _Debouncer {
  final int milliseconds;
  Timer? _timer;

  _Debouncer({required this.milliseconds});

  void run(VoidCallback action) {
    _timer?.cancel();
    _timer = Timer(Duration(milliseconds: milliseconds), action);
  }

  void dispose() {
    _timer?.cancel();
  }
}
