# Employee Details Flutter Frontend

A simple Flutter app with one employee form and two main actions:

- **Store Employee**: stores the form data locally.
- **Retrieve by Employee ID**: loads the saved record using the Employee ID as the key.
- **Clear Form**: clears the input fields.

## Fields

- Employee ID (required; used as the key)
- Full Name (required)
- Department (required)
- Designation (required)
- Email (optional; validated if entered)
- Phone Number (optional; validated if entered)

## Storage

This frontend uses `shared_preferences` to save a JSON-encoded employee record on the device. The key is normalized to uppercase, for example:

`employee_EMP001`

If you store another record with the same Employee ID, it updates/overwrites the record for that ID. This is local demo storage, not a backend database.

## Run the app

1. Install Flutter and Android Studio (or configure another Flutter target).
2. Extract this ZIP file.
3. Open a terminal in the `employee_details_flutter` folder.
4. Run:

```bash
flutter pub get
flutter run
```

To build an Android APK:

```bash
flutter build apk --release
```

## Suggested next step for a real application

For multiple users/devices or centralized employee records, replace local storage with an API and a database such as MySQL or PostgreSQL. The Employee ID can remain the unique key on the backend.
