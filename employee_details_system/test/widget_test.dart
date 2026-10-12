import 'package:flutter_test/flutter_test.dart';

import 'package:employee_details_flutter/main.dart';

void main() {
  testWidgets('Employee details form renders its fields and actions',
      (WidgetTester tester) async {
    await tester.pumpWidget(const EmployeeDetailsApp());

    expect(find.text('Employee Registration'), findsOneWidget);
    expect(find.text('Employee ID *'), findsOneWidget);
    expect(find.text('Full Name *'), findsOneWidget);
    expect(find.text('Department *'), findsOneWidget);
    expect(find.text('Designation *'), findsOneWidget);
    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Phone Number'), findsOneWidget);
    expect(find.text('Store Employee'), findsOneWidget);
    expect(find.text('Retrieve by Employee ID'), findsOneWidget);
    expect(find.text('Clear Form'), findsOneWidget);
  });
}
