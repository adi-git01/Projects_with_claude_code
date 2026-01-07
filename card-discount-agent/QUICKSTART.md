# 🚀 Quick Start Guide - Card Discount Agent

Complete guide to get the Card Discount AI Shopping Agent up and running in 10 minutes!

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **Node.js 18+** - [Download here](https://nodejs.org/)
- ✅ **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- ✅ **Git** (already installed if you cloned the repo)
- ✅ **Google AI API Key** - [Get free key](https://aistudio.google.com/apikey)

### Check Your Versions

```bash
# Check Node.js
node --version
# Should show: v18.x.x or higher

# Check Python
python --version
# Should show: Python 3.9.x or higher

# Check npm
npm --version
# Should show: 9.x.x or higher

# Check pip
pip --version
# Should show: pip 23.x.x or higher
```

## 🔑 Step 1: Get Google AI API Key

This is **required** for the AI-powered search feature.

1. Visit: https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)
5. Keep it safe - you'll need it in Step 3!

> **Note**: Free tier includes 60 requests/minute, plenty for testing!

## 🏗️ Step 2: Setup Backend (Python)

### 2.1 Navigate to Backend Directory

```bash
cd card-discount-agent/backend
```

### 2.2 Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Google Generative AI (Gemini)
- Uvicorn (server)
- And other dependencies

**Expected output:**
```
Successfully installed fastapi-0.115.5 uvicorn-0.32.1 google-generativeai-0.8.3 ...
```

### 2.4 Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file
# On macOS/Linux:
nano .env

# On Windows:
notepad .env
```

**Update the file with your API key:**
```env
# Replace YOUR_KEY_HERE with your actual API key
GOOGLE_API_KEY=AIzaSyD_your_actual_key_here

# Leave these as default
HOST=0.0.0.0
PORT=8000
DEBUG=true
ENABLE_CACHING=true
CACHE_TTL_MINUTES=60
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Save and exit** (Ctrl+X, then Y, then Enter in nano)

### 2.5 Start Backend Server

```bash
python app.py
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Starting Card Discount Agent API...
INFO:     Gemini service initialized successfully
INFO:     Application startup complete.
```

✅ **Backend is running!**

Test it: Open http://localhost:8000 in your browser
You should see:
```json
{
  "name": "Card Discount AI Shopping Agent",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs"
}
```

**Keep this terminal window open!**

## 🎨 Step 3: Setup Frontend (React)

### 3.1 Open a NEW Terminal Window

**Important**: Don't close the backend terminal!

### 3.2 Navigate to Frontend Directory

```bash
cd card-discount-agent/frontend
```

### 3.3 Install Dependencies

```bash
npm install
```

This will install:
- React, TypeScript, Vite
- Tailwind CSS
- Axios, Lucide icons
- And other dependencies

**Expected output:**
```
added 234 packages, and audited 235 packages in 15s

89 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

### 3.4 Start Frontend Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.4.11  ready in 523 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

✅ **Frontend is running!**

## 🎉 Step 4: Use the Application

### 4.1 Open in Browser

Visit: **http://localhost:5173** (or the URL shown in your terminal)

You should see:
```
┌─────────────────────────────────────┐
│  ✨ Card Discount Agent              │
│  Find the best price with your cards│
└─────────────────────────────────────┘
```

### 4.2 Select Your Credit Cards

1. **Look for the card search box** (shows "Search cards by bank name...")
2. **Type** your bank name or card name:
   - Type "HDFC" to see all HDFC cards
   - Type "Amazon" to see Amazon Pay card
   - Type "Millennia" to find HDFC Millennia

3. **Click on cards** to select them
   - ✅ Selected cards appear as badges above the search
   - Click **X** on any badge to remove it
   - Click **"Add Popular"** to add commonly used cards

**Recommended starter cards:**
- HDFC Millennia (5% cashback)
- ICICI Amazon Pay (5% on Amazon)
- Axis Airtel Rupay (10% on quick-commerce)

> **Your selection auto-saves!** Come back later and your cards will still be selected.

### 4.3 Search for a Product

**Method 1: Paste Product URL**
```
Copy any Amazon/Flipkart product URL:
https://www.amazon.in/dp/B0CHWV2WYK

Paste it in the search bar → Click Search
```

**Method 2: Type Product Name**
```
Type in search bar:
- "iPhone 15 Pro 256GB"
- "Samsung 55 inch TV"
- "Sony WH-1000XM5"

Click Search
```

### 4.4 Wait for Results (30-90 seconds)

You'll see progress updates:
```
✓ Initializing search...
⟳ Fetching prices from platforms
⟳ Finding bank offers and discounts
⟳ Calculating effective prices
⟳ Ranking best deals
```

### 4.5 View Results

You'll see deals organized by:

**E-COMMERCE:**
```
┌─ Amazon (BEST DEAL) ─────────────────┐
│ Base Price:        ₹1,29,900         │
│ - HDFC 10%:        -₹2,000           │
│ - Coupon SAVE500:  -₹500             │
│ ────────────────────────────────     │
│ Effective Price:   ₹1,27,400         │
│ Total Savings:     ₹2,500 (1.9%)    │
│ Best Card:         HDFC Millennia    │
│ [View Deal]                          │
└──────────────────────────────────────┘
```

**QUICK-COMMERCE:**
```
┌─ Blinkit ────────────────────────────┐
│ Base Price:        ₹1,35,000         │
│ Delivery:          ₹50               │
│ - Axis 10%:        -₹13,505          │
│ ────────────────────────────────     │
│ Effective Price:   ₹1,21,545         │
│ Total Savings:     ₹13,505 (10%)    │
│ Best Card:         Axis Airtel Rupay │
│ [View Deal]                          │
└──────────────────────────────────────┘
```

## 🎯 Example Searches to Try

### Electronics
- "iPhone 15"
- "Samsung Galaxy S24"
- "MacBook Air M2"
- "Sony WH-1000XM5 headphones"

### Fashion
- "Nike Air Max"
- "Levi's jeans"
- "Adidas shoes"

### Groceries (Quick-Commerce)
- "Amul milk"
- "Maggi noodles"
- "Coca Cola"

### URLs
- Amazon: `https://www.amazon.in/dp/PRODUCT_ID`
- Flipkart: `https://www.flipkart.com/product-name/p/itm...`
- Myntra: `https://www.myntra.com/product-name/123456`

## 🔧 Troubleshooting

### Backend Issues

#### Error: "GOOGLE_API_KEY not found"
**Solution:**
```bash
cd backend
cat .env    # Check if file exists
# Make sure line reads: GOOGLE_API_KEY=AIza...
# No quotes, no spaces around =
```

#### Error: "Module 'fastapi' not found"
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Error: "Address already in use" (Port 8000)
**Solution:**
```bash
# Option 1: Kill the process
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Option 2: Change port in .env
# Edit .env file:
PORT=8001
```

### Frontend Issues

#### Error: "Failed to fetch" or CORS error
**Solution:**
1. Make sure backend is running on port 8000
2. Check backend logs for errors
3. Verify `.env` file in backend has correct CORS_ORIGINS

#### Error: "npm install" fails
**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install --legacy-peer-deps
```

#### Port 5173 already in use
**Solution:**
```bash
# Vite will automatically use next available port
# Or specify port manually:
npm run dev -- --port 3000
```

### Search Issues

#### No results returned
**Possible causes:**
1. ❌ API key invalid → Check Google AI Studio
2. ❌ API quota exceeded → Wait 1 minute or upgrade
3. ❌ Product not found → Try simpler search term
4. ❌ Network issues → Check internet connection

**Solutions:**
- Check backend terminal for error logs
- Try searching for "iPhone 15" (simple, known product)
- Verify API key is working: http://localhost:8000/docs

#### Search takes too long (>2 minutes)
**Normal behavior:**
- First search: 60-90 seconds (AI searching 25+ platforms)
- Cached results: 30-45 seconds

**If stuck:**
- Check backend logs for errors
- Try with fewer cards selected (2-3 instead of 10+)
- Simplify product name

## 📊 Quick Reference

### Starting the App

**Terminal 1 (Backend):**
```bash
cd card-discount-agent/backend
source venv/bin/activate
python app.py
# Keep running...
```

**Terminal 2 (Frontend):**
```bash
cd card-discount-agent/frontend
npm run dev
# Keep running...
```

### Stopping the App

**Stop both servers:**
- Press `Ctrl+C` in each terminal window

### URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Main app UI |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive API docs |
| Health Check | http://localhost:8000/health | Check if backend is running |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Stop server |
| `F12` | Open browser dev tools |
| `Ctrl+Shift+R` | Hard refresh browser |

## 🎓 Tips for Best Results

### Card Selection
- ✅ Select 3-5 cards you actually own
- ✅ Include at least one cashback card
- ✅ Include category-specific cards (e.g., Axis Flipkart for Flipkart search)
- ❌ Don't select 20+ cards (slows down search)

### Product Search
- ✅ Use specific product names: "iPhone 15 Pro 256GB"
- ✅ Include brand and model: "Samsung Galaxy S24 Ultra"
- ✅ Paste complete product URLs for best accuracy
- ❌ Avoid generic terms: "phone", "laptop"

### Performance
- ⚡ First search: 60-90 seconds (normal)
- ⚡ Subsequent searches: Faster due to caching
- ⚡ Simple products (e.g., "iPhone") faster than complex ones

## 🆘 Still Having Issues?

### Check Logs

**Backend logs** (in backend terminal):
```
INFO:     Search request: iPhone 15
INFO:     Searching for deals: iPhone 15...
INFO:     Found 8 deals
```

**Frontend logs** (browser console - press F12):
```
[API] Searching for deals...
[API] Received 8 deals
```

### Verify Everything is Working

**1. Backend Health Check:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

**2. Test API Directly:**
Visit: http://localhost:8000/docs
- Click on `GET /api/cards`
- Click "Try it out"
- Click "Execute"
- Should see list of 80+ cards

**3. Frontend Check:**
- Open http://localhost:5173
- Press F12 → Console tab
- Should see no red errors

### Get Help

1. **Check logs** in both terminal windows
2. **Check browser console** (F12)
3. **Review error messages** - they usually tell you what's wrong
4. **Try the examples** in this guide exactly as written
5. **Restart both servers** if something seems stuck

## 🎉 You're All Set!

Now you can:
- ✅ Search from **80+ credit cards**
- ✅ Compare prices across **25+ platforms**
- ✅ Find the best deals with your specific cards
- ✅ Save money on every purchase!

### Next Steps

- 📖 Read **README_V2.md** for detailed features
- 🔧 Check **SETUP.md** for advanced configuration
- 📚 Review **PROJECT_OVERVIEW.md** for technical details
- 📝 See **CHANGELOG.md** for version history

---

**Happy shopping! 🛍️ Save more with smart card choices! 💳**
