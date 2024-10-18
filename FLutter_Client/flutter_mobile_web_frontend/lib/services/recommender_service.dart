import 'package:http/http.dart' as http;
import 'dart:convert';

class RecommenderService {
  final String baseUrl;

  RecommenderService({required this.baseUrl});

  Future<String> getRecommendation(String clusterName, String prompt) async {
    final response = await http.get(
      Uri.parse('$baseUrl/recommender/$clusterName').replace(
        queryParameters: {'prompt': prompt},
      ),
    );

    if (response.statusCode == 200) {
      final jsonBody = jsonDecode(response.body);
      return jsonBody['response'];
    } else {
      throw Exception('Failed to get recommendation: ${response.statusCode}');
    }
  }

  Future<List<String>> getDirectories() async {
    final response = await http.get(Uri.parse('$baseUrl/directories'));

    if (response.statusCode == 200) {
      final List<dynamic> jsonBody = jsonDecode(response.body);
      return jsonBody.cast<String>();
    } else {
      throw Exception('Failed to get directories: ${response.statusCode}');
    }
  }
}
