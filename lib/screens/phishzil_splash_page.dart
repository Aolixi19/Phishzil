import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../routers/phishzil_app_routes.dart';
import '../providers/phishzil_auth_provider.dart';
import '../utils/phishzil_constants.dart';

class PhishzilSplashPage extends ConsumerStatefulWidget {
  const PhishzilSplashPage({super.key});

  @override
  ConsumerState<PhishzilSplashPage> createState() => _PhishzilSplashPageState();
}

class _PhishzilSplashPageState extends ConsumerState<PhishzilSplashPage>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  double _fadeOpacity = 0.0;
  int _animationCount = 0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    );

    _scaleAnimation = TweenSequence([
      TweenSequenceItem(tween: Tween(begin: 0.8, end: 1.1), weight: 50),
      TweenSequenceItem(tween: Tween(begin: 1.1, end: 0.95), weight: 50),
    ]).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));

    _controller.addStatusListener(_handleAnimationRepeat);

    // Start fade in and scale
    Future.delayed(const Duration(milliseconds: 100), () {
      setState(() {
        _fadeOpacity = 1.0;
      });
    });

    _controller.forward();
  }

  void _handleAnimationRepeat(AnimationStatus status) async {
    if (status == AnimationStatus.completed) {
      _animationCount++;
      if (_animationCount < 3) {
        _controller.forward(from: 0);
      } else {
        _controller.removeStatusListener(_handleAnimationRepeat);
        await Future.delayed(const Duration(milliseconds: 800));
        await _navigate();
      }
    }
  }

  Future<void> _navigate() async {
    final auth = ref.read(authProvider.notifier);
    await auth.tryAutoLogin();

    final user = FirebaseAuth.instance.currentUser;
    await user?.reload();

    if (user != null && user.emailVerified) {
      Navigator.pushReplacementNamed(context, AppRoutes.home);
    } else if (user != null && !user.emailVerified) {
      Navigator.pushReplacementNamed(context, AppRoutes.verifyEmail);
    } else {
      Navigator.pushReplacementNamed(context, AppRoutes.login);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: AnimatedOpacity(
          opacity: _fadeOpacity,
          duration: const Duration(seconds: 1),
          child: AnimatedBuilder(
            animation: _controller,
            builder: (_, child) {
              return Transform.scale(
                scale: _scaleAnimation.value,
                child: child,
              );
            },
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset(PhishzilAssets.loginLogo, width: 160, height: 160),
                const SizedBox(height: 20),
                const Text(
                  'PhishZil',
                  style: TextStyle(
                    fontSize: 28,
                    color: Color(0xFF4FC3F7),
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.5,
                  ),
                ),
                const SizedBox(height: 40),
                const CircularProgressIndicator(
                  color: Colors.lightBlueAccent,
                  strokeWidth: 3,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
