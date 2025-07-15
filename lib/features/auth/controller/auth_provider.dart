import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:google_sign_in/google_sign_in.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AuthProvider extends ChangeNotifier {
  final _secureStorage = const FlutterSecureStorage();
  String baseUrl = '';

  // Auth state
  bool isLoading = false;
  bool isAuthenticated = false;
  String? errorMessage;
  String? token;
  Map<String, dynamic>? currentUser;

  // Verification flow
  String? nextAction;
  String? pendingEmail;
  DateTime? lastCodeRequestTime;

  String? get userName => currentUser?['name']?.toString();

  /// Load .env and base URL
  Future<void> initialize() async {
    if (baseUrl.isNotEmpty) return;
    await dotenv.load();
    final apiUrl = dotenv.env['API_BASE_URL'];
    if (apiUrl == null || apiUrl.isEmpty) {
      throw Exception('API_BASE_URL is not configured in .env');
    }
    baseUrl = '${apiUrl.replaceAll(RegExp(r'/+$'), '')}/auth';
  }

  /// Try auto-login
  Future<void> tryAutoLogin() async {
    await initialize();
    _setLoading(true);
    try {
      token = await _secureStorage.read(key: 'auth_token');
      final userData = await _secureStorage.read(key: 'user_data');
      if (token != null && userData != null) {
        currentUser = jsonDecode(userData);
        isAuthenticated = true;
      }
    } catch (_) {
      await _secureStorage.deleteAll();
      errorMessage = 'Session expired. Please login again.';
    } finally {
      _setLoading(false);
    }
  }

  /// Email login
  Future<bool> login({
    required String identifier,
    required String password,
  }) async {
    await initialize();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/login'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'identifier': identifier, 'password': password}),
          )
          .timeout(const Duration(seconds: 30));

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        token = data['token']?.toString();
        currentUser = Map<String, dynamic>.from(data['user']);
        isAuthenticated = true;

        await _secureStorage.write(key: 'auth_token', value: token);
        await _secureStorage.write(
          key: 'user_data',
          value: jsonEncode(currentUser),
        );
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          defaultMessage: 'Invalid credentials',
        );
        return false;
      }
    } catch (e) {
      errorMessage = _getNetworkErrorMessage(e);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// Signup
  Future<bool> signup({
    required String name,
    required String username,
    required String email,
    required String password,
  }) async {
    await initialize();
    _setLoading(true);
    errorMessage = null;
    nextAction = null;
    pendingEmail = null;

    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/register'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'name': name,
              'username': username,
              'email': email,
              'password': password,
            }),
          )
          .timeout(const Duration(seconds: 30));

      final data = _parseResponse(response);

      if (response.statusCode == 201) {
        nextAction = 'verify';
        pendingEmail = email;
        lastCodeRequestTime = DateTime.now();
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          defaultMessage: 'Registration failed',
        );
        return false;
      }
    } catch (e) {
      errorMessage = _getNetworkErrorMessage(e);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// Google Sign-In ✅
  Future<void> loginWithGoogle() async {
    _setLoading(true);
    errorMessage = null;

    try {
      final GoogleSignIn googleSignIn = GoogleSignIn.standard(
        scopes: ['email', 'profile'],
      );

      final GoogleSignInAccount? googleUser = await googleSignIn.signIn();

      if (googleUser == null) {
        errorMessage = "Google Sign-In cancelled";
        _setLoading(false);
        return;
      }

      final GoogleSignInAuthentication googleAuth =
          await googleUser.authentication;

      if (googleAuth.idToken == null) {
        errorMessage = "Google Sign-In failed: missing ID token";
        isAuthenticated = false;
        _setLoading(false);
        return;
      }

      final credential = GoogleAuthProvider.credential(
        idToken: googleAuth.idToken,
      );

      final userCredential = await FirebaseAuth.instance.signInWithCredential(
        credential,
      );

      final user = userCredential.user;
      final firebaseToken = await user?.getIdToken();

      currentUser = {
        'email': user?.email,
        'name': user?.displayName ?? 'Google User',
      };
      token = firebaseToken;
      isAuthenticated = true;

      if (firebaseToken != null) {
        await _secureStorage.write(key: 'auth_token', value: firebaseToken);
      }
      await _secureStorage.write(
        key: 'user_data',
        value: jsonEncode(currentUser),
      );
    } on FirebaseAuthException catch (e) {
      errorMessage = e.message;
      isAuthenticated = false;
    } catch (e) {
      errorMessage = "Google Sign-In failed.";
      isAuthenticated = false;
    }

    _setLoading(false);
  }

  /// Logout
  Future<void> logout() async {
    isAuthenticated = false;
    token = null;
    currentUser = null;
    errorMessage = null;
    nextAction = null;
    pendingEmail = null;

    await _secureStorage.delete(key: 'auth_token');
    await _secureStorage.delete(key: 'user_data');

    notifyListeners();
  }

  /// Verify email
  Future<bool> verifyCode(String email, String code) async {
    await initialize();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/verify-code'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'email': email, 'code': code}),
          )
          .timeout(const Duration(seconds: 30));

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        nextAction = null;
        pendingEmail = null;
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          defaultMessage: 'Invalid code',
        );
        return false;
      }
    } catch (e) {
      errorMessage = _getNetworkErrorMessage(e);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// Reset password flow
  Future<bool> requestResetCode(String email) async {
    await initialize();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/request-reset-code'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'email': email}),
          )
          .timeout(const Duration(seconds: 30));

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        nextAction = 'reset';
        pendingEmail = email;
        lastCodeRequestTime = DateTime.now();
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          defaultMessage: 'Failed to send reset code',
        );
        return false;
      }
    } catch (e) {
      errorMessage = _getNetworkErrorMessage(e);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> verifyResetCode(String email, String code) async {
    await initialize();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/verify-reset-code'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'email': email, 'code': code}),
          )
          .timeout(const Duration(seconds: 30));

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          defaultMessage: 'Invalid reset code',
        );
        return false;
      }
    } catch (e) {
      errorMessage = _getNetworkErrorMessage(e);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> resetPassword(String email, String password, String code) async {
    await initialize();
    _setLoading(true);
    errorMessage = null;

    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/reset-password'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'email': email,
              'password': password,
              'code': code,
            }),
          )
          .timeout(const Duration(seconds: 30));

      final data = _parseResponse(response);

      if (response.statusCode == 200) {
        nextAction = null;
        pendingEmail = null;
        return true;
      } else {
        errorMessage = _getErrorMessage(
          data,
          response.statusCode,
          defaultMessage: 'Reset failed',
        );
        return false;
      }
    } catch (e) {
      errorMessage = _getNetworkErrorMessage(e);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Helpers
  void _setLoading(bool loading) {
    isLoading = loading;
    notifyListeners();
  }

  Map<String, dynamic> _parseResponse(http.Response response) {
    try {
      return jsonDecode(response.body) as Map<String, dynamic>? ?? {};
    } catch (_) {
      return {'error': 'Invalid server response'};
    }
  }

  String _getErrorMessage(
    Map<String, dynamic> data,
    int statusCode, {
    required String defaultMessage,
  }) {
    return data['error']?.toString() ??
        data['message']?.toString() ??
        (statusCode >= 500 ? 'Server error' : defaultMessage);
  }

  String _getNetworkErrorMessage(dynamic error) {
    if (error is http.ClientException) {
      return 'Network error: ${error.message}';
    } else if (error is TimeoutException) {
      return 'Request timed out';
    }
    return 'An unexpected error occurred';
  }

  bool canRequestNewCode() {
    if (lastCodeRequestTime == null) return true;
    return DateTime.now().difference(lastCodeRequestTime!) >
        const Duration(minutes: 1);
  }

  Duration? getRemainingCooldown() {
    if (lastCodeRequestTime == null || canRequestNewCode()) return null;
    return const Duration(minutes: 1) -
        DateTime.now().difference(lastCodeRequestTime!);
  }

  Future resendResetCode(String email) async {}

  Future resendVerificationCode(String trim) async {}
}
