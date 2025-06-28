import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../routers/phishzil_app_routes.dart';
import '../utils/phishzil_constants.dart';
import '../providers/phishzil_auth_provider.dart';

class PhishzilLoginPage extends ConsumerStatefulWidget {
  const PhishzilLoginPage({super.key});

  @override
  ConsumerState<PhishzilLoginPage> createState() => _PhishzilLoginPageState();
}

class _PhishzilLoginPageState extends ConsumerState<PhishzilLoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  bool _obscurePassword = true;
  bool _rememberMe = false;

  void _showSnack(String message, {bool isError = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
      ),
    );
  }

  Future<void> _handleLogin() async {
    if (_formKey.currentState!.validate()) {
      final identifier = _emailController.text.trim();
      final password = _passwordController.text.trim();

      await ref
          .read(authProvider.notifier)
          .login(identifier, password, _rememberMe);

      final user = FirebaseAuth.instance.currentUser;

      if (user != null && !user.emailVerified) {
        _showSnack(
          "Please verify your email before logging in.",
          isError: true,
        );
        await FirebaseAuth.instance.signOut();
      } else if (user != null && user.emailVerified) {
        _showSnack("Login successful");
        Navigator.pushReplacementNamed(context, AppRoutes.home);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authProvider);

    ref.listen(authProvider, (previous, next) {
      if (next.errorMessage != null) {
        _showSnack(next.errorMessage!, isError: true);
      }
    });

    return SafeArea(
      child: Scaffold(
        body: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [
                PhishzilColors.safeColor,
                Color(0xFF061827),
                Colors.black,
              ],
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
                    const SizedBox(height: 20),
                    Text.rich(
                      TextSpan(
                        text: 'PhishZil',
                        style: TextStyle(
                          fontSize: 24,
                          color: const Color.fromARGB(255, 83, 178, 255),
                          fontWeight: FontWeight.bold,
                        ),
                        children: [
                          WidgetSpan(
                            child: Transform.translate(
                              offset: const Offset(2, -7),
                              child: Text(
                                '™',
                                textScaler: TextScaler.linear(1.40),
                                style: const TextStyle(
                                  color: Color.fromARGB(255, 83, 178, 255),
                                  fontWeight: FontWeight.w400,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 30),
                    Card(
                      color: Colors.transparent,
                      elevation: 6,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(10),
                        child: Form(
                          key: _formKey,
                          child: Column(
                            children: [
                              TextFormField(
                                controller: _emailController,
                                style: const TextStyle(color: Colors.white),
                                decoration: InputDecoration(
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(26),
                                  ),
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                      color: PhishzilColors.secondary,
                                      width: 2.0,
                                    ),
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  prefixIcon: Icon(
                                    Icons.person,
                                    color: PhishzilColors.secondary,
                                  ),
                                  hintText: "Enter email or username",
                                  hintStyle: const TextStyle(
                                    color: Colors.white60,
                                  ),
                                  labelText: "Username or Email",
                                  labelStyle: TextStyle(
                                    color: PhishzilColors.secondary,
                                  ),
                                ),
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Please enter email or username';
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 20),
                              TextFormField(
                                controller: _passwordController,
                                obscureText: _obscurePassword,
                                style: const TextStyle(color: Colors.white),
                                decoration: InputDecoration(
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(26),
                                  ),
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                      color: PhishzilColors.secondary,
                                      width: 2.0,
                                    ),
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  prefixIcon: Icon(
                                    Icons.lock,
                                    color: PhishzilColors.secondary,
                                  ),
                                  suffixIcon: IconButton(
                                    icon: Icon(
                                      _obscurePassword
                                          ? Icons.visibility
                                          : Icons.visibility_off,
                                      color: PhishzilColors.secondary,
                                    ),
                                    onPressed: () {
                                      setState(() {
                                        _obscurePassword = !_obscurePassword;
                                      });
                                    },
                                  ),
                                  hintText: "Enter your password",
                                  hintStyle: const TextStyle(
                                    color: Colors.white60,
                                  ),
                                  labelText: "Password",
                                  labelStyle: TextStyle(
                                    color: PhishzilColors.secondary,
                                  ),
                                ),
                                validator: (value) {
                                  if (value == null || value.length < 6) {
                                    return 'Password must be at least 6 characters';
                                  }
                                  return null;
                                },
                              ),
                              const SizedBox(height: 10),
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Row(
                                    children: [
                                      Checkbox(
                                        value: _rememberMe,
                                        activeColor: PhishzilColors.secondary,
                                        checkColor: Colors.white,
                                        onChanged: (val) {
                                          setState(() {
                                            _rememberMe = val!;
                                          });
                                        },
                                      ),
                                      Text(
                                        "Remember Me",
                                        style: TextStyle(
                                          color: PhishzilColors.secondary,
                                          fontSize: 13.0,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ],
                                  ),
                                  TextButton(
                                    onPressed: () {
                                      Navigator.pushNamed(
                                        context,
                                        AppRoutes.reset,
                                      );
                                    },
                                    child: Text(
                                      "Forgot Password?",
                                      style: TextStyle(
                                        color: PhishzilColors.secondary,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 13.0,
                                        decoration: TextDecoration.underline,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 20),
                              GestureDetector(
                                onTap: auth.isLoading ? null : _handleLogin,
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
                                            "Login",
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
                    const SizedBox(height: 15),
                    const Text(
                      "-- OR continue with --",
                      style: TextStyle(color: Colors.lightBlue),
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            shape: const CircleBorder(),
                            padding: const EdgeInsets.all(15),
                            backgroundColor: Colors.white,
                          ),
                          child: AuthImage(imageAsset: PhishzilAssets.apple),
                        ),
                        const SizedBox(width: 30),
                        ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            shape: const CircleBorder(),
                            padding: const EdgeInsets.all(15),
                            backgroundColor: Colors.white,
                          ),
                          child: AuthImage(imageAsset: PhishzilAssets.google),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text(
                          "Don't have an account?",
                          style: TextStyle(color: Colors.lightBlue),
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, AppRoutes.signup);
                          },
                          child: Text(
                            "Sign Up",
                            style: TextStyle(
                              color: PhishzilColors.secondary,
                              fontSize: 14,
                              decoration: TextDecoration.underline,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
