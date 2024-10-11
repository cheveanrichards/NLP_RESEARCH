import 'package:http/http.dart' as http;
import 'dart:convert';

class RecommenderService {
  final String baseUrl;

  RecommenderService({required this.baseUrl});

  Future<String> getRecommendation(String clusterName) async {
    final response = await http.get(Uri.parse('$baseUrl/recommender/$clusterName'));

    if (response.statusCode == 200) {
      final jsonBody = jsonDecode(response.body);
      return jsonBody['response'];
    } else {
      throw Exception('Failed to get recommendation: ${response.statusCode}');
    }
  }
}