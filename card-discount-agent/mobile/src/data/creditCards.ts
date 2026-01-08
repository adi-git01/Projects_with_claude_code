/**
 * Comprehensive database of Indian Credit Cards
 * Updated with all major banks and card offerings
 */

import type { CreditCard } from '../types';

export const INDIAN_CREDIT_CARDS: CreditCard[] = [
  // HDFC Bank
  {
    id: 'hdfc-infinia',
    name: 'Infinia',
    bank: 'HDFC',
    type: 'reward_points',
    baseReward: 3.3,
    color: '#004C8F',
    description: 'Premium rewards card with lounge access'
  },
  {
    id: 'hdfc-diners-black',
    name: 'Diners Club Black',
    bank: 'HDFC',
    type: 'reward_points',
    baseReward: 3.3,
    color: '#000000',
    description: 'Elite metal card with unlimited lounge access'
  },
  {
    id: 'hdfc-regalia-gold',
    name: 'Regalia Gold',
    bank: 'HDFC',
    type: 'reward_points',
    baseReward: 4,
    color: '#004C8F',
    description: 'Premium lifestyle rewards card'
  },
  {
    id: 'hdfc-regalia',
    name: 'Regalia',
    bank: 'HDFC',
    type: 'reward_points',
    baseReward: 4,
    color: '#004C8F',
    description: 'Premium rewards card'
  },
  {
    id: 'hdfc-millennia',
    name: 'Millennia',
    bank: 'HDFC',
    type: 'cashback',
    baseReward: 5,
    color: '#ED232A',
    description: '5% cashback on shopping & dining'
  },
  {
    id: 'hdfc-freedom',
    name: 'Freedom',
    bank: 'HDFC',
    type: 'cashback',
    baseReward: 1,
    color: '#004C8F',
    description: 'Cashback on fuel and utility bills'
  },
  {
    id: 'hdfc-swiggy',
    name: 'Swiggy',
    bank: 'HDFC',
    type: 'cashback',
    baseReward: 10,
    color: '#FC8019',
    description: '10% cashback on Swiggy'
  },
  {
    id: 'hdfc-tata-neu-infinity',
    name: 'Tata Neu Infinity',
    bank: 'HDFC',
    type: 'reward_points',
    baseReward: 5,
    color: '#8B00FF',
    description: '5% NeuCoins on Tata brands'
  },

  // ICICI Bank
  {
    id: 'icici-sapphiro',
    name: 'Sapphiro',
    bank: 'ICICI',
    type: 'reward_points',
    baseReward: 2,
    color: '#0066CC',
    description: 'Premium rewards with airport lounge access'
  },
  {
    id: 'icici-amazon-pay',
    name: 'Amazon Pay',
    bank: 'ICICI',
    type: 'cashback',
    baseReward: 5,
    color: '#FF9900',
    description: '5% unlimited cashback on Amazon'
  },
  {
    id: 'icici-coral',
    name: 'Coral',
    bank: 'ICICI',
    type: 'cashback',
    baseReward: 2,
    color: '#FF6B6B',
    description: '2% cashback on dining and utility bills'
  },
  {
    id: 'icici-rubyx',
    name: 'Rubyx',
    bank: 'ICICI',
    type: 'cashback',
    baseReward: 2,
    color: '#E74C3C',
    description: 'Cashback on fuel and movies'
  },
  {
    id: 'icici-platinum',
    name: 'Platinum',
    bank: 'ICICI',
    type: 'reward_points',
    baseReward: 1,
    color: '#C0C0C0',
    description: 'Entry-level rewards card'
  },
  {
    id: 'icici-mmt-signature',
    name: 'MMT Signature',
    bank: 'ICICI',
    type: 'reward_points',
    baseReward: 4,
    color: '#E74C3C',
    description: '4% value back on MakeMyTrip bookings'
  },

  // Axis Bank
  {
    id: 'axis-magnus',
    name: 'Magnus',
    bank: 'Axis',
    type: 'reward_points',
    baseReward: 12,
    color: '#800080',
    description: 'Super premium with 12 EdgeRewards per ₹200'
  },
  {
    id: 'axis-reserve',
    name: 'Reserve',
    bank: 'Axis',
    type: 'reward_points',
    baseReward: 3,
    color: '#000000',
    description: 'Metal card with premium benefits'
  },
  {
    id: 'axis-vistara-infinite',
    name: 'Vistara Infinite',
    bank: 'Axis',
    type: 'reward_points',
    baseReward: 4,
    color: '#6B1B7F',
    description: 'Premium travel card with CV points'
  },
  {
    id: 'axis-ace',
    name: 'Ace',
    bank: 'Axis',
    type: 'cashback',
    baseReward: 5,
    color: '#FF4B4B',
    description: '5% cashback on bill payments'
  },
  {
    id: 'axis-flipkart',
    name: 'Flipkart',
    bank: 'Axis',
    type: 'cashback',
    baseReward: 5,
    color: '#2874F0',
    description: '5% unlimited cashback on Flipkart'
  },
  {
    id: 'axis-airtel-rupay',
    name: 'Airtel Rupay',
    bank: 'Axis',
    type: 'cashback',
    baseReward: 10,
    color: '#E60000',
    description: '10% cashback on Swiggy, BigBasket, Blinkit'
  },
  {
    id: 'axis-myntra',
    name: 'Myntra',
    bank: 'Axis',
    type: 'cashback',
    baseReward: 7,
    color: '#FF3F6C',
    description: '7% cashback on Myntra'
  },

  // SBI Cards
  {
    id: 'sbi-elite',
    name: 'Elite',
    bank: 'SBI',
    type: 'reward_points',
    baseReward: 5,
    color: '#1C3F7C',
    description: '5 reward points per ₹100'
  },
  {
    id: 'sbi-cashback',
    name: 'Cashback',
    bank: 'SBI',
    type: 'cashback',
    baseReward: 5,
    color: '#1C3F7C',
    description: '5% cashback on online spends'
  },
  {
    id: 'sbi-simplysave',
    name: 'SimplySave',
    bank: 'SBI',
    type: 'cashback',
    baseReward: 5,
    color: '#1C3F7C',
    description: '5% cashback on dining, groceries, movies'
  },
  {
    id: 'sbi-prime',
    name: 'Prime',
    bank: 'SBI',
    type: 'reward_points',
    baseReward: 1,
    color: '#1C3F7C',
    description: 'Reward points on all spends'
  },
  {
    id: 'sbi-aurum',
    name: 'Aurum',
    bank: 'SBI',
    type: 'reward_points',
    baseReward: 2,
    color: '#FFD700',
    description: 'Premium card with lounge access'
  },

  // Standard Chartered
  {
    id: 'sc-ultimate',
    name: 'Ultimate',
    bank: 'Standard Chartered',
    type: 'cashback',
    baseReward: 3.3,
    color: '#0077BE',
    description: '3.3% cashback on all spends'
  },
  {
    id: 'sc-smart',
    name: 'Smart',
    bank: 'Standard Chartered',
    type: 'cashback',
    baseReward: 5,
    color: '#0077BE',
    description: '5% cashback on preferred categories'
  },
  {
    id: 'sc-titanium',
    name: 'Titanium',
    bank: 'Standard Chartered',
    type: 'reward_points',
    baseReward: 1,
    color: '#C0C0C0',
    description: 'Rewards on dining and shopping'
  },

  // American Express
  {
    id: 'amex-platinum',
    name: 'Platinum Card',
    bank: 'American Express',
    type: 'reward_points',
    baseReward: 1.5,
    color: '#006FCF',
    description: 'Premium travel and lifestyle card'
  },
  {
    id: 'amex-gold',
    name: 'Gold Card',
    bank: 'American Express',
    type: 'reward_points',
    baseReward: 1,
    color: '#CDA349',
    description: '1000 points per ₹50 spent'
  },
  {
    id: 'amex-mrcc',
    name: 'Membership Rewards',
    bank: 'American Express',
    type: 'reward_points',
    baseReward: 1,
    color: '#006FCF',
    description: 'Earn Membership Rewards points'
  },
  {
    id: 'amex-platinum-travel',
    name: 'Platinum Travel',
    bank: 'American Express',
    type: 'reward_points',
    baseReward: 5,
    color: '#006FCF',
    description: '5x points on travel bookings'
  },

  // IndusInd Bank
  {
    id: 'indusind-legend',
    name: 'Legend',
    bank: 'IndusInd',
    type: 'reward_points',
    baseReward: 3,
    color: '#ED1C24',
    description: 'Premium card with accelerated rewards'
  },
  {
    id: 'indusind-pioneer-heritage',
    name: 'Pioneer Heritage',
    bank: 'IndusInd',
    type: 'reward_points',
    baseReward: 2,
    color: '#ED1C24',
    description: 'Metal card with lounge access'
  },
  {
    id: 'indusind-iconia',
    name: 'Iconia',
    bank: 'IndusInd',
    type: 'cashback',
    baseReward: 3,
    color: '#ED1C24',
    description: 'Cashback on online shopping'
  },

  // Yes Bank
  {
    id: 'yes-reserv',
    name: 'Reserv',
    bank: 'Yes Bank',
    type: 'reward_points',
    baseReward: 3,
    color: '#003D7A',
    description: 'Metal card with premium rewards'
  },
  {
    id: 'yes-prosperity-edge',
    name: 'Prosperity Edge',
    bank: 'Yes Bank',
    type: 'cashback',
    baseReward: 2,
    color: '#003D7A',
    description: 'Cashback on all spends'
  },

  // AU Bank
  {
    id: 'au-zenith',
    name: 'Zenith',
    bank: 'AU Bank',
    type: 'cashback',
    baseReward: 10,
    color: '#FF6B00',
    description: '10% cashback on utilities'
  },
  {
    id: 'au-lit',
    name: 'LIT',
    bank: 'AU Bank',
    type: 'cashback',
    baseReward: 5,
    color: '#FF6B00',
    description: '5% cashback on online spends'
  },

  // HSBC
  {
    id: 'hsbc-live-plus',
    name: 'Live Plus',
    bank: 'HSBC',
    type: 'cashback',
    baseReward: 10,
    color: '#DB0011',
    description: '10% cashback on dining & groceries'
  },
  {
    id: 'hsbc-premier',
    name: 'Premier',
    bank: 'HSBC',
    type: 'reward_points',
    baseReward: 2,
    color: '#DB0011',
    description: 'Premium rewards card'
  },

  // Kotak Mahindra
  {
    id: 'kotak-811',
    name: '811 Credit Card',
    bank: 'Kotak',
    type: 'cashback',
    baseReward: 5,
    color: '#ED232A',
    description: '5% cashback on top 2 categories'
  },
  {
    id: 'kotak-whitereserve',
    name: 'White Reserve',
    bank: 'Kotak',
    type: 'reward_points',
    baseReward: 4,
    color: '#FFFFFF',
    description: 'Premium metal card'
  },

  // RBL Bank
  {
    id: 'rbl-shoprite',
    name: 'ShopRite',
    bank: 'RBL',
    type: 'cashback',
    baseReward: 5,
    color: '#0066CC',
    description: '5% cashback on groceries'
  },
  {
    id: 'rbl-popcorn',
    name: 'Popcorn',
    bank: 'RBL',
    type: 'cashback',
    baseReward: 10,
    color: '#FF0000',
    description: '10% cashback on BookMyShow'
  },

  // IDFC First
  {
    id: 'idfc-first-select',
    name: 'Select',
    bank: 'IDFC First',
    type: 'cashback',
    baseReward: 10,
    color: '#ED1C24',
    description: '10x rewards on top 3 spends'
  },
  {
    id: 'idfc-first-wealth',
    name: 'Wealth',
    bank: 'IDFC First',
    type: 'reward_points',
    baseReward: 3,
    color: '#ED1C24',
    description: 'Premium rewards card'
  },
];

// Helper function to search cards
export function searchCards(query: string): CreditCard[] {
  const lowerQuery = query.toLowerCase().trim();

  if (!lowerQuery) {
    return INDIAN_CREDIT_CARDS;
  }

  return INDIAN_CREDIT_CARDS.filter(card => {
    const searchText = `${card.bank} ${card.name} ${card.description}`.toLowerCase();
    return searchText.includes(lowerQuery);
  });
}

// Get cards by bank
export function getCardsByBank(bank: string): CreditCard[] {
  return INDIAN_CREDIT_CARDS.filter(card =>
    card.bank.toLowerCase() === bank.toLowerCase()
  );
}

// Get popular cards (top picks)
export function getPopularCards(): CreditCard[] {
  const popularIds = [
    'hdfc-millennia',
    'icici-amazon-pay',
    'axis-airtel-rupay',
    'axis-flipkart',
    'sbi-cashback',
    'hdfc-swiggy',
    'axis-magnus',
    'hdfc-infinia'
  ];

  return INDIAN_CREDIT_CARDS.filter(card => popularIds.includes(card.id));
}
