import 'package:flutter/material.dart';
import 'package:flutter_mobile_web_frontend/controllers/recommender_controller.dart';
import 'package:flutter_mobile_web_frontend/services/recommender_service.dart';

class RecommenderView extends StatefulWidget {
  @override
  _RecommenderViewState createState() => _RecommenderViewState();
}

class _RecommenderViewState extends State<RecommenderView> {
  late RecommenderController _recommenderController;
  String? _selectedCluster;
  String? _recommendation;
  bool _isLoading = false;
  List<String> _clusterNames = [];

  @override
  void initState() {
    super.initState();
    final recommenderService = RecommenderService(baseUrl: 'http://127.0.0.1:8000');
    _recommenderController = RecommenderController(recommenderService: recommenderService);
    _loadClusterNames();
  }

  void _loadClusterNames() async {
    final clusterNames = await _recommenderController.getClusterNames();
    setState(() {
      _clusterNames = clusterNames;
    });
  }

  void _generateRecommendation() async {
    if (_selectedCluster == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please select a cluster first')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
      _recommendation = null;
    });

    try {
      final recommendation = await _recommenderController.generateRecommendation(_selectedCluster!);
      setState(() {
        _recommendation = recommendation;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error generating recommendation: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          DropdownButton<String>(
            value: _selectedCluster,
            hint: Text('Select a cluster'),
            isExpanded: true,
            items: _clusterNames.map((String cluster) {
              return DropdownMenuItem<String>(
                value: cluster,
                child: Text(cluster),
              );
            }).toList(),
            onChanged: (String? newValue) {
              setState(() {
                _selectedCluster = newValue;
              });
            },
          ),
          SizedBox(height: 16),
          ElevatedButton(
            onPressed: _isLoading ? null : _generateRecommendation,
            child: _isLoading
                ? CircularProgressIndicator(color: Colors.white)
                : Text('Generate Recommendation'),
          ),
          SizedBox(height: 16),
          if (_recommendation != null)
            Expanded(
              child: SingleChildScrollView(
                child: Text(_recommendation!),
              ),
            ),
        ],
      ),
    );
  }
}