import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(const EmployeeDetailsApp());
}

class EmployeeDetailsApp extends StatelessWidget {
  const EmployeeDetailsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Employee Details',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF2457C5)),
        useMaterial3: true,
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
          filled: true,
          fillColor: Color(0xFFF8FAFF),
        ),
      ),
      home: const EmployeeFormPage(),
    );
  }
}

class EmployeeFormPage extends StatefulWidget {
  const EmployeeFormPage({super.key});

  @override
  State<EmployeeFormPage> createState() => _EmployeeFormPageState();
}

class _EmployeeFormPageState extends State<EmployeeFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _employeeIdController = TextEditingController();
  final _nameController = TextEditingController();
  final _departmentController = TextEditingController();
  final _designationController = TextEditingController();
  final _emailController = TextEditingController();
  final _phoneController = TextEditingController();

  bool _isBusy = false;
  String _statusMessage = 'Enter employee details, then choose Store Employee.';
  bool _statusIsError = false;

  String _storageKey(String employeeId) =>
      'employee_${employeeId.trim().toUpperCase()}';

  @override
  void dispose() {
    _employeeIdController.dispose();
    _nameController.dispose();
    _departmentController.dispose();
    _designationController.dispose();
    _emailController.dispose();
    _phoneController.dispose();
    super.dispose();
  }

  String? _requiredValidator(String? value, String label) {
    if (value == null || value.trim().isEmpty) {
      return '$label is required';
    }
    return null;
  }

  Future<void> _storeEmployee() async {
    FocusScope.of(context).unfocus();
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isBusy = true;
      _statusMessage = '';
      _statusIsError = false;
    });

    try {
      final employeeId = _employeeIdController.text.trim().toUpperCase();
      final employee = <String, String>{
        'employeeId': employeeId,
        'name': _nameController.text.trim(),
        'department': _departmentController.text.trim(),
        'designation': _designationController.text.trim(),
        'email': _emailController.text.trim(),
        'phone': _phoneController.text.trim(),
      };

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_storageKey(employeeId), jsonEncode(employee));

      if (!mounted) return;
      setState(() {
        _statusMessage = 'Employee $employeeId stored successfully on this device.';
        _statusIsError = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Employee details stored successfully')),
      );
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _statusMessage = 'Could not store employee details: $e';
        _statusIsError = true;
      });
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  Future<void> _retrieveEmployee() async {
    FocusScope.of(context).unfocus();
    final employeeId = _employeeIdController.text.trim().toUpperCase();

    if (employeeId.isEmpty) {
      setState(() {
        _statusMessage = 'Enter an Employee ID to retrieve the record.';
        _statusIsError = true;
      });
      return;
    }

    setState(() {
      _isBusy = true;
      _statusMessage = '';
      _statusIsError = false;
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      final savedValue = prefs.getString(_storageKey(employeeId));

      if (!mounted) return;
      if (savedValue == null) {
        setState(() {
          _statusMessage = 'No employee record found for ID $employeeId.';
          _statusIsError = true;
        });
        return;
      }

      final employee = Map<String, dynamic>.from(jsonDecode(savedValue) as Map);
      _nameController.text = employee['name']?.toString() ?? '';
      _departmentController.text = employee['department']?.toString() ?? '';
      _designationController.text = employee['designation']?.toString() ?? '';
      _emailController.text = employee['email']?.toString() ?? '';
      _phoneController.text = employee['phone']?.toString() ?? '';

      setState(() {
        _statusMessage = 'Employee $employeeId retrieved successfully.';
        _statusIsError = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _statusMessage = 'Could not retrieve employee details: $e';
        _statusIsError = true;
      });
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  void _clearForm() {
    _formKey.currentState?.reset();
    _employeeIdController.clear();
    _nameController.clear();
    _departmentController.clear();
    _designationController.clear();
    _emailController.clear();
    _phoneController.clear();
    setState(() {
      _statusMessage = 'Form cleared. Enter an Employee ID to start.';
      _statusIsError = false;
    });
  }

  Widget _textField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    String? Function(String?)? validator,
    TextInputType keyboardType = TextInputType.text,
    bool required = false,
  }) {
    return TextFormField(
      controller: controller,
      keyboardType: keyboardType,
      textCapitalization: label == 'Employee ID' ||
              label == 'Department' ||
              label == 'Designation'
          ? TextCapitalization.characters
          : TextCapitalization.words,
      decoration: InputDecoration(
        labelText: required ? '$label *' : label,
        prefixIcon: Icon(icon),
      ),
      validator: validator,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF1F4FA),
      appBar: AppBar(
        title: const Text('Employee Details'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 680),
            child: ListView(
              padding: const EdgeInsets.all(18),
              children: [
                Card(
                  elevation: 1,
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          const Icon(Icons.badge_outlined, size: 42),
                          const SizedBox(height: 8),
                          Text(
                            'Employee Registration',
                            textAlign: TextAlign.center,
                            style: Theme.of(context).textTheme.headlineSmall
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            'Employee ID is used as the unique storage key.',
                            textAlign: TextAlign.center,
                            style: Theme.of(context).textTheme.bodyMedium,
                          ),
                          const SizedBox(height: 22),
                          _textField(
                            controller: _employeeIdController,
                            label: 'Employee ID',
                            icon: Icons.key_outlined,
                            required: true,
                            validator: (v) => _requiredValidator(v, 'Employee ID'),
                          ),
                          const SizedBox(height: 14),
                          _textField(
                            controller: _nameController,
                            label: 'Full Name',
                            icon: Icons.person_outline,
                            required: true,
                            validator: (v) => _requiredValidator(v, 'Full Name'),
                          ),
                          const SizedBox(height: 14),
                          _textField(
                            controller: _departmentController,
                            label: 'Department',
                            icon: Icons.apartment_outlined,
                            required: true,
                            validator: (v) => _requiredValidator(v, 'Department'),
                          ),
                          const SizedBox(height: 14),
                          _textField(
                            controller: _designationController,
                            label: 'Designation',
                            icon: Icons.work_outline,
                            required: true,
                            validator: (v) => _requiredValidator(v, 'Designation'),
                          ),
                          const SizedBox(height: 14),
                          _textField(
                            controller: _emailController,
                            label: 'Email',
                            icon: Icons.email_outlined,
                            keyboardType: TextInputType.emailAddress,
                            validator: (v) {
                              if (v == null || v.trim().isEmpty) return null;
                              if (!RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
                                  .hasMatch(v.trim())) {
                                return 'Enter a valid email address';
                              }
                              return null;
                            },
                          ),
                          const SizedBox(height: 14),
                          _textField(
                            controller: _phoneController,
                            label: 'Phone Number',
                            icon: Icons.phone_outlined,
                            keyboardType: TextInputType.phone,
                            validator: (v) {
                              if (v == null || v.trim().isEmpty) return null;
                              if (!RegExp(r'^[0-9+\-\s()]{7,20}$')
                                  .hasMatch(v.trim())) {
                                return 'Enter a valid phone number';
                              }
                              return null;
                            },
                          ),
                          const SizedBox(height: 22),
                          FilledButton.icon(
                            onPressed: _isBusy ? null : _storeEmployee,
                            icon: const Icon(Icons.save_outlined),
                            label: const Text('Store Employee'),
                          ),
                          const SizedBox(height: 10),
                          OutlinedButton.icon(
                            onPressed: _isBusy ? null : _retrieveEmployee,
                            icon: const Icon(Icons.search),
                            label: const Text('Retrieve by Employee ID'),
                          ),
                          const SizedBox(height: 10),
                          TextButton.icon(
                            onPressed: _isBusy ? null : _clearForm,
                            icon: const Icon(Icons.refresh),
                            label: const Text('Clear Form'),
                          ),
                          if (_isBusy) ...[
                            const SizedBox(height: 12),
                            const Center(child: CircularProgressIndicator()),
                          ],
                          if (_statusMessage.isNotEmpty) ...[
                            const SizedBox(height: 14),
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: _statusIsError
                                    ? const Color(0xFFFFEEEE)
                                    : const Color(0xFFEAF6ED),
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: Text(
                                _statusMessage,
                                style: TextStyle(
                                  color: _statusIsError
                                      ? const Color(0xFF9B1C1C)
                                      : const Color(0xFF176534),
                                ),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 8),
                  child: Text(
                    'Note: This demo saves data locally on this device using SharedPreferences. '
                    'It does not send employee data to a server or database.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.black54, fontSize: 12),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
