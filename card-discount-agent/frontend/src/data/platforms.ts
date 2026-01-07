/**
 * Comprehensive database of E-commerce and Quick-commerce platforms in India
 */

export interface PlatformInfo {
  id: string;
  name: string;
  type: 'ecommerce' | 'quickcommerce';
  domain: string;
  categories: string[];
  description: string;
}

export const ECOMMERCE_PLATFORMS: PlatformInfo[] = [
  // Major E-commerce
  {
    id: 'amazon',
    name: 'Amazon India',
    type: 'ecommerce',
    domain: 'amazon.in',
    categories: ['electronics', 'fashion', 'home', 'books', 'groceries'],
    description: 'Largest online marketplace in India'
  },
  {
    id: 'flipkart',
    name: 'Flipkart',
    type: 'ecommerce',
    domain: 'flipkart.com',
    categories: ['electronics', 'fashion', 'home', 'mobiles'],
    description: 'Leading Indian e-commerce platform'
  },
  {
    id: 'myntra',
    name: 'Myntra',
    type: 'ecommerce',
    domain: 'myntra.com',
    categories: ['fashion', 'beauty', 'accessories'],
    description: 'Fashion and lifestyle shopping'
  },
  {
    id: 'ajio',
    name: 'AJIO',
    type: 'ecommerce',
    domain: 'ajio.com',
    categories: ['fashion', 'accessories'],
    description: 'Reliance fashion e-commerce'
  },
  {
    id: 'meesho',
    name: 'Meesho',
    type: 'ecommerce',
    domain: 'meesho.com',
    categories: ['fashion', 'home', 'beauty'],
    description: 'Social commerce platform'
  },

  // Specialized E-commerce
  {
    id: 'nykaa',
    name: 'Nykaa',
    type: 'ecommerce',
    domain: 'nykaa.com',
    categories: ['beauty', 'fashion', 'wellness'],
    description: 'Beauty and wellness specialist'
  },
  {
    id: 'tatacliq',
    name: 'Tata CLiQ',
    type: 'ecommerce',
    domain: 'tatacliq.com',
    categories: ['electronics', 'fashion', 'home'],
    description: 'Tata group e-commerce'
  },
  {
    id: 'snapdeal',
    name: 'Snapdeal',
    type: 'ecommerce',
    domain: 'snapdeal.com',
    categories: ['electronics', 'fashion', 'home'],
    description: 'Value-focused marketplace'
  },
  {
    id: 'shopclues',
    name: 'ShopClues',
    type: 'ecommerce',
    domain: 'shopclues.com',
    categories: ['electronics', 'fashion', 'home'],
    description: 'Unstructured marketplace'
  },
  {
    id: 'paytmmall',
    name: 'Paytm Mall',
    type: 'ecommerce',
    domain: 'paytmmall.com',
    categories: ['electronics', 'fashion', 'groceries'],
    description: 'Paytm e-commerce platform'
  },

  // Electronics
  {
    id: 'croma',
    name: 'Croma',
    type: 'ecommerce',
    domain: 'croma.com',
    categories: ['electronics', 'appliances'],
    description: 'Tata electronics retail'
  },
  {
    id: 'reliancedigital',
    name: 'Reliance Digital',
    type: 'ecommerce',
    domain: 'reliancedigital.in',
    categories: ['electronics', 'appliances'],
    description: 'Electronics and appliances'
  },
  {
    id: 'vijaysales',
    name: 'Vijay Sales',
    type: 'ecommerce',
    domain: 'vijaysales.com',
    categories: ['electronics', 'appliances'],
    description: 'Consumer electronics retailer'
  },

  // Fashion
  {
    id: 'zara',
    name: 'Zara India',
    type: 'ecommerce',
    domain: 'zara.com/in',
    categories: ['fashion'],
    description: 'International fashion brand'
  },
  {
    id: 'hm',
    name: 'H&M India',
    type: 'ecommerce',
    domain: 'hm.com/in',
    categories: ['fashion'],
    description: 'Swedish fashion retailer'
  },
  {
    id: 'firstcry',
    name: 'FirstCry',
    type: 'ecommerce',
    domain: 'firstcry.com',
    categories: ['kids', 'toys', 'baby'],
    description: 'Kids and baby products'
  },

  // Books & Media
  {
    id: 'bookswagon',
    name: 'Bookswagon',
    type: 'ecommerce',
    domain: 'bookswagon.com',
    categories: ['books'],
    description: 'Online bookstore'
  },

  // Home & Furniture
  {
    id: 'pepperfry',
    name: 'Pepperfry',
    type: 'ecommerce',
    domain: 'pepperfry.com',
    categories: ['furniture', 'home'],
    description: 'Furniture and home decor'
  },
  {
    id: 'urbanladder',
    name: 'Urban Ladder',
    type: 'ecommerce',
    domain: 'urbanladder.com',
    categories: ['furniture', 'home'],
    description: 'Premium furniture retailer'
  },

  // Health & Pharmacy
  {
    id: 'netmeds',
    name: 'Netmeds',
    type: 'ecommerce',
    domain: 'netmeds.com',
    categories: ['pharmacy', 'health'],
    description: 'Online pharmacy'
  },
  {
    id: 'pharmeasy',
    name: 'PharmEasy',
    type: 'ecommerce',
    domain: 'pharmeasy.in',
    categories: ['pharmacy', 'health'],
    description: 'Healthcare and medicines'
  },
  {
    id: 'apollo247',
    name: 'Apollo 24/7',
    type: 'ecommerce',
    domain: 'apollo247.com',
    categories: ['pharmacy', 'health'],
    description: 'Apollo online pharmacy'
  },

  // Groceries
  {
    id: 'bigbasket',
    name: 'BigBasket',
    type: 'ecommerce',
    domain: 'bigbasket.com',
    categories: ['groceries', 'food'],
    description: 'Online grocery store'
  },
  {
    id: 'jiomart',
    name: 'JioMart',
    type: 'ecommerce',
    domain: 'jiomart.com',
    categories: ['groceries', 'electronics', 'fashion'],
    description: 'Reliance retail platform'
  },
];

