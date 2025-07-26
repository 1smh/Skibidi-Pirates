import React, { useState } from 'react';
import { ChevronDown, Settings, Key } from 'lucide-react';
import useCaseStore from '../store/useCaseStore';

const SettingsAccordion = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '');
  const { settings, updateSettings } = useCaseStore();

  const handleApiKeyChange = (value) => {
    setApiKey(value);
    localStorage.setItem('gemini_api_key', value);
  };

  const jurisdictions = [
    { value: 'CA', label: 'California' },
    { value: 'NY', label: 'New York' },
    { value: 'TX', label: 'Texas' },
    { value: 'FL', label: 'Florida' },
  ];

  return (
    <div className="border-b border-gray-200">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between text-left hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Settings size={20} className="text-gray-400" />
          <span className="text-sm font-medium text-gray-900">Settings</span>
        </div>
        <ChevronDown 
          size={16} 
          className={`text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
        />
      </button>

      {isOpen && (
        <div className="p-4 space-y-4 bg-gray-50">
          {/* API Key */}
          <div>
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
              <Key size={16} />
              Gemini API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => handleApiKeyChange(e.target.value)}
              placeholder="Enter your Gemini API key"
              className="w-full input text-sm"
            />
          </div>

          {/* Budget vs Thoroughness */}
          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">
              Budget vs Thoroughness
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={settings.budget}
              onChange={(e) => updateSettings({ budget: Number(e.target.value) })}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Fast & Cheap</span>
              <span>Thorough & Expensive</span>
            </div>
          </div>

          {/* Plain English Toggle */}
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-gray-700">Plain English</label>
            <button
              onClick={() => updateSettings({ plainEnglish: !settings.plainEnglish })}
              className={`
                relative w-12 h-6 rounded-full transition-colors
                ${settings.plainEnglish ? 'bg-gray-900' : 'bg-gray-300'}
              `}
            >
              <div className={`
                absolute top-1 w-4 h-4 bg-white rounded-full transition-transform
                ${settings.plainEnglish ? 'translate-x-7' : 'translate-x-1'}
              `} />
            </button>
          </div>

          {/* Jurisdiction */}
          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">
              Jurisdiction
            </label>
            <select
              value={settings.jurisdiction}
              onChange={(e) => updateSettings({ jurisdiction: e.target.value })}
              className="w-full input text-sm"
            >
              {jurisdictions.map((j) => (
                <option key={j.value} value={j.value}>{j.label}</option>
              ))}
            </select>
          </div>
        </div>
      )}
    </div>
  );
};

export default SettingsAccordion;