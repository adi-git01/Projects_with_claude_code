# Card Discount AI Shopping Agent - Project Overview

## 🎯 Vision

A real-time "Deal Intelligence" agent that moves beyond simple price tracking to calculate the **Final Effective Price** by dynamically combining:

1. Live market prices across platforms
2. Site-specific coupons and promo codes
3. Real-time bank-to-card collaborations (Instant Discounts/Cashback)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Search  │  │   Card   │  │ Progress │  │  Deals   │   │
│  │   Bar    │  │ Selector │  │ Tracker  │  │   Grid   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Gemini 2.5 Flash Service                   │  │
│  │         (with Google Search Grounding)                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────┼────────────────────────────────┐ │
│  │  Discount Calculator │  Price Aggregator  │  Ranker  │ │
│  └──────────────────────┴────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │   Google Search (Live Web Data)     │
        │  • Prices across platforms          │
        │  • Bank offers & discounts          │
        │  • Coupon codes                     │
        │  • Stock availability               │
        └─────────────────────────────────────┘
```

## 📦 Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: Tailwind CSS 3.4
- **Build Tool**: Vite 5
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State Management**: React Hooks (in-memory)

### Backend
- **Framework**: FastAPI
- **AI Engine**: Google Gemini 2.5 Flash Preview
- **Search**: Google Search Grounding (built into Gemini)
- **Language**: Python 3.9+
- **Server**: Uvicorn (ASGI)

## 🎴 Supported Credit Cards

| Card | Bank | Type | Base Benefit | Use Case |
|------|------|------|--------------|----------|
| Regalia Gold | HDFC | Reward Points | 4 pts/₹100 | Premium rewards, flights |
| Millennia | HDFC | Cashback | 5% | All-rounder cashback |
| Amazon Pay | ICICI | Cashback | 5% Unlimited | Amazon purchases |
| Airtel Rupay | Axis | Cashback | 10% | Quick-commerce (Swiggy, BB) |

## 🏪 Supported Platforms

### E-Commerce
- Amazon India (amazon.in)
- Flipkart (flipkart.com)
- Myntra (myntra.com)

### Quick-Commerce
- Blinkit (blinkit.com)
- Zepto (zepto.com)
- Swiggy Instamart (swiggy.com/instamart)

## 💡 Core Features (Phase 1 - MVP)

### ✅ Completed Features

1. **Smart Search Bar**
   - Accepts product URLs (Amazon, Flipkart, etc.)
   - Accepts product names (e.g., "iPhone 15 Pro")
   - Auto-detects platform from URL

2. **Multi-Card Selection**
   - Visual card selector with color coding
   - Shows card type badges (Cashback/Instant/Points)
   - Displays base reward rates

3. **Real-Time Progress Tracking**
   - Step-by-step progress indicators
   - Visual status (pending → in progress → completed)
   - Transparent AI search process

4. **AI-Powered Search**
   - Gemini 2.5 Flash with Google Search Grounding
   - Finds current prices across 6+ platforms
   - Discovers active bank offers and discounts
   - Identifies available coupon codes
   - Checks stock availability

5. **Smart Discount Calculation**
   - Priority-based discount application:
     1. Instant Discounts (best liquidity)
     2. High % Cashback (10% Axis Airtel)
     3. Flat Cashback (5% ICICI/HDFC)
     4. Reward Points (last resort)
   - Automatic card-to-offer matching
   - Max cap and minimum purchase validation

6. **Deal Comparison UI**
   - Side-by-side E-commerce vs Quick-commerce
   - Visual price breakdowns
   - "Best Deal" badge with savings highlight
   - Out-of-stock indicators
   - Direct purchase links

7. **Intelligent Ranking**
   - Sorts by effective price (lowest first)
   - Prioritizes in-stock items
   - Shows total savings per deal
   - Displays savings percentage

## 🔄 How It Works

### User Flow

```
1. User enters product URL or name
   ↓
2. Selects credit cards from wallet
   ↓
3. Clicks "Search"
   ↓
4. AI Agent (Gemini) executes:
   a. Identifies exact product & specs
   b. Searches web for prices on each platform
   c. Finds bank offers for selected cards
   d. Discovers coupon codes
   e. Checks delivery charges
   f. Verifies stock status
   ↓
5. Backend calculates:
   - Effective Price = Base + Delivery - Discounts
   - Best card for each platform
   - Total savings
   ↓
6. Frontend displays:
   - Ranked comparison table
   - E-commerce vs Quick-commerce sections
   - Best deal highlighted
   - Price breakdowns
   ↓
