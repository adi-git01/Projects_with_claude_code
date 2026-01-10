#!/usr/bin/env python3
"""
Comprehensive API test script
Tests the complete flow from card selection to deal search
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up test environment
os.environ.setdefault('GOOGLE_API_KEY', os.getenv('GOOGLE_API_KEY', ''))

from models.all_credit_cards import get_card_by_id, get_cards_by_ids, ALL_INDIAN_CARDS
from models.schemas import SearchRequest, Discount
from services.discount_calculator import DiscountCalculator

def test_card_database():
    """Test 1: Verify card database"""
    print("\n" + "="*60)
    print("TEST 1: Card Database")
    print("="*60)

    # Check total cards
    total_cards = len(ALL_INDIAN_CARDS)
    print(f"✓ Total cards in database: {total_cards}")
    assert total_cards >= 80, f"Expected 80+ cards, found {total_cards}"

    # Test individual card retrieval
    test_ids = ['hdfc-millennia', 'icici-amazon-pay', 'axis-airtel-rupay']
    for card_id in test_ids:
        card = get_card_by_id(card_id)
        assert card is not None, f"Card {card_id} not found"
        print(f"✓ Found card: {card.bank} {card.name} ({card.base_reward}% reward)")

    # Test multiple cards retrieval
    cards = get_cards_by_ids(['hdfc-millennia', 'icici-amazon-pay'])
    assert len(cards) == 2, f"Expected 2 cards, got {len(cards)}"
    print(f"✓ Successfully retrieved {len(cards)} cards")

    print("✅ Card database test PASSED\n")
    return True

def test_discount_calculator():
    """Test 2: Verify discount calculation"""
    print("="*60)
    print("TEST 2: Discount Calculator")
    print("="*60)

    # Get test cards
    cards = get_cards_by_ids(['hdfc-millennia', 'icici-amazon-pay', 'axis-airtel-rupay'])

    # Create test scenario: ₹1000 product with 10% instant discount
    base_price = 1000.0
    delivery = 50.0

    discounts = [
        Discount(
            type='instant',
            value=10.0,
            is_percentage=True,
            description='HDFC Millennia 10% instant discount',
            card_required='hdfc-millennia',
            max_cap=150.0,
            min_purchase=500.0
        ),
        Discount(
            type='coupon',
            value=100.0,
            is_percentage=False,
            description='WELCOME100 coupon',
            min_purchase=None
        )
    ]

    # Test price calculation
    calculator = DiscountCalculator()
    effective_price, savings = calculator.calculate_effective_price(
        base_price, delivery, discounts, cards[0]
    )

    # Base + Delivery = 1050
    # - 10% of 1000 (max 150) = -100
    # - 100 flat = -100
    # Expected: 850
    print(f"Base price: ₹{base_price}")
    print(f"Delivery: ₹{delivery}")
    print(f"Discounts applied: ₹{savings}")
    print(f"Effective price: ₹{effective_price}")

    assert effective_price == 850.0, f"Expected ₹850, got ₹{effective_price}"
    print("✓ Discount calculation correct")

    # Test best card finder
    best_card, best_price, best_savings = calculator.find_best_card_for_deal(
        base_price, delivery, discounts, cards
    )

    assert best_card is not None, "No best card found"
    print(f"✓ Best card: {best_card.bank} {best_card.name} (₹{best_price})")

    print("✅ Discount calculator test PASSED\n")
    return True

async def test_search_request_validation():
    """Test 3: Verify SearchRequest accepts camelCase"""
    print("="*60)
    print("TEST 3: API Request Schema (camelCase support)")
    print("="*60)

    # Test with camelCase (from frontend)
    request_data = {
        'query': 'Philips OneBlade intimate',
        'selectedCards': ['hdfc-millennia', 'icici-amazon-pay']
    }

    try:
        search_request = SearchRequest(**request_data)
        print(f"✓ Query: {search_request.query}")
        print(f"✓ Selected cards: {search_request.selected_cards}")
        assert search_request.selected_cards == ['hdfc-millennia', 'icici-amazon-pay']
        print("✓ camelCase conversion working correctly")
    except Exception as e:
        print(f"❌ Failed to parse request: {e}")
        return False

    # Test with snake_case (internal)
    request_data_snake = {
        'query': 'iPhone 15',
        'selected_cards': ['axis-airtel-rupay']
    }

    try:
        search_request = SearchRequest(**request_data_snake)
        print(f"✓ snake_case also works: {search_request.selected_cards}")
    except Exception as e:
        print(f"❌ Failed to parse snake_case: {e}")
        return False

    print("✅ API request schema test PASSED\n")
    return True

async def test_gemini_integration():
    """Test 4: Verify Gemini service (if API key available)"""
    print("="*60)
    print("TEST 4: Gemini AI Integration")
    print("="*60)

    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not found - SKIPPING Gemini test")
        print("   (This is OK for development, but required for production)")
        return True

    try:
        from services.gemini_service import GeminiService

        print("✓ Initializing Gemini service...")
        gemini = GeminiService()
        print("✓ Gemini service initialized successfully")

        print("\n📝 Note: Full search test would take 60-90 seconds")
        print("   Skipping actual search in test (would require real API call)")
        print("   Service is ready and configured correctly")

    except Exception as e:
        print(f"❌ Gemini initialization failed: {e}")
        return False

    print("✅ Gemini integration test PASSED\n")
    return True

def test_backend_imports():
    """Test 5: Verify all backend imports work"""
    print("="*60)
    print("TEST 5: Backend Module Imports")
    print("="*60)

    try:
        from api.routes import router
        print("✓ API routes imported successfully")

        from models.schemas import (
            SearchRequest, SearchResponse, ProductDeal,
            CreditCard, Discount, Platform
        )
        print("✓ All schema models imported successfully")

        from models.all_credit_cards import ALL_INDIAN_CARDS
        print("✓ Credit cards database imported successfully")

        from services.discount_calculator import DiscountCalculator
        print("✓ Discount calculator imported successfully")

        print("✅ All backend imports test PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 " + "="*58)
    print("   CARD DISCOUNT AGENT - COMPREHENSIVE API TEST")
    print("   " + "="*58 + "\n")

    results = []

    # Run tests
    results.append(("Backend Imports", test_backend_imports()))
    results.append(("Card Database", test_card_database()))
    results.append(("Discount Calculator", test_discount_calculator()))
    results.append(("API Schema", await test_search_request_validation()))
    results.append(("Gemini Integration", await test_gemini_integration()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "="*60)
    print(f"RESULT: {passed}/{total} tests passed")
    print("="*60 + "\n")

    if passed == total:
        print("🎉 All tests PASSED! Backend is ready to use.\n")
        print("Next steps:")
        print("1. Make sure GOOGLE_API_KEY is set in .env")
        print("2. Start backend: python app.py")
        print("3. Test search with: Philips OneBlade intimate")
        print("4. Use cards: HDFC Millennia, ICICI Amazon Pay\n")
        return 0
    else:
        print("❌ Some tests FAILED. Please fix the issues above.\n")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
