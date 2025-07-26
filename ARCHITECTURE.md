# Agentic Legal Assistant - Architecture

## High-Level Diagram

```
[ User ]
   |
   v
[ React Frontend ] <----> [ FastAPI Backend ] <----> [ Gemini LLM API ]
   |                           |
   |                           v
   |                  [ Specialized Agents ]
   |                           |
   |                           v
   |                  [ Local JSON Storage ]
   |                           |
   |                           v
   |                  [ Document Processing (OCR, PDF) ]
```

## Component Breakdown

- **Frontend (React + Zustand + Tailwind)**
  - Chat interface, agent results, timeline, file upload, settings
  - State managed with Zustand
  - Communicates with backend via REST API

- **Backend (FastAPI + Python)**
  - API endpoints for agent orchestration, file upload, case management
  - Task planner and executor for agent workflow
  - LLM client for Gemini API integration
  - Specialized agents for legal domains (traffic, small claims, landlord-tenant)
  - Local JSON storage for user data and artifacts
  - Document processing with OCR (tesseract, pdfplumber)

- **Agents**
  - BaseAgent: Abstract class for agent logic
  - TrafficTicketAgent, SmallClaimsAgent, LandlordTenantAgent: Specialized implementations

- **Storage**
  - All user data and artifacts stored locally in JSON and file system

- **Deployment**
  - Docker and Conda support
  - CI workflow for smoke testing
