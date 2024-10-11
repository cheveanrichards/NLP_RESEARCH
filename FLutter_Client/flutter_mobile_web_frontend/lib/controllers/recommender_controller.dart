import 'package:flutter_mobile_web_frontend/services/recommender_service.dart';

class RecommenderController {
  final RecommenderService _recommenderService;

  RecommenderController({required RecommenderService recommenderService})
      : _recommenderService = recommenderService;

  Future<String> generateRecommendation(String clusterName) async {
    try {
      return await _recommenderService.getRecommendation(clusterName);
    } catch (e) {
      throw Exception('Failed to generate recommendation: $e');
    }
  }

  // You can add more methods here if needed, such as fetching cluster names
  Future<List<String>> getClusterNames() async {
    // This is a placeholder. In a real app, you might fetch this from an API
    return ['cluster_1', 'cluster2', 'cluster3'];
  }
}