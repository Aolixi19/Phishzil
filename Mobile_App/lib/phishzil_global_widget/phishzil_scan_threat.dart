// lib/global_widgets/scan_button.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../phishzil_dashboard/phishzil_dashboard_provider.dart';

class ScanButton extends StatelessWidget {
  const ScanButton({super.key});

  @override
  Widget build(BuildContext context) {
    final dashboardProvider = Provider.of<DashboardProvider>(context);

    return Center(
      child: ElevatedButton.icon(
        onPressed: dashboardProvider.isScanning
            ? null
            : () async {
                await dashboardProvider.startScan();
              },
        icon: dashboardProvider.isScanning
            ? const SizedBox(
                width: 16,
                height: 16,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: Colors.white,
                ),
              )
            : const Icon(Icons.search),
        label: Text(dashboardProvider.isScanning ? "Scanning..." : "Scan Now"),
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 16),
          backgroundColor: Colors.lightBlueAccent,
          disabledBackgroundColor: Colors.lightBlueAccent.withOpacity(0.6),
          foregroundColor: Colors.white,
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
    );
  }
}
