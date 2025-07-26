from fastapi import FastAPI, HTTPException, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
import logging
from pathlib import Path

from planner import plan_tasks
from executor import execute_tasks
from memory import load_memory, save_memory
from llm_client import LLMClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agentic Legal Assistant API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure storage directories exist
os.makedirs("storage/artifacts", exist_ok=True)
os.makedirs("storage/logs", exist_ok=True)

# Request models
class AgentRequest(BaseModel):
    user_id: str
    prompt: str
    files: Optional[List[str]] = []

class ApproveStepRequest(BaseModel):
    step_id: str
    decision: str

# Response models
class AgentResponse(BaseModel):
    agents: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    artifacts: List[Dict[str, Any]]
    summary: str

@app.post("/api/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest, x_api_key: Optional[str] = Header(None)):
    """Main endpoint to run the agentic legal assistant"""
    try:
        # Initialize LLM client with API key from header or env
        api_key = x_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=400, detail="No API key provided")
        
        llm_client = LLMClient(api_key)
        
        # Load user memory
        memory = load_memory(request.user_id)
        
        # Add current prompt to memory
        memory.setdefault("conversations", []).append({
            "prompt": request.prompt,
            "files": request.files,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        # Plan tasks
        logger.info(f"Planning tasks for user {request.user_id}")
        tasks = plan_tasks(request.prompt, memory, llm_client)
        
        # Execute tasks
        logger.info(f"Executing {len(tasks)} tasks")
        results = execute_tasks(tasks, memory, llm_client)
        
        # Save updated memory
        save_memory(request.user_id, memory)
        
        # Create response
        agents = []
        timeline = []
        artifacts = []
        
        # Process results to create agents
        for task in tasks:
            if task.get("type") == "deploy_agent":
                agent = {
                    "id": task.get("id", f"agent_{len(agents)}"),
                    "name": task.get("agent_name", "Legal Agent"),
                    "type": task.get("agent_type", "general"),
                    "status": task.get("status", "running"),
                    "progress": task.get("progress", 25),
                    "winPercentage": task.get("win_percentage", 65),
                    "stepsRemaining": task.get("steps_remaining", 3),
                    "formsCompleted": task.get("forms_completed", 1),
                    "contactsNeeded": task.get("contacts_needed", 2),
                    "summary": task.get("summary", "Analyzing your case and preparing documents..."),
                    "lastUpdate": "Working on document analysis...",
                    "artifacts": task.get("artifacts", []),
                    "formFields": task.get("form_fields", []),
                    "nextSteps": task.get("next_steps", [])
                }
                agents.append(agent)
        
        # Create timeline from tasks
        for i, task in enumerate(tasks):
            timeline_step = {
                "id": f"step_{i}",
                "title": task.get("title", f"Step {i+1}"),
                "description": task.get("description", "Processing..."),
                "type": task.get("type", "general"),
                "status": task.get("status", "running" if i == 0 else "waiting"),
                "agent": task.get("agent", "Master Agent"),
                "progress": task.get("progress", 0),
                "input": task.get("input", {}),
                "output": task.get("output", {}),
                "logs": task.get("logs", [])
            }
            timeline.append(timeline_step)
        
        # Create artifacts list
        artifacts_dir = Path("storage/artifacts")
        if artifacts_dir.exists():
            for artifact_file in artifacts_dir.rglob("*"):
                if artifact_file.is_file():
                    artifacts.append({
                        "name": artifact_file.name,
                        "path": str(artifact_file.relative_to("storage")),
                        "type": artifact_file.suffix[1:] if artifact_file.suffix else "unknown",
                        "size": artifact_file.stat().st_size
                    })
        
        return AgentResponse(
            agents=agents,
            timeline=timeline,
            artifacts=artifacts,
            summary="I've analyzed your legal case and deployed specialized agents to assist you. Review the agent results and timeline for detailed progress."
        )
        
    except Exception as e:
        logger.error(f"Error processing agent request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process files (OCR for PDFs/images)"""
    try:
        # Create unique file ID
        file_id = f"file_{len(os.listdir('storage/artifacts')) + 1}"
        file_path = f"storage/artifacts/{file_id}_{file.filename}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text based on file type
        extracted_text = ""
        if file.content_type == "application/pdf":
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    extracted_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            except Exception as e:
                logger.warning(f"Could not extract text from PDF: {e}")
                extracted_text = "PDF uploaded but text extraction failed"
        
        elif file.content_type.startswith("image/"):
            try:
                import pytesseract
                from PIL import Image
                image = Image.open(file_path)
                extracted_text = pytesseract.image_to_string(image)
            except Exception as e:
                logger.warning(f"Could not perform OCR on image: {e}")
                extracted_text = "Image uploaded but OCR failed"
        
        elif file.content_type.startswith("text/"):
            with open(file_path, "r", encoding="utf-8") as f:
                extracted_text = f.read()
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "extracted_text": extracted_text
        }
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/case/{case_id}")
async def get_case(case_id: str):
    """Get case information"""
    try:
        memory = load_memory(case_id)
        return {"case_id": case_id, "memory": memory}
    except Exception as e:
        logger.error(f"Error getting case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/approve-step")
async def approve_step(request: ApproveStepRequest):
    """Approve or reject a step in the process"""
    try:
        # Log the decision
        logger.info(f"Step {request.step_id} decision: {request.decision}")
        
        # Here you would update the step status in your memory/database
        # For now, just return success
        return {"status": "success", "message": f"Step {request.step_id} {request.decision}"}
        
    except Exception as e:
        logger.error(f"Error approving step: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/artifact/{path:path}")
async def get_artifact(path: str):
    """Download an artifact file"""
    try:
        file_path = f"storage/{path}"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Artifact not found")
        
        return FileResponse(file_path)
        
    except Exception as e:
        logger.error(f"Error getting artifact: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Agentic Legal Assistant API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)