from typing import Dict, Any, List
import json
import os
from pathlib import Path
from llm_client import LLMClient
from simulator import simulate_case_outcome
from agents.traffic_ticket import TrafficTicketAgent
from agents.small_claims import SmallClaimsAgent
from agents.landlord_tenant import LandlordTenantAgent

def execute_tasks(tasks: List[Dict[str, Any]], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Execute all planned tasks"""
    
    results = {
        "completed_tasks": [],
        "failed_tasks": [],
        "generated_artifacts": [],
        "deployed_agents": []
    }
    
    for task in tasks:
        try:
            print(f"Executing task: {task.get('title', 'Unknown')}")
            
            task_result = run_task(task, memory, llm_client)
            task["status"] = "completed"
            task["output"] = task_result
            task["progress"] = 100
            
            results["completed_tasks"].append(task)
            
            # Handle agent deployment
            if task.get("type") == "deploy_agent":
                results["deployed_agents"].append(task_result)
                
        except Exception as e:
            print(f"Task failed: {task.get('title')} - {str(e)}")
            task["status"] = "error"
            task["error"] = str(e)
            task["progress"] = 0
            results["failed_tasks"].append(task)
    
    return results

def run_task(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Execute a single task based on its type"""
    
    task_type = task.get("type", "")
    
    if task_type == "analyze_case":
        return analyze_case(task, memory, llm_client)
    elif task_type == "deploy_agent":
        return deploy_agent(task, memory, llm_client)
    elif task_type == "extract_documents":
        return extract_documents(task, memory, llm_client)
    elif task_type == "research_precedent":
        return research_precedent(task, memory, llm_client)
    elif task_type == "draft_documents":
        return draft_documents(task, memory, llm_client)
    elif task_type == "simulate_outcome":
        return simulate_outcome(task, memory, llm_client)
    elif task_type == "schedule_deadlines":
        return schedule_deadlines(task, memory, llm_client)
    else:
        return {"result": "Unknown task type", "status": "skipped"}

def analyze_case(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Analyze the legal case"""
    
    # Get the latest conversation
    conversations = memory.get("conversations", [])
    latest_prompt = conversations[-1].get("prompt", "") if conversations else ""
    
    analysis_prompt = f"""
    Perform a detailed legal case analysis:
    
    Case Description: {latest_prompt}
    Jurisdiction: {memory.get('preferences', {}).get('jurisdiction', 'CA')}
    
    Provide analysis including:
    1. Legal issues identified
    2. Potential claims or defenses
    3. Required evidence
    4. Estimated timeline
    5. Success probability
    """
    
    analysis = llm_client.chat(analysis_prompt)
    
    return {
        "analysis": analysis,
        "legal_issues": ["Issue 1", "Issue 2"],  # Would be extracted from LLM response
        "success_probability": 70,
        "timeline_estimate": "2-4 weeks"
    }

def deploy_agent(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Deploy a specialized agent"""
    
    agent_type = task.get("agent_type", "general")
    
    # Create appropriate agent
    if agent_type == "traffic_ticket":
        agent = TrafficTicketAgent(llm_client)
    elif agent_type == "small_claims":
        agent = SmallClaimsAgent(llm_client)
    elif agent_type == "landlord_tenant":
        agent = LandlordTenantAgent(llm_client)
    else:
        # Default generic agent behavior
        return create_generic_agent_result(task, memory)
    
    # Get case context
    conversations = memory.get("conversations", [])
    case_context = conversations[-1].get("prompt", "") if conversations else ""
    
    # Execute agent workflow
    agent_plan = agent.plan(case_context, memory)
    agent_results = agent.execute(agent_plan, memory)
    agent_summary = agent.summarize(agent_results)
    
    # Create artifacts directory for this agent
    agent_id = task.get("id", "agent")
    artifacts_dir = Path(f"storage/artifacts/{agent_id}")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate sample artifacts
    artifacts = generate_sample_artifacts(agent_type, artifacts_dir, llm_client, case_context)
    
    return {
        "agent_id": agent_id,
        "agent_type": agent_type,
        "agent_name": task.get("agent_name", "Legal Agent"),
        "plan": agent_plan,
        "results": agent_results,
        "summary": agent_summary,
        "artifacts": artifacts,
        "status": "deployed",
        "progress": 25,
        "next_steps": [
            {"title": "Review generated documents", "completed": False, "description": "Check draft documents for accuracy"},
            {"title": "Gather additional evidence", "completed": False, "description": "Collect supporting documentation"},
            {"title": "Prepare for deadlines", "completed": False, "description": "Schedule important dates"}
        ],
        "form_fields": [
            {"label": "Full Name", "type": "text", "value": "", "placeholder": "Enter your full legal name"},
            {"label": "Case Details", "type": "textarea", "value": "", "placeholder": "Additional case information"}
        ]
    }

def create_generic_agent_result(task: Dict[str, Any], memory: Dict[str, Any]) -> Dict[str, Any]:
    """Create a generic agent result when specialized agent isn't available"""
    
    return {
        "agent_id": task.get("id", "generic_agent"),
        "agent_type": task.get("agent_type", "general"),
        "agent_name": task.get("agent_name", "Legal Assistant"),
        "summary": "I'm analyzing your case and preparing recommendations. This may take a few minutes.",
        "status": "running",
        "progress": 25,
        "artifacts": [],
        "next_steps": [
            {"title": "Complete case analysis", "completed": False, "description": "Analyzing legal documents and case details"},
            {"title": "Research precedents", "completed": False, "description": "Finding similar cases and outcomes"},
            {"title": "Draft initial documents", "completed": False, "description": "Preparing legal forms and letters"}
        ]
    }

def extract_documents(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Extract and process uploaded documents"""
    
    # This would process files in storage/artifacts
    artifacts_dir = Path("storage/artifacts")
    processed_files = []
    
    if artifacts_dir.exists():
        for file_path in artifacts_dir.glob("*"):
            if file_path.is_file():
                processed_files.append({
                    "name": file_path.name,
                    "type": file_path.suffix,
                    "size": file_path.stat().st_size
                })
    
    return {
        "processed_files": processed_files,
        "extracted_entities": ["Date: 2024-01-01", "Amount: $500"],
        "key_information": "Important case details extracted from documents"
    }

def research_precedent(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Research legal precedents (stubbed with mock data)"""
    
    return {
        "precedents_found": [
            {"case": "Smith v. Jones", "relevance": 0.85, "outcome": "favorable"},
            {"case": "Doe v. Company", "relevance": 0.72, "outcome": "mixed"}
        ],
        "legal_principles": ["Principle 1", "Principle 2"],
        "recommendations": "Based on precedent research, consider these strategies..."
    }

def draft_documents(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Draft legal documents"""
    
    conversations = memory.get("conversations", [])
    case_context = conversations[-1].get("prompt", "") if conversations else ""
    
    draft_prompt = f"""
    Draft a legal document for this case:
    
    Case: {case_context}
    Document Type: {task.get('document_type', 'General Legal Letter')}
    Jurisdiction: {memory.get('preferences', {}).get('jurisdiction', 'CA')}
    
    Create a professional legal document with proper formatting.
    """
    
    draft_content = llm_client.chat(draft_prompt)
    
    # Save draft to file
    doc_name = f"draft_{task.get('id', 'document')}.txt"
    doc_path = Path(f"storage/artifacts/{doc_name}")
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(doc_path, "w") as f:
        f.write(draft_content)
    
    return {
        "document_name": doc_name,
        "document_path": str(doc_path),
        "content_preview": draft_content[:200] + "..." if len(draft_content) > 200 else draft_content
    }

def simulate_outcome(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Simulate case outcome"""
    
    conversations = memory.get("conversations", [])
    case_context = conversations[-1].get("prompt", "") if conversations else ""
    
    outcome = simulate_case_outcome(case_context, memory)
    
    return {
        "win_probability": outcome.get("win_probability", 65),
        "best_strategy": outcome.get("best_strategy", "Negotiate settlement"),
        "risk_factors": outcome.get("risk_factors", ["Factor 1", "Factor 2"]),
        "estimated_duration": outcome.get("estimated_duration", "2-3 months")
    }

def schedule_deadlines(task: Dict[str, Any], memory: Dict[str, Any], llm_client: LLMClient) -> Dict[str, Any]:
    """Schedule important deadlines"""
    
    from datetime import datetime, timedelta
    
    # Create sample deadlines
    today = datetime.now()
    deadlines = [
        {
            "title": "File Response",
            "date": (today + timedelta(days=30)).isoformat(),
            "priority": "high"
        },
        {
            "title": "Discovery Deadline", 
            "date": (today + timedelta(days=60)).isoformat(),
            "priority": "medium"
        }
    ]
    
    # Generate ICS file
    calendar_content = generate_ics_calendar(deadlines)
    ics_path = Path("storage/artifacts/case_deadlines.ics")
    
    with open(ics_path, "w") as f:
        f.write(calendar_content)
    
    return {
        "deadlines": deadlines,
        "calendar_file": str(ics_path),
        "reminders_set": len(deadlines)
    }

def generate_sample_artifacts(agent_type: str, artifacts_dir: Path, llm_client: LLMClient, case_context: str) -> List[Dict[str, Any]]:
    """Generate sample artifacts for the agent"""
    
    artifacts = []
    
    # Generate a sample legal document
    doc_prompt = f"""
    Create a brief legal document template for a {agent_type} case:
    
    Case Context: {case_context}
    
    Make it professional but concise (under 500 words).
    """
    
    doc_content = llm_client.chat(doc_prompt)
    doc_path = artifacts_dir / f"{agent_type}_document.txt"
    
    with open(doc_path, "w") as f:
        f.write(doc_content)
    
    artifacts.append({
        "name": f"{agent_type}_document.txt",
        "path": str(doc_path.relative_to("storage")),
        "type": "txt",
        "description": f"Generated legal document for {agent_type} case"
    })
    
    return artifacts

def generate_ics_calendar(deadlines: List[Dict[str, Any]]) -> str:
    """Generate ICS calendar content"""
    
    ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Legal Assistant//Case Deadlines//EN
"""
    
    for deadline in deadlines:
        ics_content += f"""BEGIN:VEVENT
SUMMARY:{deadline['title']}
DTSTART:{deadline['date'].replace('-', '').replace(':', '')}Z
PRIORITY:{1 if deadline['priority'] == 'high' else 5}
END:VEVENT
"""
    
    ics_content += "END:VCALENDAR"
    return ics_content