export const QUICKCOMMERCE_PLATFORMS: PlatformInfo[] = [
  {
    id: 'blinkit',
    name: 'Blinkit',
    type: 'quickcommerce',
    domain: 'blinkit.com',
    categories: ['groceries', 'food', 'essentials'],
    description: '10-minute grocery delivery (Zomato)'
  },
  {
    id: 'zepto',
    name: 'Zepto',
    type: 'quickcommerce',
    domain: 'zepto.com',
    categories: ['groceries', 'food', 'essentials'],
    description: '10-minute delivery service'
  },
  {
    id: 'swiggy-instamart',
    name: 'Swiggy Instamart',
    type: 'quickcommerce',
    domain: 'swiggy.com/instamart',
    categories: ['groceries', 'food', 'essentials'],
    description: 'Swiggy quick commerce'
  },
  {
    id: 'bigbasket-bb-now',
    name: 'BB Now',
    type: 'quickcommerce',
    domain: 'bigbasket.com/bbnow',
    categories: ['groceries', 'food'],
    description: 'BigBasket express delivery'
  },
  {
    id: 'dunzo-daily',
    name: 'Dunzo Daily',
    type: 'quickcommerce',
    domain: 'dunzo.com',
    categories: ['groceries', 'essentials'],
    description: 'Quick delivery service'
  },
  {
    id: 'amazon-fresh',
    name: 'Amazon Fresh',
    type: 'quickcommerce',
    domain: 'amazon.in/fresh',
    categories: ['groceries', 'food'],
    description: 'Amazon quick grocery delivery'
  },
  {
    id: 'flipkart-quick',
    name: 'Flipkart Quick',
    type: 'quickcommerce',
    domain: 'flipkart.com/quick',
    categories: ['groceries', 'essentials'],
    description: 'Flipkart quick commerce'
  },
  {
    id: 'jiomart-express',
    name: 'JioMart Express',
    type: 'quickcommerce',
    domain: 'jiomart.com/express',
    categories: ['groceries', 'essentials'],
    description: 'JioMart quick delivery'
  },
];

export const ALL_PLATFORMS = [...ECOMMERCE_PLATFORMS, ...QUICKCOMMERCE_PLATFORMS];

// Helper functions
export function getPlatformByDomain(domain: string): PlatformInfo | undefined {
  return ALL_PLATFORMS.find(p =>
    domain.toLowerCase().includes(p.domain.toLowerCase())
  );
}

export function getPlatformsByType(type: 'ecommerce' | 'quickcommerce'): PlatformInfo[] {
  return ALL_PLATFORMS.filter(p => p.type === type);
}

export function searchPlatforms(query: string): PlatformInfo[] {
  const lowerQuery = query.toLowerCase().trim();

  if (!lowerQuery) {
    return ALL_PLATFORMS;
  }

  return ALL_PLATFORMS.filter(platform => {
    const searchText = `${platform.name} ${platform.description} ${platform.categories.join(' ')}`.toLowerCase();
    return searchText.includes(lowerQuery);
  });
}

// Get platform domains for search
export function getEcommerceDomains(): string[] {
  return ECOMMERCE_PLATFORMS.map(p => p.domain);
}

export function getQuickcommerceDomains(): string[] {
  return QUICKCOMMERCE_PLATFORMS.map(p => p.domain);
}

export function getAllDomains(): string[] {
  return ALL_PLATFORMS.map(p => p.domain);
}
