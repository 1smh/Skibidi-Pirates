import React, { useState } from 'react';
import ChatThread from './components/ChatThread';
import ChatComposer from './components/ChatComposer';
import FileDropzone from './components/FileDropzone';
import SettingsAccordion from './components/SettingsAccordion';
import MasterAgentControls from './components/MasterAgentControls';
import AgentResultsGrid from './components/AgentResultsGrid';
import TimelineView from './components/TimelineView';
import DetailDrawer from './components/DetailDrawer';
import Toaster from './components/Toaster';
import { Menu, X } from 'lucide-react';

function App() {
  const [leftPaneOpen, setLeftPaneOpen] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      <Toaster />
      
      {/* Mobile menu button */}
      <div className="sm:hidden fixed top-4 left-4 z-50">
        <button
          onClick={() => setLeftPaneOpen(!leftPaneOpen)}
          className="p-2 bg-white rounded-xl shadow-sm border border-gray-200"
        >
          {leftPaneOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Left Pane */}
      <div className={`
        ${leftPaneOpen ? 'translate-x-0' : '-translate-x-full'}
        sm:translate-x-0 transition-transform duration-300 ease-in-out
        fixed sm:relative z-40 sm:z-auto
        w-full sm:w-96 h-full bg-white border-r border-gray-200
        flex flex-col
      `}>
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-xl font-semibold text-gray-900">Legal Assistant</h1>
          <p className="text-sm text-gray-600 mt-1">AI-powered legal case management</p>
        </div>
        
        <div className="flex-1 overflow-hidden flex flex-col">
          <div className="flex-1 overflow-y-auto">
            <ChatThread />
          </div>
          
          <div className="p-4 border-t border-gray-100">
            <ChatComposer />
          </div>
        </div>
        
        <div className="border-t border-gray-200">
          <FileDropzone />
          <SettingsAccordion />
          <MasterAgentControls />
        </div>
      </div>

      {/* Mobile overlay */}
      {leftPaneOpen && (
        <div 
          className="sm:hidden fixed inset-0 bg-black bg-opacity-25 z-30"
          onClick={() => setLeftPaneOpen(false)}
        />
      )}

      {/* Right Pane */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Agent Results</h2>
          <p className="text-sm text-gray-600 mt-1">Monitor agent progress and outcomes</p>
        </div>
        
        <div className="flex-1 overflow-hidden flex flex-col">
          <div className="flex-1 min-h-0 max-h-[50vh] overflow-y-auto p-6">
            <AgentResultsGrid onSelectAgent={setSelectedAgent} />
          </div>
          
          <div className="border-t border-gray-200 p-6 max-h-[50vh] overflow-y-auto">
            <TimelineView />
          </div>
        </div>
      </div>

      {/* Detail Drawer */}
      <DetailDrawer 
        agent={selectedAgent} 
        onClose={() => setSelectedAgent(null)}
      />
    </div>
  );
}

export default App;