import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:google_fonts/google_fonts.dart';
import 'firebase_options.dart';

import 'routers/phishzil_route_generator.dart';
import 'utils/phishzil_constants.dart';
import 'routers/phishzil_app_routes.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const ProviderScope(child: PhishZilApp()));
}

class PhishZilApp extends StatelessWidget {
  const PhishZilApp({super.key});

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
      initialRoute: AppRoutes.splash, // ✅ Starts at Splash
      onGenerateRoute: PhishZilRouteGenerator.generateRoute,
    );
  }
}
