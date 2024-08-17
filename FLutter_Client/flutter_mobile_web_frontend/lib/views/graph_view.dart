import 'package:flutter/material.dart';
import 'package:flutter_mobile_web_frontend/models/graph_model.dart';

class GraphView extends StatelessWidget {
  final List<GraphModel> data;

  GraphView({required this.data});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Graph Mock')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: data.map((item) => _buildBar(item)).toList(),
        ),
      ),
    );
  }

  Widget _buildBar(GraphModel item) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Text(item.label),
          SizedBox(width: 10),
          Container(
            width: item.value.toDouble(),
            height: 20,
            color: Colors.blue,
          ),
          SizedBox(width: 10),
          Text('${item.value}'),
        ],
      ),
    );
  }
}