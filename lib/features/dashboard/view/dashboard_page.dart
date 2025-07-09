import 'package:flutter/material.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF00172B),
      appBar: AppBar(
        title: const Text('Dashboard'),
        backgroundColor: Colors.lightBlueAccent,
      ),
      body: const Center(
        child: Text(
          'Welcome to the Dashboard!',
          style: TextStyle(color: Colors.white, fontSize: 24),
        ),
      ),
    );
  }
}
