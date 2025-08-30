// ignore_for_file: use_build_context_synchronously

import 'dart:io';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lottie/lottie.dart';
import 'package:provider/provider.dart';
import 'package:top_snackbar_flutter/top_snack_bar.dart';
import 'package:top_snackbar_flutter/custom_snack_bar.dart';

import '../phishzil_auth/phishzil_auth_provider.dart';
import '../phishzil_global_widget/phishzil_button.dart';
import '../phishzil_routes/phishzil_route_name.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController emailController;
  late final TextEditingController passwordController;
  bool rememberMe = false;
  bool _obscurePassword = true;

  @override
  void initState() {
    super.initState();
    emailController = TextEditingController();
    passwordController = TextEditingController();
  }

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  void handleLogin() async {
    if ((_formKey.currentState?.validate() ?? false)) {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      await authProvider.login(
        identifier: emailController.text.trim(),
        password: passwordController.text,
      );

      if (authProvider.isAuthenticated) {
        showTopSnackBar(
          Overlay.of(context),
          const CustomSnackBar.success(message: 'Login successful ✅'),
        );
        context.go(RouteNames.dashboard);
      } else if ((authProvider.errorMessage ?? '').isNotEmpty) {
        showTopSnackBar(
          Overlay.of(context),
          CustomSnackBar.error(message: authProvider.errorMessage!),
        );
      }
    }
  }

  Future<void> handleGoogleSignIn() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    await authProvider.loginWithGoogle();

    if (authProvider.isAuthenticated) {
      showTopSnackBar(
        Overlay.of(context),
        const CustomSnackBar.success(message: 'Signed in with Google ✅'),
      );
      context.go(RouteNames.dashboard);
    } else if ((authProvider.errorMessage ?? '').isNotEmpty) {
      showTopSnackBar(
        Overlay.of(context),
        CustomSnackBar.error(message: authProvider.errorMessage!),
      );
    } else {
      context.push(RouteNames.login);
      showTopSnackBar(
        Overlay.of(context),
        const CustomSnackBar.error(
          message:
              'Google login failed, please check your internet connection.',
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);

    return Scaffold(
      backgroundColor: Colors.white,
      body: GestureDetector(
        onTap: () => FocusScope.of(context).unfocus(),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Form(
              key: _formKey,
              child: Column(
                children: [
                  const SizedBox(height: 10.0),

                  // Logo
                  Container(
                    width: 70,
                    height: 70,
                    padding: const EdgeInsets.all(13),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [
                          Colors.blue,
                          Colors.lightBlueAccent,
                          Colors.green,
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(15),
                    ),
                    child: Image.asset(
                      'assets/images/logo.png',
                      color: Colors.white,
                    ),
                  ),

                  const SizedBox(height: 20),
                  const Text(
                    'PhishZil™ Login',
                    style: TextStyle(
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                      color: Colors.lightBlue,
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Email Field
                  TextFormField(
                    controller: emailController,
                    style: const TextStyle(color: Colors.black),
                    decoration: InputDecoration(
                      hintText: 'example@email.com',
                      hintStyle: const TextStyle(color: Colors.black38),
                      filled: true,
                      fillColor: Colors.grey.shade100,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Email is required';
                      }
                      if (!value.contains('@')) {
                        return 'Enter a valid email';
                      }
                      return null;
                    },
                  ),

                  const SizedBox(height: 20),

                  // Password Field
                  TextFormField(
                    controller: passwordController,
                    obscureText: _obscurePassword,
                    style: const TextStyle(color: Colors.black),
                    decoration: InputDecoration(
                      hintText: 'Enter your password',
                      hintStyle: const TextStyle(color: Colors.black38),
                      filled: true,
                      fillColor: Colors.grey.shade100,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                      suffixIcon: IconButton(
                        icon: Icon(
                          _obscurePassword
                              ? Icons.visibility_off
                              : Icons.visibility,
                          color: Colors.grey,
                        ),
                        onPressed: () {
                          setState(() {
                            _obscurePassword = !_obscurePassword;
                          });
                        },
                      ),
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Password is required';
                      }
                      if (value.length < 6) {
                        return 'Password must be at least 6 characters';
                      }
                      return null;
                    },
                  ),

                  const SizedBox(height: 10),

                  // Remember Me & Forgot Password
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Checkbox(
                            value: rememberMe,
                            activeColor: Colors.lightBlue,
                            onChanged: (value) {
                              setState(() {
                                rememberMe = value ?? false;
                              });
                            },
                          ),
                          const Text(
                            'Remember Me',
                            style: TextStyle(color: Colors.black87),
                          ),
                        ],
                      ),
                      TextButton(
                        onPressed: () {
                          context.push(RouteNames.forgotPassword);
                        },
                        child: const Text(
                          'Forgot Password?',
                          style: TextStyle(color: Colors.blue),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 20),

                  // Login Button
                  GradientButton(
                    onPressed: handleLogin,
                    label: 'Login',
                    isLoading: auth.isLoading,
                    gradient: const LinearGradient(
                      colors: [Colors.lightBlueAccent, Colors.blue],
                    ),
                    textColor: Colors.white,
                  ),

                  const SizedBox(height: 30),

                  const Text(
                    '--- Or continue with ---',
                    style: TextStyle(color: Colors.black54),
                  ),

                  const SizedBox(height: 20),

                  // Google Sign-In
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        tooltip: 'Sign in with Google',
                        icon: Image.asset(
                          'assets/icons/icons8-google-48-2.png',
                          width: 40,
                          height: 40,
                        ),
                        onPressed: handleGoogleSignIn,
                      ),
                      const SizedBox(width: 20),
                      if (Platform.isIOS || Platform.isMacOS)
                        IconButton(
                          icon: const Icon(Icons.apple, size: 40),
                          onPressed: () {},
                        ),
                    ],
                  ),

                  const SizedBox(height: 20),

                  // Sign Up Link
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        "Don't have an account? ",
                        style: TextStyle(color: Colors.black87),
                      ),
                      GestureDetector(
                        onTap: () {
                          context.push(RouteNames.signup);
                        },
                        child: const Text(
                          'Sign Up',
                          style: TextStyle(
                            color: Colors.blueAccent,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 30),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
