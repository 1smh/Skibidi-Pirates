import React from 'react';
import useCaseStore from '../store/useCaseStore';
import { Bot, User } from 'lucide-react';

const ChatThread = () => {
  const { messages } = useCaseStore();

  if (messages.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        <Bot size={48} className="mx-auto mb-4 text-gray-300" />
        <p className="text-sm">Start by describing your legal case or uploading documents</p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      {messages.map((message) => (
        <div key={message.id} className="flex gap-3">
          <div className="flex-shrink-0">
            {message.type === 'user' ? (
              <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                <User size={16} />
              </div>
            ) : (
              <div className="w-8 h-8 bg-gray-900 rounded-full flex items-center justify-center">
                <Bot size={16} className="text-white" />
              </div>
            )}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm font-medium text-gray-900">
                {message.type === 'user' ? 'You' : message.agent || 'Assistant'}
              </span>
              <span className="text-xs text-gray-500">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
            
            <div className="bg-gray-50 rounded-2xl p-3 text-sm text-gray-700">
              {message.content}
            </div>
            
            {message.files && message.files.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {message.files.map((file, idx) => (
                  <span key={idx} className="text-xs bg-gray-200 px-2 py-1 rounded-lg">
                    📎 {file.name}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatThread;