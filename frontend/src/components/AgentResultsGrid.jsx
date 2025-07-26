import React from 'react';
import AgentCard from './AgentCard';
import useCaseStore from '../store/useCaseStore';
import { Bot } from 'lucide-react';

const AgentResultsGrid = ({ onSelectAgent }) => {
  const { agents } = useCaseStore();

  if (agents.length === 0) {
    return (
      <div className="text-center text-gray-500 py-12">
        <Bot size={48} className="mx-auto mb-4 text-gray-300" />
        <p>No agents deployed yet</p>
        <p className="text-sm mt-1">Start a conversation to deploy specialized agents</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {agents.map((agent) => (
        <AgentCard
          key={agent.id}
          agent={agent}
          onClick={() => onSelectAgent(agent)}
        />
      ))}
    </div>
  );
};

export default AgentResultsGrid;