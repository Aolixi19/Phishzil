// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart' show GoRouterHelper;
import 'package:top_snackbar_flutter/top_snack_bar.dart';
import 'package:top_snackbar_flutter/custom_snack_bar.dart';
import 'package:lottie/lottie.dart';
import 'dart:io';

import '../controller/auth_provider.dart';
import 'package:phishzil/global_widgets/custom_button.dart';
import '../../../routes/route_names.dart';

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
      context.push(
        RouteNames.login,
      ); // Redirect to signup if Google login fails
      showTopSnackBar(
        Overlay.of(context),
        const CustomSnackBar.error(
          message:
              'Google login failed, please  check your internet Connection.',
        ),
      );
    }
  }
  /*
  Future<void> handleAppleSignIn() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    await authProvider.loginWithApple();

    if (authProvider.isAuthenticated) {
      showTopSnackBar(
        Overlay.of(context),
        const CustomSnackBar.success(message: 'Signed in with Apple ✅'),
      );
      context.go(RouteNames.dashboard);
    } else if ((authProvider.errorMessage ?? '').isNotEmpty) {
      showTopSnackBar(
        Overlay.of(context),
        CustomSnackBar.error(message: authProvider.errorMessage!),
      );
    }
  }
  */

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);

    return Scaffold(
      backgroundColor: const Color(0xFF00172B),
      body: GestureDetector(
        onTap: () => FocusScope.of(context).unfocus(),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 10.0),
                  Center(
                    child: LottieBuilder.asset(
                      'assets/animations/Security000-Purple.json',
                      height: 150,
                      width: 150,
                      repeat: true,
                    ),
                  ),
                  const SizedBox(height: 30.0),
                  const Center(
                    child: Text(
                      'PhishZil Login',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.lightBlueAccent,
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    'Email',
                    style: TextStyle(color: Colors.white70, fontSize: 16),
                  ),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: emailController,
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
                  const Text(
                    'Password',
                    style: TextStyle(color: Colors.white70, fontSize: 16),
                  ),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: passwordController,
                    obscureText: _obscurePassword,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Enter your password',
                      hintStyle: const TextStyle(color: Colors.white30),
                      filled: true,
                      fillColor: Colors.white10,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                      suffixIcon: IconButton(
                        icon: Icon(
                          _obscurePassword
                              ? Icons.visibility_off
                              : Icons.visibility,
                          color: Colors.white54,
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
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Checkbox(
                            value: rememberMe,
                            activeColor: Colors.lightBlueAccent,
                            onChanged: (value) {
                              setState(() {
                                rememberMe = value ?? false;
                              });
                            },
                          ),
                          const Text(
                            'Remember Me',
                            style: TextStyle(color: Colors.white70),
                          ),
                        ],
                      ),
                      TextButton(
                        onPressed: () {
                          context.push(RouteNames.forgotPassword);
                        },
                        child: const Text(
                          'Forgot Password?',
                          style: TextStyle(color: Colors.lightBlueAccent),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 30),
                  GradientButton(
                    onPressed: handleLogin,
                    label: 'Login',
                    isLoading: auth.isLoading,
                  ),
                  const SizedBox(height: 30),

                  /// Social Login Section
                  if ((auth.errorMessage ?? '').isNotEmpty)
                    const SizedBox(height: 10),

                  Center(
                    child: Text(
                      '--- Or continue with ---',
                      style: TextStyle(color: Colors.white70, fontSize: 16),
                    ),
                  ),
                  const SizedBox(height: 20),

                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        color: Colors.lightBlueAccent,
                        tooltip: 'Sign in with Google',
                        icon: Image.asset(
                          'assets/icons/icons8-google-48.png',
                          width: 40,
                          height: 40,
                        ),
                        onPressed: handleGoogleSignIn,
                      ),
                      const SizedBox(width: 20),
                      if (Platform.isIOS || Platform.isMacOS)
                        IconButton(
                          icon: Image.asset(
                            'assets/icons/icons8-apple-50.png',
                            width: 40,
                            height: 40,
                          ),
                          onPressed: () {},
                        ),
                    ],
                  ),
                  const SizedBox(height: 30),

                  Center(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text(
                          "Don't have an account? ",
                          style: TextStyle(color: Colors.white70),
                        ),
                        GestureDetector(
                          onTap: () {
                            context.push(RouteNames.signup);
                          },
                          child: const Text(
                            'Sign Up',
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
      ),
    );
  }
}
