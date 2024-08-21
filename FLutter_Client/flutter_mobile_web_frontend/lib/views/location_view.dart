import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
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
        title: Text('USA Map with Pins'),
      ),
      body: FutureBuilder<List<Location>>(
        future: _locations,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            final locations = snapshot.data!;
            return FlutterMap(
              options: MapOptions(
                center: LatLng(37.0902, -95.7129), // Center of the United States
                zoom: 4.0,
              ),
              children: [
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'com.example.app',
                ),
                MarkerLayer(
                  markers: locations.map((location) {
                    return Marker(
                      width: 40.0,
                      height: 40.0,
                      point: LatLng(location.lat, location.long),
                      builder: (ctx) => GestureDetector(
                        onTap: () {
                          showDialog(
                            context: ctx,
                            builder: (context) => AlertDialog(
                              title: Text(location.name),
                              content: Text(location.details),
                              actions: [
                                TextButton(
                                  onPressed: () => Navigator.of(context).pop(),
                                  child: Text('Close'),
                                )
                              ],
                            ),
                          );
                        },
                        child: Tooltip(
                          message: location.name,
                          child: Icon(
                            Icons.location_pin,
                            color: Colors.red,
                            size: 40.0,
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          } else {
            return Center(
              child: CircularProgressIndicator(),
            );
          }
        },
      ),
    );
  }
}
