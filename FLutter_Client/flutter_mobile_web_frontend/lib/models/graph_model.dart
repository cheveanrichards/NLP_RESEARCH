// graph_model.dart
class GraphModel {
  final String label;
  final int value;

  GraphModel({required this.label, required this.value});

  factory GraphModel.fromJson(Map<String, dynamic> json) {
    return GraphModel(
      label: json['label'],
      value: json['value'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'label': label,
      'value': value,
    };
  }
}
