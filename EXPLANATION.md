# Technical Design Explanation

## Design Choices

### 1. Local-First Privacy
- All user data, artifacts, and memory are stored locally in JSON files.
- No external database or cloud storage is used; only LLM API calls leave the machine.

### 2. Modular Agent Architecture
- Agents are implemented as Python classes inheriting from a common BaseAgent.
- Each agent specializes in a legal domain (traffic, small claims, landlord-tenant).
- New agents can be added by subclassing and registering in the executor.

### 3. FastAPI Backend
- Chosen for its speed, async support, and easy OpenAPI docs.
- Handles agent orchestration, file uploads, and case management.

### 4. React Frontend
- Modern, responsive UI with Zustand for state management.
- Split-pane layout for chat and agent results.
- File upload and settings controls for user flexibility.

### 5. LLM Integration
- Gemini API is used for planning, analysis, and document generation.
- LLM responses are parsed and structured for agent workflows.

### 6. Document Intelligence
- PDF and image uploads are processed with tesseract and pdfplumber.
- Extracted text is used in agent analysis and document drafting.

### 7. DevOps & Testing
- Docker and Conda support for reproducible environments.
- CI workflow runs a smoke test to verify core backend functionality.

## Why This Structure?
- **Separation of concerns:** Frontend, backend, and agent logic are clearly separated.
- **Extensibility:** New legal domains or agent types can be added with minimal changes.
- **User privacy:** No sensitive data leaves the user's machine except for LLM queries.
- **Hackathon-ready:** Easy to test, demo, and deploy with Docker or Conda.
