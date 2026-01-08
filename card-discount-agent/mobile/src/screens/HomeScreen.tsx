import React, { useState } from 'react';
import {
  View,
  ScrollView,
  Text,
  StyleSheet,
  SafeAreaView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import SearchBar from '../components/SearchBar';
import CardSelector from '../components/CardSelector';
import DealCard from '../components/DealCard';
import { searchDeals } from '../services/api';
import type { SearchResponse, ProductDeal } from '../types';

export default function HomeScreen() {
  const [selectedCards, setSelectedCards] = useState<string[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      Alert.alert('Error', 'Please enter a product URL or name');
      return;
    }

    if (selectedCards.length === 0) {
      Alert.alert('Error', 'Please select at least one credit card');
      return;
    }

    setIsSearching(true);
    setError(null);
    setSearchResults(null);

    try {
      const results = await searchDeals({
        query,
        selectedCards,
      });

      setSearchResults(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search deals');
      Alert.alert('Error', 'Failed to search for deals. Please check your connection and try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const ecommerceDeals = searchResults?.deals.filter(
    d => d.platform.type === 'ecommerce'
  ) || [];
  const quickcommerceDeals = searchResults?.deals.filter(
    d => d.platform.type === 'quickcommerce'
  ) || [];
  const bestDeal = searchResults?.deals.find(d => d.isBestDeal);

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Card Discount Agent</Text>
          <Text style={styles.headerSubtitle}>
            Find the best price with your cards
          </Text>
        </View>

        {/* Search */}
        <SearchBar onSearch={handleSearch} isLoading={isSearching} />

        {/* Card Selector */}
        <CardSelector
          selectedCards={selectedCards}
          onSelectionChange={setSelectedCards}
        />

        {/* Loading */}
        {isSearching && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#3B82F6" />
            <Text style={styles.loadingText}>
              Searching 25+ platforms...
            </Text>
            <Text style={styles.loadingSubtext}>
              This may take 60-90 seconds
            </Text>
          </View>
        )}

        {/* Error */}
        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}

        {/* Results */}
        {searchResults && (
          <View style={styles.results}>
            {/* Product Info */}
            <View style={styles.productInfo}>
              <Text style={styles.productName}>{searchResults.productName}</Text>
              <Text style={styles.resultsCount}>
                Found {searchResults.deals.length} deals
              </Text>
              {bestDeal && (
                <Text style={styles.bestDealInfo}>
                  🏆 Best: Save ₹{bestDeal.savings.toFixed(0)} on {bestDeal.platform.name}
                </Text>
              )}
            </View>

            {/* E-Commerce Deals */}
            {ecommerceDeals.length > 0 && (
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>
                  🛒 E-Commerce ({ecommerceDeals.length})
                </Text>
                {ecommerceDeals.map((deal, idx) => (
                  <DealCard key={idx} deal={deal} />
                ))}
              </View>
            )}

            {/* Quick-Commerce Deals */}
            {quickcommerceDeals.length > 0 && (
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>
                  ⚡ Quick-Commerce ({quickcommerceDeals.length})
                </Text>
                {quickcommerceDeals.map((deal, idx) => (
                  <DealCard key={idx} deal={deal} />
                ))}
              </View>
            )}

            {searchResults.deals.length === 0 && (
              <View style={styles.emptyState}>
                <Text style={styles.emptyText}>No deals found</Text>
                <Text style={styles.emptySubtext}>Try a different product</Text>
              </View>
            )}
          </View>
        )}

        {/* Empty State */}
        {!isSearching && !searchResults && (
          <View style={styles.emptyState}>
            <Text style={styles.emptyIcon}>✨</Text>
            <Text style={styles.emptyTitle}>Welcome!</Text>
            <Text style={styles.emptySubtext}>
              Select your cards and search for a product to find the best deals
            </Text>
          </View>
        )}

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Powered by Gemini 2.5 Flash
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  container: {
    flex: 1,
    padding: 16,
  },
  header: {
    marginBottom: 24,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: '#1F2937',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#6B7280',
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 40,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    marginVertical: 16,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
  },
  loadingSubtext: {
    marginTop: 8,
    fontSize: 14,
    color: '#6B7280',
  },
  errorContainer: {
    backgroundColor: '#FEE2E2',
    padding: 16,
    borderRadius: 8,
    marginVertical: 16,
  },
  errorText: {
    color: '#991B1B',
    fontSize: 14,
  },
  results: {
    marginTop: 16,
  },
  productInfo: {
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
  },
  productName: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1F2937',
    marginBottom: 8,
  },
  resultsCount: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 8,
  },
  bestDealInfo: {
    fontSize: 14,
    color: '#10B981',
    fontWeight: '600',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1F2937',
    marginBottom: 12,
  },
  emptyState: {
    alignItems: 'center',
    padding: 40,
    marginTop: 40,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#6B7280',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#9CA3AF',
    textAlign: 'center',
    maxWidth: 280,
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  footerText: {
    fontSize: 12,
    color: '#9CA3AF',
  },
});
