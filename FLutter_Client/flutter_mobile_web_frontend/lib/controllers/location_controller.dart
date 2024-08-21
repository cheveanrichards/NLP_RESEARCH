import 'package:flutter_mobile_web_frontend/models/location_model.dart';
import 'package:flutter_mobile_web_frontend/services/location_service.dart';

class LocationController {
  final LocationService locationService;

  LocationController({required this.locationService});

  Future<List<Location>> getLocations() async {
    return await locationService.fetchLocations();
  }
}
