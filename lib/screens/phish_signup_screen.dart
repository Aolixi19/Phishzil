import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../utils/phishzil_constants.dart';
import '../providers/phishzil_auth_provider.dart';
import '../routers/phishzil_app_routes.dart';

class PhishzilSignUpPage extends ConsumerStatefulWidget {
  const PhishzilSignUpPage({super.key});

  @override
  ConsumerState<PhishzilSignUpPage> createState() => _PhishzilSignUpPageState();
}

class _PhishzilSignUpPageState extends ConsumerState<PhishzilSignUpPage> {
  final _formKey = GlobalKey<FormState>();
  final _username = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _confirmPassword = TextEditingController();

  bool _obscurePassword = true;
  bool _agreedToTerms = false;

  String _passwordStrength = "";

  @override
  void dispose() {
    _username.dispose();
    _email.dispose();
    _password.dispose();
    _confirmPassword.dispose();
    super.dispose();
  }

  void _updatePasswordStrength(String password) {
    setState(() {
      if (password.length < 6) {
        _passwordStrength = "Weak";
      } else if (password.length < 10) {
        _passwordStrength = "Medium";
      } else {
        _passwordStrength = "Strong";
      }
    });
  }

  void _showSnack(String msg, {bool isError = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: isError ? Colors.red : Colors.green,
      ),
    );
  }

  Future<void> _handleSignUp() async {
    if (!_agreedToTerms) {
      _showSnack("You must agree to the Terms and Conditions", isError: true);
      return;
    }

    if (_formKey.currentState!.validate()) {
      await ref
          .read(authProvider.notifier)
          .signUp(
            _username.text.trim(),
            _email.text.trim(),
            _password.text.trim(),
          );
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authProvider);

    ref.listen(authProvider, (prev, next) {
      if (next.errorMessage != null) {
        if (next.errorMessage!.contains("verify your email")) {
          _showSnack("Signup successful! Redirecting to verify...");
          Future.delayed(const Duration(seconds: 2), () {
            Navigator.pushReplacementNamed(context, AppRoutes.verifyEmail);
          });
        } else {
          _showSnack(next.errorMessage!, isError: true);
        }
      }
    });

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [PhishzilColors.safeColor, Color(0xFF061827), Colors.black],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 420),
              child: Column(
                children: [
                  Hero(
                    tag: "tag",
                    child: Image.asset(
                      PhishzilAssets.loginLogo,
                      height: 100,
                      width: 100,
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    "Create Account",
                    style: TextStyle(
                      color: Colors.lightBlueAccent,
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  Card(
                    elevation: 8,
                    color: Colors.transparent,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Form(
                        key: _formKey,
                        child: Column(
                          children: [
                            _buildTextField(
                              controller: _username,
                              label: "Username",
                              hint: "Enter your Username",
                              icon: Icons.person,
                              validator: (val) =>
                                  val == null || val.trim().isEmpty
                                  ? "Username is required"
                                  : null,
                            ),
                            const SizedBox(height: 20),
                            _buildTextField(
                              controller: _email,
                              label: "Email",
                              hint: "Enter your Email",
                              icon: Icons.email,
                              validator: (val) =>
                                  val == null || !val.contains('@')
                                  ? "Enter a valid email"
                                  : null,
                            ),
                            const SizedBox(height: 20),
                            _buildTextField(
                              controller: _password,
                              label: "Password",
                              hint: "Enter your Password",
                              icon: Icons.lock,
                              obscureText: _obscurePassword,
                              validator: (val) => val == null || val.length < 6
                                  ? "Min. 6 characters"
                                  : null,
                              suffixIcon: IconButton(
                                icon: Icon(
                                  _obscurePassword
                                      ? Icons.visibility
                                      : Icons.visibility_off,
                                  color: PhishzilColors.secondary,
                                ),
                                onPressed: () {
                                  setState(
                                    () => _obscurePassword = !_obscurePassword,
                                  );
                                },
                              ),
                            ),
                            const SizedBox(height: 6),
                            Align(
                              alignment: Alignment.centerLeft,
                              child: Text(
                                "Strength: $_passwordStrength",
                                style: TextStyle(
                                  color: _passwordStrength == "Strong"
                                      ? Colors.green
                                      : _passwordStrength == "Medium"
                                      ? Colors.orange
                                      : Colors.red,
                                ),
                              ),
                            ),
                            const SizedBox(height: 20),
                            _buildTextField(
                              controller: _confirmPassword,
                              label: "Confirm Password",
                              hint: "Re-enter your Password",
                              icon: Icons.lock_outline,
                              obscureText: true,
                              validator: (val) => val != _password.text
                                  ? "Passwords do not match"
                                  : null,
                            ),
                            const SizedBox(height: 15),
                            Row(
                              children: [
                                Checkbox(
                                  value: _agreedToTerms,
                                  activeColor: PhishzilColors.secondary,
                                  onChanged: (val) {
                                    setState(
                                      () => _agreedToTerms = val ?? false,
                                    );
                                  },
                                ),
                                Expanded(
                                  child: GestureDetector(
                                    onTap: () =>
                                        Navigator.pushNamed(context, "/terms"),
                                    child: Text.rich(
                                      TextSpan(
                                        text: "I agree to the ",
                                        style: const TextStyle(
                                          color: Colors.white70,
                                          fontSize: 13,
                                        ),
                                        children: [
                                          TextSpan(
                                            text: "Terms & Conditions",
                                            style: TextStyle(
                                              color: PhishzilColors.secondary,
                                              decoration:
                                                  TextDecoration.underline,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 10),
                            GestureDetector(
                              onTap: auth.isLoading ? null : _handleSignUp,
                              child: Container(
                                width: double.infinity,
                                padding: const EdgeInsets.symmetric(
                                  vertical: 15,
                                ),
                                decoration: BoxDecoration(
                                  gradient: const LinearGradient(
                                    colors: [
                                      Color(0xFF00B4DB),
                                      Color(0xFF0083B0),
                                    ],
                                  ),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Center(
                                  child: auth.isLoading
                                      ? const CircularProgressIndicator(
                                          color: Colors.white,
                                        )
                                      : const Text(
                                          "Sign Up",
                                          style: TextStyle(
                                            fontSize: 18,
                                            color: Colors.white,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  TextButton(
                    onPressed: () => Navigator.pushReplacementNamed(
                      context,
                      AppRoutes.login,
                    ),
                    child: Text(
                      "Already have an account? Login",
                      style: TextStyle(
                        color: PhishzilColors.secondary,
                        fontSize: 14,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required String hint,
    required IconData icon,
    bool obscureText = false,
    Widget? suffixIcon,
    required String? Function(String?) validator,
  }) {
    return TextFormField(
      controller: controller,
      obscureText: obscureText,
      onChanged: label == "Password"
          ? (val) => _updatePasswordStrength(val)
          : null,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        labelStyle: TextStyle(color: PhishzilColors.secondary),
        hintStyle: const TextStyle(color: Colors.white60),
        prefixIcon: Icon(icon, color: PhishzilColors.secondary),
        suffixIcon: suffixIcon,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(26)),
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(color: PhishzilColors.secondary, width: 2),
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      validator: validator,
    );
  }
}
