export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`;
};

export const extractProductFromUrl = (url: string): string | null => {
  try {
    const urlObj = new URL(url);
    const hostname = urlObj.hostname;

    if (hostname.includes('amazon')) {
      return 'amazon';
    } else if (hostname.includes('flipkart')) {
      return 'flipkart';
    } else if (hostname.includes('myntra')) {
      return 'myntra';
    } else if (hostname.includes('blinkit')) {
      return 'blinkit';
    } else if (hostname.includes('zepto')) {
      return 'zepto';
    } else if (hostname.includes('swiggy')) {
      return 'swiggy';
    }

    return null;
  } catch {
    return null;
  }
};

export const isValidUrl = (str: string): boolean => {
  try {
    new URL(str);
    return true;
  } catch {
    return false;
  }
};
