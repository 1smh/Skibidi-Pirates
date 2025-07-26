import React from 'react';
import { ChevronRight, Clock, CheckCircle, AlertCircle, Users, FileText, TrendingUp } from 'lucide-react';

const AgentCard = ({ agent, onClick }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle size={16} className="text-green-600" />;
      case 'running':
        return <Clock size={16} className="text-yellow-600" />;
      case 'error':
        return <AlertCircle size={16} className="text-red-600" />;
      default:
        return <Clock size={16} className="text-gray-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'running':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div 
      className="card p-6 hover:shadow-md transition-shadow cursor-pointer"
      onClick={onClick}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-semibold text-gray-900 mb-1">{agent.name}</h3>
          <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium ${getStatusColor(agent.status)}`}>
            {getStatusIcon(agent.status)}
            {agent.status}
          </div>
        </div>
        <ChevronRight size={20} className="text-gray-400" />
      </div>

      <div className="space-y-3">
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <TrendingUp size={16} className="text-gray-400" />
            <div>
              <div className="text-sm font-medium text-gray-900">{agent.winPercentage || 0}%</div>
              <div className="text-xs text-gray-500">Win Rate</div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Clock size={16} className="text-gray-400" />
            <div>
              <div className="text-sm font-medium text-gray-900">{agent.stepsRemaining || 0}</div>
              <div className="text-xs text-gray-500">Steps Left</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <FileText size={16} className="text-gray-400" />
            <div>
              <div className="text-sm font-medium text-gray-900">{agent.formsCompleted || 0}</div>
              <div className="text-xs text-gray-500">Forms Done</div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Users size={16} className="text-gray-400" />
            <div>
              <div className="text-sm font-medium text-gray-900">{agent.contactsNeeded || 0}</div>
              <div className="text-xs text-gray-500">Contacts</div>
            </div>
          </div>
        </div>
      </div>

      {agent.lastUpdate && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <p className="text-xs text-gray-500">{agent.lastUpdate}</p>
        </div>
      )}
    </div>
  );
};

export default AgentCard;