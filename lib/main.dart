import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'routers/phishzil_route_generator.dart';

void main() {
  runApp(const ProviderScope(child: PhishZilApp()));
}

class PhishZilApp extends StatelessWidget {
  const PhishZilApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        textTheme: GoogleFonts.poppinsTextTheme(),
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      ),
      initialRoute: '/login',
      onGenerateRoute: PhishZilRouteGenerator.generateRoute,
    );
  }
}
