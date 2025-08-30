import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:phishzil/phishzil_dashboard/phishzil_dashboard.dart';
import 'package:phishzil/phishzil_forms/phishzil_forgotten_verify.dart';
import 'package:phishzil/phishzil_forms/phishzil_reset.dart';
import 'package:phishzil/phishzil_forms/phishzil_signup_verify.dart';
import 'package:phishzil/phishzil_forms/phishzil_terms_page.dart';
import 'package:phishzil/phishzil_routes/phishzil_route_name.dart';
import '../phishzil_forms/phishzil_login.dart';
import '../phishzil_forms/phishzil_signup.dart';
import '../phishzil_forms/phishzil_forgotten.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: '/login',
  debugLogDiagnostics: true,
  routes: [
    GoRoute(
      path: '/login',
      name: RouteNames.login,
      builder: (context, state) => const LoginPage(),
    ),
    GoRoute(
      path: '/signup',
      name: RouteNames.signup,
      builder: (context, state) => const SignupPage(),
    ),
    GoRoute(
      path: '/forgot-password',
      name: RouteNames.forgotPassword,
      builder: (context, state) => const ForgotPasswordPage(),
    ),
    GoRoute(
      path: '/verify-code',
      name: RouteNames.verifyCode,
      builder: (context, state) {
        final email = (state.extra as Map<String, dynamic>?)?['email'] ?? '';
        return VerifyCodePage(email: email);
      },
    ),
    GoRoute(
      path: '/reset-password',
      name: RouteNames.resetPassword,
      builder: (context, state) {
        final email = (state.extra as Map<String, dynamic>?)?['email'] ?? '';
        return ResetPasswordPage(email: email);
      },
    ),
    GoRoute(
      path: '/verify',
      name: RouteNames.verify,
      builder: (context, state) {
        final email = (state.extra as Map<String, dynamic>?)?['email'] ?? '';
        return VerifyPage(email: email);
      },
    ),
    GoRoute(
      path: '/terms',
      name: RouteNames.terms,
      builder: (context, state) => const TermsPage(),
    ),
    GoRoute(
      path: '/dashboard',
      name: RouteNames.dashboard,
      builder: (context, state) => const DashboardPage(),
    ),
  ],
  errorBuilder: (context, state) => Scaffold(
    backgroundColor: const Color(0xFF0D1B2A),
    body: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.error_outline, color: Colors.redAccent, size: 64),
          const SizedBox(height: 16),
          Text(
            'Page Not Found',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 12),
          ElevatedButton(
            onPressed: () => context.goNamed(RouteNames.login),
            child: const Text("Back to Login"),
          ),
        ],
      ),
    ),
  ),
);
