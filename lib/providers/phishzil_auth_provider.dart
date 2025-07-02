import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:shared_preferences/shared_preferences.dart';

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

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier() : super(AuthState.initial());

  final String _baseUrl =
      dotenv.env['API_BASE_URL']?.trim() ?? 'http://192.168.169.92:8000/auth';

  Future<void> signUp(String username, String email, String password) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    try {
      final response = await http.post(
        Uri.parse("$_baseUrl/register"),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': username,
          'username': username,
          'email': email,
          'password': password,
        }),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 201) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('email', email);
        await prefs.setString('username', username);

        state = state.copyWith(
          isLoading: false,
          errorMessage: "Signup successful! Please verify your email.",
        );
      } else {
        state = state.copyWith(
          isLoading: false,
          errorMessage: data['error'] ?? "Signup failed.",
        );
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: "Connection failed. Please try again.",
      );
    }
  }

  Future<void> login(
    String identifier,
    String password,
    bool rememberMe,
  ) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    try {
      final response = await http.post(
        Uri.parse("$_baseUrl/login"),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'identifier': identifier, 'password': password}),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 200 && data['token'] != null) {
        final prefs = await SharedPreferences.getInstance();

        if (rememberMe) {
          await prefs.setBool("remember_me", true);
          await prefs.setString("saved_email", identifier);
          await prefs.setString("saved_password", password);
        } else {
          await prefs.remove("saved_email");
          await prefs.remove("saved_password");
          await prefs.setBool("remember_me", false);
        }

        await prefs.setString("token", data['token']);
        await prefs.setString("username", data['user']['username'] ?? '');
        await prefs.setString("email", data['user']['email'] ?? '');

        state = state.copyWith(isAuthenticated: true, isLoading: false);
      } else {
        state = state.copyWith(
          isLoading: false,
          errorMessage: data['error'] ?? "Invalid login credentials.",
        );
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: "Login failed. Server not reachable.",
      );
    }
  }

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

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    state = AuthState.initial();
  }

  Future<void> verifyToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString("token");

    if (token != null) {
      final response = await http.get(
        Uri.parse("$_baseUrl/users"),
        headers: {'Authorization': 'Bearer $token'},
      );

      if (response.statusCode == 200) {
        state = state.copyWith(isAuthenticated: true);
      } else {
        state = state.copyWith(isAuthenticated: false);
      }
    }
  }

  // ✅ Email Code Verification (correct)
  Future<bool> verifyCode(String code) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final email = prefs.getString('email');

      if (email == null) return false;

      final response = await http.post(
        Uri.parse("$_baseUrl/verify-code"),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'code': code}),
      );

      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  // ✅ Resend Email Code
  Future<bool> resendVerificationCode() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final email = prefs.getString('email');

      if (email == null) return false;

      final response = await http.post(
        Uri.parse("$_baseUrl/resend-code"),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      );

      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});
