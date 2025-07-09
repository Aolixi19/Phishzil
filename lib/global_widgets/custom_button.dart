// lib/global_widgets/custom_button.dart
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:lottie/lottie.dart';

class GradientButton extends StatelessWidget {
  final VoidCallback onPressed;
  final String label;
  final bool isLoading;
  final bool isSuccess;

  const GradientButton({
    super.key,
    required this.onPressed,
    required this.label,
    this.isLoading = false,
    this.isSuccess = false,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 400),
      height: 50,
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: isSuccess
              ? [Colors.green, Colors.greenAccent]
              : [Colors.blueAccent, Colors.lightBlueAccent],
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: TextButton(
        onPressed: isLoading || isSuccess ? null : onPressed,
        child: Center(
          child: isLoading
              ? const SpinKitThreeBounce(color: Colors.white, size: 18)
              : isSuccess
              ? Lottie.asset(
                  'assets/animations/success-check.json',
                  height: 40,
                  fit: BoxFit.contain,
                  repeat: false,
                )
              : Text(
                  label,
                  style: const TextStyle(color: Colors.white, fontSize: 16),
                ),
        ),
      ),
    );
  }
}
