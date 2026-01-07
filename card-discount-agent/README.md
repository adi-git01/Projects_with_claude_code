# Card Discount AI Shopping Agent

A real-time "Deal Intelligence" agent that calculates the **Final Effective Price** by dynamically combining:
- Live market prices across E-commerce & Quick-commerce
- Site-specific coupons and promo codes
- Real-time bank-to-card collaborations (Instant Discounts/Cashback)

## Features

### Phase 1 - MVP (Current)
- ✅ Search Bar for product links (Amazon, Flipkart) or names
- ✅ Real-time AI-powered search grounding
- ✅ Progress tracking UI for transparency
- ✅ Side-by-side E-com vs Q-com comparison
- ✅ Dynamic card benefit calculations for:
  - HDFC Regalia Gold (Reward Points/Flights)
  - HDFC Millennia (5% CashPoints)
  - ICICI Amazon Pay (5% Unlimited Cashback)
  - Axis Airtel Rupay (10% Q-Com Cashback)

## Tech Stack

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: Python FastAPI
- **AI Engine**: Google Gemini 2.5 Flash Preview
- **Search**: Google Search Grounding API
- **State**: In-memory (session-based)

## Quick Start

### Backend Setup
```bash
cd card-discount-agent/backend
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
python app.py
```

### Frontend Setup
```bash
cd card-discount-agent/frontend
npm install
npm run dev
```

## Usage

1. Enter a product URL (Amazon/Flipkart) or product name
2. Select your credit cards from the wallet
3. AI agent searches for:
   - Current prices across platforms
   - Active bank offers and discounts
   - Available coupon codes
4. View ranked comparison with effective prices
5. Click "Best Deal" to navigate to the offer

## Card Priority Logic

The agent calculates benefits in this order:
1. **Instant Discounts** - Immediate price reduction (best liquidity)
2. **High % Cashback** - 10% on Axis Airtel for Swiggy/BigBasket
3. **Flat Cashback** - 5% on Amazon Pay ICICI (safety net)
4. **Reward Points** - Last resort when no other offer exists

## Architecture

```
Frontend (React)
    ↓
Backend API (FastAPI)
    ↓
Gemini 2.5 Flash (with Search Grounding)
    ↓
[Live Web Data: Prices + Offers + Coupons]
    ↓
Price Calculator (Card-aware)
    ↓
Ranked Results
```

## API Endpoints

- `POST /api/search` - Search for product deals
- `GET /api/cards` - Get supported credit cards
- `POST /api/calculate` - Calculate effective prices

## Environment Variables

```env
GOOGLE_API_KEY=your_gemini_api_key
SEARCH_API_KEY=your_search_api_key (optional)
ENABLE_CACHING=true
CACHE_TTL_MINUTES=60
```

## License

MIT
