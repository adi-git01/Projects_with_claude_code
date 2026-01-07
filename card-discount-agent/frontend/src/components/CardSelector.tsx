import { CREDIT_CARDS } from '../types';
import { CreditCard as CreditCardIcon, Check } from 'lucide-react';
import clsx from 'clsx';

interface CardSelectorProps {
  selectedCards: string[];
  onSelectionChange: (cardIds: string[]) => void;
}

export default function CardSelector({ selectedCards, onSelectionChange }: CardSelectorProps) {
  const toggleCard = (cardId: string) => {
    if (selectedCards.includes(cardId)) {
      onSelectionChange(selectedCards.filter(id => id !== cardId));
    } else {
      onSelectionChange([...selectedCards, cardId]);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-2 mb-4">
        <CreditCardIcon className="w-5 h-5 text-gray-700" />
        <h2 className="text-lg font-semibold text-gray-900">Your Credit Cards</h2>
        <span className="text-sm text-gray-500">({selectedCards.length} selected)</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {CREDIT_CARDS.map((card) => {
          const isSelected = selectedCards.includes(card.id);

          return (
            <button
              key={card.id}
              onClick={() => toggleCard(card.id)}
              className={clsx(
                'relative p-4 rounded-lg border-2 transition-all text-left',
                'hover:shadow-md active:scale-95',
                isSelected
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              )}
            >
              {isSelected && (
                <div className="absolute top-2 right-2 bg-blue-500 rounded-full p-1">
                  <Check className="w-3 h-3 text-white" />
                </div>
              )}

              <div className="flex items-center space-x-2 mb-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: card.color }}
                />
                <span className="text-xs font-medium text-gray-600">{card.bank}</span>
              </div>

              <h3 className="font-semibold text-gray-900 mb-1">{card.name}</h3>

              <div className="flex items-baseline space-x-1">
                <span className="text-lg font-bold text-blue-600">{card.baseReward}</span>
                <span className="text-xs text-gray-600">
                  {card.type === 'reward_points' ? 'pts/₹100' : '% back'}
                </span>
              </div>

              <div className="mt-2">
                <span className={clsx(
                  'inline-block px-2 py-0.5 rounded text-xs font-medium',
                  card.type === 'instant_discount' && 'bg-green-100 text-green-800',
                  card.type === 'cashback' && 'bg-purple-100 text-purple-800',
                  card.type === 'reward_points' && 'bg-orange-100 text-orange-800'
                )}>
                  {card.type.replace('_', ' ')}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
