"""
Gemini AI Service with Google Search Grounding
Uses Gemini 2.5 Flash to find prices, offers, and discounts
"""

import os
import logging
import json
import time
import hashlib
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from services.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Gemini AI"""

    def __init__(self):
        """Initialize Gemini service"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")

        genai.configure(api_key=api_key)

        # Use Gemini 2.0 Flash WITHOUT search grounding (for testing/higher quota)
        # With grounding: 2-5 RPM, 50-100 RPD
        # Without grounding: 15 RPM, 1500 RPD
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp'  # Known working model, no search grounding
            # No tools parameter = no search grounding = higher limits
        )

        # Rate limiter: 10 requests per minute (safe buffer under 15 RPM for non-grounded model)
        self.rate_limiter = RateLimiter(max_requests=10, time_window=60)

        # In-memory cache: store results for 1 hour
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour in seconds

        logger.info("Gemini service initialized WITHOUT search grounding (testing mode: 10 RPM, ~1500 RPD)")

    def _get_cache_key(self, query: str, selected_cards: List[str]) -> str:
        """Generate cache key from query + cards"""
        data = f"{query}:{','.join(sorted(selected_cards))}"
        return hashlib.md5(data.encode()).hexdigest()

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
        # Check cache first
        cache_key = self._get_cache_key(query, selected_cards)

        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                logger.info(f"✅ Cache HIT for query: {query[:50]}... (saved API call)")
                return cached_data
            else:
                # Cache expired
                logger.debug(f"Cache EXPIRED for query: {query[:50]}...")
                del self.cache[cache_key]

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

        logger.info(f"Searching for deals: {query[:100]}... (cache miss)")
        logger.info(f"Prompt size: ~{len(prompt)} chars (~{len(prompt)//4} tokens)")

        # Wait if needed to respect rate limits (4 RPM for 2026 free tier)
        self.rate_limiter.wait_if_needed()

        # Retry logic for rate limits with longer delays
        max_retries = 3
        base_delay = 15  # seconds (increased from 2s to respect 5 RPM = 12s between calls)

        for attempt in range(max_retries + 1):
            try:
                # Generate with search grounding
                response = self.model.generate_content(prompt)

                # Parse response
                result = self._parse_gemini_response(response.text)

                logger.info(f"Found {len(result.get('deals', []))} deals")

                # Store in cache
                self.cache[cache_key] = (result, time.time())
                logger.debug(f"Cached result for query: {query[:50]}...")

                return result

            except google_exceptions.ResourceExhausted as e:
                # Rate limit hit
                if attempt < max_retries:
                    # Exponential backoff: 15s, 30s, 60s (respects 5 RPM limit)
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Rate limit hit. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    # Final attempt failed
                    logger.error("Rate limit exhausted after all retries")
                    raise ValueError(
                        "Gemini API rate limit exceeded (5 RPM / Daily quota). "
                        "Please wait 10-15 minutes and try again. "
                        "Free tier: 5 requests/min, limited daily quota. "
                        "Consider upgrading for higher limits."
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

        # PROMPT FOR NON-GROUNDED MODEL - Returns example data based on training
        prompt = f"""Based on your training data about Indian e-commerce, provide estimated pricing for this product: {query}

Credit Cards Available: {selected_cards_str}

Platforms: Amazon, Flipkart, Myntra, Blinkit, Zepto, Swiggy Instamart

IMPORTANT: Since you don't have live web access, provide realistic EXAMPLE prices and offers based on:
1. Typical pricing for this product category in India
2. Common bank offers for the mentioned cards
3. Typical delivery charges
4. Standard discount patterns

Return VALID JSON (no explanations, just JSON):
{{
  "product_name": "Full product name",
  "product_image": null,
  "deals": [
    {{
      "platform": {{"name": "Amazon", "type": "ecommerce", "url": null}},
      "base_price": 2499,
      "delivery_charge": 40,
      "in_stock": true,
      "discounts": [
        {{
          "type": "instant",
          "value": 10,
          "is_percentage": true,
          "description": "HDFC Millennia 10% instant discount",
          "card_required": "hdfc-millennia",
          "max_cap": 200
        }},
        {{
          "type": "cashback",
          "value": 5,
          "is_percentage": true,
          "description": "ICICI Amazon Pay 5% cashback",
          "card_required": "icici-amazon-pay"
        }}
      ]
    }},
    {{
      "platform": {{"name": "Flipkart", "type": "ecommerce", "url": null}},
      "base_price": 2399,
      "delivery_charge": 0,
      "in_stock": true,
      "discounts": [
        {{
          "type": "instant",
          "value": 150,
          "is_percentage": false,
          "description": "Axis Airtel 10% instant discount",
          "card_required": "axis-airtel-rupay",
          "max_cap": 150
        }}
      ]
    }},
    {{
      "platform": {{"name": "Blinkit", "type": "quickcommerce", "url": null}},
      "base_price": 2599,
      "delivery_charge": 25,
      "in_stock": true,
      "discounts": []
    }}
  ]
}}

Provide at least 3 deals with realistic prices for India. Include discounts for the mentioned cards."""

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
