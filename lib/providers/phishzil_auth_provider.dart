import 'package:flutter_riverpod/flutter_riverpod.dart';

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

  /// Simulates a sign-up process (connect to your backend here).
  Future<void> signUp(String username, String email, String password) async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      await Future.delayed(const Duration(seconds: 2));

      // Simulate sign-up success (replace with real API call)
      final isSuccessful = email.contains('@') && password.length >= 6;

      if (isSuccessful) {
        state = state.copyWith(isAuthenticated: true, isLoading: false);
      } else {
        state = state.copyWith(
          isLoading: false,
          errorMessage: 'Signup failed: Invalid credentials',
        );
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'Signup failed: ${e.toString()}',
      );
    }
  }

  /// Simulates a login process (replace with backend logic).
  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true, errorMessage: null);

    try {
      await Future.delayed(const Duration(seconds: 2));

      // Simulate login logic — update this block with actual logic
      if (email == "admin@phishzil.com" && password == "123456") {
        state = state.copyWith(isAuthenticated: true, isLoading: false);
      } else {
        state = state.copyWith(
          isLoading: false,
          errorMessage: "Login failed: Invalid email or password",
        );
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'Login failed: ${e.toString()}',
      );
    }
  }

  /// Logs out the user and resets the state.
  void logout() {
    state = AuthState.initial();
  }
}

/// Global Riverpod provider for the authentication state.
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});
