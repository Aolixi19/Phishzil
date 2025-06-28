import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../routers/phishzil_app_routes.dart';
import '../utils/phishzil_constants.dart';
import '../providers/phishzil_auth_provider.dart';
import '../providers/phishzil_auth_storage.dart';

class PhishzilDrawer extends ConsumerWidget {
  const PhishzilDrawer({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Drawer(
      backgroundColor: const Color(0xFF0A0E21),
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: BoxDecoration(color: PhishzilColors.primaryColor),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Center(
                  child: Image.asset(
                    PhishzilAssets.loginLogo,
                    height: 60,
                    width: 60,
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  'PhishZil',
                  style: GoogleFonts.poppins(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  "Cybersecurity Defender",
                  style: GoogleFonts.poppins(
                    color: Colors.white70,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),

          _buildTile(
            icon: Icons.home,
            label: 'Home',
            onTap: () => Navigator.pushNamed(context, AppRoutes.home),
          ),
          _buildTile(
            icon: Icons.qr_code_scanner,
            label: 'Start Scan',
            onTap: () => Navigator.pushNamed(context, AppRoutes.scan),
          ),
          _buildTile(
            icon: Icons.history,
            label: 'Scan History',
            onTap: () => Navigator.pushNamed(context, AppRoutes.history),
          ),
          _buildTile(
            icon: Icons.warning_amber,
            label: 'Threat Alerts',
            onTap: () => Navigator.pushNamed(context, AppRoutes.alerts),
          ),
          _buildTile(
            icon: Icons.admin_panel_settings,
            label: 'Admin Panel',
            onTap: () => Navigator.pushNamed(context, AppRoutes.admin),
          ),
          _buildTile(
            icon: Icons.settings,
            label: 'Settings',
            onTap: () => Navigator.pushNamed(context, AppRoutes.settings),
          ),

          const Divider(color: Colors.white30),

          _buildTile(
            icon: Icons.logout,
            label: 'Logout',
            iconColor: PhishzilColors.danger,
            textColor: PhishzilColors.danger,
            onTap: () async {
              // ✅ Clear stored credentials
              await AuthStorage.clearCredentials();

              // ✅ Reset auth state
              ref.read(authProvider.notifier).logout();

              // ✅ Navigate to login screen and prevent back navigation
              Navigator.pushNamedAndRemoveUntil(
                context,
                AppRoutes.login,
                (route) => false,
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildTile({
    required IconData icon,
    required String label,
    Color iconColor = Colors.white,
    Color textColor = Colors.white,
    required VoidCallback onTap,
  }) {
    return ListTile(
      leading: Icon(icon, size: 24, color: iconColor),
      title: Text(
        label,
        style: GoogleFonts.poppins(fontSize: 15, color: textColor),
      ),
      onTap: onTap,
    );
  }
}
