import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:flutter_map_heatmap/flutter_map_heatmap.dart';
import 'package:flutter_mobile_web_frontend/models/location_model.dart';
import 'package:flutter_mobile_web_frontend/controllers/location_controller.dart';
import 'package:flutter_mobile_web_frontend/services/location_service.dart';

class MapScreen extends StatefulWidget {
  @override
  _MapScreenState createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late Future<List<Location>> _locations;
  late LocationController _locationController;
  final MapController _mapController = MapController();

  @override
  void initState() {
    super.initState();
    final locationService = LocationService(baseUrl: 'http://127.0.0.1:8000');
    _locationController = LocationController(locationService: locationService);
    _locations = _locationController.getLocations();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Knowledge Graph Heatmap'),
      ),
      body: FutureBuilder<List<Location>>(
        future: _locations,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No locations available'));
          }

          final locations = snapshot.data!;
          return FlutterMap(
            mapController: _mapController,
            options: MapOptions(
              center: LatLng(37.0902, -95.7129),
              zoom: 4.0,
              onTap: (tapPosition, point) => _showNearestLocationDetails(locations, point),
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                subdomains: ['a', 'b', 'c'],
              ),
              HeatMapLayer(
                heatMapDataSource: InMemoryHeatMapDataSource(
                  data: locations
                      .map((location) => WeightedLatLng(
                            LatLng(location.lat, location.long),
                            1.0,
                          ))
                      .toList(),
                ),
                heatMapOptions: HeatMapOptions(
                  gradient: HeatMapOptions.defaultGradient,
                  minOpacity: 0.1,
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  void _showNearestLocationDetails(List<Location> locations, LatLng tappedPoint) {
    Location? nearestLocation;
    double minDistance = double.infinity;

    for (var location in locations) {
      final distance = const Distance().as(
        LengthUnit.Kilometer,
        LatLng(location.lat, location.long),
        tappedPoint,
      );

      if (distance < minDistance) {
        minDistance = distance;
        nearestLocation = location;
      }
    }

    if (nearestLocation != null) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Text(nearestLocation?.name ?? 'Unknown Location'),
          content: Text(nearestLocation?.details ?? 'No details available'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text('Close'),
            ),
          ],
        ),
      );
    }
  }
}