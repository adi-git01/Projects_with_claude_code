import { CheckCircle2, Loader2, XCircle, Circle } from 'lucide-react';
import type { SearchProgress } from '../types';
import clsx from 'clsx';

interface ProgressTrackerProps {
  progress: SearchProgress[];
}

export default function ProgressTracker({ progress }: ProgressTrackerProps) {
  const getIcon = (status: SearchProgress['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'in_progress':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Circle className="w-5 h-5 text-gray-300" />;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Search Progress</h2>

      <div className="space-y-4">
        {progress.map((item, index) => (
          <div key={item.step} className="flex items-start space-x-3">
            {/* Icon */}
            <div className="flex-shrink-0 mt-0.5">
              {getIcon(item.status)}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
              <p className={clsx(
                'text-sm font-medium',
                item.status === 'completed' && 'text-gray-900',
                item.status === 'in_progress' && 'text-blue-600',
                item.status === 'error' && 'text-red-600',
                item.status === 'pending' && 'text-gray-400'
              )}>
                {item.message}
              </p>

              {/* Progress bar for in_progress */}
              {item.status === 'in_progress' && (
                <div className="mt-2 w-full bg-gray-200 rounded-full h-1.5">
                  <div className="bg-blue-500 h-1.5 rounded-full animate-pulse-slow" style={{ width: '60%' }} />
                </div>
              )}
            </div>

            {/* Step number */}
            <div className="flex-shrink-0">
              <span className="text-xs text-gray-500">
                {index + 1}/{progress.length}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
