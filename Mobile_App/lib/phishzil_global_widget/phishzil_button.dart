import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:lottie/lottie.dart';

class GradientButton extends StatelessWidget {
  final VoidCallback onPressed;
  final String label;
  final bool isLoading;
  final bool isSuccess;
  final LinearGradient? gradient;
  final Color textColor;

  const GradientButton({
    super.key,
    required this.onPressed,
    required this.label,
    this.isLoading = false,
    this.isSuccess = false,
    this.gradient,
    this.textColor = Colors.white,
  });

  @override
  Widget build(BuildContext context) {
    final LinearGradient appliedGradient = isSuccess
        ? const LinearGradient(colors: [Colors.green, Colors.greenAccent])
        : (gradient ??
              const LinearGradient(
                colors: [Colors.blueAccent, Colors.lightBlueAccent],
              ));

    return AnimatedContainer(
      duration: const Duration(milliseconds: 400),
      height: 50,
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: appliedGradient,
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
                  style: TextStyle(
                    color: textColor,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
        ),
      ),
    );
  }
}
