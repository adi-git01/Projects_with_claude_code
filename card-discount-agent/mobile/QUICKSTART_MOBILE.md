# 📱 Android App - 10 Minute Setup

Get the Card Discount Agent Android app running in 10 minutes!

## ⚡ Prerequisites (5 minutes)

### 1. Install Node.js
```bash
# Check if installed
node --version  # Need 18+

# If not: Download from https://nodejs.org/
```

### 2. Install JDK 17
```bash
# Check if installed
java --version  # Need 17+

# If not: Download from Oracle
```

### 3. Install Android Studio
- Download: https://developer.android.com/studio
- Install with default settings
- Open → More Actions → SDK Manager
- Install:
  - ✓ Android SDK Platform 33
  - ✓ Android SDK Build-Tools 33.0.0
  - ✓ Android Emulator

### 4. Set Environment Variables

**macOS/Linux** (`~/.bashrc` or `~/.zshrc`):
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

**Windows** (System Environment Variables):
```
ANDROID_HOME=C:\Users\YourName\AppData\Local\Android\Sdk
PATH=%PATH%;%ANDROID_HOME%\emulator;%ANDROID_HOME%\platform-tools
```

Restart terminal after adding!

## 🚀 Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd card-discount-agent/mobile
npm install
```

This installs React Native, React Navigation, and all dependencies.

### Step 2: Start Backend

**Important**: The app needs the backend API!

```bash
# In a separate terminal
cd card-discount-agent/backend
source venv/bin/activate  # if using venv
python app.py
```

Backend runs on `http://localhost:8000`

### Step 3: Create Android Emulator

**Option A: Using Android Studio**
1. Open Android Studio
2. Tools → Device Manager
3. Create Device → Pixel 5
4. System Image → Android 13 (API 33)
5. Finish

**Option B: Command Line**
```bash
# List available images
sdkmanager --list

# Download image
sdkmanager "system-images;android-33;google_apis;x86_64"

# Create emulator
avdmanager create avd -n Pixel5 -k "system-images;android-33;google_apis;x86_64" -d pixel_5
```

### Step 4: Start Metro Bundler

```bash
npm start
```

Keep this terminal open!

### Step 5: Run App

**Option A: Android Emulator** (Recommended)
```bash
# In a new terminal
npm run android
```

**Option B: Physical Device**
1. Enable Developer Options on phone
   - Settings → About Phone
   - Tap "Build Number" 7 times
2. Enable USB Debugging
   - Settings → Developer Options → USB Debugging
3. Connect phone via USB
4. Run: `npm run android`

## 🎯 First Use

### 1. App Opens Automatically

You'll see:
```
┌─────────────────────────────┐
│ Card Discount Agent         │
│ Find best price with cards  │
│                             │
│ [Search Bar]                │
│ [Your Cards (0)]            │
│                             │
│ Welcome! ✨                 │
└─────────────────────────────┘
```

### 2. Add Your Cards

1. Tap **"+ Add Card"**
2. Search modal opens
3. Type **"hdfc millennia"**
4. Tap the card
5. Card is selected and saved! ✓

Add 2-3 more cards:
- "icici amazon pay"
- "axis airtel"

### 3. Search Product

1. In search bar, type: **"iPhone 15"**
2. Tap **"Search"**
3. Wait 60-90 seconds (AI searching 25+ platforms)
4. See results!

### 4. View Deals

Results show:
```
┌─ Product ─────────────────────┐
│ Apple iPhone 15               │
│ Found 8 deals                 │
│ 🏆 Best: Save ₹2,500 on Amazon│
└───────────────────────────────┘

🛒 E-Commerce (5)
┌─ Amazon (BEST DEAL) ──────────┐
│ Base: ₹1,29,900               │
│ - HDFC 10%: -₹2,000           │
│ - Coupon: -₹500               │
│ ────────────────              │
│ Final: ₹1,27,400              │
│ Save: ₹2,500 (1.9%)           │
│                               │
│ [View Deal →]                 │
└───────────────────────────────┘
```

5. Tap **"View Deal"** → Opens browser to buy!

## 💡 Tips

### Finding Your Computer's IP (for physical device)

**macOS/Linux:**
```bash
ifconfig | grep "inet "
# Look for: 192.168.x.x
```

**Windows:**
```cmd
ipconfig
# Look for IPv4: 192.168.x.x
```

Then update `mobile/src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://192.168.1.100:8000/api';
//                          ^^^^ Your IP
```

### Hot Reload

Press **R** twice in terminal to reload
Press **Ctrl+M** on emulator for dev menu

### Debug Menu

Shake device or **Ctrl+M** (emulator):
- Enable Hot Reloading
- Enable Live Reload
- Debug with Chrome

## 🐛 Common Issues

### "Metro bundler not found"
```bash
npm start
# Keep it running, then in new terminal:
npm run android
```

### "Android SDK not found"
```bash
# Check ANDROID_HOME
echo $ANDROID_HOME
# Should show: /Users/you/Library/Android/sdk

# If empty, add to ~/.bashrc or ~/.zshrc
```

### "Emulator won't start"
1. Open Android Studio
2. Tools → Device Manager
3. Start emulator manually
4. Then `npm run android`

### "Can't connect to backend"

**On Emulator:**
- Backend should use: `http://10.0.2.2:8000` (default ✓)
- Check backend is running: `curl http://localhost:8000/health`

**On Physical Device:**
- Find your IP: `ifconfig` or `ipconfig`
- Update API_BASE_URL in `src/services/api.ts`
- Make sure phone and PC on same WiFi

### "Build failed"
```bash
# Clean and rebuild
cd android
./gradlew clean
cd ..
npm run android
```

## 📊 What You Get

### ✨ Features

- **80+ Cards** - All major Indian banks
- **25+ Platforms** - E-commerce + Quick-commerce
- **AI Search** - Gemini 2.5 Flash
- **Offline Storage** - Cards saved locally
- **Native UI** - Touch-optimized

### 📱 Screens

1. **Home** - Search + Card selector
2. **Card Modal** - Full-screen card search
3. **Results** - Scrollable deal list

### 💾 Storage

- Cards saved to AsyncStorage
- Loads instantly on app open
- No login required

## 🏗️ Build APK (Optional)

To install on any Android device:

```bash
npm run build:android
```

APK created at:
`android/app/build/outputs/apk/release/app-release.apk`

Transfer to phone and install!

## 📚 More Help

- **Detailed Guide**: [MOBILE_SETUP.md](MOBILE_SETUP.md)
- **Backend Setup**: [../backend/README.md](../backend/README.md)
- **Web Version**: [../frontend/README.md](../frontend/README.md)

## 🎉 You're Ready!

Now you can:
- ✅ Search products on mobile
- ✅ Compare prices across 25+ platforms
- ✅ Find best deals with your cards
- ✅ Shop smarter!

---

**Next Steps:**
1. Try searching different products
2. Add all your credit cards
3. Compare e-commerce vs quick-commerce
4. Save money! 💰

**Happy mobile shopping! 📱🛍️**
