import 'package:flutter/material.dart';
import 'package:flutter_mobile_web_frontend/controllers/graph_controller.dart';
import 'package:flutter_mobile_web_frontend/views/graph_view.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final String jsonString = '''
  [
    {"label": "A", "value": 50},
    {"label": "B", "value": 70},
    {"label": "C", "value": 100}
  ]
  ''';

  @override
  Widget build(BuildContext context) {
    final controller = GraphController();
    final data = controller.parseJson(jsonString);

    return MaterialApp(
      title: 'Flutter MVC Graph',
      theme: ThemeData(primarySwatch: Colors.blue),
      localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('en', ''), // English, no country code
          ],
      home: GraphView(data: data),
    );
  }
}