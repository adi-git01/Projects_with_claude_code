"""
Credit card definitions and configurations
"""

from typing import Dict, List
from .schemas import CreditCard

# Card definitions matching frontend
CREDIT_CARDS: Dict[str, CreditCard] = {
    'hdfc-regalia-gold': CreditCard(
        id='hdfc-regalia-gold',
        name='Regalia Gold',
        bank='HDFC',
        type='reward_points',
        base_reward=4.0,  # 4 points per 100
        color='#004C8F'
    ),
    'hdfc-millennia': CreditCard(
        id='hdfc-millennia',
        name='Millennia',
        bank='HDFC',
        type='cashback',
        base_reward=5.0,  # 5% cashback
        color='#ED232A'
    ),
    'icici-amazon-pay': CreditCard(
        id='icici-amazon-pay',
        name='Amazon Pay',
        bank='ICICI',
        type='cashback',
        base_reward=5.0,  # 5% unlimited
        color='#FF9900'
    ),
    'axis-airtel-rupay': CreditCard(
        id='axis-airtel-rupay',
        name='Airtel Rupay',
        bank='Axis',
        type='cashback',
        base_reward=10.0,  # 10% on Q-com
        color='#E60000'
    ),
}

def get_card_by_id(card_id: str) -> CreditCard:
    """Get card by ID"""
    return CREDIT_CARDS.get(card_id)

def get_cards_by_ids(card_ids: List[str]) -> List[CreditCard]:
    """Get multiple cards by IDs"""
    return [CREDIT_CARDS[cid] for cid in card_ids if cid in CREDIT_CARDS]
