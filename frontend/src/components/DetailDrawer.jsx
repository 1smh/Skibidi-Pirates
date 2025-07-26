import React from 'react';
import { X, Download, Check, AlertTriangle } from 'lucide-react';
import { agentAPI } from '../api';

const DetailDrawer = ({ agent, onClose }) => {
  if (!agent) return null;

  const handleDownloadArtifact = async (artifact) => {
    try {
      const response = await agentAPI.getArtifact(artifact.path);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', artifact.name);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading artifact:', error);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-white border-l border-gray-200 shadow-xl z-50 overflow-hidden flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">{agent.name}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={20} />
          </button>
        </div>
        <p className="text-sm text-gray-600 mt-1">{agent.type}</p>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="p-6 space-y-6">
          {/* Status */}
          <div>
            <h3 className="font-medium text-gray-900 mb-3">Status</h3>
            <div className="bg-gray-50 rounded-xl p-4">
              <p className="text-sm text-gray-700">{agent.summary || 'Processing your legal case...'}</p>
            </div>
          </div>

          {/* Progress */}
          <div>
            <h3 className="font-medium text-gray-900 mb-3">Progress</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span>Overall Progress</span>
                <span>{agent.progress || 0}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-gray-900 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${agent.progress || 0}%` }}
                />
              </div>
            </div>
          </div>

          {/* Artifacts */}
          {agent.artifacts && agent.artifacts.length > 0 && (
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Generated Documents</h3>
              <div className="space-y-2">
                {agent.artifacts.map((artifact, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                    <div>
                      <div className="font-medium text-sm">{artifact.name}</div>
                      <div className="text-xs text-gray-500">{artifact.type}</div>
                    </div>
                    <button
                      onClick={() => handleDownloadArtifact(artifact)}
                      className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      <Download size={16} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Form Fields */}
          {agent.formFields && agent.formFields.length > 0 && (
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Required Information</h3>
              <div className="space-y-3">
                {agent.formFields.map((field, idx) => (
                  <div key={idx}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {field.label}
                    </label>
                    {field.type === 'text' && (
                      <input
                        type="text"
                        value={field.value || ''}
                        placeholder={field.placeholder}
                        className="w-full input text-sm"
                        readOnly={field.readonly}
                      />
                    )}
                    {field.type === 'textarea' && (
                      <textarea
                        value={field.value || ''}
                        placeholder={field.placeholder}
                        className="w-full input text-sm min-h-[80px]"
                        readOnly={field.readonly}
                      />
                    )}
                    {field.type === 'select' && (
                      <select className="w-full input text-sm">
                        {field.options?.map((option, optIdx) => (
                          <option key={optIdx} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Next Steps */}
          {agent.nextSteps && agent.nextSteps.length > 0 && (
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Next Steps</h3>
              <div className="space-y-2">
                {agent.nextSteps.map((step, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-xl">
                    <div className="mt-0.5">
                      {step.completed ? (
                        <Check size={16} className="text-green-600" />
                      ) : (
                        <AlertTriangle size={16} className="text-yellow-600" />
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium">{step.title}</div>
                      <div className="text-xs text-gray-600 mt-1">{step.description}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="p-6 border-t border-gray-200">
        <div className="flex gap-3">
          <button className="flex-1 btn-primary">
            Approve & Continue
          </button>
          <button className="flex-1 btn-secondary">
            Modify
          </button>
        </div>
      </div>
    </div>
  );
};

export default DetailDrawer;