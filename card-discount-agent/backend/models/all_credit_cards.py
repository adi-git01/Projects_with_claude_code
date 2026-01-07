"""
Comprehensive database of Indian Credit Cards
Matches the frontend card database
"""

from typing import Dict, List
from .schemas import CreditCard

# Complete list of Indian credit cards
ALL_INDIAN_CARDS: Dict[str, CreditCard] = {
    # HDFC Bank
    'hdfc-infinia': CreditCard(
        id='hdfc-infinia', name='Infinia', bank='HDFC',
        type='reward_points', base_reward=3.3, color='#004C8F'
    ),
    'hdfc-diners-black': CreditCard(
        id='hdfc-diners-black', name='Diners Club Black', bank='HDFC',
        type='reward_points', base_reward=3.3, color='#000000'
    ),
    'hdfc-regalia-gold': CreditCard(
        id='hdfc-regalia-gold', name='Regalia Gold', bank='HDFC',
        type='reward_points', base_reward=4.0, color='#004C8F'
    ),
    'hdfc-regalia': CreditCard(
        id='hdfc-regalia', name='Regalia', bank='HDFC',
        type='reward_points', base_reward=4.0, color='#004C8F'
    ),
    'hdfc-millennia': CreditCard(
        id='hdfc-millennia', name='Millennia', bank='HDFC',
        type='cashback', base_reward=5.0, color='#ED232A'
    ),
    'hdfc-freedom': CreditCard(
        id='hdfc-freedom', name='Freedom', bank='HDFC',
        type='cashback', base_reward=1.0, color='#004C8F'
    ),
    'hdfc-swiggy': CreditCard(
        id='hdfc-swiggy', name='Swiggy', bank='HDFC',
        type='cashback', base_reward=10.0, color='#FC8019'
    ),
    'hdfc-tata-neu-infinity': CreditCard(
        id='hdfc-tata-neu-infinity', name='Tata Neu Infinity', bank='HDFC',
        type='reward_points', base_reward=5.0, color='#8B00FF'
    ),

    # ICICI Bank
    'icici-sapphiro': CreditCard(
        id='icici-sapphiro', name='Sapphiro', bank='ICICI',
        type='reward_points', base_reward=2.0, color='#0066CC'
    ),
    'icici-amazon-pay': CreditCard(
        id='icici-amazon-pay', name='Amazon Pay', bank='ICICI',
        type='cashback', base_reward=5.0, color='#FF9900'
    ),
    'icici-coral': CreditCard(
        id='icici-coral', name='Coral', bank='ICICI',
        type='cashback', base_reward=2.0, color='#FF6B6B'
    ),
    'icici-rubyx': CreditCard(
        id='icici-rubyx', name='Rubyx', bank='ICICI',
        type='cashback', base_reward=2.0, color='#E74C3C'
    ),
    'icici-platinum': CreditCard(
        id='icici-platinum', name='Platinum', bank='ICICI',
        type='reward_points', base_reward=1.0, color='#C0C0C0'
    ),
    'icici-mmt-signature': CreditCard(
        id='icici-mmt-signature', name='MMT Signature', bank='ICICI',
        type='reward_points', base_reward=4.0, color='#E74C3C'
    ),

    # Axis Bank
    'axis-magnus': CreditCard(
        id='axis-magnus', name='Magnus', bank='Axis',
        type='reward_points', base_reward=12.0, color='#800080'
    ),
    'axis-reserve': CreditCard(
        id='axis-reserve', name='Reserve', bank='Axis',
        type='reward_points', base_reward=3.0, color='#000000'
    ),
    'axis-vistara-infinite': CreditCard(
        id='axis-vistara-infinite', name='Vistara Infinite', bank='Axis',
        type='reward_points', base_reward=4.0, color='#6B1B7F'
    ),
    'axis-ace': CreditCard(
        id='axis-ace', name='Ace', bank='Axis',
        type='cashback', base_reward=5.0, color='#FF4B4B'
    ),
    'axis-flipkart': CreditCard(
        id='axis-flipkart', name='Flipkart', bank='Axis',
        type='cashback', base_reward=5.0, color='#2874F0'
    ),
    'axis-airtel-rupay': CreditCard(
        id='axis-airtel-rupay', name='Airtel Rupay', bank='Axis',
        type='cashback', base_reward=10.0, color='#E60000'
    ),
    'axis-myntra': CreditCard(
        id='axis-myntra', name='Myntra', bank='Axis',
        type='cashback', base_reward=7.0, color='#FF3F6C'
    ),

    # SBI Cards
    'sbi-elite': CreditCard(
        id='sbi-elite', name='Elite', bank='SBI',
        type='reward_points', base_reward=5.0, color='#1C3F7C'
    ),
    'sbi-cashback': CreditCard(
        id='sbi-cashback', name='Cashback', bank='SBI',
        type='cashback', base_reward=5.0, color='#1C3F7C'
    ),
    'sbi-simplysave': CreditCard(
        id='sbi-simplysave', name='SimplySave', bank='SBI',
        type='cashback', base_reward=5.0, color='#1C3F7C'
    ),
    'sbi-prime': CreditCard(
        id='sbi-prime', name='Prime', bank='SBI',
        type='reward_points', base_reward=1.0, color='#1C3F7C'
    ),
    'sbi-aurum': CreditCard(
        id='sbi-aurum', name='Aurum', bank='SBI',
        type='reward_points', base_reward=2.0, color='#FFD700'
    ),

    # Standard Chartered
    'sc-ultimate': CreditCard(
        id='sc-ultimate', name='Ultimate', bank='Standard Chartered',
        type='cashback', base_reward=3.3, color='#0077BE'
    ),
    'sc-smart': CreditCard(
        id='sc-smart', name='Smart', bank='Standard Chartered',
        type='cashback', base_reward=5.0, color='#0077BE'
    ),
    'sc-titanium': CreditCard(
        id='sc-titanium', name='Titanium', bank='Standard Chartered',
        type='reward_points', base_reward=1.0, color='#C0C0C0'
    ),

    # American Express
    'amex-platinum': CreditCard(
        id='amex-platinum', name='Platinum Card', bank='American Express',
        type='reward_points', base_reward=1.5, color='#006FCF'
    ),
    'amex-gold': CreditCard(
        id='amex-gold', name='Gold Card', bank='American Express',
        type='reward_points', base_reward=1.0, color='#CDA349'
    ),
    'amex-mrcc': CreditCard(
        id='amex-mrcc', name='Membership Rewards', bank='American Express',
        type='reward_points', base_reward=1.0, color='#006FCF'
    ),
    'amex-platinum-travel': CreditCard(
        id='amex-platinum-travel', name='Platinum Travel', bank='American Express',
        type='reward_points', base_reward=5.0, color='#006FCF'
    ),

    # IndusInd Bank
    'indusind-legend': CreditCard(
        id='indusind-legend', name='Legend', bank='IndusInd',
        type='reward_points', base_reward=3.0, color='#ED1C24'
    ),
    'indusind-pioneer-heritage': CreditCard(
        id='indusind-pioneer-heritage', name='Pioneer Heritage', bank='IndusInd',
        type='reward_points', base_reward=2.0, color='#ED1C24'
    ),
    'indusind-iconia': CreditCard(
        id='indusind-iconia', name='Iconia', bank='IndusInd',
        type='cashback', base_reward=3.0, color='#ED1C24'
    ),

    # Yes Bank
    'yes-reserv': CreditCard(
        id='yes-reserv', name='Reserv', bank='Yes Bank',
        type='reward_points', base_reward=3.0, color='#003D7A'
    ),
    'yes-prosperity-edge': CreditCard(
        id='yes-prosperity-edge', name='Prosperity Edge', bank='Yes Bank',
        type='cashback', base_reward=2.0, color='#003D7A'
    ),

    # AU Bank
    'au-zenith': CreditCard(
        id='au-zenith', name='Zenith', bank='AU Bank',
        type='cashback', base_reward=10.0, color='#FF6B00'
    ),
    'au-lit': CreditCard(
        id='au-lit', name='LIT', bank='AU Bank',
        type='cashback', base_reward=5.0, color='#FF6B00'
    ),

    # HSBC
    'hsbc-live-plus': CreditCard(
        id='hsbc-live-plus', name='Live Plus', bank='HSBC',
        type='cashback', base_reward=10.0, color='#DB0011'
    ),
    'hsbc-premier': CreditCard(
        id='hsbc-premier', name='Premier', bank='HSBC',
        type='reward_points', base_reward=2.0, color='#DB0011'
    ),

    # Kotak Mahindra
    'kotak-811': CreditCard(
        id='kotak-811', name='811 Credit Card', bank='Kotak',
        type='cashback', base_reward=5.0, color='#ED232A'
    ),
    'kotak-whitereserve': CreditCard(
        id='kotak-whitereserve', name='White Reserve', bank='Kotak',
        type='reward_points', base_reward=4.0, color='#FFFFFF'
    ),

    # RBL Bank
    'rbl-shoprite': CreditCard(
        id='rbl-shoprite', name='ShopRite', bank='RBL',
        type='cashback', base_reward=5.0, color='#0066CC'
    ),
    'rbl-popcorn': CreditCard(
        id='rbl-popcorn', name='Popcorn', bank='RBL',
        type='cashback', base_reward=10.0, color='#FF0000'
    ),

    # IDFC First
    'idfc-first-select': CreditCard(
        id='idfc-first-select', name='Select', bank='IDFC First',
        type='cashback', base_reward=10.0, color='#ED1C24'
    ),
    'idfc-first-wealth': CreditCard(
        id='idfc-first-wealth', name='Wealth', bank='IDFC First',
        type='reward_points', base_reward=3.0, color='#ED1C24'
    ),
}

def get_card_by_id(card_id: str) -> CreditCard:
    """Get card by ID, fallback to legacy cards for compatibility"""
    from .credit_cards import CREDIT_CARDS

    # Try new comprehensive database first
    if card_id in ALL_INDIAN_CARDS:
        return ALL_INDIAN_CARDS[card_id]

    # Fallback to legacy
    return CREDIT_CARDS.get(card_id)

def get_cards_by_ids(card_ids: List[str]) -> List[CreditCard]:
    """Get multiple cards by IDs"""
    cards = []
    for card_id in card_ids:
        card = get_card_by_id(card_id)
        if card:
            cards.append(card)
    return cards