7. User clicks "View Deal" → Redirects to platform
```

## 🧮 Discount Calculation Logic

### Priority Order (Per Card)

```python
def calculate_effective_price(base_price, delivery, discounts, card):
    total = base_price + delivery

    # Sort discounts by priority
    priority = {
        'instant': 1,      # Best: Immediate reduction
        'cashback': 2,     # Good: Post-purchase value
        'coupon': 3,       # Fair: Manual application
        'reward_points': 4 # Last: Delayed value
    }

    for discount in sorted(discounts, key=priority):
        if discount.card_required == card.id:
            total -= calculate_discount_amount(discount)

    return total
```

### Example Calculation

**Product**: iPhone 15 Pro (256GB)
**Platform**: Amazon
**Base Price**: ₹1,29,900
**Delivery**: ₹0 (Free)
**Card**: HDFC Millennia

**Discounts Found**:
1. HDFC Instant Discount: 10% (max ₹2000) ✅
2. Coupon SAVE500: ₹500 off ✅
3. HDFC Millennia Base: 5% cashback ❌ (already have instant)

**Calculation**:
```
Base Price:        ₹1,29,900
+ Delivery:        ₹0
- Instant (10%):   ₹2,000 (capped)
- Coupon:          ₹500
────────────────────────────
Effective Price:   ₹1,27,400
Total Savings:     ₹2,500 (1.9%)
```

## 📁 Project Structure

```
card-discount-agent/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.tsx       # Product search input
│   │   │   ├── CardSelector.tsx    # Card selection UI
│   │   │   ├── ProgressTracker.tsx # Search progress
│   │   │   ├── DealsComparison.tsx # Results grid
│   │   │   └── DealCard.tsx        # Individual deal card
│   │   ├── services/
│   │   │   └── api.ts              # Backend API client
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript definitions
│   │   ├── utils/
│   │   │   └── formatters.ts       # Utility functions
│   │   ├── App.tsx                 # Main app component
│   │   ├── main.tsx                # React entry point
│   │   └── index.css               # Tailwind imports
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── backend/
│   ├── api/
│   │   └── routes.py               # FastAPI endpoints
│   ├── models/
│   │   ├── schemas.py              # Pydantic models
│   │   └── credit_cards.py         # Card definitions
│   ├── services/
│   │   ├── gemini_service.py       # Gemini AI integration
│   │   └── discount_calculator.py  # Price calculation logic
│   ├── utils/
│   ├── app.py                      # FastAPI app
│   ├── requirements.txt
│   └── .env.example
│
├── README.md
├── SETUP.md
└── PROJECT_OVERVIEW.md (this file)
```

## 🚀 Quick Start

### 1. Get Google AI API Key
Visit: https://aistudio.google.com/apikey

### 2. Setup Backend
```bash
cd card-discount-agent/backend
pip install -r requirements.txt
cp .env.example .env
# Add GOOGLE_API_KEY to .env
python app.py
```

### 3. Setup Frontend
```bash
cd card-discount-agent/frontend
npm install
npm run dev
```

### 4. Test
Open http://localhost:3000 and search for "iPhone 15"

## 🔮 Future Roadmap

### Phase 2: Personalization & Reliability
- [ ] Smart Price Alerts (target price notifications)
- [ ] User Authentication & Saved Cards
- [ ] Price History Graphs
- [ ] Direct Buy Links (verified sellers only)
- [ ] Browser Extension

### Phase 3: Advanced Optimization
- [ ] Variant Matching (256GB vs 128GB auto-compare)
- [ ] Multi-Product Cart Optimization
- [ ] Automated Coupon Application
- [ ] EMI Calculator with Card Benefits
- [ ] Cashback Tracking Dashboard

## 📊 Performance Targets

- **Search Time**: < 60 seconds (AI search + calculation)
- **Platforms Covered**: 6+ (3 e-com, 3 q-com)
- **Accuracy**: 95%+ for price matching
- **Uptime**: 99.5%
- **Concurrent Users**: 100+ (with caching)

## 🔐 Security & Privacy

- ✅ No user data storage (session-based only)
- ✅ No credit card details collected
- ✅ HTTPS required for production
- ✅ Rate limiting on API endpoints
- ✅ Input validation & sanitization

## 📝 API Endpoints

### POST /api/search
Search for product deals

**Request**:
```json
{
  "query": "iPhone 15 Pro",
  "selected_cards": ["hdfc-millennia", "icici-amazon-pay"]
}
```

**Response**:
```json
{
  "product_name": "Apple iPhone 15 Pro 256GB",
  "product_image": "https://...",
  "deals": [
    {
      "platform": {"name": "Amazon", "type": "ecommerce"},
      "base_price": 129900,
      "delivery_charge": 0,
      "available_discounts": [...],
      "effective_price": 127400,
      "savings": 2500,
      "is_best_deal": true,
      "in_stock": true
    }
  ]
}
```

### GET /api/cards
Get supported credit cards

### GET /api/health
Health check

## 🤝 Contributing

This is a personal project but open for improvements:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📄 License

MIT License

---

**Built with ❤️ using Gemini 2.5 Flash and React**
