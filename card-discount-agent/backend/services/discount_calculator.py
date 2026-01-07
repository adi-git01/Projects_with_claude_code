"""
Discount calculation service
Calculates effective prices based on card benefits
"""

import logging
from typing import List, Tuple, Optional
from models.schemas import Discount, CreditCard, ProductDeal
from models.credit_cards import get_card_by_id

logger = logging.getLogger(__name__)

class DiscountCalculator:
    """Calculate effective prices with card-specific discounts"""

    @staticmethod
    def calculate_effective_price(
        base_price: float,
        delivery_charge: float,
        discounts: List[Discount],
        card: Optional[CreditCard] = None
    ) -> Tuple[float, float]:
        """
        Calculate effective price and savings

        Args:
            base_price: Original product price
            delivery_charge: Delivery fee
            discounts: List of applicable discounts
            card: Credit card being used (optional)

        Returns:
            Tuple of (effective_price, total_savings)
        """
        total_price = base_price + delivery_charge
        total_discount = 0

        # Priority order: instant > cashback > coupon > reward_points
        discount_priority = {
            'instant': 1,
            'cashback': 2,
            'coupon': 3,
            'reward_points': 4
        }

        # Sort discounts by priority
        sorted_discounts = sorted(
            discounts,
            key=lambda d: discount_priority.get(d.type, 99)
        )

        for discount in sorted_discounts:
            # Check if card requirement is met
            if discount.card_required and card:
                if discount.card_required != card.id:
                    continue

            # Check minimum purchase
            if discount.min_purchase and base_price < discount.min_purchase:
                continue

            # Calculate discount amount
            if discount.is_percentage:
                discount_amount = (base_price * discount.value) / 100
                # Apply max cap if exists
                if discount.max_cap:
                    discount_amount = min(discount_amount, discount.max_cap)
            else:
                discount_amount = discount.value

            total_discount += discount_amount

        effective_price = max(total_price - total_discount, 0)
        return effective_price, total_discount

    @staticmethod
    def find_best_card_for_deal(
        base_price: float,
        delivery_charge: float,
        discounts: List[Discount],
        available_cards: List[CreditCard]
    ) -> Tuple[Optional[CreditCard], float, float]:
        """
        Find the best card for a specific deal

        Returns:
            Tuple of (best_card, best_effective_price, best_savings)
        """
        best_card = None
        best_price = float('inf')
        best_savings = 0

        for card in available_cards:
            # Get card-specific discounts
            card_discounts = [
                d for d in discounts
                if not d.card_required or d.card_required == card.id
            ]

            # Add base card reward if no better discount exists
            has_instant_or_cashback = any(
                d.type in ['instant', 'cashback'] for d in card_discounts
            )

            if not has_instant_or_cashback and card.type == 'cashback':
                # Add base cashback
                card_discounts.append(Discount(
                    type='cashback',
                    value=card.base_reward,
                    is_percentage=True,
                    description=f'{card.bank} {card.name} base cashback',
                    card_required=card.id
                ))

            effective_price, savings = DiscountCalculator.calculate_effective_price(
                base_price,
                delivery_charge,
                card_discounts,
                card
            )

            if effective_price < best_price:
                best_price = effective_price
                best_savings = savings
                best_card = card

        return best_card, best_price, best_savings

    @staticmethod
    def rank_deals(deals: List[ProductDeal]) -> List[ProductDeal]:
        """
        Rank deals by effective price and mark the best deal

        Args:
            deals: List of product deals

        Returns:
            Sorted list with best_deal flag set
        """
        # Filter only in-stock deals for ranking
        in_stock_deals = [d for d in deals if d.in_stock]
        out_of_stock_deals = [d for d in deals if not d.in_stock]

        # Sort by effective price
        sorted_deals = sorted(in_stock_deals, key=lambda d: d.effective_price)

        # Mark the best deal
        if sorted_deals:
            sorted_deals[0].is_best_deal = True

        # Combine: in-stock (sorted) + out-of-stock
        return sorted_deals + out_of_stock_deals
