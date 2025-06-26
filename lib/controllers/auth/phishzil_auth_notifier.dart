import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

final authNotifierProvider =
    StateNotifierProvider<AuthNotifier, AsyncValue<String>>(
      (ref) => AuthNotifier(),
    );

class AuthNotifier extends StateNotifier<AsyncValue<String>> {
  AuthNotifier() : super(const AsyncValue.data(''));

  Future<void> signupUser({
    required String username,
    required String email,
    required String password,
  }) async {
    state = const AsyncValue.loading();

    try {
      final response = await http.post(
        Uri.parse(
          "https://your-api-url.com/signup.php",
        ), // change to your backend URL
        body: {'username': username, 'email': email, 'password': password},
      );

      if (response.statusCode == 200) {
        final body = json.decode(response.body);
        if (body['success'] == true) {
          state = AsyncValue.data("Signup successful");
        } else {
          state = AsyncValue.error(
            body['message'] ?? 'Signup failed',
            StackTrace.current,
          );
        }
      } else {
        state = AsyncValue.error("Server error", StackTrace.current);
      }
    } catch (e) {
      state = AsyncValue.error("Error: $e", StackTrace.current);
    }
  }
}
