import { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
}

export default function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          {isLoading ? (
            <Loader2 className="h-5 w-5 text-gray-400 animate-spin" />
          ) : (
            <Search className="h-5 w-5 text-gray-400" />
          )}
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Paste product URL (Amazon, Flipkart) or enter product name..."
          disabled={isLoading}
          className="block w-full pl-12 pr-32 py-4 text-base border border-gray-300 rounded-xl
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent
                   disabled:bg-gray-100 disabled:cursor-not-allowed
                   shadow-sm transition-all"
        />
        <div className="absolute inset-y-0 right-0 flex items-center pr-2">
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white
                     font-medium rounded-lg hover:from-blue-700 hover:to-purple-700
                     disabled:opacity-50 disabled:cursor-not-allowed
                     transition-all shadow-sm"
          >
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>
      <p className="mt-2 text-sm text-gray-500">
        Supports: Amazon, Flipkart, Myntra, Blinkit, Zepto, Swiggy Instamart
      </p>
    </form>
  );
}
