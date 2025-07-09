import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

class AuthProvider extends ChangeNotifier {
  late final String baseUrl;
  final _secureStorage = const FlutterSecureStorage();

  bool isLoading = false;
  bool isAuthenticated = false;
  String? errorMessage;
  String? token;
  String? userName;

  // 👇 Added for verification flow
  String? nextAction;
  String? pendingEmail;

  /// Initialize base URL from .env
  Future<void> initialize() async {
    final apiUrl = dotenv.env['API_BASE_URL'];
    if (apiUrl == null || apiUrl.isEmpty) {
      throw Exception('API_BASE_URL is not configured in .env file');
    }
    baseUrl = '${apiUrl.replaceAll(RegExp(r'/+$'), '')}/auth';
  }

  Future<void> _checkInitialized() async {
    if (baseUrl.isEmpty) {
      await initialize();
    }
  }

  /// Try auto-login from secure storage
  Future<void> tryAutoLogin() async {
    await _checkInitialized();
    token = await _secureStorage.read(key: 'auth_token');
    userName = await _secureStorage.read(key: 'user_name');
    isAuthenticated = token != null;
    notifyListeners();
  }

  /// LOGIN
  Future<void> login({
    required String identifier,
    required String password,
  }) async {
    await _checkInitialized();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'identifier': identifier, 'password': password}),
      );

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        token = data['token']?.toString();
        userName =
            data['user']?['username']?.toString() ??
            data['user']?['name']?.toString();
        isAuthenticated = true;

        await _secureStorage.write(key: 'auth_token', value: token);
        await _secureStorage.write(key: 'user_name', value: userName);
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          'Login failed',
        );
      }
    } catch (e) {
      errorMessage = 'Network error: ${e.toString()}';
    } finally {
      _setLoading(false);
    }
  }

  /// SIGNUP
  Future<void> signup({
    required String name,
    required String username,
    required String email,
    required String password,
  }) async {
    await _checkInitialized();
    _setLoading(true);
    errorMessage = null;
    nextAction = null;
    pendingEmail = null;

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': name,
          'username': username,
          'email': email,
          'password': password,
        }),
      );

      final data = _parseResponse(response);

      if (response.statusCode == 200 || response.statusCode == 201) {
        // ✅ Verification flow
        if (data['next'] == 'verify') {
          pendingEmail = email;
          nextAction = 'verify';
        } else {
          errorMessage = null;
        }
      } else if (response.statusCode == 409) {
        errorMessage = 'Email or username already exists';
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          'Signup failed',
        );
      }
    } catch (e) {
      errorMessage = 'Signup error: ${e.toString()}';
    } finally {
      _setLoading(false);
    }
  }

  /// VERIFY EMAIL
  Future<bool> verifyCode(String email, String code) async {
    await _checkInitialized();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/verify-code'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'code': code}),
      );

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          'Verification failed',
        );
        return false;
      }
    } catch (e) {
      errorMessage = 'Verification error: ${e.toString()}';
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// REQUEST RESET CODE
  Future<bool> requestResetCode(String email) async {
    await _checkInitialized();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/request-reset-code'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      );

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          'Reset code request failed',
        );
        return false;
      }
    } catch (e) {
      errorMessage = 'Reset request failed: ${e.toString()}';
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// VERIFY RESET CODE
  Future<bool> verifyResetCode(String email, String code) async {
    await _checkInitialized();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/verify-reset-code'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'code': code}),
      );

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          'Invalid reset code',
        );
        return false;
      }
    } catch (e) {
      errorMessage = 'Verification error: ${e.toString()}';
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// RESET PASSWORD
  Future<bool> resetPassword(String email, String password) async {
    await _checkInitialized();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/reset-password'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          'Reset failed',
        );
        return false;
      }
    } catch (e) {
      errorMessage = 'Reset error: ${e.toString()}';
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// Parse API response
  Map<String, dynamic> _parseResponse(http.Response response) {
    try {
      return jsonDecode(response.body) as Map<String, dynamic>? ?? {};
    } catch (e) {
      return {'error': 'Invalid server response format'};
    }
  }

  /// Friendly error extractor
  String _getErrorMessage(
    Map<String, dynamic> data,
    int statusCode,
    String fallback,
  ) {
    return data['error']?.toString() ??
        data['message']?.toString() ??
        data['error_message']?.toString() ??
        '$fallback (Status: $statusCode)';
  }

  /// Set loading state
  void _setLoading(bool loading) {
    isLoading = loading;
    notifyListeners();
  }

  /// Logout
  Future<void> logout() async {
    isAuthenticated = false;
    token = null;
    userName = null;
    errorMessage = null;
    await _secureStorage.deleteAll();
    notifyListeners();
  }
}
