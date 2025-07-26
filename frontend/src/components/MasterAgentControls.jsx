import React, { useState } from 'react';
import { Play, Square, Settings } from 'lucide-react';
import useCaseStore from '../store/useCaseStore';

const MasterAgentControls = () => {
  const [showConfig, setShowConfig] = useState(false);
  const { isRunning, setIsRunning, settings, updateSettings } = useCaseStore();

  const handleStop = () => {
    setIsRunning(false);
    // Here you would also call an API to stop the agents
  };

  return (
    <div className="p-4">
      <div className="flex gap-2 mb-3">
        <button
          disabled={isRunning}
          className="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Play size={16} />
          {isRunning ? 'Running...' : 'Run Agents'}
        </button>
        
        {isRunning && (
          <button
            onClick={handleStop}
            className="px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors"
          >
            <Square size={16} />
          </button>
        )}
        
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors"
        >
          <Settings size={16} />
        </button>
      </div>

      {showConfig && (
        <div className="space-y-3 p-3 bg-gray-50 rounded-xl">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-1 block">
              Max Depth: {settings.maxDepth}
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={settings.maxDepth}
              onChange={(e) => updateSettings({ maxDepth: Number(e.target.value) })}
              className="w-full"
            />
          </div>
          
          <div>
            <label className="text-sm font-medium text-gray-700 mb-1 block">
              Token Budget: {settings.tokenBudget.toLocaleString()}
            </label>
            <input
              type="range"
              min="1000"
              max="50000"
              step="1000"
              value={settings.tokenBudget}
              onChange={(e) => updateSettings({ tokenBudget: Number(e.target.value) })}
              className="w-full"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default MasterAgentControls;