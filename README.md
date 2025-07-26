# Agentic Legal Assistant

A complete local-only AI legal assistant that dynamically spawns specialized agents to help with various legal cases. Features a modern React frontend with a Python FastAPI backend, all running locally with JSON-based storage.

## Features

### Core Functionality
- **Master Agent System**: Dynamically deploys specialized sub-agents for different legal areas
- **Specialized Agents**: Traffic Tickets, Small Claims, Landlord-Tenant disputes, and more
- **Local Storage**: Everything runs locally using JSON files - no external databases
- **Document Processing**: Upload and OCR legal documents (PDFs, images)
- **Timeline Visualization**: Track agent progress and execution steps
- **Artifact Generation**: Automatically create legal documents, calendars, and forms

### User Interface
- **Split-Pane Design**: Chat interface on left, agent results on right
- **Responsive Layout**: Works on desktop and mobile devices
- **Real-time Updates**: Live agent status and progress monitoring
- **Document Management**: Drag-and-drop file uploads with text extraction
- **Settings Control**: Adjust budget, thoroughness, and jurisdiction preferences

### Privacy & Security
- **API Key Management**: User provides their own Gemini API key
- **Local Processing**: No data leaves your machine except for LLM API calls
- **No Tracking**: Zero telemetry or usage tracking

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and setup**:
```bash
git clone <repository>
cd agentic-lawyer
```

2. **Configure environment**:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your GEMINI_API_KEY
```

3. **Start with Docker**:
```bash
docker-compose up -d
```

4. **Access the application**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Installation

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage

### Getting Started
1. **Add API Key**: Open the Settings accordion and enter your Gemini API key
2. **Describe Your Case**: Type your legal situation in the chat
3. **Upload Documents**: Drag and drop relevant files (tickets, contracts, etc.)
4. **Review Agent Results**: Monitor specialized agents as they analyze your case
5. **Download Artifacts**: Get generated legal documents and calendars

### Supported Case Types
- **Traffic Tickets**: Speeding, parking, moving violations
- **Small Claims Court**: Contract disputes, property damage, unpaid debts
- **Landlord-Tenant**: Security deposits, habitability issues, evictions
- **Contract Disputes**: Breach of contract, service agreements
- **Employment Issues**: Wage disputes, workplace violations
- **Personal Injury**: Basic injury claims and documentation

### Agent Capabilities
Each specialized agent can:
- Analyze case documents and facts
- Research relevant laws and precedents
- Draft legal documents and forms
- Calculate damages and success probability
- Generate deadlines and calendar reminders
- Provide step-by-step action plans

## Architecture

### Frontend (React + Tailwind)
- **Components**: Modular UI components for chat, timeline, and agent results
- **State Management**: Zustand for global state management
- **API Client**: Axios for backend communication
- **Styling**: Tailwind CSS with grayscale design system

### Backend (FastAPI + Python)
- **API Endpoints**: RESTful API for agent management and file processing
- **Agent System**: Base agent class with specialized implementations
- **LLM Integration**: Gemini API client with structured response parsing
- **Document Processing**: PDF text extraction and OCR capabilities
- **Local Storage**: JSON-based memory and artifact management

### File Structure
```
agentic-lawyer/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── store/          # State management
│   │   └── styles/         # CSS styles
├── backend/                 # FastAPI application
│   ├── agents/             # Specialized agent implementations
│   ├── storage/            # Local JSON storage and artifacts
│   ├── app.py              # Main FastAPI app
│   ├── planner.py          # Task planning logic
│   ├── executor.py         # Task execution engine
│   └── llm_client.py       # Gemini API client
└── docker-compose.yml      # Container orchestration
```

## Configuration

### Environment Variables
```bash
# Backend (.env)
GEMINI_API_KEY=your_api_key_here
ENVIRONMENT=development

# Frontend (localStorage)
gemini_api_key=your_api_key_here  # Set via UI
```

### Settings
- **Budget vs Thoroughness**: Slider to balance speed vs. depth of analysis
- **Plain English Mode**: Toggle between legal terminology and plain language
- **Jurisdiction**: Select your state/region for applicable laws
- **Agent Limits**: Configure maximum agent depth and token usage

## Development

### Adding New Agents
1. Create a new agent class in `backend/agents/`
2. Inherit from `BaseAgent` and implement required methods
3. Register the agent in `executor.py`
4. Update the planner to recognize relevant case types

### Extending Document Types
1. Add support in `upload_file` endpoint for new file types
2. Implement extraction logic in `executor.py`
3. Update frontend dropzone to accept new formats

### Customizing UI
1. Modify Tailwind classes in components
2. Update color palette in `tailwind.config.js`
3. Add new components in `frontend/src/components/`

## API Reference

### Key Endpoints

#### POST /api/agent
Deploy and run agents for a legal case
```json
{
  "user_id": "string",
  "prompt": "string", 
  "files": ["file_id1", "file_id2"]
}
```

#### POST /api/upload
Upload and process legal documents
- Supports PDF, image, and text files
- Returns extracted text and file ID

#### GET /api/case/{case_id}
Retrieve saved case information and history

#### POST /api/approve-step
Approve or reject agent execution steps
```json
{
  "step_id": "string",
  "decision": "approve|reject"
}
```

### Response Format
All agent responses include:
- **agents**: Array of deployed agent objects
- **timeline**: Execution steps and progress
- **artifacts**: Generated documents and files
- **summary**: Human-readable case summary

## Security Considerations

### API Key Handling
- Keys stored locally in browser storage
- Transmitted via secure headers to backend
- Never logged or persisted server-side

### Data Privacy
- All case data stored locally in JSON files
- No external database connections
- LLM calls only include necessary case context

### File Security
- Uploaded files stored in local storage directory
- OCR processing happens locally
- Generated artifacts remain on local filesystem

## Troubleshooting

### Common Issues

**"No API key provided" error**:
- Ensure you've entered your Gemini API key in Settings
- Check that the key is valid and active

**File upload failures**:
- Verify file size is under limits
- Check that required system dependencies are installed (tesseract, poppler)

**Agent timeouts**:
- Reduce token budget in Master Agent Controls
- Check API key rate limits

**UI not loading**:
- Ensure both frontend and backend are running
- Check CORS configuration in backend

### Getting Help
- Check API documentation at `/docs` endpoint
- Review browser console for frontend errors
- Check backend logs for API issues

## License

This project is provided as-is for educational and personal use. Please ensure compliance with all applicable laws and regulations when using this tool for legal matters.

## Disclaimer

This AI legal assistant is for informational purposes only and does not constitute legal advice. Always consult with a qualified attorney for legal matters. The accuracy and completeness of AI-generated legal information cannot be guaranteed.