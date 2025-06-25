import 'package:flutter/material.dart';
import '../routers/phishzil_app_routes.dart';
import 'package:google_fonts/google_fonts.dart';
import '../utils/phishzil_constants.dart';
// Adjusted to match your import

class PhishzilDrawer extends StatelessWidget {
  const PhishzilDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          // Drawer header with app name and logo
          DrawerHeader(
            decoration: BoxDecoration(
              color: PhishzilColors.primaryColor, // Use constant
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Image.asset(
                  PhishzilAssets.logo, // Use constant
                  height: PhishzilSpacing.height, // Use constant
                  width: PhishzilSpacing.height, // Use constant
                  fit: BoxFit.cover,
                ),
                SizedBox(height: PhishzilSpacing.padding), // Use constant
                Text(
                  'PhishZil',
                  style: GoogleFonts.poppins(
                    // Changed to Schyler to match pubspec.yaml
                    color: Colors.white,
                    fontSize: PhishzilSpacing.height, // Use constant
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          // Navigation items
          ListTile(
            leading: Icon(
              Icons.home,
              size: PhishzilSpacing.height,
            ), // Use constant
            title: Text(
              'Home',
              style: GoogleFonts.poppins(
                fontSize: PhishzilSpacing.height, // Use constant
              ),
            ),
            onTap: () {
              Navigator.pushNamed(context, AppRoutes.home);
            },
          ),
          ListTile(
            leading: Icon(
              Icons.history,
              size: PhishzilSpacing.height,
            ), // Use constant
            title: Text(
              'History',
              style: GoogleFonts.poppins(
                fontSize: PhishzilSpacing.height, // Use constant
              ),
            ),
            onTap: () {
              Navigator.pushNamed(context, AppRoutes.history);
            },
          ),
          ListTile(
            leading: Icon(
              Icons.settings,
              size: PhishzilSpacing.height,
            ), // Use constant
            title: Text(
              'Settings',
              style: GoogleFonts.poppins(
                fontSize: PhishzilSpacing.height, // Use constant
              ),
            ),
            onTap: () {
              Navigator.pushNamed(context, AppRoutes.scan);
            },
          ),
          ListTile(
            leading: Icon(
              Icons.warning_amber,
              size: PhishzilSpacing.height,
            ), // Use constant
            title: Text(
              'Test Alert',
              style: GoogleFonts.poppins(
                fontSize: PhishzilSpacing.height, // Use constant
              ),
            ),
            onTap: () {
              Navigator.pushNamed(context, AppRoutes.admin);
            },
          ),

          Divider(),
          ListTile(
            leading: Icon(
              Icons.logout,
              size: PhishzilSpacing.height,
            ), // Use constant
            title: Text(
              'Logout',
              style: GoogleFonts.poppins(
                fontSize: PhishzilSpacing.height, // Use constant
                color: PhishzilColors.danger, // Use constant
              ),
            ),
            onTap: () {
              print('Logout tapped - Implement backend logout here');
              Navigator.pop(context);
              // TODO: Add navigation to login screen or app reset
            },
          ),
        ],
      ),
    );
  }
}
