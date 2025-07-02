import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/phishzil_auth_provider.dart';
import '../routers/phishzil_app_routes.dart';

class VerifyEmailCodeScreen extends ConsumerStatefulWidget {
  const VerifyEmailCodeScreen({super.key});

  @override
  ConsumerState<VerifyEmailCodeScreen> createState() =>
      _VerifyEmailCodeScreenState();
}

class _VerifyEmailCodeScreenState extends ConsumerState<VerifyEmailCodeScreen>
    with TickerProviderStateMixin {
  final List<TextEditingController> _controllers = List.generate(
    6,
    (_) => TextEditingController(),
  );
  final List<FocusNode> _focusNodes = List.generate(6, (_) => FocusNode());

  bool _isLoading = false;
  bool _isSuccess = false;

  late final AnimationController _animationController;
  late final Animation<double> _scaleAnimation;

  String get _enteredCode => _controllers.map((c) => c.text).join();

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 200),
    );
    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: 1.1,
    ).animate(_animationController);
  }

  Future<void> _onCodeChanged(int index, String value) async {
    if (value.length == 1 && index < 5) {
      _focusNodes[index + 1].requestFocus();
    }
    if (value.isEmpty && index > 0) {
      _focusNodes[index - 1].requestFocus();
    }

    if (_enteredCode.length == 6 && !_isLoading && !_isSuccess) {
      await _verifyCode();
    }
  }

  Future<void> _verifyCode() async {
    setState(() => _isLoading = true);

    final result = await ref
        .read(authProvider.notifier)
        .verifyCode(_enteredCode);

    setState(() {
      _isLoading = false;
      _isSuccess = result;
    });

    if (result) {
      HapticFeedback.mediumImpact();
      _animationController.forward();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("✅ Email Verified Successfully!")),
      );

      await Future.delayed(const Duration(seconds: 2));
      if (mounted) {
        Navigator.pushReplacementNamed(context, AppRoutes.login);
      }
    } else {
      HapticFeedback.vibrate();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("❌ Invalid or expired code")),
      );
    }
  }

  Future<void> _resendCode() async {
    setState(() => _isLoading = true);

    final result = await ref
        .read(authProvider.notifier)
        .resendVerificationCode();

    setState(() => _isLoading = false);

    if (result) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("📩 New verification code sent.")),
      );
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text("⚠️ Failed to resend code")));
    }
  }

  Future<void> _handlePaste() async {
    final clipboardData = await Clipboard.getData(Clipboard.kTextPlain);
    final code = clipboardData?.text?.replaceAll(RegExp(r'\D'), '') ?? '';

    if (code.length == 6) {
      for (int i = 0; i < 6; i++) {
        _controllers[i].text = code[i];
      }
      _focusNodes[5].unfocus();
      await _verifyCode();
    }
  }

  @override
  void dispose() {
    for (final controller in _controllers) {
      controller.dispose();
    }
    for (final focus in _focusNodes) {
      focus.dispose();
    }
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final successColor = Colors.green;
    final defaultColor = Colors.deepPurple.shade700;

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.deepPurple,
        title: const Text("Verify Email"),
      ),
      body: GestureDetector(
        onLongPress: _handlePaste,
        behavior: HitTestBehavior.opaque,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 40),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Text(
                "Enter the 6-digit code sent to your email",
                style: TextStyle(color: Colors.white70, fontSize: 16),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: List.generate(6, (index) {
                  return ScaleTransition(
                    scale: _scaleAnimation,
                    child: SizedBox(
                      width: 45,
                      child: TextField(
                        controller: _controllers[index],
                        focusNode: _focusNodes[index],
                        keyboardType: TextInputType.number,
                        maxLength: 1,
                        textAlign: TextAlign.center,
                        autofillHints: const [AutofillHints.oneTimeCode],
                        style: const TextStyle(
                          fontSize: 24,
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                        decoration: InputDecoration(
                          counterText: '',
                          filled: true,
                          fillColor: _isSuccess ? successColor : defaultColor,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(12),
                            borderSide: BorderSide.none,
                          ),
                        ),
                        onChanged: (val) => _onCodeChanged(index, val),
                        enabled: !_isSuccess,
                      ),
                    ),
                  );
                }),
              ),
              const SizedBox(height: 32),
              if (!_isSuccess)
                ElevatedButton.icon(
                  onPressed: _isLoading ? null : _verifyCode,
                  icon: const Icon(Icons.verified),
                  label: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text("Verify"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurpleAccent,
                    padding: const EdgeInsets.symmetric(
                      vertical: 14,
                      horizontal: 64,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                  ),
                ),
              const SizedBox(height: 20),
              TextButton(
                onPressed: _isLoading ? null : _resendCode,
                child: const Text(
                  "Resend Code",
                  style: TextStyle(color: Colors.white70, fontSize: 16),
                ),
              ),
              const SizedBox(height: 10),
              const Text(
                "📋 Long press anywhere to paste the code",
                style: TextStyle(color: Colors.white38),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
