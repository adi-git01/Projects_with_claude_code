import { useState, useEffect } from 'react';
import { Globe, Zap, AlertCircle } from 'lucide-react';
import {
  getSearchGroundingConfig,
  toggleSearchGrounding,
  type SearchGroundingConfig,
} from '../services/api';

interface SearchGroundingToggleProps {
  className?: string;
}

export default function SearchGroundingToggle({ className = '' }: SearchGroundingToggleProps) {
  const [config, setConfig] = useState<SearchGroundingConfig | null>(null);
  const [isToggling, setIsToggling] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  // Fetch current config on mount
  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const currentConfig = await getSearchGroundingConfig();
      setConfig(currentConfig);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch config');
    }
  };

  const handleToggle = async () => {
    if (!config || isToggling) return;

    setIsToggling(true);
    setError(null);

    try {
      const newEnabled = !config.search_grounding_enabled;
      const response = await toggleSearchGrounding(newEnabled);

      // Update local config
      await fetchConfig();

      // Show success toast
      setToastMessage(response.message);
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to toggle search grounding');
    } finally {
      setIsToggling(false);
    }
  };

  if (!config) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <div className="animate-pulse bg-gray-200 h-8 w-48 rounded"></div>
      </div>
    );
  }

  const isGrounded = config.search_grounding_enabled;
  const Icon = isGrounded ? Globe : Zap;

  return (
    <div className={`relative ${className}`}>
      {/* Main Toggle Container */}
      <div className="flex items-center space-x-3 bg-white rounded-lg border border-gray-200 px-4 py-2 shadow-sm">
        {/* Icon */}
        <div className={`p-1.5 rounded ${isGrounded ? 'bg-blue-100' : 'bg-green-100'}`}>
          <Icon className={`w-4 h-4 ${isGrounded ? 'text-blue-600' : 'text-green-600'}`} />
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium text-gray-900">
              {isGrounded ? 'Real-Time' : 'Testing'}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full ${
              isGrounded
                ? 'bg-blue-100 text-blue-700'
                : 'bg-green-100 text-green-700'
            }`}>
              {config.rpm} RPM
            </span>
          </div>
          <p className="text-xs text-gray-500">
            {isGrounded ? `~${config.rpd_estimate} RPD` : `~${config.rpd_estimate} RPD`}
          </p>
        </div>

        {/* Toggle Switch */}
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className={`
            relative inline-flex h-6 w-11 items-center rounded-full
            transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
            ${isToggling ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            ${isGrounded ? 'bg-blue-600' : 'bg-gray-300'}
          `}
          aria-label="Toggle search grounding"
        >
          <span
            className={`
              inline-block h-4 w-4 transform rounded-full bg-white transition-transform
              ${isGrounded ? 'translate-x-6' : 'translate-x-1'}
            `}
          />
        </button>

        {/* Info Tooltip Icon */}
        <div className="relative group">
          <AlertCircle className="w-4 h-4 text-gray-400 cursor-help" />

          {/* Tooltip */}
          <div className="absolute right-0 top-8 w-64 bg-gray-900 text-white text-xs rounded-lg p-3 shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
            <div className="space-y-2">
              <div>
                <strong className="text-blue-300">Real-Time Mode (ON):</strong>
                <ul className="mt-1 ml-3 space-y-0.5">
                  <li>• Live prices from websites</li>
                  <li>• Actual product URLs</li>
                  <li>• {config.mode === 'grounded' ? config.rpm : 2} RPM, ~{config.mode === 'grounded' ? config.rpd_estimate : '50-100'} RPD</li>
                </ul>
              </div>
              <div>
                <strong className="text-green-300">Testing Mode (OFF):</strong>
                <ul className="mt-1 ml-3 space-y-0.5">
                  <li>• Example prices</li>
                  <li>• Fast responses</li>
                  <li>• {config.mode === 'non-grounded' ? config.rpm : 10} RPM, ~{config.mode === 'non-grounded' ? config.rpd_estimate : '1500'} RPD</li>
                </ul>
              </div>
              <p className="text-gray-300 border-t border-gray-700 pt-2 mt-2">
                Cache: {config.cache_size} queries
              </p>
            </div>
            {/* Arrow */}
            <div className="absolute -top-1 right-4 w-2 h-2 bg-gray-900 transform rotate-45"></div>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="absolute top-full left-0 right-0 mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-700">
          {error}
        </div>
      )}

      {/* Success Toast */}
      {showToast && (
        <div className="fixed bottom-4 right-4 bg-gray-900 text-white px-4 py-3 rounded-lg shadow-lg z-50 flex items-center space-x-2">
          <div className={`p-1 rounded ${isGrounded ? 'bg-blue-600' : 'bg-green-600'}`}>
            <Icon className="w-4 h-4 text-white" />
          </div>
          <span className="text-sm">{toastMessage}</span>
        </div>
      )}
    </div>
  );
}
