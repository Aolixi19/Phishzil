// ignore_for_file: curly_braces_in_flow_control_structures, use_build_context_synchronously

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:lottie/lottie.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:go_router/go_router.dart';

import '../controller/auth_provider.dart';
import '../../../global_widgets/custom_button.dart';
import '../../../routes/route_names.dart';

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

          // Use named route with encoded parameters
          context.goNamed(
            RouteNames.resetPassword,
            pathParameters: {'email': Uri.encodeComponent(email)},
          );
        } else {
          debugPrint("Failed to send reset code: ${authProvider.errorMessage}");
          setState(() => debugInfo = "Error: ${authProvider.errorMessage}");
        }
      } catch (e) {
        debugPrint("Exception in handleRequestResetCode: $e");
        if (mounted) {
          setState(() => debugInfo = "Network error occurred");
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: const Color(0xFF00172B),
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
                    style: TextStyle(color: Colors.white70),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 30),

                  Form(
                    key: _formKey,
                    child: TextFormField(
                      controller: emailController,
                      keyboardType: TextInputType.emailAddress,
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        labelText: 'Email Address',
                        hintText: 'example@email.com',
                        hintStyle: const TextStyle(color: Colors.white30),
                        labelStyle: const TextStyle(color: Colors.white70),
                        filled: true,
                        fillColor: Colors.white10,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide.none,
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
                        if (value == null || value.isEmpty) {
                          return 'Email is required';
                        }

                        return null;
                      },
                    ),
                  ),
                  const SizedBox(height: 30),

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

                  // Debug information
                  if (debugInfo != null)
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16.0),
                      child: Text(
                        debugInfo!,
                        style: const TextStyle(color: Colors.yellow),
                        textAlign: TextAlign.center,
                      ),
                    ),

                  if (auth.errorMessage?.isNotEmpty ?? false)
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16.0),
                      child: Text(
                        auth.errorMessage!,
                        style: const TextStyle(color: Colors.redAccent),
                        textAlign: TextAlign.center,
                      ),
                    ),
                ],

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
