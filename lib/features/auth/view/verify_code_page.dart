import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

import '../controller/auth_provider.dart';
import '../../../global_widgets/custom_button.dart';
import '../../../routes/route_names.dart'; // for RouteNames.login

class VerifyCodePage extends StatefulWidget {
  final String email;

  const VerifyCodePage({super.key, required this.email});

  @override
  State<VerifyCodePage> createState() => _VerifyCodePageState();
}

class _VerifyCodePageState extends State<VerifyCodePage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController codeController = TextEditingController();
  String? localError;

  @override
  void initState() {
    super.initState();
    assert(
      widget.email.trim().isNotEmpty,
      'Email must not be empty for VerifyCodePage',
    );
  }

  @override
  void dispose() {
    codeController.dispose();
    super.dispose();
  }

  Future<void> handleVerifyCode() async {
    if (_formKey.currentState?.validate() ?? false) {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      final success = await authProvider.verifyCode(
        widget.email.trim(),
        codeController.text.trim(),
      );

      if (success) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Verification successful ✅')),
        );

        /// ✅ Replace current route with login page
        context.go(RouteNames.login);
      } else {
        setState(() => localError = authProvider.errorMessage);
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
                const Text(
                  'Enter the 6-digit code sent to your email',
                  style: TextStyle(color: Colors.white70),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 30),

                /// Code Input Field
                TextFormField(
                  controller: codeController,
                  keyboardType: TextInputType.number,
                  maxLength: 6,
                  style: const TextStyle(
                    color: Colors.white,
                    letterSpacing: 2.0,
                  ),
                  decoration: InputDecoration(
                    hintText: 'Enter code',
                    hintStyle: const TextStyle(color: Colors.white30),
                    filled: true,
                    fillColor: Colors.white10,
                    counterText: '',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Code is required';
                    }
                    if (value.length != 6) {
                      return 'Enter a 6-digit code';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 30),

                /// Verify Button
                GradientButton(
                  onPressed: handleVerifyCode,
                  label: 'Verify Code',
                  isLoading: auth.isLoading,
                ),
                const SizedBox(height: 20),

                /// Error Message
                if (localError != null && localError!.isNotEmpty)
                  Text(localError!, style: const TextStyle(color: Colors.red)),

                const SizedBox(height: 30),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
