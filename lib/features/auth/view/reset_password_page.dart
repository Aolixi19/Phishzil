// ignore_for_file: use_build_context_synchronously

import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

import '../controller/auth_provider.dart';
import 'package:phishzil/global_widgets/custom_button.dart';
import 'package:phishzil/routes/route_names.dart';

class ResetPasswordPage extends StatefulWidget {
  final String email;

  const ResetPasswordPage({super.key, required this.email});

  @override
  State<ResetPasswordPage> createState() => _ResetPasswordPageState();
}

class _ResetPasswordPageState extends State<ResetPasswordPage> {
  final _formKey = GlobalKey<FormState>();
  final codeController = TextEditingController();
  final passwordController = TextEditingController();
  final _debouncer = _Debouncer(milliseconds: 500);

  bool _obscurePassword = true;
  Timer? _resendTimer;
  int _secondsRemaining = 180;
  bool _canResend = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      debugPrint("Reset page received email: ${widget.email}");
      _startResendTimer();
    });
  }

  @override
  void dispose() {
    _resendTimer?.cancel();
    codeController.dispose();
    passwordController.dispose();
    _debouncer.dispose();
    super.dispose();
  }

  void _startResendTimer() {
    setState(() {
      _secondsRemaining = 180;
      _canResend = false;
    });

    _resendTimer?.cancel();
    _resendTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_secondsRemaining <= 0) {
        timer.cancel();
        setState(() => _canResend = true);
      } else {
        // Only update UI every 5 seconds to reduce rebuilds
        if (_secondsRemaining % 5 == 0 || _secondsRemaining <= 5) {
          setState(() => _secondsRemaining--);
        } else {
          _secondsRemaining--;
        }
      }
    });
  }

  Future<void> _resendCode() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final email = widget.email.trim();
    debugPrint("Resending code to: $email");

    final success = await authProvider.resendResetCode(email);
    if (!mounted) return;

    if (success) {
      _startResendTimer();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Verification code resent to your email.'),
          backgroundColor: Colors.green,
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(authProvider.errorMessage ?? 'Failed to resend code'),
          backgroundColor: Colors.redAccent,
        ),
      );
    }
  }

  void _togglePasswordVisibility() {
    setState(() => _obscurePassword = !_obscurePassword);
  }

  Future<void> handleResetPassword() async {
    _debouncer.run(() async {
      if (!_formKey.currentState!.validate()) return;

      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      final email = widget.email.trim();
      final code = codeController.text.trim();

      final verified = await authProvider.verifyResetCode(email, code);
      if (!verified || !mounted) return;

      final success = await authProvider.resetPassword(
        email,
        passwordController.text,
        code,
      );

      if (success && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Password reset successful. Please login.'),
            backgroundColor: Colors.green,
          ),
        );
        context.go(RouteNames.login);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);

    return Scaffold(
      backgroundColor: const Color(0xFF0D1B2A),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 450),
            child: Form(
              key: _formKey,
              child: Column(
                children: [
                  const Icon(
                    Icons.lock_reset,
                    color: Colors.cyanAccent,
                    size: 60,
                  ),
                  const SizedBox(height: 20),
                  Text(
                    'Reset Password',
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      color: Colors.cyanAccent,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    'Enter the code sent to ${widget.email} and set a new password',
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white70),
                  ),
                  const SizedBox(height: 30),

                  _buildCodeInputField(),
                  const SizedBox(height: 20),

                  _buildPasswordInputField(),
                  const SizedBox(height: 15),

                  _buildResendButton(),
                  const SizedBox(height: 20),

                  GradientButton(
                    onPressed: handleResetPassword,
                    label: 'Reset Password',
                    isLoading: auth.isLoading,
                  ),
                  if (auth.errorMessage?.isNotEmpty ?? false) ...[
                    const SizedBox(height: 20),
                    Text(
                      auth.errorMessage!,
                      style: const TextStyle(color: Colors.redAccent),
                    ),
                  ],
                  const SizedBox(height: 20),
                  _buildBackToLoginButton(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildCodeInputField() {
    return TextFormField(
      controller: codeController,
      keyboardType: TextInputType.number,
      style: const TextStyle(color: Colors.white),
      validator: (value) {
        if (value == null || value.isEmpty) return 'Code is required';
        if (value.length != 6) return 'Must be 6 digits';
        return null;
      },
      decoration: InputDecoration(
        labelText: 'Verification Code',
        hintText: '6-digit code',
        hintStyle: const TextStyle(color: Colors.white30),
        labelStyle: const TextStyle(color: Colors.white70),
        prefixIcon: const Icon(Icons.verified, color: Colors.cyanAccent),
        filled: true,
        fillColor: Colors.white10,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }

  Widget _buildPasswordInputField() {
    return TextFormField(
      controller: passwordController,
      obscureText: _obscurePassword,
      style: const TextStyle(color: Colors.white),
      validator: (value) {
        if (value == null || value.isEmpty) return 'Password is required';
        if (value.length < 6) return 'At least 6 characters';
        return null;
      },
      decoration: InputDecoration(
        labelText: 'New Password',
        hintText: 'Create new password',
        hintStyle: const TextStyle(color: Colors.white30),
        labelStyle: const TextStyle(color: Colors.white70),
        prefixIcon: const Icon(Icons.lock, color: Colors.cyanAccent),
        suffixIcon: IconButton(
          icon: Icon(
            _obscurePassword ? Icons.visibility_off : Icons.visibility,
            color: Colors.cyanAccent,
          ),
          onPressed: _togglePasswordVisibility,
        ),
        filled: true,
        fillColor: Colors.white10,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }

  Widget _buildResendButton() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        if (_canResend)
          TextButton(
            onPressed: _resendCode,
            child: const Text(
              'Resend Code',
              style: TextStyle(color: Colors.cyanAccent),
            ),
          )
        else
          Text(
            'Resend in ${_secondsRemaining ~/ 60}:${(_secondsRemaining % 60).toString().padLeft(2, '0')}',
            style: const TextStyle(color: Colors.white54),
          ),
      ],
    );
  }

  Widget _buildBackToLoginButton() {
    return TextButton(
      onPressed: () => context.go(RouteNames.login),
      child: const Text(
        '← Back to Login',
        style: TextStyle(color: Colors.cyanAccent),
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
