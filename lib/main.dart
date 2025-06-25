import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'routers/phishzil_route_generator.dart'; // ✅ FIXED import

void main() {
  runApp(const PhishZilApp());
}

class PhishZilApp extends StatelessWidget {
  const PhishZilApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PhishZil',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        textTheme: GoogleFonts.poppinsTextTheme(),
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      ),
      initialRoute: '/',
      onGenerateRoute: PhishZilRouteGenerator.generateRoute, // ✅ FIXED
    );
  }
}
