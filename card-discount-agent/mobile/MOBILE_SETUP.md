# 📱 Card Discount Agent - Android App Setup

Complete guide to build and run the Android app version of Card Discount Agent.

## 📋 Prerequisites

### Required Software

1. **Node.js 18+** - [Download](https://nodejs.org/)
2. **JDK 17** - [Download](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
3. **Android Studio** - [Download](https://developer.android.com/studio)
4. **React Native CLI** - Install via npm

### Android Studio Setup

1. Install Android Studio
2. Open Android Studio → More Actions → SDK Manager
3. Install:
   - Android SDK Platform 33 (Android 13)
   - Android SDK Build-Tools 33.0.0
   - Android Emulator
   - Android SDK Platform-Tools

4. Add to PATH (in `~/.bashrc` or `~/.zshrc`):
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd card-discount-agent/mobile
npm install
```

### 2. Start Backend Server

The mobile app needs the backend API running:

```bash
cd ../backend
python app.py
```

Backend will run on `http://localhost:8000`

**For Android Emulator**: The app is pre-configured to use `10.0.2.2:8000` (emulator's localhost)

**For Physical Device**:
- Find your computer's IP: `ifconfig` or `ipconfig`
- Update `mobile/src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://YOUR_IP:8000/api';
// Example: 'http://192.168.1.100:8000/api'
```

### 3. Start Metro Bundler

```bash
npm start
```

### 4. Run on Android

**Option A: Android Emulator**
```bash
# Create emulator in Android Studio first
# Then run:
npm run android
```

**Option B: Physical Device**
```bash
# Enable USB Debugging on your Android phone
# Connect via USB
# Run:
npm run android
```

## 🏗️ Building APK

### Development APK (for testing)

```bash
npm run build:android
```

APK location: `android/app/build/outputs/apk/release/app-release.apk`

### Production Bundle (for Play Store)

```bash
npm run build:android:bundle
```

AAB location: `android/app/build/outputs/bundle/release/app-release.aab`

## 📱 Features

### ✨ Mobile-Optimized UI

- **Touch-friendly** - Large buttons, easy tapping
- **Swipe gestures** - Natural mobile navigation
- **Modal search** - Full-screen card selection
- **Responsive** - Works on all screen sizes
- **Native feel** - Platform-specific components

### 💾 Offline Storage

- **AsyncStorage** - Cards saved locally
- **Persistent selection** - No login required
- **Fast access** - Cards load instantly

### 🔍 Search Features

- **Same AI power** - Gemini 2.5 Flash
- **25+ platforms** - All e-commerce & quick-commerce
- **80+ cards** - Full database included
- **Real-time** - Live price comparisons

## 📊 App Structure

```
mobile/
├── src/
│   ├── components/
│   │   ├── SearchBar.tsx          # Search input
│   │   ├── CardSelector.tsx       # Card selection modal
│   │   └── DealCard.tsx           # Deal display
│   ├── screens/
│   │   └── HomeScreen.tsx         # Main screen
│   ├── services/
│   │   └── api.ts                 # Backend API
│   ├── data/
│   │   ├── creditCards.ts         # 80+ cards
│   │   └── platforms.ts           # 25+ platforms
│   ├── types/
│   │   └── index.ts               # TypeScript types
│   └── App.tsx                    # Root component
├── android/                       # Android native code
├── package.json
└── tsconfig.json
```

## 🔧 Configuration

### API Endpoint

Edit `src/services/api.ts`:

```typescript
const API_BASE_URL = __DEV__
  ? 'http://10.0.2.2:8000/api'     // Emulator
  : 'https://your-api.com/api';    // Production
```

### App Name & Bundle ID

Edit `android/app/build.gradle`:

```gradle
defaultConfig {
    applicationId "com.carddiscountagent"
    // ...
}
```

### App Icon

Replace icons in `android/app/src/main/res/mipmap-*/`:
- `ic_launcher.png` - Standard icon
- `ic_launcher_round.png` - Round icon

Use [Android Asset Studio](https://romannurik.github.io/AndroidAssetStudio/icons-launcher.html)

## 🐛 Troubleshooting

### Metro Bundler Issues

```bash
# Clear cache and restart
npm start -- --reset-cache
```

### Build Errors

```bash
# Clean and rebuild
cd android
./gradlew clean
cd ..
npm run android
```

### ADB Device Not Found

```bash
# Check devices
adb devices

# Restart ADB
adb kill-server
adb start-server
```

### Emulator Won't Start

1. Open Android Studio
2. Tools → Device Manager
3. Create new Virtual Device
4. Use Pixel 5, Android 13

### Backend Connection Failed

**Emulator:**
- Use `10.0.2.2` instead of `localhost`
- Check backend is running: `curl http://localhost:8000/health`

**Physical Device:**
- Use computer's IP address
- Both devices must be on same WiFi
- Check firewall settings

## 📦 Dependencies

### Core
- `react-native`: 0.73.2
- `react`: 18.2.0

### Navigation
- `@react-navigation/native`: 6.1.9
- `@react-navigation/native-stack`: 6.9.17

### Storage
- `@react-native-async-storage/async-storage`: 1.21.0

### HTTP
- `axios`: 1.6.5

### UI
- `react-native-vector-icons`: 10.0.3
- `react-native-svg`: 14.1.0

## 🎯 Usage Flow

1. **Open App** → See card selector
2. **Tap "Add Card"** → Search modal opens
3. **Type "HDFC"** → See all HDFC cards
4. **Tap card** → Selected (auto-saved)
5. **Enter product** → "iPhone 15 Pro"
6. **Tap Search** → Wait 60-90 seconds
7. **View results** → E-com + Q-com deals
8. **Tap "View Deal"** → Opens browser

## 🚀 Performance

- **App Size**: ~15MB (release)
- **First Load**: 2-3 seconds
- **Search Time**: 60-90 seconds (AI search)
- **Card Load**: Instant (cached)

## 📈 Next Steps

### Planned Features (Future)

- [ ] Price history graphs
- [ ] Push notifications for price drops
- [ ] Barcode scanner
- [ ] Wishlist / Favorites
- [ ] Price alerts
- [ ] Share deals
- [ ] Dark mode

### Deploy to Play Store

1. Generate signing key
2. Configure `android/app/build.gradle`
3. Build release bundle
4. Upload to Play Console
5. Fill store listing
6. Submit for review

See: [Publishing Guide](https://reactnative.dev/docs/signed-apk-android)

## 💡 Tips

### For Developers

- Use React Native Debugger
- Enable Hermes for performance
- Use Flipper for debugging

### For Testing

- Test on multiple screen sizes
- Test on Android 10+ devices
- Check offline behavior
- Verify deep links

### For Users

- Keep app updated
- Clear cache if slow
- Report bugs via email

## 📄 License

MIT License - Same as web version

---

**Built with React Native for Android! 📱**
