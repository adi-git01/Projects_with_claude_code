import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Linking,
} from 'react-native';
import type { ProductDeal } from '../types';
import { formatCurrency } from '../utils/formatters';

interface DealCardProps {
  deal: ProductDeal;
}

export default function DealCard({ deal }: DealCardProps) {
  const savingsPercent = ((deal.savings / deal.basePrice) * 100).toFixed(1);

  const handleViewDeal = () => {
    if (deal.inStock && deal.productUrl) {
      Linking.openURL(deal.productUrl);
    }
  };

  return (
    <View style={[styles.card, deal.isBestDeal && styles.bestDealCard]}>
      {deal.isBestDeal && (
        <View style={styles.bestDealBadge}>
          <Text style={styles.bestDealText}>🏆 BEST DEAL</Text>
        </View>
      )}

      {/* Platform Name */}
      <View style={styles.header}>
        <Text style={styles.platformName}>{deal.platform.name}</Text>
        <View style={[
          styles.typeBadge,
          deal.platform.type === 'ecommerce' ? styles.ecommerceBadge : styles.qcommerceBadge
        ]}>
          <Text style={styles.typeBadgeText}>
            {deal.platform.type === 'ecommerce' ? 'E-Com' : 'Quick'}
          </Text>
        </View>
      </View>

      {!deal.inStock && (
        <Text style={styles.outOfStock}>Out of Stock</Text>
      )}

      {/* Price Breakdown */}
      <View style={styles.priceSection}>
        <View style={styles.priceRow}>
          <Text style={styles.priceLabel}>Base Price</Text>
          <Text style={styles.priceValue}>{formatCurrency(deal.basePrice)}</Text>
        </View>

        {deal.deliveryCharge > 0 && (
          <View style={styles.priceRow}>
            <Text style={styles.priceLabel}>+ Delivery</Text>
            <Text style={styles.priceValue}>{formatCurrency(deal.deliveryCharge)}</Text>
          </View>
        )}

        {deal.availableDiscounts.map((discount, idx) => (
          <View key={idx} style={styles.priceRow}>
            <Text style={styles.discountLabel}>- {discount.description}</Text>
            <Text style={styles.discountValue}>
              -{discount.isPercentage ? `${discount.value}%` : formatCurrency(discount.value)}
            </Text>
          </View>
        ))}

        <View style={styles.divider} />

        <View style={styles.priceRow}>
          <Text style={styles.finalLabel}>Final Price</Text>
          <Text style={styles.finalPrice}>{formatCurrency(deal.effectivePrice)}</Text>
        </View>
      </View>

      {/* Savings */}
      {deal.savings > 0 && (
        <View style={styles.savingsBox}>
          <Text style={styles.savingsText}>
            You Save: {formatCurrency(deal.savings)} ({savingsPercent}%)
          </Text>
        </View>
      )}

      {/* Best Card */}
      {deal.bestCard && (
        <Text style={styles.bestCard}>
          Best with: {deal.bestCard.bank} {deal.bestCard.name}
        </Text>
      )}

      {/* View Deal Button */}
      <TouchableOpacity
        style={[styles.viewButton, !deal.inStock && styles.viewButtonDisabled]}
        onPress={handleViewDeal}
        disabled={!deal.inStock}>
        <Text style={styles.viewButtonText}>
          {deal.inStock ? 'View Deal →' : 'Out of Stock'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#E5E7EB',
  },
  bestDealCard: {
    borderColor: '#10B981',
  },
  bestDealBadge: {
    backgroundColor: '#10B981',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  bestDealText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '700',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  platformName: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1F2937',
  },
  typeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  ecommerceBadge: {
    backgroundColor: '#DBEAFE',
  },
  qcommerceBadge: {
    backgroundColor: '#F3E8FF',
  },
  typeBadgeText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#1F2937',
  },
  outOfStock: {
    color: '#EF4444',
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 8,
  },
  priceSection: {
    backgroundColor: '#F9FAFB',
    borderRadius: 8,
    padding: 12,
    marginVertical: 12,
  },
  priceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  priceLabel: {
    fontSize: 14,
    color: '#6B7280',
  },
  priceValue: {
    fontSize: 14,
    color: '#1F2937',
    fontWeight: '500',
  },
  discountLabel: {
    fontSize: 14,
    color: '#10B981',
    flex: 1,
  },
  discountValue: {
    fontSize: 14,
    color: '#10B981',
    fontWeight: '600',
  },
  divider: {
    height: 1,
    backgroundColor: '#E5E7EB',
    marginVertical: 8,
  },
  finalLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
  },
  finalPrice: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1F2937',
  },
  savingsBox: {
    backgroundColor: '#D1FAE5',
    padding: 8,
    borderRadius: 6,
    marginBottom: 12,
  },
  savingsText: {
    color: '#065F46',
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
  },
  bestCard: {
    fontSize: 12,
    color: '#6B7280',
    marginBottom: 12,
  },
  viewButton: {
    backgroundColor: '#3B82F6',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  viewButtonDisabled: {
    backgroundColor: '#9CA3AF',
  },
  viewButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});
