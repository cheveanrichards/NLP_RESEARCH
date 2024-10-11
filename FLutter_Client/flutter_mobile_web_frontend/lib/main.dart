import 'package:flutter/material.dart';
import 'package:flutter_mobile_web_frontend/views/location_view.dart';
import 'package:flutter_mobile_web_frontend/views/floating_menu.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_mobile_web_frontend/views/recommender_view.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'USA Map with Pins',
      theme: ThemeData(primarySwatch: Colors.green),
      home: MainScreen(),
      localizationsDelegates: [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: [
        Locale('en', ''), // English
        // Add more locales as needed
      ],
    );
  }
}

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState () => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;
  final List<Widget> _pages = [
    MapScreen(),
    RecommenderView(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_currentIndex],
      floatingActionButton: FloatingMenu(
        onItemSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
      ),
    );
  }
}