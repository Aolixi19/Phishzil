// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';

import '../controller/auth_provider.dart';
import '../../../global_widgets/custom_button.dart';
import '../../../routes/route_names.dart';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController nameController;
  late final TextEditingController usernameController;
  late final TextEditingController emailController;
  late final TextEditingController passwordController;
  late final TextEditingController confirmPasswordController;

  bool _agreeToTerms = false;
  double _passwordStrength = 0.0;
  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;

  @override
  void initState() {
    super.initState();
    nameController = TextEditingController();
    usernameController = TextEditingController();
    emailController = TextEditingController();
    passwordController = TextEditingController();
    confirmPasswordController = TextEditingController();

    passwordController.addListener(() {
      setState(() {
        _passwordStrength = _calculatePasswordStrength(passwordController.text);
      });
    });
  }

  @override
  void dispose() {
    nameController.dispose();
    usernameController.dispose();
    emailController.dispose();
    passwordController.dispose();
    confirmPasswordController.dispose();
    super.dispose();
  }

  void handleSignup() async {
    if ((_formKey.currentState?.validate() ?? false)) {
      if (!_agreeToTerms) {
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: const Text('Terms Required'),
            content: const Text(
              'You must accept the terms and conditions to continue.',
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('OK'),
              ),
            ],
          ),
        );
        return;
      }

      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      await authProvider.signup(
        name: nameController.text.trim(),
        username: usernameController.text.trim(),
        email: emailController.text.trim(),
        password: passwordController.text.trim(),
      );

      if (authProvider.errorMessage == null) {
        // ✅ Check for verification step
        if (authProvider.nextAction == 'verify') {
          context.go(
            RouteNames.verify,
            extra: {'email': emailController.text.trim()},
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Signup successful ✅"),
              backgroundColor: Colors.green,
            ),
          );
          context.go(RouteNames.login);
        }
      }
    }
  }

  double _calculatePasswordStrength(String password) {
    if (password.isEmpty) return 0;
    double strength = 0;
    if (password.length >= 6) strength += 0.3;
    if (password.contains(RegExp(r'[A-Z]'))) strength += 0.2;
    if (password.contains(RegExp(r'[0-9]'))) strength += 0.2;
    if (password.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'))) strength += 0.3;
    return strength.clamp(0.0, 1.0);
  }

  String _passwordHint() {
    if (_passwordStrength < 0.3) {
      return 'Weak: Add numbers, uppercase, and special characters';
    } else if (_passwordStrength < 0.7) {
      return 'Medium: Try more characters or symbols';
    } else {
      return 'Strong password ✅';
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
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Center(
                  child: Text(
                    'Create Account',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.lightBlueAccent,
                    ),
                  ),
                ),
                const SizedBox(height: 40),

                _buildLabel('Full Name'),
                _buildTextField(
                  controller: nameController,
                  hint: 'John Doe',
                  validator: (v) => v!.isEmpty ? 'Name is required' : null,
                ),
                const SizedBox(height: 20),

                _buildLabel('Username'),
                _buildTextField(
                  controller: usernameController,
                  hint: 'john_doe',
                  validator: (v) => v!.isEmpty ? 'Username is required' : null,
                ),
                const SizedBox(height: 20),

                _buildLabel('Email'),
                _buildTextField(
                  controller: emailController,
                  hint: 'example@email.com',
                  keyboardType: TextInputType.emailAddress,
                  validator: (v) {
                    if (v!.isEmpty) return 'Email is required';
                    if (!v.contains('@')) return 'Enter a valid email';
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                _buildLabel('Password'),
                _buildTextField(
                  controller: passwordController,
                  hint: 'Create a password',
                  obscureText: _obscurePassword,
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscurePassword
                          ? Icons.visibility_off
                          : Icons.visibility,
                      color: Colors.white54,
                    ),
                    onPressed: () {
                      setState(() => _obscurePassword = !_obscurePassword);
                    },
                  ),
                  validator: (v) {
                    if (v!.isEmpty) return 'Password is required';
                    if (v.length < 6) {
                      return 'Password must be at least 6 characters';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 8),

                LinearProgressIndicator(
                  value: _passwordStrength,
                  minHeight: 6,
                  backgroundColor: Colors.white10,
                  color: _passwordStrength <= 0.4
                      ? Colors.red
                      : _passwordStrength <= 0.7
                      ? Colors.orange
                      : Colors.green,
                ),
                const SizedBox(height: 6),
                Text(
                  _passwordHint(),
                  style: const TextStyle(color: Colors.white70),
                ),
                const SizedBox(height: 20),

                _buildLabel('Confirm Password'),
                _buildTextField(
                  controller: confirmPasswordController,
                  hint: 'Repeat password',
                  obscureText: _obscureConfirmPassword,
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscureConfirmPassword
                          ? Icons.visibility_off
                          : Icons.visibility,
                      color: Colors.white54,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscureConfirmPassword = !_obscureConfirmPassword;
                      });
                    },
                  ),
                  validator: (v) {
                    if (v != passwordController.text) {
                      return 'Passwords do not match';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                Row(
                  children: [
                    Checkbox(
                      value: _agreeToTerms,
                      onChanged: (v) =>
                          setState(() => _agreeToTerms = v ?? false),
                      activeColor: Colors.lightBlueAccent,
                    ),
                    const Text(
                      'I agree to the ',
                      style: TextStyle(color: Colors.white70),
                    ),
                    GestureDetector(
                      onTap: () => context.push(RouteNames.terms),
                      child: const Text(
                        'Terms and Conditions',
                        style: TextStyle(
                          color: Colors.lightBlueAccent,
                          decoration: TextDecoration.underline,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 10),

                GradientButton(
                  onPressed: handleSignup,
                  label: 'Sign Up',
                  isLoading: auth.isLoading,
                ),
                const SizedBox(height: 20),

                if ((auth.errorMessage ?? '').isNotEmpty)
                  Center(
                    child: Text(
                      auth.errorMessage!,
                      style: const TextStyle(color: Colors.red),
                    ),
                  ),
                const SizedBox(height: 30),

                Center(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        "Already have an account? ",
                        style: TextStyle(color: Colors.white70),
                      ),
                      GestureDetector(
                        onTap: () => context.go(RouteNames.login),
                        child: const Text(
                          'Login',
                          style: TextStyle(
                            color: Colors.lightBlueAccent,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLabel(String label) {
    return Text(
      label,
      style: const TextStyle(color: Colors.white70, fontSize: 16),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String hint,
    bool obscureText = false,
    TextInputType keyboardType = TextInputType.text,
    String? Function(String?)? validator,
    Widget? suffixIcon,
  }) {
    return TextFormField(
      controller: controller,
      obscureText: obscureText,
      keyboardType: keyboardType,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: const TextStyle(color: Colors.white30),
        suffixIcon: suffixIcon,
        filled: true,
        fillColor: Colors.white10,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
      ),
      validator: validator,
    );
  }
}
