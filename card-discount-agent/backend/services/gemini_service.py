"""
Gemini AI Service with Google Search Grounding
Uses Gemini 2.5 Flash to find prices, offers, and discounts
"""

import os
import logging
import json
import time
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Gemini AI"""

    def __init__(self):
        """Initialize Gemini service"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")

        genai.configure(api_key=api_key)

        # Use Gemini 2.5 Flash Preview with search grounding
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            tools='google_search_retrieval'
        )

        logger.info("Gemini service initialized with search grounding")

    async def search_product_deals(
        self,
        query: str,
        selected_cards: List[str],
        platforms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search for product deals using Gemini with Google Search

        Args:
            query: Product URL or name
            selected_cards: List of card IDs to consider
            platforms: List of platforms to search (default: all)

        Returns:
            Dict with product info and deals
        """
        # Default platforms if not specified - Expanded list
        if not platforms:
            platforms = [
                # Major E-commerce
                'amazon.in', 'flipkart.com', 'myntra.com', 'ajio.com', 'meesho.com',
                'nykaa.com', 'tatacliq.com', 'snapdeal.com', 'jiomart.com',
                # Electronics
                'croma.com', 'reliancedigital.in', 'vijaysales.com',
                # Groceries & Essentials
                'bigbasket.com', 'pharmeasy.in', 'netmeds.com',
                # Quick-commerce
                'blinkit.com', 'zepto.com', 'swiggy.com/instamart',
                'bigbasket.com/bbnow', 'dunzo.com', 'amazon.in/fresh'
            ]

        # Build comprehensive prompt for Gemini
        prompt = self._build_search_prompt(query, selected_cards, platforms)

        logger.info(f"Searching for deals: {query[:100]}...")

        # Retry logic for rate limits
        max_retries = 3
        base_delay = 2  # seconds

        for attempt in range(max_retries + 1):
            try:
                # Generate with search grounding
                response = self.model.generate_content(prompt)

                # Parse response
                result = self._parse_gemini_response(response.text)

                logger.info(f"Found {len(result.get('deals', []))} deals")
                return result

            except google_exceptions.ResourceExhausted as e:
                # Rate limit hit
                if attempt < max_retries:
                    # Exponential backoff: 2s, 4s, 8s
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Rate limit hit. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    # Final attempt failed
                    logger.error("Rate limit exhausted after all retries")
                    raise ValueError(
                        "Gemini API rate limit exceeded. Please try again in a few minutes. "
                        "The free tier has limits on requests per minute and per day."
                    ) from e

            except Exception as e:
                logger.error(f"Error in search_product_deals: {e}")
                raise

    def _build_search_prompt(
        self,
        query: str,
        selected_cards: List[str],
        platforms: List[str]
    ) -> str:
        """Build comprehensive search prompt for Gemini"""

        # Import card database
        from models.all_credit_cards import get_card_by_id

        # Build card info strings
        cards_info_list = []
        for card_id in selected_cards:
            card = get_card_by_id(card_id)
            if card:
                reward_text = f"{card.base_reward}%" if card.type == 'cashback' else f"{card.base_reward} pts/₹100"
                cards_info_list.append(f"{card.bank} {card.name} ({reward_text})")
            else:
                cards_info_list.append(card_id)

        selected_cards_str = ', '.join(cards_info_list)

        prompt = f"""You are a shopping deal intelligence agent. Search the web for the best prices and offers for this product.

PRODUCT QUERY: {query}

AVAILABLE CREDIT CARDS: {selected_cards_str}

PLATFORMS TO SEARCH:
E-Commerce: Amazon India, Flipkart, Myntra, AJIO, Meesho, Nykaa, Tata CLiQ, Snapdeal, JioMart, Croma, Reliance Digital, BigBasket
Quick-Commerce: Blinkit, Zepto, Swiggy Instamart, BB Now, Dunzo Daily, Amazon Fresh, Flipkart Quick, JioMart Express

YOUR TASK:
1. Identify the exact product name and specifications
2. Search for current prices on each platform
3. Find ALL active bank offers and discounts (especially for the cards mentioned)
4. Find available coupon codes (like WELCOME100, BRAND20, etc.)
5. Check delivery charges
6. Verify stock availability

IMPORTANT - CARD DISCOUNT PRIORITY:
1. Instant Discounts (best - immediate price reduction)
2. High % Cashback (10% on Axis Airtel for quick-commerce)
3. Flat Cashback (5% on ICICI Amazon Pay, HDFC Millennia)
4. Reward Points (last resort - HDFC Regalia Gold)

For each platform, provide:
- Platform name and type (ecommerce/quickcommerce)
- Product URL
- Base price (in ₹)
- Delivery charge
- ALL applicable discounts with these details:
  * Type: instant/cashback/coupon/reward_points
  * Value: amount or percentage
  * Description (e.g., "HDFC Millennia 5% instant discount")
  * Card required (if any)
  * Validity date (if mentioned)
- Stock status

OUTPUT FORMAT (JSON):
{{
    "product_name": "Exact product name",
    "product_image": "Image URL if found",
    "deals": [
        {{
            "platform": {{"name": "Amazon", "type": "ecommerce", "url": "product_url"}},
            "base_price": 1299,
            "delivery_charge": 40,
            "in_stock": true,
            "discounts": [
                {{
                    "type": "instant",
                    "value": 10,
                    "is_percentage": true,
                    "description": "HDFC Millennia 10% instant discount",
                    "card_required": "hdfc-millennia",
                    "max_cap": 150
                }},
                {{
                    "type": "coupon",
                    "value": 100,
                    "is_percentage": false,
                    "description": "WELCOME100 coupon",
                    "min_purchase": 999
                }}
            ]
        }}
    ]
}}

Search the web NOW and provide accurate, current information. Be thorough!"""

        return prompt

    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured data"""
        try:
            # Try to extract JSON from response
            # Gemini might wrap JSON in markdown code blocks
            response_text = response_text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            elif response_text.startswith('```'):
                response_text = response_text[3:]

            if response_text.endswith('```'):
                response_text = response_text[:-3]

            response_text = response_text.strip()

            # Parse JSON
            data = json.loads(response_text)

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.debug(f"Response text: {response_text[:500]}")

            # Fallback: return empty structure
            return {
                "product_name": "Unknown Product",
                "deals": []
            }

    async def extract_product_info(self, url: str) -> Dict[str, str]:
        """Extract product information from URL"""
        try:
            prompt = f"""Extract product information from this URL: {url}

Return JSON with:
- product_name: The exact product name
- platform: The platform (amazon/flipkart/myntra/etc)
- category: Product category

Just return the JSON, nothing else."""

            response = self.model.generate_content(prompt)
            return self._parse_gemini_response(response.text)

        except Exception as e:
            logger.error(f"Error extracting product info: {e}")
            return {"product_name": url, "platform": "unknown"}
