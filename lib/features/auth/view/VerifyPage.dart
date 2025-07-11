// ignore_for_file: use_build_context_synchronously, file_names
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../controller/auth_provider.dart';
import '../../../global_widgets/custom_button.dart';
import '../../../routes/route_names.dart';

class VerifyPage extends StatefulWidget {
  final String email;

  const VerifyPage({super.key, required this.email});

  @override
  State<VerifyPage> createState() => _VerifyPageState();
}

class _VerifyPageState extends State<VerifyPage>
    with SingleTickerProviderStateMixin {
  final _formKey = GlobalKey<FormState>();
  late List<FocusNode> _focusNodes;
  late List<TextEditingController> _controllers;
  bool _isVerifying = false;
  bool _success = false;
  bool _error = false;

  int _secondsRemaining = 600; // 10 mins
  Timer? _timer;

  late AnimationController _shakeController;
  late Animation<double> _shakeAnimation;

  @override
  void initState() {
    super.initState();
    _focusNodes = List.generate(6, (_) => FocusNode());
    _controllers = List.generate(6, (_) => TextEditingController());

    _startTimer();

    _shakeController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );

    _shakeAnimation = Tween<double>(
      begin: 0,
      end: 24,
    ).chain(CurveTween(curve: Curves.elasticIn)).animate(_shakeController);
  }

  @override
  void dispose() {
    _timer?.cancel();
    for (var node in _focusNodes) {
      node.dispose();
    }
    for (var ctrl in _controllers) {
      ctrl.dispose();
    }
    _shakeController.dispose();
    super.dispose();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_secondsRemaining > 0) {
        setState(() => _secondsRemaining--);
      } else {
        timer.cancel();
      }
    });
  }

  String _getFormattedTime() {
    final minutes = (_secondsRemaining ~/ 60).toString().padLeft(2, '0');
    final seconds = (_secondsRemaining % 60).toString().padLeft(2, '0');
    return "$minutes:$seconds";
  }

  void _verifyCode() async {
    final code = _controllers.map((c) => c.text).join();

    if (code.length != 6) {
      _triggerShake();
      return;
    }

    setState(() {
      _isVerifying = true;
      _error = false;
    });

    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final success = await authProvider.verifyCode(widget.email, code);

    setState(() {
      _isVerifying = false;
      _success = success;
      _error = !success;
    });

    if (success) {
      await Future.delayed(const Duration(seconds: 1));
      context.go(RouteNames.login);
    } else {
      _triggerShake();
    }
  }

  void _triggerShake() {
    _shakeController.forward(from: 0);
  }

  void _resendCode() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final result = await authProvider.requestResetCode(widget.email);
    if (result) {
      setState(() {
        _secondsRemaining = 600;
      });
      _startTimer();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("New code sent to your email ✅"),
          backgroundColor: Colors.green,
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Failed to resend code ❌"),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Widget _buildDigitField(int index) {
    return AnimatedBuilder(
      animation: _shakeController,
      builder: (context, child) {
        final offset = _error
            ? _shakeAnimation.value * (index.isEven ? 1 : -1)
            : 0.0;
        return Transform.translate(
          offset: Offset(offset, 0),
          child: SizedBox(
            width: 48,
            child: TextFormField(
              controller: _controllers[index],
              focusNode: _focusNodes[index],
              keyboardType: TextInputType.number,
              maxLength: 1,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.white, fontSize: 20),
              decoration: InputDecoration(
                counterText: '',
                filled: true,
                fillColor: Colors.white10,
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(
                    color: _success
                        ? Colors.green
                        : _error
                        ? Colors.red
                        : Colors.white30,
                    width: 1.5,
                  ),
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              onChanged: (value) {
                if (value.isNotEmpty && index < 5) {
                  FocusScope.of(context).requestFocus(_focusNodes[index + 1]);
                } else if (value.isEmpty && index > 0) {
                  FocusScope.of(context).requestFocus(_focusNodes[index - 1]);
                }
              },
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF00172B),
      appBar: AppBar(
        title: const Text("Email Verification"),
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                const Text(
                  'Enter the 6-digit code sent to your email.',
                  style: TextStyle(color: Colors.white70, fontSize: 16),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),

                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: List.generate(
                    6,
                    (index) => _buildDigitField(index),
                  ),
                ),

                const SizedBox(height: 20),

                Text(
                  _secondsRemaining > 0
                      ? "Expires in ${_getFormattedTime()}"
                      : "Code expired. Tap resend.",
                  style: TextStyle(
                    color: _secondsRemaining > 0
                        ? Colors.white60
                        : Colors.redAccent,
                  ),
                ),

                const SizedBox(height: 20),

                _success
                    ? const Icon(
                        Icons.check_circle,
                        color: Colors.green,
                        size: 48,
                      )
                    : GradientButton(
                        label: 'Verify',
                        isLoading: _isVerifying,
                        onPressed: () {
                          if (_secondsRemaining > 0 && !_isVerifying) {
                            _verifyCode();
                          }
                        },
                      ),

                const SizedBox(height: 16),

                TextButton(
                  onPressed: _secondsRemaining == 0 ? _resendCode : null,
                  child: const Text(
                    'Resend Code',
                    style: TextStyle(
                      color: Colors.lightBlueAccent,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),

                const SizedBox(height: 30),

                const Text(
                  'Didn’t get the code? Check your spam folder.',
                  style: TextStyle(color: Colors.white38),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
