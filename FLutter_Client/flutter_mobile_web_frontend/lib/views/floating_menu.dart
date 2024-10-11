import 'package:flutter/material.dart';
import 'package:flutter_mobile_web_frontend/controllers/menu_controller.dart';

class FloatingMenu extends StatelessWidget {
  final Function(int) onItemSelected;
  final MYMenuController _menuController = MYMenuController();

  FloatingMenu({required this.onItemSelected});

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton(
      child: Icon(Icons.menu),
      onPressed: () {
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return SimpleDialog(
              title: Text('Menu'),
              children: [
                SimpleDialogOption(
                  onPressed: () {
                    _menuController.navigateToPage(context, 0);
                    onItemSelected(0);
                  },
                  child: Text('Cluster Visualization'),
                ),
                SimpleDialogOption(
                  onPressed: () {
                    _menuController.navigateToPage(context, 1);
                    onItemSelected(1);
                  },
                  child: Text('Recommender View'),
                ),
                SimpleDialogOption(
                  onPressed: () {
                    _menuController.navigateToPage(context, 2);
                    onItemSelected(2);
                  },
                  child: Text('LLM/QA Recommender'),
                ),
                SimpleDialogOption(
                  onPressed: () {
                    _menuController.navigateToPage(context, 3);
                    onItemSelected(3);
                  },
                  child: Text('Model Generation'),
                ),
            
              ],
            );
          },
        );
      },
    );
  }
}