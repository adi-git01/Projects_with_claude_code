import type { SearchResponse } from '../types';
import DealCard from './DealCard';
import { Trophy, ShoppingBag, Zap } from 'lucide-react';

interface DealsComparisonProps {
  results: SearchResponse;
}

export default function DealsComparison({ results }: DealsComparisonProps) {
  const ecommerceDeals = results.deals.filter(d => d.platform.type === 'ecommerce');
  const quickcommerceDeals = results.deals.filter(d => d.platform.type === 'quickcommerce');
  const bestDeal = results.deals.find(d => d.isBestDeal);

  return (
    <div className="space-y-8">
      {/* Product Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-start space-x-4">
          {results.productImage && (
            <img
              src={results.productImage}
              alt={results.productName}
              className="w-24 h-24 object-contain rounded-lg border border-gray-200"
            />
          )}
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {results.productName}
            </h2>
            <p className="text-sm text-gray-500">
              Found {results.deals.length} deals across {ecommerceDeals.length} e-commerce
              and {quickcommerceDeals.length} quick-commerce platforms
            </p>
            {bestDeal && (
              <div className="mt-3 inline-flex items-center space-x-2 px-3 py-1.5 bg-green-50 border border-green-200 rounded-lg">
                <Trophy className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-800">
                  Best Deal: Save ₹{bestDeal.savings.toFixed(0)} on {bestDeal.platform.name}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* E-commerce Section */}
      {ecommerceDeals.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <ShoppingBag className="w-5 h-5 text-blue-600" />
            <h3 className="text-xl font-semibold text-gray-900">E-Commerce</h3>
            <span className="text-sm text-gray-500">({ecommerceDeals.length} options)</span>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {ecommerceDeals.map((deal, index) => (
              <DealCard key={index} deal={deal} />
            ))}
          </div>
        </div>
      )}

      {/* Quick-commerce Section */}
      {quickcommerceDeals.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <Zap className="w-5 h-5 text-purple-600" />
            <h3 className="text-xl font-semibold text-gray-900">Quick Commerce</h3>
            <span className="text-sm text-gray-500">({quickcommerceDeals.length} options)</span>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {quickcommerceDeals.map((deal, index) => (
              <DealCard key={index} deal={deal} />
            ))}
          </div>
        </div>
      )}

      {results.deals.length === 0 && (
        <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
          <p className="text-gray-600">No deals found for this product</p>
        </div>
      )}
    </div>
  );
}
