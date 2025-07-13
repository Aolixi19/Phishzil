# 📱 PhishZil Mobile App

**PhishZil** is a real-time phishing detection mobile application developed using Flutter. It is designed to help users detect suspicious links, phishing attempts, and scam behaviors through intelligent scanning and alerts. The app integrates secure user authentication, email verification, and will support background scanning for suspicious content.

---

## 🚀 Features Implemented

### ✅ 1. Mobile App Setup
- Flutter project initialized with platform-specific configurations.
- Project theming and folder structure organized.
- Routing implemented using `GoRouter`.

### ✅ 2. Authentication System
- Firebase Email & Password login integrated.
- Google Sign-In with Firebase Auth setup.
- Sign-Up, Login, and Forgot Password UI with form validation.
- User state managed securely with `Provider`.

### ✅ 3. OTP Email Verification & Reset
- OTP code request & cooldown implemented.
- Email code verification after signup.
- Reset code flow for password recovery.

### ✅ 4. Security & Local Storage
- Used `flutter_secure_storage` to securely store:
  - Authentication tokens
  - User data
- Auto-login and logout implemented.

### ✅ 5. Dashboard Redirection
- Redirect users to dashboard upon successful login (email or Google).
- Clear UI feedback with snackbars for success/error states.

### ✅ 6. Backend Integration
- Connected app to a live backend using `.env` and `flutter_dotenv`.
- Verified registration, login, and OTP verification via real-time endpoints.

---

## 🔄 In Progress / Upcoming Features

- 🔍 **Notification Scanner**: Scan notifications and detect suspicious links (background service).
- 🛡️ **Phishing Detection API**: Integrate backend service to scan links/files for phishing.
- 🎨 UI and UX refinements.
- 🚀 Deployment preparation for Play Store & iOS (signing, testing, assets).

---

## 📁 Tech Stack

- Flutter (Dart)
- Firebase Auth & Google Sign-In
- flutter_secure_storage
- Provider for State Management
- GoRouter for Navigation
- dotenv for Environment Configuration

---
