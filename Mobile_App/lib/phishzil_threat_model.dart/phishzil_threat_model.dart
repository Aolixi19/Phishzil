// lib/features/dashboard/view/models/threat_model.dart
class ThreatModel {
  final String severity;
  final DateTime detectedAt;
  final String? description;

  ThreatModel({
    required this.severity,
    required this.detectedAt,
    this.description,
  });

  String get formattedDate =>
      "${detectedAt.day}/${detectedAt.month}/${detectedAt.year}";

  String get url => url;

  Null get type => null;
}
