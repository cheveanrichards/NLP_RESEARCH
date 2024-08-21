import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_mobile_web_frontend/models/location_model.dart';

class LocationService {
  final String baseUrl;

  LocationService({required this.baseUrl});

  Future<List<Location>> fetchLocations() async {
    final response = await http.get(Uri.parse('$baseUrl/locations'));

    if (response.statusCode == 200) {
      final List<dynamic> locationsData = jsonDecode(response.body);
      return locationsData.map((data) => Location.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load locations');
    }
  }
}
