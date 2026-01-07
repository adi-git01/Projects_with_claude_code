export interface CreditCard {
  id: string;
  name: string;
  bank: string;
  type: 'reward_points' | 'cashback' | 'instant_discount';
  baseReward: number; // percentage or points per 100
  color: string;
  logo?: string;
}

export interface Platform {
  name: string;
  type: 'ecommerce' | 'quickcommerce';
  url: string;
}

export interface Discount {
  type: 'instant' | 'cashback' | 'coupon' | 'reward_points';
  value: number;
  isPercentage: boolean;
  maxCap?: number;
  minPurchase?: number;
  description: string;
  cardRequired?: string;
  validUntil?: string;
}

export interface ProductDeal {
  platform: Platform;
  productName: string;
  productUrl: string;
  basePrice: number;
  deliveryCharge: number;
  availableDiscounts: Discount[];
  effectivePrice: number;
  bestCard?: CreditCard;
  savings: number;
  isBestDeal: boolean;
  inStock: boolean;
}

export interface SearchProgress {
  step: string;
  status: 'pending' | 'in_progress' | 'completed' | 'error';
  message: string;
}

export interface SearchRequest {
  query: string; // URL or product name
  selectedCards: string[]; // card IDs
}

export interface SearchResponse {
  productName: string;
  productImage?: string;
  deals: ProductDeal[];
  searchTimestamp: string;
  progress: SearchProgress[];
}

export const CREDIT_CARDS: CreditCard[] = [
  {
    id: 'hdfc-regalia-gold',
    name: 'Regalia Gold',
    bank: 'HDFC',
    type: 'reward_points',
    baseReward: 4, // 4 points per 100
    color: '#004C8F'
  },
  {
    id: 'hdfc-millennia',
    name: 'Millennia',
    bank: 'HDFC',
    type: 'cashback',
    baseReward: 5, // 5% cashback
    color: '#ED232A'
  },
  {
    id: 'icici-amazon-pay',
    name: 'Amazon Pay',
    bank: 'ICICI',
    type: 'cashback',
    baseReward: 5, // 5% unlimited
    color: '#FF9900'
  },
  {
    id: 'axis-airtel-rupay',
    name: 'Airtel Rupay',
    bank: 'Axis',
    type: 'cashback',
    baseReward: 10, // 10% on Q-com
    color: '#E60000'
  }
];
