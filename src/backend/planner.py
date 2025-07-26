from typing import Dict, Any, List
from llm_client import LLMClient

def plan_tasks(prompt: str, memory: Dict[str, Any], llm_client: LLMClient) -> List[Dict[str, Any]]:
    """Plan tasks based on user prompt and memory"""
    
    # Determine case type and create appropriate plan
    case_type = determine_case_type(prompt, llm_client)
    
    # Get case-specific planning
    planning_prompt = f"""
    Analyze this legal case and create a detailed execution plan:
    
    User Request: {prompt}
    Case Type: {case_type}
    Past Cases: {len(memory.get('past_cases', []))}
    User Jurisdiction: {memory.get('preferences', {}).get('jurisdiction', 'CA')}
    
    Create a plan with these task types:
    1. analyze_case - Initial case analysis
    2. deploy_agent - Deploy specialized agents 
    3. extract_documents - Process uploaded documents
    4. research_precedent - Research similar cases
    5. draft_documents - Create legal documents
    6. simulate_outcome - Predict case outcomes
    7. schedule_deadlines - Set important dates
    
    For each deploy_agent task, specify:
    - agent_type: traffic_ticket, small_claims, landlord_tenant, etc.
    - agent_name: Human readable name
    - expected_outcome: What the agent should accomplish
    - win_percentage: Estimated success rate
    - forms_needed: List of forms to complete
    - contacts_needed: People/entities to contact
    """
    
    schema = {
        "tasks": [
            {
                "id": "string",
                "type": "string", 
                "title": "string",
                "description": "string",
                "agent_type": "string",
                "agent_name": "string",
                "priority": "integer",
                "estimated_duration": "integer",
                "dependencies": ["string"],
                "win_percentage": "integer",
                "forms_completed": "integer",
                "contacts_needed": "integer",
                "steps_remaining": "integer"
            }
        ]
    }
    
    response = llm_client.structured_chat(planning_prompt, schema)
    tasks = response.get("tasks", [])
    
    # Add default tasks if none generated
    if not tasks:
        tasks = create_default_plan(case_type, prompt)
    
    return tasks

def determine_case_type(prompt: str, llm_client: LLMClient) -> str:
    """Determine the type of legal case from the prompt"""
    
    analysis_prompt = f"""
    Analyze this legal request and determine the case type:
    
    "{prompt}"
    
    Choose the most appropriate case type from:
    - traffic_ticket
    - small_claims  
    - landlord_tenant
    - contract_dispute
    - employment
    - personal_injury
    - family_law
    - immigration
    - criminal_defense
    - general_legal
    
    Return just the case type, nothing else.
    """
    
    case_type = llm_client.chat(analysis_prompt).strip().lower()
    
    # Validate case type
    valid_types = [
        "traffic_ticket", "small_claims", "landlord_tenant", 
        "contract_dispute", "employment", "personal_injury",
        "family_law", "immigration", "criminal_defense", "general_legal"
    ]
    
    if case_type not in valid_types:
        case_type = "general_legal"
    
    return case_type

def create_default_plan(case_type: str, prompt: str) -> List[Dict[str, Any]]:
    """Create a default plan when LLM planning fails"""
    
    plans = {
        "traffic_ticket": [
            {
                "id": "analyze_ticket",
                "type": "analyze_case",
                "title": "Analyze Traffic Ticket",
                "description": "Review ticket details and identify potential defenses",
                "priority": 1,
                "estimated_duration": 300,
                "dependencies": []
            },
            {
                "id": "deploy_traffic_agent", 
                "type": "deploy_agent",
                "title": "Deploy Traffic Ticket Agent",
                "description": "Specialized agent for traffic violations",
                "agent_type": "traffic_ticket",
                "agent_name": "Traffic Defense Agent",
                "priority": 2,
                "estimated_duration": 1800,
                "dependencies": ["analyze_ticket"],
                "win_percentage": 75,
                "forms_completed": 0,
                "contacts_needed": 2,
                "steps_remaining": 4
            }
        ],
        "small_claims": [
            {
                "id": "analyze_claim",
                "type": "analyze_case", 
                "title": "Analyze Small Claims Case",
                "description": "Review claim details and evidence",
                "priority": 1,
                "estimated_duration": 600,
                "dependencies": []
            },
            {
                "id": "deploy_claims_agent",
                "type": "deploy_agent",
                "title": "Deploy Small Claims Agent", 
                "description": "Specialized agent for small claims court",
                "agent_type": "small_claims",
                "agent_name": "Small Claims Specialist",
                "priority": 2,
                "estimated_duration": 2400,
                "dependencies": ["analyze_claim"],
                "win_percentage": 65,
                "forms_completed": 1,
                "contacts_needed": 3,
                "steps_remaining": 5
            }
        ]
    }
    
    return plans.get(case_type, plans["small_claims"])