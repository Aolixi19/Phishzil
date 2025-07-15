// lib/features/dashboard/view/providers/dashboard_provider.dart
import 'package:flutter/material.dart';
import '../models/threat_model.dart';

class DashboardProvider extends ChangeNotifier {
  List<ThreatModel> threats = [];
  bool isScanning = false;

  int get threatCount => threats.length;

  Future<void> fetchThreats() async {
    // Fetch or update threats here
    notifyListeners();
  }

  void clearThreats() {
    threats.clear();
    notifyListeners();
  }

  Future<void> startScan() async {
    isScanning = true;
    notifyListeners();
    // Simulate scan
    await Future.delayed(const Duration(seconds: 2));
    isScanning = false;
    notifyListeners();
  }
}