import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:phishzil/routes/route_names.dart';
import '../features/auth/view/login_page.dart';
import '../features/auth/view/verify_code_page.dart';
import '../features/auth/view/signup_page.dart';
import '../features/auth/view/terms_page.dart';
import '../features/auth/view/forgot_password_page.dart';
import '../features/dashboard/view/dashboard_page.dart';
import '../features/auth/view//reset_password_page.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: RouteNames.login,
  debugLogDiagnostics: true,
  routes: [
    GoRoute(
      path: RouteNames.login,
      builder: (context, state) => const LoginPage(),
    ),
    GoRoute(
      path: RouteNames.signup,
      builder: (context, state) => const SignupPage(),
    ),
    GoRoute(
      path: RouteNames.forgotPassword,
      builder: (context, state) => const ForgotPasswordPage(),
    ),
    GoRoute(
      path: '/verify-code/:email',
      builder: (context, state) {
        final email = state.pathParameters['email'] ?? '';
        return VerifyCodePage(email: email);
      },
    ),
    GoRoute(
      path: RouteNames.verify,
      name: RouteNames.verify,
      builder: (context, state) {
        final extra = state.extra as Map<String, dynamic>?;
        final email = extra?['email'] ?? '';
        return VerifyPage(email: email);
      },
    ),

    GoRoute(
      path: '/reset-password/:email',
      builder: (context, state) {
        final email = state.pathParameters['email'] ?? '';
        return ResetPasswordPage(email: email);
      },
    ),
    GoRoute(
      path: '/terms',
      name: RouteNames.terms,
      builder: (context, state) => const TermsPage(),
    ),

    /// ✅ New Dashboard route
    GoRoute(
      path: RouteNames.dashboard,
      builder: (context, state) => const DashboardPage(),
    ),
  ],
  errorBuilder: (context, state) => Scaffold(
    backgroundColor: Colors.black,
    appBar: AppBar(title: const Text('Error'), backgroundColor: Colors.red),
    body: Center(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Text(
          state.error.toString(),
          style: const TextStyle(color: Colors.redAccent, fontSize: 18),
          textAlign: TextAlign.center,
        ),
      ),
    ),
  ),
);
