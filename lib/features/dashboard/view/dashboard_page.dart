import 'package:flutter/material.dart';
import 'package:phishzil/features/auth/controller/auth_provider.dart';
import 'package:provider/provider.dart';
import '../../dashboard/view/providers/dashboard_provider.dart';
import '../../../global_widgets/threat_card.dart';
import '../../../global_widgets/scan_button.dart';
import 'package:go_router/go_router.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Provider<DashboardProvider>(
      create: (_) => DashboardProvider()..fetchThreats(),
      builder: (context, child) {
        return Scaffold(
          backgroundColor: const Color(0xFF0A192F),
          appBar: AppBar(
            foregroundColor: Colors.lightBlueAccent,
            backgroundColor: Colors.transparent,
            elevation: 0,
            title: const Text(
              'PhishZil™ Dashboard',
              style: TextStyle(
                color: Colors.lightBlueAccent,
                fontSize: 22,
                fontWeight: FontWeight.w600,
              ),
            ),
            centerTitle: true,
            actions: [
              IconButton(
                icon: const Icon(Icons.history, color: Colors.lightBlue),
                tooltip: 'Clear Threats',
                onPressed: () => _confirmClearThreats(context),
              ),
            ],
          ),
          drawer: _buildDrawer(context),
          body: Consumer<DashboardProvider>(
            builder: (context, provider, _) {
              return RefreshIndicator(
                onRefresh: () async => await provider.fetchThreats(),
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  physics: const AlwaysScrollableScrollPhysics(),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildStatsHeader(provider),
                      const SizedBox(height: 25),
                      const Text(
                        'Detected Threats',
                        style: TextStyle(
                          color: Colors.white70,
                          fontSize: 18,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      const SizedBox(height: 12),
                      _buildThreatsList(provider),
                      const SizedBox(height: 30),
                      const Center(child: ScanButton()),
                    ],
                  ),
                ),
              );
            },
          ),
        );
      },
    );
  }

  Drawer _buildDrawer(BuildContext context) {
    return Drawer(
      backgroundColor: const Color(0xFF112240),
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(color: Color(0xFF0F3D5F)),
            child: Column(
              children: [
                const CircleAvatar(
                  radius: 40,
                  backgroundImage: AssetImage('assets/images/logo.png'),
                ),
                const SizedBox(height: 10),
                const Text(
                  'PhishZil™',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          _drawerItem(Icons.refresh, 'Refresh Threats', () {
            Provider.of<DashboardProvider>(
              context,
              listen: false,
            ).fetchThreats();
            Navigator.pop(context);
          }),
          _drawerItem(Icons.logout, 'Logout', () {
            Provider.of<AuthProvider>(context, listen: false).logout();
            context.go('/login'); // Navigate to login page
          }),
        ],
      ),
    );
  }

  Widget _drawerItem(IconData icon, String title, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: Colors.lightBlueAccent),
      title: Text(title, style: const TextStyle(color: Colors.white70)),
      onTap: onTap,
    );
  }

  Widget _buildStatsHeader(DashboardProvider provider) {
    return Container(
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF1F4068), Color(0xFF162447)],
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildStatBox(
            title: 'Total Threats',
            value: provider.threatCount.toString(),
            icon: Icons.security,
            color: Colors.amberAccent,
          ),
          _buildStatBox(
            title: 'High Severity',
            value: provider.threats
                .where((t) => t.severity == 'High')
                .length
                .toString(),
            icon: Icons.warning_amber_rounded,
            color: Colors.redAccent,
          ),
        ],
      ),
    );
  }

  Widget _buildStatBox({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Column(
      children: [
        Icon(icon, color: color, size: 28),
        const SizedBox(height: 6),
        Text(
          title,
          style: const TextStyle(color: Colors.white70, fontSize: 14),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: TextStyle(
            color: color,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _buildThreatsList(DashboardProvider provider) {
    if (provider.threats.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.symmetric(vertical: 40),
          child: Text(
            '✅ No threats detected yet.',
            style: TextStyle(color: Colors.white30),
          ),
        ),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: provider.threats.length,
      itemBuilder: (context, index) {
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 6),
          child: ThreatCard(threat: provider.threats[index]),
        );
      },
    );
  }

  Future<void> _confirmClearThreats(BuildContext context) async {
    final provider = Provider.of<DashboardProvider>(context, listen: false);
    if (provider.threats.isEmpty) return;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Clear All Threats?'),
        content: const Text(
          'Are you sure you want to delete all detected threat logs?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              provider.clearThreats();
              Navigator.pop(context);
            },
            child: const Text('Clear', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }
}
