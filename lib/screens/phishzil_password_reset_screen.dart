import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import '../utils/phishzil_constants.dart';

class PhishzilPasswordResetScreen extends ConsumerStatefulWidget {
  const PhishzilPasswordResetScreen({super.key});

  @override
  ConsumerState<PhishzilPasswordResetScreen> createState() =>
      _PhishzilPasswordResetScreenState();
}

class _PhishzilPasswordResetScreenState
    extends ConsumerState<PhishzilPasswordResetScreen> {
  final _emailController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _isSending = false;

  static const String _baseUrl = "http://192.168.105.92:8000/auth";

  void _showSnack(String message, {bool isError = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
      ),
    );
  }

  Future<void> _handleReset() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isSending = true);

      try {
        final response = await http.post(
          Uri.parse("$_baseUrl/reset-password"),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'email': _emailController.text.trim()}),
        );

        final data = jsonDecode(response.body);

        if (response.statusCode == 200) {
          _showSnack("Reset link sent to ${_emailController.text.trim()}");
          Navigator.pop(context);
        } else {
          _showSnack(
            data['error'] ?? "Failed to send reset link",
            isError: true,
          );
        }
      } catch (e) {
        _showSnack("Error: Could not reach the server", isError: true);
      } finally {
        setState(() => _isSending = false);
      }
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [PhishzilColors.safeColor, Color(0xFF061827), Colors.black],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 420),
              child: Column(
                children: [
                  Hero(
                    tag: "tag",
                    child: Image.asset(
                      "assets/images/sh.png",
                      height: 100,
                      width: 100,
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    "Reset Password",
                    style: TextStyle(
                      color: Colors.lightBlueAccent,
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 30),
                  Card(
                    color: Colors.transparent,
                    elevation: 6,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Form(
                        key: _formKey,
                        child: Column(
                          children: [
                            TextFormField(
                              controller: _emailController,
                              keyboardType: TextInputType.emailAddress,
                              style: const TextStyle(color: Colors.white),
                              decoration: InputDecoration(
                                border: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(26),
                                ),
                                focusedBorder: OutlineInputBorder(
                                  borderSide: BorderSide(
                                    color: PhishzilColors.secondary,
                                    width: 2.0,
                                  ),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                prefixIcon: Icon(
                                  Icons.email,
                                  color: PhishzilColors.secondary,
                                ),
                                hintText: "Enter your Email",
                                hintStyle: const TextStyle(
                                  color: Colors.white60,
                                ),
                                labelText: "Email",
                                labelStyle: TextStyle(
                                  color: PhishzilColors.secondary,
                                ),
                              ),
                              validator: (value) {
                                if (value == null ||
                                    value.trim().isEmpty ||
                                    !value.contains('@')) {
                                  return "Enter a valid email";
                                }
                                return null;
                              },
                            ),
                            const SizedBox(height: 30),
                            GestureDetector(
                              onTap: _isSending ? null : _handleReset,
                              child: Container(
                                width: double.infinity,
                                padding: const EdgeInsets.symmetric(
                                  vertical: 15,
                                ),
                                decoration: BoxDecoration(
                                  gradient: const LinearGradient(
                                    colors: [
                                      Color(0xFF00B4DB),
                                      Color(0xFF0083B0),
                                    ],
                                  ),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Center(
                                  child: _isSending
                                      ? const CircularProgressIndicator(
                                          color: Colors.white,
                                        )
                                      : const Text(
                                          "Send Reset Link",
                                          style: TextStyle(
                                            fontSize: 18,
                                            color: Colors.white,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                ),
                              ),
                            ),
                            const SizedBox(height: 20),
                            TextButton(
                              onPressed: () => Navigator.pop(context),
                              child: Text(
                                "Back to Login",
                                style: TextStyle(
                                  color: PhishzilColors.secondary,
                                  fontSize: 14,
                                  decoration: TextDecoration.underline,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
