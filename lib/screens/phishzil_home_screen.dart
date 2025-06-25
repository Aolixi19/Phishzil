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
    setState(() {
      _selectedIndex = index;
    });

    if (index == 0) {
      // Already on Home, do nothing
    } else if (index == 1) {
      Navigator.pushNamed(context, AppRoutes.scan);
    } else if (index == 2) {
      Navigator.pushNamed(context, AppRoutes.settings);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: const IconThemeData(color: Colors.lightBlue),
        title: const Text(
          "PhishZil",
          style: TextStyle(
            color: PhishzilColors.primaryColor,
            fontSize: 20.0,
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: PhishzilColors.safeColor,
        elevation: 0.0,
      ),
      drawer: PhishzilDrawer(),
      backgroundColor: const Color.fromARGB(255, 8, 12, 68),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome, Abihu 👋',
              style: GoogleFonts.poppins(
                fontSize: 24,
                color: Colors.pink,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              'Protecting you from phishing in real-time.',
              style: GoogleFonts.poppins(
                fontSize: 25.0,
                color: Colors.lightBlue,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 6),
            Center(
              child: Lottie.asset('assets/animations/shield.json', height: 180),
            ),
            const SizedBox(height: 20),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisSpacing: 10,
              mainAxisSpacing: 10,
              children: [
                _HomeActionCard(
                  icon: Icons.qr_code_scanner,
                  label: 'Start Scan',
                  onTap: () => Navigator.pushNamed(context, AppRoutes.scan),
                ),
                _HomeActionCard(
                  icon: Icons.history,
                  label: 'Scan History',
                  onTap: () => Navigator.pushNamed(context, AppRoutes.history),
                ),
                _HomeActionCard(
                  icon: Icons.warning_amber,
                  label: 'Threat Alerts',
                  onTap: () => Navigator.pushNamed(context, AppRoutes.alerts),
                ),
                _HomeActionCard(
                  icon: Icons.admin_panel_settings,
                  label: 'Admin Panel',
                  onTap: () => Navigator.pushNamed(context, AppRoutes.admin),
                ),
              ],
            ),
            const SizedBox(height: 30),
            Row(
              children: [
                const Icon(Icons.shield, color: Colors.lightBlue),
                const SizedBox(width: 8),
                Text(
                  'Security Tip:',
                  style: GoogleFonts.poppins(
                    fontWeight: FontWeight.bold,
                    color: Colors.lightBlue,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Text(
              'Never click suspicious links in unexpected emails, even if they look familiar.',
              style: GoogleFonts.poppins(fontSize: 14, color: Colors.lightBlue),
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

class _HomeActionCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _HomeActionCard({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: const [
            BoxShadow(
              color: Colors.black12,
              blurRadius: 6,
              offset: Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: Colors.blue),
            const SizedBox(height: 10),
            Text(
              label,
              textAlign: TextAlign.center,
              style: GoogleFonts.poppins(fontSize: 14),
            ),
          ],
        ),
      ),
    );
  }
}
