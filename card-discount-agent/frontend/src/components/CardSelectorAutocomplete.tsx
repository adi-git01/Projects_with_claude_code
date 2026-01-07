import { useState, useEffect, useRef } from 'react';
import { CreditCard as CreditCardIcon, Check, Search, X, Star } from 'lucide-react';
import clsx from 'clsx';
import type { CreditCard } from '../types';
import { INDIAN_CREDIT_CARDS, searchCards, getPopularCards } from '../data/creditCards';

interface CardSelectorAutocompleteProps {
  selectedCards: string[];
  onSelectionChange: (cardIds: string[]) => void;
}

const STORAGE_KEY = 'card-discount-agent-selected-cards';

export default function CardSelectorAutocomplete({
  selectedCards,
  onSelectionChange
}: CardSelectorAutocompleteProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [filteredCards, setFilteredCards] = useState<CreditCard[]>([]);
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Load saved cards from localStorage on mount
  useEffect(() => {
    const savedCards = localStorage.getItem(STORAGE_KEY);
    if (savedCards && selectedCards.length === 0) {
      try {
        const parsed = JSON.parse(savedCards);
        if (Array.isArray(parsed) && parsed.length > 0) {
          onSelectionChange(parsed);
        }
      } catch (e) {
        console.error('Failed to load saved cards:', e);
      }
    }
  }, []);

  // Save selected cards to localStorage whenever they change
  useEffect(() => {
    if (selectedCards.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(selectedCards));
    }
  }, [selectedCards]);

  // Filter cards based on search query
  useEffect(() => {
    if (isSearchOpen) {
      const results = searchCards(searchQuery);
      setFilteredCards(results.slice(0, 50)); // Limit to 50 results
    }
  }, [searchQuery, isSearchOpen]);

  // Focus search input when dropdown opens
  useEffect(() => {
    if (isSearchOpen && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [isSearchOpen]);

  const toggleCard = (cardId: string) => {
    if (selectedCards.includes(cardId)) {
      onSelectionChange(selectedCards.filter(id => id !== cardId));
    } else {
      onSelectionChange([...selectedCards, cardId]);
    }
  };

  const removeCard = (cardId: string) => {
    onSelectionChange(selectedCards.filter(id => id !== cardId));
  };

  const clearAll = () => {
    onSelectionChange([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  const addPopularCards = () => {
    const popularIds = getPopularCards().map(c => c.id);
    const newSelection = [...new Set([...selectedCards, ...popularIds])];
    onSelectionChange(newSelection);
  };

  const getSelectedCardObjects = (): CreditCard[] => {
    return selectedCards
      .map(id => INDIAN_CREDIT_CARDS.find(card => card.id === id))
      .filter((card): card is CreditCard => card !== undefined);
  };

  const selectedCardObjects = getSelectedCardObjects();

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <CreditCardIcon className="w-5 h-5 text-gray-700" />
          <h2 className="text-lg font-semibold text-gray-900">Your Credit Cards</h2>
          <span className="text-sm text-gray-500">
            ({selectedCards.length} selected)
          </span>
        </div>

        <div className="flex items-center space-x-2">
          {selectedCards.length > 0 && (
            <button
              onClick={clearAll}
              className="text-sm text-red-600 hover:text-red-700 font-medium"
            >
              Clear All
            </button>
          )}
          <button
            onClick={addPopularCards}
            className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            <Star className="w-4 h-4" />
            <span>Add Popular</span>
          </button>
        </div>
      </div>

      {/* Selected Cards Display */}
      {selectedCardObjects.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-2">
          {selectedCardObjects.map((card) => (
            <div
              key={card.id}
              className="inline-flex items-center space-x-2 px-3 py-1.5 bg-blue-50 border border-blue-200 rounded-lg"
            >
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: card.color }}
              />
              <span className="text-sm font-medium text-gray-900">
                {card.bank} {card.name}
              </span>
              <span className="text-xs text-gray-600">
                ({card.baseReward}{card.type === 'reward_points' ? ' pts' : '%'})
              </span>
              <button
                onClick={() => removeCard(card.id)}
                className="text-gray-400 hover:text-red-600 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Search Bar */}
      <div className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            ref={searchInputRef}
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onFocus={() => setIsSearchOpen(true)}
            placeholder="Search cards by bank name or card name (e.g., 'HDFC Millennia', 'Amazon Pay')..."
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Search Results Dropdown */}
        {isSearchOpen && (
          <>
            {/* Backdrop */}
            <div
              className="fixed inset-0 z-10"
              onClick={() => setIsSearchOpen(false)}
            />

            {/* Results */}
            <div className="absolute z-20 mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto">
              {filteredCards.length === 0 ? (
                <div className="p-4 text-center text-gray-500">
                  {searchQuery ? 'No cards found' : 'Start typing to search...'}
                </div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {filteredCards.map((card) => {
                    const isSelected = selectedCards.includes(card.id);

                    return (
                      <button
                        key={card.id}
                        onClick={() => {
                          toggleCard(card.id);
                          setSearchQuery('');
                          setIsSearchOpen(false);
                        }}
                        className={clsx(
                          'w-full p-3 hover:bg-gray-50 transition-colors text-left',
                          isSelected && 'bg-blue-50'
                        )}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-1">
                              <div
                                className="w-3 h-3 rounded-full flex-shrink-0"
                                style={{ backgroundColor: card.color }}
                              />
                              <span className="font-semibold text-gray-900">
                                {card.bank} {card.name}
                              </span>
                              {isSelected && (
                                <Check className="w-4 h-4 text-blue-600" />
                              )}
                            </div>

                            <div className="flex items-center space-x-3 text-sm">
                              <span className={clsx(
                                'inline-block px-2 py-0.5 rounded text-xs font-medium',
                                card.type === 'instant_discount' && 'bg-green-100 text-green-800',
                                card.type === 'cashback' && 'bg-purple-100 text-purple-800',
                                card.type === 'reward_points' && 'bg-orange-100 text-orange-800'
                              )}>
                                {card.type === 'reward_points' ? `${card.baseReward} pts/₹100` : `${card.baseReward}% back`}
                              </span>
                              {card.description && (
                                <span className="text-gray-600 text-xs truncate">
                                  {card.description}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          </>
        )}
      </div>

      {/* Helper Text */}
      <p className="mt-3 text-sm text-gray-500">
        Search from {INDIAN_CREDIT_CARDS.length}+ cards • Your selection is auto-saved
      </p>
    </div>
  );
}
