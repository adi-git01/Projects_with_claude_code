import type { ProductDeal } from '../types';
import { formatCurrency } from '../utils/formatters';
import { ExternalLink, TrendingDown, CreditCard, Package, Trophy, AlertCircle } from 'lucide-react';
import clsx from 'clsx';

interface DealCardProps {
  deal: ProductDeal;
}

export default function DealCard({ deal }: DealCardProps) {
  const savingsPercent = ((deal.savings / deal.basePrice) * 100).toFixed(1);

  return (
    <div className={clsx(
      'bg-white rounded-xl border-2 p-5 transition-all hover:shadow-lg',
      deal.isBestDeal
        ? 'border-green-500 shadow-md'
        : 'border-gray-200'
    )}>
      {/* Best Deal Badge */}
      {deal.isBestDeal && (
        <div className="flex items-center space-x-1 mb-3 text-green-700">
          <Trophy className="w-4 h-4" />
          <span className="text-sm font-bold">BEST DEAL</span>
        </div>
      )}

      {/* Platform Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-900">{deal.platform.name}</h3>
          <span className={clsx(
            'inline-block mt-1 px-2 py-0.5 rounded text-xs font-medium',
            deal.platform.type === 'ecommerce'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-purple-100 text-purple-800'
          )}>
            {deal.platform.type === 'ecommerce' ? 'E-Commerce' : 'Quick Commerce'}
          </span>
        </div>

        {!deal.inStock && (
          <div className="flex items-center space-x-1 text-red-600">
            <AlertCircle className="w-4 h-4" />
            <span className="text-xs font-medium">Out of Stock</span>
          </div>
        )}
      </div>

      {/* Price Breakdown */}
      <div className="space-y-2 mb-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Base Price</span>
          <span className="font-medium text-gray-900">{formatCurrency(deal.basePrice)}</span>
        </div>

        {deal.deliveryCharge > 0 && (
          <div className="flex justify-between text-sm">
            <span className="text-gray-600 flex items-center space-x-1">
              <Package className="w-3 h-3" />
              <span>Delivery</span>
            </span>
            <span className="font-medium text-gray-900">+{formatCurrency(deal.deliveryCharge)}</span>
          </div>
        )}

        {deal.availableDiscounts.map((discount, idx) => (
          <div key={idx} className="flex justify-between text-sm">
            <span className="text-green-600 flex items-center space-x-1">
              <TrendingDown className="w-3 h-3" />
              <span className="truncate max-w-[180px]" title={discount.description}>
                {discount.description}
              </span>
            </span>
            <span className="font-medium text-green-600">
              -{discount.isPercentage ? `${discount.value}%` : formatCurrency(discount.value)}
            </span>
          </div>
        ))}

        <div className="pt-2 mt-2 border-t border-gray-200">
          <div className="flex justify-between items-baseline">
            <span className="text-gray-900 font-semibold">Effective Price</span>
            <span className="text-2xl font-bold text-gray-900">
              {formatCurrency(deal.effectivePrice)}
            </span>
          </div>
        </div>
      </div>

      {/* Savings Badge */}
      {deal.savings > 0 && (
        <div className="mb-4 p-2 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-sm text-green-800">Total Savings</span>
            <div className="text-right">
              <span className="text-lg font-bold text-green-700">
                {formatCurrency(deal.savings)}
              </span>
              <span className="text-xs text-green-600 ml-2">({savingsPercent}% off)</span>
            </div>
          </div>
        </div>
      )}

      {/* Best Card */}
      {deal.bestCard && (
        <div className="mb-4 flex items-center space-x-2 text-sm">
          <CreditCard className="w-4 h-4 text-gray-600" />
          <span className="text-gray-600">Best with:</span>
          <span className="font-semibold text-gray-900">
            {deal.bestCard.bank} {deal.bestCard.name}
          </span>
        </div>
      )}

      {/* Action Button */}
      <a
        href={deal.productUrl}
        target="_blank"
        rel="noopener noreferrer"
        className={clsx(
          'flex items-center justify-center space-x-2 w-full py-3 rounded-lg font-medium transition-all',
          deal.inStock
            ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700'
            : 'bg-gray-300 text-gray-600 cursor-not-allowed'
        )}
        onClick={(e) => !deal.inStock && e.preventDefault()}
      >
        <span>{deal.inStock ? 'View Deal' : 'Out of Stock'}</span>
        {deal.inStock && <ExternalLink className="w-4 h-4" />}
      </a>
    </div>
  );
}
