import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'firebase_options.dart';
import 'routers/phishzil_route_generator.dart';
import 'routers/phishzil_app_routes.dart';
import 'utils/phishzil_constants.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // ✅ Load environment variables from .env file
  try {
    await dotenv.load(fileName: ".env");
  } catch (e) {
    debugPrint("⚠️ .env file failed to load: $e");
  }

  // ✅ Initialize Firebase
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  runApp(const ProviderScope(child: PhishZilApp()));
}

class PhishZilApp extends ConsumerStatefulWidget {
  const PhishZilApp({super.key});

  @override
  ConsumerState<PhishZilApp> createState() => _PhishZilAppState();
}

class _PhishZilAppState extends ConsumerState<PhishZilApp> {
  String _initialRoute = AppRoutes.splash;

  @override
  void initState() {
    super.initState();
    _checkVerificationStatus();
  }

  Future<void> _checkVerificationStatus() async {
    final prefs = await SharedPreferences.getInstance();
    final isVerified = prefs.getBool('is_verified') ?? false;
    final token = prefs.getString('token');
    final email = prefs.getString('email');

    setState(() {
      if (!isVerified && email != null && token == null) {
        _initialRoute = AppRoutes.verifyCode;
      } else if (token != null) {
        _initialRoute = AppRoutes.home;
      } else {
        _initialRoute = AppRoutes.login;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "PhishZil",
      theme: ThemeData(
        useMaterial3: true,
        textTheme: GoogleFonts.poppinsTextTheme(),
        colorScheme: ColorScheme.fromSeed(seedColor: PhishzilColors.safeColor),
      ),
      initialRoute: _initialRoute,
      onGenerateRoute: PhishZilRouteGenerator.generateRoute,
    );
  }
}
