import React, { useState } from 'react';
import { Send, Paperclip } from 'lucide-react';
import useCaseStore from '../store/useCaseStore';
import { agentAPI } from '../api';

const ChatComposer = () => {
  const [message, setMessage] = useState('');
  const { addMessage, setIsRunning, uploadedFiles, setAgents, setTimeline, setArtifacts } = useCaseStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Add user message
    addMessage({
      type: 'user',
      content: message,
      files: uploadedFiles.map(f => ({ name: f.name, id: f.id }))
    });

    const userMessage = message;
    setMessage('');
    setIsRunning(true);

    try {
      // Call agent API
      const response = await agentAPI.runAgent({
        user_id: 'default_user',
        prompt: userMessage,
        files: uploadedFiles.map(f => f.id)
      });

      // Update store with results
      setAgents(response.data.agents || []);
      setTimeline(response.data.timeline || []);
      setArtifacts(response.data.artifacts || []);

      // Add assistant response
      addMessage({
        type: 'assistant',
        agent: 'Master Agent',
        content: response.data.summary || 'I\'ve analyzed your case and deployed specialized agents to help you.'
      });

    } catch (error) {
      console.error('Error running agent:', error);
      addMessage({
        type: 'assistant',
        agent: 'System',
        content: 'Sorry, I encountered an error processing your request. Please check your API key and try again.'
      });
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="relative">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Describe your legal situation..."
          className="w-full input resize-none min-h-[80px] pr-12"
          rows={3}
        />
        
        <div className="absolute bottom-3 right-3 flex gap-2">
          <button
            type="button"
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <Paperclip size={16} />
          </button>
          
          <button
            type="submit"
            disabled={!message.trim()}
            className="p-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
      
      {uploadedFiles.length > 0 && (
        <div className="text-xs text-gray-500">
          {uploadedFiles.length} file(s) attached
        </div>
      )}
    </form>
  );
};

export default ChatComposer;