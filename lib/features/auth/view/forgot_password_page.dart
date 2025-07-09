// ignore_for_file: curly_braces_in_flow_control_structures

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

  bool codeSent = false;
  bool successAnimationPlayed = false;

  @override
  void dispose() {
    emailController.dispose();
    super.dispose();
  }

  Future<void> handleRequestResetCode() async {
    if (_formKey.currentState?.validate() ?? false) {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      final success = await authProvider.requestResetCode(
        emailController.text.trim(),
      );

      if (success) {
        setState(() {
          codeSent = true;
        });
        await Future.delayed(const Duration(milliseconds: 300));
        setState(() {
          successAnimationPlayed = true;
        });

        // ✅ Navigate to ResetPassword page using GoRouter
        context.go(
          '${RouteNames.resetPassword}?email=${emailController.text.trim()}',
        );
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
                const Text(
                  'Forgot Password',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.lightBlueAccent,
                  ),
                ),
                const SizedBox(height: 20),

                const Text(
                  'Enter your email to receive a reset code',
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
                      hintText: 'example@email.com',
                      hintStyle: const TextStyle(color: Colors.white30),
                      filled: true,
                      fillColor: Colors.white10,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty)
                        return 'Email is required';
                      if (!value.contains('@')) return 'Enter a valid email';
                      return null;
                    },
                  ),
                ),
                const SizedBox(height: 30),

                auth.isLoading
                    ? const SpinKitFadingCircle(
                        color: Colors.lightBlueAccent,
                        size: 50,
                      )
                    : GradientButton(
                        onPressed: handleRequestResetCode,
                        label: 'Send Reset Code',
                      ),
                const SizedBox(height: 20),

                if (auth.errorMessage?.isNotEmpty ?? false)
                  Text(
                    auth.errorMessage!,
                    style: const TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
              ],

              if (codeSent && !successAnimationPlayed)
                const Padding(
                  padding: EdgeInsets.only(top: 24.0),
                  child: Text(
                    "Check your email for the reset code.",
                    style: TextStyle(color: Colors.greenAccent),
                    textAlign: TextAlign.center,
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
