import 'package:flutter_mobile_web_frontend/services/recommender_service.dart';

class RecommenderController {
  final RecommenderService _recommenderService;

  RecommenderController({required RecommenderService recommenderService})
      : _recommenderService = recommenderService;

  Future<String> generateRecommendation(String clusterName, String prompt) async {
    try {
      return await _recommenderService.getRecommendation(clusterName, prompt);
    } catch (e) {
      throw Exception('Failed to generate recommendation: $e');
    }
  }

  Future<List<String>> getDirectories() async {
    try {
      return await _recommenderService.getDirectories();
    } catch (e) {
      throw Exception('Failed to get directories: $e');
    }
  }
}
