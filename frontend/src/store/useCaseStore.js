import { create } from 'zustand';

const useCaseStore = create((set, get) => ({
  // State
  currentCase: null,
  agents: [],
  timeline: [],
  artifacts: [],
  messages: [],
  isRunning: false,
  settings: {
    budget: 50,
    thoroughness: 75,
    plainEnglish: true,
    jurisdiction: 'CA',
    maxDepth: 5,
    tokenBudget: 10000,
  },
  uploadedFiles: [],
  
  // Actions
  setCurrentCase: (caseData) => set({ currentCase: caseData }),
  
  setAgents: (agents) => set({ agents }),
  
  updateAgent: (agentId, updates) => set((state) => ({
    agents: state.agents.map(agent => 
      agent.id === agentId ? { ...agent, ...updates } : agent
    )
  })),
  
  setTimeline: (timeline) => set({ timeline }),
  
  addTimelineStep: (step) => set((state) => ({
    timeline: [...state.timeline, step]
  })),
  
  updateTimelineStep: (stepId, updates) => set((state) => ({
    timeline: state.timeline.map(step =>
      step.id === stepId ? { ...step, ...updates } : step
    )
  })),
  
  setArtifacts: (artifacts) => set({ artifacts }),
  
  addArtifact: (artifact) => set((state) => ({
    artifacts: [...state.artifacts, artifact]
  })),
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      ...message
    }]
  })),
  
  setIsRunning: (isRunning) => set({ isRunning }),
  
  updateSettings: (newSettings) => set((state) => ({
    settings: { ...state.settings, ...newSettings }
  })),
  
  addUploadedFile: (file) => set((state) => ({
    uploadedFiles: [...state.uploadedFiles, file]
  })),
  
  removeUploadedFile: (fileId) => set((state) => ({
    uploadedFiles: state.uploadedFiles.filter(f => f.id !== fileId)
  })),
  
  reset: () => set({
    currentCase: null,
    agents: [],
    timeline: [],
    artifacts: [],
    messages: [],
    isRunning: false,
    uploadedFiles: [],
  }),
}));

export default useCaseStore;