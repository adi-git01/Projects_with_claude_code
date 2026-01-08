import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  Modal,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { INDIAN_CREDIT_CARDS, searchCards } from '../data/creditCards';
import type { CreditCard } from '../types';

interface CardSelectorProps {
  selectedCards: string[];
  onSelectionChange: (cardIds: string[]) => void;
}

const STORAGE_KEY = '@card_discount_agent:selected_cards';

export default function CardSelector({
  selectedCards,
  onSelectionChange,
}: CardSelectorProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [filteredCards, setFilteredCards] = useState<CreditCard[]>([]);

  // Load saved cards
  useEffect(() => {
    loadSavedCards();
  }, []);

  // Save cards when changed
  useEffect(() => {
    if (selectedCards.length > 0) {
      AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(selectedCards));
    }
  }, [selectedCards]);

  // Filter cards
  useEffect(() => {
    const results = searchCards(searchQuery);
    setFilteredCards(results.slice(0, 50));
  }, [searchQuery]);

  const loadSavedCards = async () => {
    try {
      const saved = await AsyncStorage.getItem(STORAGE_KEY);
      if (saved && selectedCards.length === 0) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          onSelectionChange(parsed);
        }
      }
    } catch (error) {
      console.error('Failed to load saved cards:', error);
    }
  };

  const toggleCard = (cardId: string) => {
    if (selectedCards.includes(cardId)) {
      onSelectionChange(selectedCards.filter(id => id !== cardId));
    } else {
      onSelectionChange([...selectedCards, cardId]);
    }
    setModalVisible(false);
    setSearchQuery('');
  };

  const removeCard = (cardId: string) => {
    onSelectionChange(selectedCards.filter(id => id !== cardId));
  };

  const clearAll = () => {
    onSelectionChange([]);
    AsyncStorage.removeItem(STORAGE_KEY);
  };

  const getSelectedCardObjects = (): CreditCard[] => {
    return selectedCards
      .map(id => INDIAN_CREDIT_CARDS.find(card => card.id === id))
      .filter((card): card is CreditCard => card !== undefined);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Your Cards ({selectedCards.length})</Text>
        {selectedCards.length > 0 && (
          <TouchableOpacity onPress={clearAll}>
            <Text style={styles.clearButton}>Clear All</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Selected Cards */}
      {getSelectedCardObjects().map(card => (
        <View key={card.id} style={styles.selectedCard}>
          <View style={[styles.cardDot, { backgroundColor: card.color }]} />
          <Text style={styles.selectedCardText}>
            {card.bank} {card.name}
          </Text>
          <Text style={styles.selectedCardReward}>
            ({card.baseReward}{card.type === 'reward_points' ? ' pts' : '%'})
          </Text>
          <TouchableOpacity
            onPress={() => removeCard(card.id)}
            style={styles.removeButton}>
            <Text style={styles.removeButtonText}>×</Text>
          </TouchableOpacity>
        </View>
      ))}

      {/* Add Card Button */}
      <TouchableOpacity
        style={styles.addButton}
        onPress={() => setModalVisible(true)}>
        <Text style={styles.addButtonText}>+ Add Card</Text>
      </TouchableOpacity>

      {/* Card Search Modal */}
      <Modal
        visible={modalVisible}
        animationType="slide"
        onRequestClose={() => setModalVisible(false)}>
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Search Cards</Text>
            <TouchableOpacity onPress={() => setModalVisible(false)}>
              <Text style={styles.closeButton}>Close</Text>
            </TouchableOpacity>
          </View>

          <TextInput
            style={styles.searchInput}
            value={searchQuery}
            onChangeText={setSearchQuery}
            placeholder="Search by bank or card name..."
            placeholderTextColor="#9CA3AF"
            autoFocus
          />

          <FlatList
            data={filteredCards}
            keyExtractor={item => item.id}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={[
                  styles.cardItem,
                  selectedCards.includes(item.id) && styles.cardItemSelected,
                ]}
                onPress={() => toggleCard(item.id)}>
                <View style={[styles.cardDot, { backgroundColor: item.color }]} />
                <View style={styles.cardInfo}>
                  <Text style={styles.cardName}>
                    {item.bank} {item.name}
                  </Text>
                  <Text style={styles.cardDescription}>{item.description}</Text>
                  <Text style={styles.cardReward}>
                    {item.baseReward}
                    {item.type === 'reward_points' ? ' pts/₹100' : '% back'}
                  </Text>
                </View>
                {selectedCards.includes(item.id) && (
                  <Text style={styles.checkmark}>✓</Text>
                )}
              </TouchableOpacity>
            )}
          />
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    marginBottom: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1F2937',
  },
  clearButton: {
    color: '#EF4444',
    fontSize: 14,
    fontWeight: '500',
  },
  selectedCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#EFF6FF',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
  },
  cardDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  selectedCardText: {
    flex: 1,
    fontSize: 14,
    fontWeight: '500',
    color: '#1F2937',
  },
  selectedCardReward: {
    fontSize: 12,
    color: '#6B7280',
    marginRight: 8,
  },
  removeButton: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#FEE2E2',
    alignItems: 'center',
    justifyContent: 'center',
  },
  removeButtonText: {
    color: '#EF4444',
    fontSize: 18,
    fontWeight: '600',
  },
  addButton: {
    backgroundColor: '#3B82F6',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  addButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  modalContainer: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1F2937',
  },
  closeButton: {
    color: '#3B82F6',
    fontSize: 16,
    fontWeight: '500',
  },
  searchInput: {
    margin: 16,
    padding: 12,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    fontSize: 16,
  },
  cardItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#F3F4F6',
  },
  cardItemSelected: {
    backgroundColor: '#EFF6FF',
  },
  cardInfo: {
    flex: 1,
    marginLeft: 12,
  },
  cardName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 4,
  },
  cardDescription: {
    fontSize: 12,
    color: '#6B7280',
    marginBottom: 4,
  },
  cardReward: {
    fontSize: 12,
    color: '#3B82F6',
    fontWeight: '500',
  },
  checkmark: {
    fontSize: 20,
    color: '#3B82F6',
    fontWeight: '600',
  },
});
