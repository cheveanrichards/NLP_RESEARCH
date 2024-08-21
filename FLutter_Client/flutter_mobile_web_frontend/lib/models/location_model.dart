class Location {
  final String name;
  final double lat;
  final double long;
  final String details;

  Location({
    required this.name,
    required this.lat,
    required this.long,
    required this.details,
  });

  // Factory constructor to create a Location object from JSON data
  factory Location.fromJson(Map<String, dynamic> json) {
    return Location(
      name: json['name'] as String,
      lat: json['lat'].toDouble(),  // Ensures the latitude is a double
      long: json['long'].toDouble(),  // Ensures the longitude is a double
      details: json['details'] as String,
    );
  }

  // Optional: Convert Location object to JSON
  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'lat': lat,
      'long': long,
      'details': details,
    };
  }
}
