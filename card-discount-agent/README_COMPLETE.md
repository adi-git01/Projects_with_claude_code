# 🎴 Card Discount AI Shopping Agent - Complete Documentation

## 📖 Documentation Index

Your complete guide to the Card Discount AI Shopping Agent. Choose the guide that fits your needs:

### 🚀 Getting Started

| Guide | Time | For Who | Read When |
|-------|------|---------|-----------|
| **[START_HERE.md](START_HERE.md)** | 5 min | Complete beginners | You just want to run it NOW |
| **[QUICKSTART.md](QUICKSTART.md)** | 10 min | New users | You want step-by-step guidance |
| **[SETUP.md](SETUP.md)** | 15 min | Technical users | You want detailed configuration |

### 📚 Understanding the App

| Guide | Purpose | Read When |
|-------|---------|-----------|
| **[README.md](README.md)** | Feature overview | You want to know what it does |
| **[README_V2.md](README_V2.md)** | V2.0 features & enhancements | You want to see what's new |
| **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** | Technical architecture | You want to understand how it works |

### 🔧 When Things Go Wrong

| Guide | Coverage | Read When |
|-------|----------|-----------|
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | All common issues | Something isn't working |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history | You want to see what changed |

---

## ⚡ Super Quick Start

**Just want to run it? Follow these 3 steps:**

### 1️⃣ Get API Key (1 minute)
Visit: https://aistudio.google.com/apikey → Copy your key

### 2️⃣ Backend (2 minutes)
```bash
cd card-discount-agent/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key
python app.py
```

### 3️⃣ Frontend (2 minutes) - New Terminal
```bash
cd card-discount-agent/frontend
npm install
npm run dev
```

**Open**: http://localhost:5173 → Select cards → Search products! 🎉

> **Detailed instructions**: See [START_HERE.md](START_HERE.md)

---

## 🎯 What Does This App Do?

The Card Discount Agent is an AI-powered shopping assistant that:

### ✨ Main Features

1. **Smart Card Search** - Search from **80+ Indian credit cards**
   - HDFC, ICICI, Axis, SBI, Amex, and 10+ more banks
   - Autocomplete dropdown with instant results
   - Your selection auto-saves for next time

2. **Massive Platform Coverage** - Compares prices across **25+ platforms**
   - E-commerce: Amazon, Flipkart, Myntra, Nykaa, Tata CLiQ, etc.
   - Quick-commerce: Blinkit, Zepto, Swiggy Instamart, etc.

3. **AI-Powered Search** - Uses Gemini 2.5 Flash with Google Search
   - Finds current prices across all platforms
   - Discovers active bank offers and discounts
   - Identifies available coupon codes
   - Checks stock availability

4. **Smart Discount Calculation** - Priority-based logic
   - Instant discounts (best - immediate savings)
   - High % cashback (10% on quick-commerce)
   - Flat cashback (5% safety net)
   - Reward points (last resort)

5. **Best Deal Highlighting** - Ranks all deals
   - Shows effective price after all discounts
   - Recommends best card for each platform
   - Displays total savings amount
   - Marks the absolute best deal

### 🎴 Example Search Flow

```
1. You type: "iPhone 15 Pro"
2. Select cards: HDFC Millennia, ICICI Amazon Pay, Axis Airtel
3. AI searches 25+ platforms (60 seconds)
4. Results show:

┌─ Amazon (BEST DEAL) ─────────────────┐
│ Base:          ₹1,29,900             │
│ - HDFC 10%:    -₹2,000               │
│ - Coupon:      -₹500                 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━     │
│ Final:         ₹1,27,400             │
│ Save:          ₹2,500 (1.9%)         │
│ Best card:     HDFC Millennia        │
└──────────────────────────────────────┘

You click [View Deal] → Redirected to Amazon
You buy with HDFC Millennia → Save ₹2,500!
```

---

## 📊 Version Comparison

