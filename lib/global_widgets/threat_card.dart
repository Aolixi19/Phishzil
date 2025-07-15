// lib/global_widgets/threat_card.dart
import 'package:flutter/material.dart';
import '../features/dashboard/view/models/threat_model.dart';

class ThreatCard extends StatelessWidget {
  final ThreatModel threat;
  final VoidCallback? onTap;

  const ThreatCard({super.key, required this.threat, this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white10,
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                threat.url,
                style: const TextStyle(color: Colors.white, fontSize: 16),
              ),
              const SizedBox(height: 8),
              Text(
                'Type: ${threat.type}',
                style: const TextStyle(color: Colors.white70),
              ),
              const SizedBox(height: 4),
              Text(
                'Detected: ${threat.formattedDate}',
                style: const TextStyle(color: Colors.white54),
              ),
              if (threat.description != null) ...[
                const SizedBox(height: 8),
                Text(
                  threat.description!,
                  style: const TextStyle(color: Colors.white60),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
