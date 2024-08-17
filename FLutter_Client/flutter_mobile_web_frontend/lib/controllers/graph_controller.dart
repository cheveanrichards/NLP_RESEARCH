// graph_controller.dart
import 'dart:convert';
import 'package:flutter_mobile_web_frontend/models/graph_model.dart';

class GraphController {
  List<GraphModel> parseJson(String jsonString) {
    final parsed = json.decode(jsonString).cast<Map<String, dynamic>>();
    return parsed.map<GraphModel>((json) => GraphModel.fromJson(json)).toList();
  }
}
