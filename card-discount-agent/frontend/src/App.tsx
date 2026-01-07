import { useState } from 'react';
import SearchBar from './components/SearchBar';
import CardSelector from './components/CardSelector';
import ProgressTracker from './components/ProgressTracker';
import DealsComparison from './components/DealsComparison';
import { searchDeals } from './services/api';
import type { SearchResponse, SearchProgress } from './types';
import { Sparkles } from 'lucide-react';

function App() {
  const [selectedCards, setSelectedCards] = useState<string[]>(['hdfc-millennia', 'icici-amazon-pay']);
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [progress, setProgress] = useState<SearchProgress[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setError('Please enter a product URL or name');
      return;
    }

    if (selectedCards.length === 0) {
      setError('Please select at least one credit card');
      return;
    }

    setIsSearching(true);
    setError(null);
    setSearchResults(null);
    setProgress([
      { step: 'initialize', status: 'in_progress', message: 'Initializing search...' },
      { step: 'fetch_prices', status: 'pending', message: 'Fetching prices from platforms' },
      { step: 'fetch_offers', status: 'pending', message: 'Finding bank offers and discounts' },
      { step: 'calculate', status: 'pending', message: 'Calculating effective prices' },
      { step: 'rank', status: 'pending', message: 'Ranking best deals' },
    ]);

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          const inProgressIndex = prev.findIndex(p => p.status === 'in_progress');
          if (inProgressIndex === -1 || inProgressIndex === prev.length - 1) {
            clearInterval(progressInterval);
            return prev;
          }

          const updated = [...prev];
          updated[inProgressIndex].status = 'completed';
          if (inProgressIndex + 1 < updated.length) {
            updated[inProgressIndex + 1].status = 'in_progress';
          }
          return updated;
        });
      }, 2000);

      const results = await searchDeals({
        query,
        selectedCards,
      });

      clearInterval(progressInterval);
      setProgress(prev => prev.map(p => ({ ...p, status: 'completed' as const })));
      setSearchResults(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search deals');
      setProgress(prev => prev.map((p, i) =>
        p.status === 'in_progress' ? { ...p, status: 'error' as const } : p
      ));
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Card Discount Agent</h1>
                <p className="text-sm text-gray-600">Find the best price with your cards</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="mb-8">
          <SearchBar onSearch={handleSearch} isLoading={isSearching} />

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Card Selector */}
        <div className="mb-8">
          <CardSelector
            selectedCards={selectedCards}
            onSelectionChange={setSelectedCards}
          />
        </div>

        {/* Progress Tracker */}
        {isSearching && progress.length > 0 && (
          <div className="mb-8">
            <ProgressTracker progress={progress} />
          </div>
        )}

        {/* Results */}
        {searchResults && (
          <DealsComparison results={searchResults} />
        )}

        {/* Empty State */}
        {!isSearching && !searchResults && (
          <div className="text-center py-16">
            <div className="inline-block p-4 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full mb-4">
              <Sparkles className="w-12 h-12 text-blue-600" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              Welcome to Card Discount Agent
            </h2>
            <p className="text-gray-600 max-w-md mx-auto">
              Enter a product URL or name above to find the best deal across platforms
              with your credit card discounts automatically calculated.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            Powered by Gemini 2.5 Flash with Google Search Grounding
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
