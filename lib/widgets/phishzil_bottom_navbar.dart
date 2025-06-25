import 'package:flutter/material.dart';

import '../utils/phishzil_constants.dart';

class PhishzilBottomBar extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap; // Slightly more idiomatic than Function(int)

  const PhishzilBottomBar({
    super.key,
    required this.currentIndex,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      type: BottomNavigationBarType.fixed, // Ensures even spacing for all items
      backgroundColor: PhishzilColors.safeColor,
      currentIndex: currentIndex,
      onTap: onTap,

      selectedItemColor: Colors.lightBlue, // Selected label/icon color
      unselectedItemColor: Colors.pink, // Unselected label/icon color

      selectedLabelStyle: const TextStyle(fontWeight: FontWeight.bold),
      unselectedLabelStyle: const TextStyle(fontWeight: FontWeight.normal),

      items: const [
        BottomNavigationBarItem(
          icon: Icon(Icons.home),
          label: "Home",
          tooltip: "Home",
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.qr_code_scanner),
          label: "Scan",
          tooltip: "Scan QR",
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.person),
          label: "Profile",
          tooltip: "User Profile",
        ),
      ],
    );
  }
}
