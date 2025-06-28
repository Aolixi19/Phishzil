import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Represents the current state of authentication.
class AuthState {
  final bool isAuthenticated;
  final bool isLoading;
  final String? errorMessage;

  const AuthState({
    required this.isAuthenticated,
    required this.isLoading,
    this.errorMessage,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    bool? isLoading,
    String? errorMessage,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage,
    );
  }

  factory AuthState.initial() {
    return const AuthState(
      isAuthenticated: false,
      isLoading: false,
      errorMessage: null,
    );
  }
}

/// Notifier that manages login/signup/logout logic.
class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier() : super(AuthState.initial());

  final FirebaseAuth _auth = FirebaseAuth.instance;

  /// Sign up with Firebase Auth and send verification email
  Future<void> signUp(String username, String email, String password) async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      // Create Firebase user
      await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );

      // Set display name
      await _auth.currentUser?.updateDisplayName(username);

      // Send email verification
      await _auth.currentUser?.sendEmailVerification();

      // Store locally for login with username
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("username", username);
      await prefs.setString("email", email);

      state = state.copyWith(
        isAuthenticated: false,
        isLoading: false,
        errorMessage:
            "Signup successful! Please verify your email before login.",
      );
    } on FirebaseAuthException catch (e) {
      final error = e.code == 'email-already-in-use'
          ? 'Account already exists. Please login.'
          : e.message ?? 'Signup failed.';
      state = state.copyWith(isLoading: false, errorMessage: error);
    }
  }

  /// Login with email or username and check verification
  Future<void> login(
    String identifier,
    String password,
    bool rememberMe,
  ) async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      final prefs = await SharedPreferences.getInstance();
      String? email = identifier;

      // Handle login with username
      if (!identifier.contains("@")) {
        final savedUsername = prefs.getString("username");
        if (savedUsername == identifier) {
          email = prefs.getString("email");
        } else {
          throw FirebaseAuthException(
            code: "user-not-found",
            message: "Username not found.",
          );
        }
      }

      // Sign in with email
      await _auth.signInWithEmailAndPassword(email: email!, password: password);

      // Check if email is verified
      final user = _auth.currentUser;
      if (user != null && !user.emailVerified) {
        await _auth.signOut();
        throw FirebaseAuthException(
          code: "email-not-verified",
          message: "Please verify your email before logging in.",
        );
      }

      // Store remember me
      if (rememberMe) {
        await prefs.setBool("remember_me", true);
        await prefs.setString("saved_email", email);
        await prefs.setString("saved_password", password);
      } else {
        await prefs.setBool("remember_me", false);
        await prefs.remove("saved_email");
        await prefs.remove("saved_password");
      }

      state = state.copyWith(isAuthenticated: true, isLoading: false);
    } on FirebaseAuthException catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: e.message ?? "Login failed.",
      );
    }
  }

  /// Try to auto-login from saved credentials
  Future<void> tryAutoLogin() async {
    final prefs = await SharedPreferences.getInstance();
    final remember = prefs.getBool("remember_me") ?? false;

    if (remember) {
      final email = prefs.getString("saved_email");
      final password = prefs.getString("saved_password");

      if (email != null && password != null) {
        await login(email, password, true);
      }
    }
  }

  /// Logout and clear local storage
  Future<void> logout() async {
    await _auth.signOut();

    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool("remember_me", false);
    await prefs.remove("saved_email");
    await prefs.remove("saved_password");

    state = AuthState.initial();
  }

  /// Send verification email again
  Future<void> resendVerificationEmail() async {
    try {
      final user = _auth.currentUser;
      if (user != null && !user.emailVerified) {
        await user.sendEmailVerification();
      }
    } catch (_) {
      // Optionally handle errors
    }
  }
}

/// Riverpod provider for global access
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});
