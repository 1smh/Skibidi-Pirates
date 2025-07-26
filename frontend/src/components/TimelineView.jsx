import React, { useState } from 'react';
import { List, BarChart3, Clock, CheckCircle, AlertCircle, Eye } from 'lucide-react';
import useCaseStore from '../store/useCaseStore';

const TimelineView = () => {
  const [viewMode, setViewMode] = useState('stepper'); // stepper | gantt
  const [selectedStep, setSelectedStep] = useState(null);
  const { timeline } = useCaseStore();

  const getStepIcon = (type) => {
    switch (type) {
      case 'ocr':
        return '📄';
      case 'rag':
        return '🔍';
      case 'draft':
        return '✏️';
      case 'simulate':
        return '⚖️';
      default:
        return '🤖';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle size={16} className="text-green-600" />;
      case 'running':
        return <Clock size={16} className="text-yellow-600 animate-spin" />;
      case 'blocked':
        return <AlertCircle size={16} className="text-red-600" />;
      default:
        return <Clock size={16} className="text-gray-400" />;
    }
  };

  if (timeline.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        <Clock size={32} className="mx-auto mb-2 text-gray-300" />
        <p className="text-sm">No timeline steps yet</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-semibold text-gray-900">Execution Timeline</h3>
        
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('stepper')}
            className={`px-3 py-1 rounded-lg text-sm transition-colors ${
              viewMode === 'stepper' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <List size={16} className="inline mr-1" />
            Steps
          </button>
          <button
            onClick={() => setViewMode('gantt')}
            className={`px-3 py-1 rounded-lg text-sm transition-colors ${
              viewMode === 'gantt' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <BarChart3 size={16} className="inline mr-1" />
            Gantt
          </button>
        </div>
      </div>

      {viewMode === 'stepper' ? (
        <div className="space-y-4">
          {timeline.map((step, index) => (
            <div key={step.id} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="w-8 h-8 bg-white border-2 border-gray-300 rounded-full flex items-center justify-center text-sm">
                  {getStepIcon(step.type)}
                </div>
                {index < timeline.length - 1 && (
                  <div className="w-0.5 h-8 bg-gray-200 mt-2" />
                )}
              </div>
              
              <div className="flex-1 pb-8">
                <div className="flex items-center gap-3 mb-2">
                  <h4 className="font-medium text-gray-900">{step.title}</h4>
                  {getStatusIcon(step.status)}
                  <button
                    onClick={() => setSelectedStep(step)}
                    className="text-gray-400 hover:text-gray-600 transition-colors"
                  >
                    <Eye size={16} />
                  </button>
                </div>
                
                <p className="text-sm text-gray-600 mb-2">{step.description}</p>
                
                {step.agent && (
                  <span className="text-xs bg-gray-100 px-2 py-1 rounded-lg">
                    {step.agent}
                  </span>
                )}
                
                {step.duration && (
                  <span className="text-xs text-gray-500 ml-2">
                    {step.duration}ms
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {timeline.map((step) => (
            <div key={step.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
              <div className="text-lg">{getStepIcon(step.type)}</div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-sm">{step.title}</span>
                  {getStatusIcon(step.status)}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-gray-900 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${step.progress || 0}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Step Detail Modal */}
      {selectedStep && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">{selectedStep.title}</h3>
              <button
                onClick={() => setSelectedStep(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Input</h4>
                <pre className="bg-gray-50 p-3 rounded-xl text-sm overflow-x-auto">
                  {JSON.stringify(selectedStep.input, null, 2)}
                </pre>
              </div>
              
              <div>
                <h4 className="font-medium mb-2">Output</h4>
                <pre className="bg-gray-50 p-3 rounded-xl text-sm overflow-x-auto">
                  {JSON.stringify(selectedStep.output, null, 2)}
                </pre>
              </div>
              
              {selectedStep.logs && (
                <div>
                  <h4 className="font-medium mb-2">Logs</h4>
                  <div className="bg-gray-900 text-green-400 p-3 rounded-xl text-sm font-mono">
                    {selectedStep.logs.map((log, idx) => (
                      <div key={idx}>{log}</div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TimelineView;