| Feature | V1.0 (Initial) | V2.0 (Current) |
|---------|----------------|----------------|
| Credit Cards | 4 pre-selected | **80+ searchable** |
| Card Selection | Manual grid | **Autocomplete** |
| Card Memory | None | **Auto-saved** |
| E-commerce | 3 platforms | **15 platforms** |
| Quick-commerce | 3 platforms | **8 platforms** |
| Total Platforms | 6 | **25+** |
| Search Speed | 90s | **60s** |
| User Experience | Basic | **Enhanced** |

---

## 🗺️ Documentation Roadmap

### For First-Time Users

1. **Start with**: [START_HERE.md](START_HERE.md)
   - Get running in 5 minutes
   - Absolute minimum steps

2. **Then read**: [QUICKSTART.md](QUICKSTART.md)
   - Understand each step
   - Learn best practices
   - See usage examples

3. **Finally check**: [README_V2.md](README_V2.md)
   - Explore all features
   - Discover advanced options
   - Read tips and tricks

### For Developers

1. **Start with**: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
   - Understand architecture
   - See tech stack
   - Review API design

2. **Then read**: [SETUP.md](SETUP.md)
   - Advanced configuration
   - Production deployment
   - Environment variables

3. **Reference**: [CHANGELOG.md](CHANGELOG.md)
   - Version history
   - Breaking changes
   - Migration guides

### When Debugging

1. **Check**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - All common issues
   - Step-by-step fixes
   - Debug checklist

2. **Review**: Logs in terminals
   - Backend logs
   - Frontend console (F12)
   - Network tab

---

## 🎯 Quick Reference

### Essential URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Main app |
| Backend API | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive docs |
| Health Check | http://localhost:8000/health | Server status |

### Essential Commands

**Start Backend:**
```bash
cd card-discount-agent/backend
source venv/bin/activate  # if using venv
python app.py
```

**Start Frontend:**
```bash
cd card-discount-agent/frontend
npm run dev
```

**Stop Servers:**
- Press `Ctrl+C` in each terminal

### Essential Files

| File | Purpose | When to Edit |
|------|---------|--------------|
| `backend/.env` | API key & config | Setup, troubleshooting |
| `frontend/.env` | API URL | Changing backend port |
| `backend/requirements.txt` | Python packages | Adding dependencies |
| `frontend/package.json` | npm packages | Adding dependencies |

---

## 🎓 Learning Path

### Level 1: User (15 minutes)
1. Follow [START_HERE.md](START_HERE.md)
2. Select your cards
3. Search a product
4. Understand results
5. Find best deals

### Level 2: Power User (30 minutes)
1. Read [README_V2.md](README_V2.md)
2. Try all 80+ cards
3. Search different products
4. Compare e-com vs q-com
5. Learn card combinations

### Level 3: Developer (2 hours)
1. Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
2. Study architecture
3. Review API endpoints
4. Understand AI prompts
5. Modify and extend

---

## 💡 Pro Tips

### For Best Results

1. **Card Selection**
   - Select 3-5 cards you actually own
   - Include one cashback card minimum
   - Add category cards for specific searches

2. **Product Search**
   - Use specific names: "iPhone 15 Pro 256GB"
   - Paste complete URLs for accuracy
   - Try brand + model number

3. **Performance**
   - First search takes 60-90s (normal)
   - Results are cached for 60 minutes
   - Fewer cards = faster search

### Popular Card Combos

**For Amazon Shopping:**
- ICICI Amazon Pay (5% always)
- HDFC Millennia (5% during sales)
- Axis Magnus (for reward points)

**For Fashion:**
- Axis Myntra (7% on Myntra)
- HDFC Millennia (5% everywhere else)
- SBI Cashback (5% backup)

**For Quick-Commerce:**
- Axis Airtel Rupay (10% Swiggy/BB/Blinkit)
- HDFC Swiggy (10% on Swiggy)
- HDFC Millennia (5% backup)

