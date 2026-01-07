"""
API Routes for Card Discount Agent
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request

from models.schemas import (
    SearchRequest,
    SearchResponse,
    ProductDeal,
    Platform,
    CreditCard,
    ErrorResponse
)
from models.credit_cards import get_cards_by_ids, CREDIT_CARDS
from services.gemini_service import GeminiService
from services.discount_calculator import DiscountCalculator

logger = logging.getLogger(__name__)
router = APIRouter()

def get_gemini_service(request: Request) -> GeminiService:
    """Dependency to get Gemini service from app state"""
    return request.app.state.gemini_service

@router.post("/search", response_model=SearchResponse)
async def search_deals(
    search_request: SearchRequest,
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> SearchResponse:
    """
    Search for product deals across platforms

    This endpoint:
    1. Uses Gemini AI with Google Search to find current prices
    2. Discovers bank offers and coupon codes
    3. Calculates effective prices for each selected card
    4. Ranks deals by best price
    """
    try:
        logger.info(f"Search request: {search_request.query}")

        # Validate selected cards
        if not search_request.selected_cards:
            raise HTTPException(status_code=400, detail="No cards selected")

        # Get card objects
        selected_cards = get_cards_by_ids(search_request.selected_cards)
        if not selected_cards:
            raise HTTPException(status_code=400, detail="Invalid card IDs")

        # Search using Gemini with Google Search
        search_results = await gemini_service.search_product_deals(
            query=search_request.query,
            selected_cards=search_request.selected_cards
        )

        # Build product deals
        deals: List[ProductDeal] = []

        for deal_data in search_results.get('deals', []):
            # Parse platform
            platform_data = deal_data.get('platform', {})
            platform = Platform(
                name=platform_data.get('name', 'Unknown'),
                type=platform_data.get('type', 'ecommerce'),
                url=platform_data.get('url', '')
            )

            # Parse discounts
            discounts = []
            for disc in deal_data.get('discounts', []):
                from models.schemas import Discount
                discounts.append(Discount(**disc))

            # Find best card for this deal
            calculator = DiscountCalculator()
            best_card, effective_price, savings = calculator.find_best_card_for_deal(
                base_price=deal_data.get('base_price', 0),
                delivery_charge=deal_data.get('delivery_charge', 0),
                discounts=discounts,
                available_cards=selected_cards
            )

            # Create deal object
            deal = ProductDeal(
                platform=platform,
                product_name=search_results.get('product_name', 'Unknown Product'),
                product_url=platform_data.get('url', ''),
                base_price=deal_data.get('base_price', 0),
                delivery_charge=deal_data.get('delivery_charge', 0),
                available_discounts=discounts,
                effective_price=effective_price,
                best_card=best_card,
                savings=savings,
                in_stock=deal_data.get('in_stock', True)
            )

            deals.append(deal)

        # Rank deals and mark best one
        ranked_deals = DiscountCalculator.rank_deals(deals)

        # Build response
        response = SearchResponse(
            product_name=search_results.get('product_name', 'Unknown Product'),
            product_image=search_results.get('product_image'),
            deals=ranked_deals
        )

        logger.info(f"Returning {len(ranked_deals)} deals")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search_deals: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cards", response_model=List[CreditCard])
async def get_supported_cards() -> List[CreditCard]:
    """Get list of supported credit cards"""
    return list(CREDIT_CARDS.values())

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "card-discount-agent"}
