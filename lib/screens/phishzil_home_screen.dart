import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:lottie/lottie.dart';
import '../utils/phishzil_constants.dart';
import '../routers/phishzil_app_routes.dart';
import '../widgets/phishzil_drawer.dart';
import '../widgets/phishzil_bottom_navbar.dart';

class PhishzilHomeScreen extends StatefulWidget {
  const PhishzilHomeScreen({super.key});

  @override
  State<PhishzilHomeScreen> createState() => _PhishzilHomeScreenState();
}

class _PhishzilHomeScreenState extends State<PhishzilHomeScreen> {
  int _selectedIndex = 0;

  void _onBottomNavTap(int index) {
    setState(() => _selectedIndex = index);

    switch (index) {
      case 1:
        Navigator.pushNamed(context, AppRoutes.scan);
        break;
      case 2:
        Navigator.pushNamed(context, AppRoutes.settings);
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0E21),
      appBar: AppBar(
        iconTheme: const IconThemeData(color: Colors.lightBlueAccent),
        title: const Text(
          "PhishZil Dashboard",
          style: TextStyle(
            color: Colors.lightBlueAccent,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: const Color(0xFF121B3C),
        elevation: 0,
      ),
      drawer: PhishzilDrawer(),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Welcome, Abihu 👋",
              style: GoogleFonts.poppins(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              "Your real-time phishing protection system.",
              style: GoogleFonts.poppins(
                color: Colors.lightBlueAccent,
                fontSize: 14,
              ),
            ),
            const SizedBox(height: 16),
            Center(
              child: Lottie.asset("assets/animations/shield.json", height: 180),
            ),
            const SizedBox(height: 24),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              crossAxisSpacing: 14,
              mainAxisSpacing: 14,
              physics: const NeverScrollableScrollPhysics(),
              children: [
                _HomeCard(
                  icon: Icons.qr_code_scanner,
                  label: 'Start Scan',
                  color: Colors.green,
                  onTap: () => Navigator.pushNamed(context, AppRoutes.scan),
                ),
                _HomeCard(
                  icon: Icons.history,
                  label: 'Scan History',
                  color: Colors.orange,
                  onTap: () => Navigator.pushNamed(context, AppRoutes.history),
                ),
                _HomeCard(
                  icon: Icons.warning_amber,
                  label: 'Threat Alerts',
                  color: Colors.redAccent,
                  onTap: () => Navigator.pushNamed(context, AppRoutes.alerts),
                ),
                _HomeCard(
                  icon: Icons.admin_panel_settings,
                  label: 'Admin Panel',
                  color: Colors.deepPurple,
                  onTap: () => Navigator.pushNamed(context, AppRoutes.admin),
                ),
              ],
            ),
            const SizedBox(height: 30),
            Row(
              children: [
                const Icon(Icons.shield, color: Colors.lightBlueAccent),
                const SizedBox(width: 8),
                Text(
                  'Security Tip',
                  style: GoogleFonts.poppins(
                    color: Colors.lightBlueAccent,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              'Avoid clicking suspicious links. Always verify before responding.',
              style: GoogleFonts.poppins(fontSize: 13, color: Colors.white70),
            ),
          ],
        ),
      ),
      bottomNavigationBar: PhishzilBottomBar(
        currentIndex: _selectedIndex,
        onTap: _onBottomNavTap,
      ),
    );
  }
}

class _HomeCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _HomeCard({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      splashColor: Colors.blue.withOpacity(0.2),
      borderRadius: BorderRadius.circular(16),
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [color.withOpacity(0.85), color.withOpacity(0.65)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.3),
              blurRadius: 6,
              offset: const Offset(2, 4),
            ),
          ],
        ),
        padding: const EdgeInsets.all(18),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 36, color: Colors.white),
            const SizedBox(height: 12),
            Text(
              label,
              textAlign: TextAlign.center,
              style: GoogleFonts.poppins(
                fontSize: 14,
                color: Colors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
