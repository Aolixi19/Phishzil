import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:phishzil/routes/route_names.dart';

// Auth Screens
import '../features/auth/view/login_page.dart';
import '../features/auth/view/verify_code_page.dart';
import '../features/auth/view/signup_page.dart';
import '../features/auth/view/terms_page.dart';
import '../features/auth/view/verifyPage.dart';
import '../features/auth/view/forgot_password_page.dart';
import '../features/auth/view/reset_password_page.dart';

// Dashboard
import '../features/dashboard/view/dashboard_page.dart';

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
      path: '/forgot-password',
      name: RouteNames.forgotPassword,
      builder: (context, state) => const ForgotPasswordPage(),
    ),
    GoRoute(
      path: '/signup',
      name: RouteNames.signup,
      builder: (context, state) => const SignupPage(),
    ),
    GoRoute(
      path: '/verify-code/:email',
      name: RouteNames.verifyCode,
      builder: (context, state) {
        final email = Uri.decodeComponent(state.pathParameters['email'] ?? '');
        return VerifyCodePage(email: email);
      },
    ),
    GoRoute(
      path: '/reset-password/:email',
      name: RouteNames.resetPassword,
      builder: (context, state) {
        final email = Uri.decodeComponent(state.pathParameters['email'] ?? '');
        return ResetPasswordPage(email: email);
      },
    ),
    GoRoute(
      path: '/verify',
      name: RouteNames.verify, // ✅ This must match
      builder: (context, state) {
        final extra = state.extra as Map<String, dynamic>?;
        final email = extra?['email']?.toString() ?? '';
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
  redirect: (context, state) => null,
  errorBuilder: (context, state) => Scaffold(
    backgroundColor: const Color(0xFF0D1B2A),
    body: Center(
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, color: Colors.redAccent, size: 64),
            const SizedBox(height: 20),
            Text(
              'Page Not Found',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Text(
                state.error?.toString() ??
                    'The requested page could not be found',
                style: const TextStyle(color: Colors.white70),
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: () => context.goNamed(RouteNames.login),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.cyanAccent,
                foregroundColor: Colors.black,
                padding: const EdgeInsets.symmetric(
                  horizontal: 32,
                  vertical: 16,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: const Text(
                'Return to Login',
                style: TextStyle(fontSize: 16),
              ),
            ),
          ],
        ),
      ),
    ),
  ),
);
