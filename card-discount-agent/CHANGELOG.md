# Changelog

All notable changes to the Card Discount AI Shopping Agent project.

## [2.0.0] - 2026-01-07

### 🎉 Major Features Added

#### Smart Card Management
- **80+ Credit Cards Database** - Comprehensive database of all major Indian credit cards
  - HDFC Bank (8 cards)
  - ICICI Bank (6 cards)
  - Axis Bank (7 cards)
  - SBI Cards (5 cards)
  - American Express (4 cards)
  - Standard Chartered, IndusInd, Yes Bank, AU Bank, HSBC, Kotak, RBL, IDFC First
- **Autocomplete Card Selector** - Type to search cards by bank name or card name
- **Persistent Card Selection** - Cards auto-saved using localStorage
- **Quick Actions** - "Add Popular" button and "Clear All" button
- **Visual Feedback** - Selected cards shown as dismissible badges

#### Expanded Platform Coverage
- **15 E-commerce Platforms** (up from 3)
  - Added: AJIO, Meesho, Nykaa, Tata CLiQ, Snapdeal, JioMart
  - Added: Croma, Reliance Digital, Vijay Sales
  - Added: BigBasket, PharmEasy, Netmeds
- **8 Quick-commerce Platforms** (up from 3)
  - Added: BB Now, Dunzo Daily, Amazon Fresh, Flipkart Quick, JioMart Express

### 🔧 Technical Improvements

#### Frontend
- Created `CardSelectorAutocomplete.tsx` component with search functionality
- Added `data/creditCards.ts` with 80+ card definitions
- Added `data/platforms.ts` with 25+ platform definitions
- Updated `App.tsx` to use new autocomplete selector
- Enhanced TypeScript types with `description` field for cards

#### Backend
- Created `models/all_credit_cards.py` with complete card database
- Updated `services/gemini_service.py` with expanded platforms list
- Updated `api/routes.py` to serve 80+ cards via `/api/cards` endpoint
- Dynamic card info generation in AI prompts

### 📚 Documentation
- Created `README_V2.md` with comprehensive feature documentation
- Added platform comparison tables
- Added card combination recommendations
- Added usage examples and pro tips

### 🐛 Bug Fixes
- Fixed card persistence across page reloads
- Improved search performance with result limiting

### ⚡ Performance
- Limited autocomplete results to 50 cards for faster rendering
- Optimized card search with lowercase comparison

## [1.0.0] - 2026-01-07

### Initial Release
- React frontend with Tailwind CSS
- FastAPI backend with Gemini 2.5 Flash
- Google Search Grounding integration
- 4 credit cards support
- 6 platforms support (3 e-com + 3 q-com)
- Price comparison and deal ranking
- Progress tracking UI
- Real-time discount calculation

---

## Version History Summary

| Version | Cards | Platforms | Key Feature |
|---------|-------|-----------|-------------|
| 2.0.0   | 80+   | 25+       | Autocomplete card search |
| 1.0.0   | 4     | 6         | Initial MVP release |

## Upcoming Features

See PROJECT_OVERVIEW.md for detailed roadmap:
- Phase 2: Price alerts, user authentication, price history
- Phase 3: Browser extension, mobile app, EMI calculator
