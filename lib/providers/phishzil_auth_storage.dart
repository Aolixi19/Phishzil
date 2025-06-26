import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthStorage {
  // Create a secure storage instance
  static final _storage = FlutterSecureStorage();

  // Storage keys
  static const _keyEmail = 'user_email';
  static const _keyPassword = 'user_password';
  static const _keyRemember = 'remember_me';

  /// Save credentials and remember flag
  static Future<void> saveCredentials(String email, String password) async {
    await _storage.write(key: _keyEmail, value: email);
    await _storage.write(key: _keyPassword, value: password);
    await _storage.write(key: _keyRemember, value: 'true');
  }

  /// Retrieve credentials (email, password, and remember flag)
  static Future<Map<String, String?>> getCredentials() async {
    final email = await _storage.read(key: _keyEmail);
    final password = await _storage.read(key: _keyPassword);
    final remember = await _storage.read(key: _keyRemember);
    return {'email': email, 'password': password, 'remember': remember};
  }

  /// Clear only login-related keys
  static Future<void> clearCredentials() async {
    await _storage.delete(key: _keyEmail);
    await _storage.delete(key: _keyPassword);
    await _storage.delete(key: _keyRemember);
  }
}
