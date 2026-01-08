# 📱 Card Discount Agent - Android App

React Native Android app for finding the best prices with your credit card discounts.

## ✨ Features

- 🎴 **80+ Credit Cards** - Search and select from all major Indian banks
- 🏪 **25+ Platforms** - E-commerce & Quick-commerce price comparison
- 🤖 **AI-Powered** - Gemini 2.5 Flash with Google Search
- 💾 **Offline Storage** - Your cards saved locally
- 📱 **Native UI** - Smooth, touch-optimized interface

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- JDK 17
- Android Studio
- Backend server running

### Install & Run

```bash
# Install dependencies
npm install

# Start Metro
npm start

# Run on Android
npm run android
```

### Build APK

```bash
npm run build:android
```

## 📖 Documentation

- **Setup Guide**: [MOBILE_SETUP.md](MOBILE_SETUP.md)
- **Backend Setup**: [../backend/README.md](../backend/README.md)

## 🎯 Usage

1. Open app
2. Tap "Add Card" and select your cards
3. Enter product URL or name
4. Tap "Search"
5. View deals across 25+ platforms
6. Tap "View Deal" to purchase

## 🏗️ Tech Stack

- React Native 0.73
- TypeScript
- React Navigation
- AsyncStorage
- Axios

## 📱 Screenshots

[Add screenshots here after building]

## 🐛 Troubleshooting

See [MOBILE_SETUP.md](MOBILE_SETUP.md#-troubleshooting)

Common issues:
- Backend connection: Use `10.0.2.2:8000` for emulator
- Build errors: Run `cd android && ./gradlew clean`
- Metro issues: `npm start -- --reset-cache`

## 📄 License

MIT License
