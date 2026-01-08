export interface CreditCard {
  id: string;
  name: string;
  bank: string;
  type: 'reward_points' | 'cashback' | 'instant_discount';
  baseReward: number;
  color: string;
  description?: string;
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
  query: string;
  selectedCards: string[];
}

export interface SearchResponse {
  productName: string;
  productImage?: string;
  deals: ProductDeal[];
  searchTimestamp: string;
  progress: SearchProgress[];
}
