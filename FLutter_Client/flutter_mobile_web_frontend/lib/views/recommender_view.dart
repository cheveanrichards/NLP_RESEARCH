import 'package:flutter/material.dart';
import 'package:flutter_mobile_web_frontend/controllers/recommender_controller.dart';
import 'package:flutter_mobile_web_frontend/services/recommender_service.dart';

class RecommenderView extends StatefulWidget {
  @override
  _RecommenderViewState createState() => _RecommenderViewState();
}

class _RecommenderViewState extends State<RecommenderView> {
  late RecommenderController _recommenderController;
  String? _selectedDirectory;
  String? _recommendation;
  bool _isLoading = false;
  List<String> _directories = [];
  final TextEditingController _promptController = TextEditingController();

  @override
  void initState() {
    super.initState();
    final recommenderService = RecommenderService(baseUrl: 'http://127.0.0.1:8000');
    _recommenderController = RecommenderController(recommenderService: recommenderService);
    _loadDirectories();
  }

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  void _loadDirectories() async {
    setState(() {
      _isLoading = true;
    });
    try {
      final directories = await _recommenderController.getDirectories();
      setState(() {
        _directories = directories;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading directories: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _generateRecommendation() async {
    if (_selectedDirectory == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please select a directory first')),
      );
      return;
    }

    if (_promptController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter a prompt')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
      _recommendation = null;
    });

    try {
      final recommendation = await _recommenderController.generateRecommendation(_selectedDirectory!, _promptController.text);
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
            value: _selectedDirectory,
            hint: Text('Select a directory'),
            isExpanded: true,
            items: _directories.map((String directory) {
              return DropdownMenuItem<String>(
                value: directory,
                child: Text(directory),
              );
            }).toList(),
            onChanged: (String? newValue) {
              setState(() {
                _selectedDirectory = newValue;
              });
            },
          ),
          SizedBox(height: 16),
          TextField(
            controller: _promptController,
            decoration: InputDecoration(
              labelText: 'Enter your prompt',
              border: OutlineInputBorder(),
            ),
            maxLines: 3,
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
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: SingleChildScrollView(
                    child: Text(_recommendation!),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