**All-Rounders:**
- SBI Cashback (5% all online)
- HDFC Millennia (5% shopping/dining)
- SC Ultimate (3.3% everything)

---

## 🔧 System Requirements

### Minimum
- **Node.js**: 18.0.0+
- **Python**: 3.9.0+
- **RAM**: 4GB
- **Disk**: 500MB
- **Internet**: Required

### Recommended
- **Node.js**: 20.0.0+
- **Python**: 3.11.0+
- **RAM**: 8GB
- **Disk**: 1GB
- **Internet**: Broadband

---

## 📦 What's Included

```
card-discount-agent/
├── 📖 Documentation
│   ├── START_HERE.md              ← 5-min quick start
│   ├── QUICKSTART.md              ← 10-min detailed guide
│   ├── SETUP.md                   ← Technical setup
│   ├── TROUBLESHOOTING.md         ← Fix all issues
│   ├── README.md                  ← Feature overview
│   ├── README_V2.md               ← V2 enhancements
│   ├── PROJECT_OVERVIEW.md        ← Architecture
│   └── CHANGELOG.md               ← Version history
│
├── 💻 Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/
│   │   │   ├── CardSelectorAutocomplete.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   ├── DealsComparison.tsx
│   │   │   └── DealCard.tsx
│   │   ├── data/
│   │   │   ├── creditCards.ts     ← 80+ cards
│   │   │   └── platforms.ts       ← 25+ platforms
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   └── utils/
│   │       └── formatters.ts
│   └── package.json
│
└── 🔧 Backend (Python + FastAPI)
    ├── api/
    │   └── routes.py              ← API endpoints
    ├── models/
    │   ├── all_credit_cards.py    ← 80+ cards DB
    │   ├── credit_cards.py        ← Legacy cards
    │   └── schemas.py             ← Data models
    ├── services/
    │   ├── gemini_service.py      ← AI search
    │   └── discount_calculator.py ← Price logic
    ├── app.py                     ← Main server
    └── requirements.txt
```

---

## 🚀 Deployment

### Development (Current)
- Backend: `python app.py`
- Frontend: `npm run dev`
- Access: http://localhost:5173

### Production (Future)
- **Backend**: Railway, Render, Google Cloud Run
- **Frontend**: Vercel, Netlify, Cloudflare Pages
- **Database**: Firestore (for Phase 2)

---

## 🎯 Use Cases

### 1. Electronics Shopping
```
Search: "iPhone 15 Pro 256GB"
Compare: Amazon vs Flipkart vs Croma
Best Card: ICICI Amazon Pay (5%) on Amazon
Savings: ₹6,495
```

### 2. Fashion Shopping
```
Search: "Nike Air Max 270"
Compare: Myntra vs AJIO vs Flipkart
Best Card: Axis Myntra (7%) on Myntra
Savings: ₹875
```

### 3. Grocery Shopping
```
Search: "Amul Gold Milk 1L"
Compare: BigBasket vs Blinkit vs Zepto
Best Card: Axis Airtel (10%) on Blinkit
Savings: ₹7
```

---

## 📞 Support & Help

### Where to Look

1. **Can't start**: Read [START_HERE.md](START_HERE.md)
2. **Errors**: Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. **Features**: Read [README_V2.md](README_V2.md)
4. **Architecture**: Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

### Still Stuck?

1. Check both terminal logs
2. Check browser console (F12)
3. Verify API key is valid
4. Restart both servers
5. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📄 License

MIT License - Free to use, modify, and distribute

---

## 🎉 Ready to Start?

**New User?** → [START_HERE.md](START_HERE.md)

**Want Details?** → [QUICKSTART.md](QUICKSTART.md)

**Need Help?** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Explore Features?** → [README_V2.md](README_V2.md)

---

**Happy Shopping! Save more with smart card choices! 🛍️💳**
