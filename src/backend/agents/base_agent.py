from abc import ABC, abstractmethod
from typing import Dict, Any, List
from llm_client import LLMClient

class BaseAgent(ABC):
    """Base class for all specialized legal agents"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.agent_type = "base"
        self.name = "Base Legal Agent"
    
    @abstractmethod
    def plan(self, case_context: str, memory: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create an execution plan for this case type"""
        pass
    
    @abstractmethod
    def execute(self, plan: List[Dict[str, Any]], memory: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planned actions"""
        pass
    
    @abstractmethod
    def summarize(self, results: Dict[str, Any]) -> str:
        """Summarize the results for the user"""
        pass
    
    def get_jurisdiction_info(self, memory: Dict[str, Any]) -> str:
        """Get jurisdiction-specific information"""
        jurisdiction = memory.get("preferences", {}).get("jurisdiction", "CA")
        
        jurisdiction_info = {
            "CA": "California state law applies. Consumer-friendly jurisdiction.",
            "NY": "New York state law applies. Complex legal environment.", 
            "TX": "Texas state law applies. Business-friendly jurisdiction.",
            "FL": "Florida state law applies. Varies by county."
        }
        
        return jurisdiction_info.get(jurisdiction, "General US legal principles apply.")
    
    def extract_key_facts(self, case_context: str) -> Dict[str, Any]:
        """Extract key facts from case description using LLM"""
        
        extraction_prompt = f"""
        Extract key facts from this legal case description:
        
        {case_context}
        
        Identify:
        1. Parties involved
        2. Key dates
        3. Monetary amounts
        4. Legal issues
        5. Desired outcomes
        
        Return as structured information.
        """
        
        try:
            facts = self.llm_client.chat(extraction_prompt)
            return {"extracted_facts": facts}
        except Exception as e:
            return {"extracted_facts": "Unable to extract facts", "error": str(e)}
    
    def research_strategies(self, case_type: str, jurisdiction: str) -> List[str]:
        """Research common strategies for this case type"""
        
        # Mock strategy database - would be populated from legal research
        strategies = {
            "traffic_ticket": [
                "Challenge radar calibration",
                "Question officer testimony", 
                "Request traffic school",
                "Negotiate reduced charges"
            ],
            "small_claims": [
                "Gather documentary evidence",
                "Prepare witness testimony",
                "Calculate damages accurately",
                "Consider settlement options"
            ],
            "landlord_tenant": [
                "Review lease terms carefully",
                "Document property conditions",
                "Know tenant rights",
                "Seek mediation first"
            ]
        }
        
        return strategies.get(case_type, ["Consult legal precedents", "Gather evidence", "Consider alternatives"])
    
    def estimate_timeline(self, case_complexity: str = "medium") -> Dict[str, Any]:
        """Estimate case timeline based on complexity"""
        
        timelines = {
            "simple": {"total_days": 30, "milestones": ["File paperwork", "Await response", "Resolution"]},
            "medium": {"total_days": 90, "milestones": ["Discovery", "Negotiation", "Hearing", "Resolution"]},
            "complex": {"total_days": 180, "milestones": ["Investigation", "Discovery", "Motions", "Trial Prep", "Trial", "Resolution"]}
        }
        
        return timelines.get(case_complexity, timelines["medium"])
    
    def generate_forms_list(self, case_type: str, jurisdiction: str) -> List[Dict[str, Any]]:
        """Generate list of required forms"""
        
        # Mock forms database
        forms = {
            "traffic_ticket": [
                {"name": "Trial by Declaration", "required": True, "deadline_days": 25},
                {"name": "Request for Traffic School", "required": False, "deadline_days": 30}
            ],
            "small_claims": [
                {"name": "Small Claims Complaint", "required": True, "deadline_days": 0},
                {"name": "Proof of Service", "required": True, "deadline_days": 15},
                {"name": "Evidence List", "required": False, "deadline_days": 5}
            ],
            "landlord_tenant": [
                {"name": "Answer to Unlawful Detainer", "required": True, "deadline_days": 5},
                {"name": "Discovery Requests", "required": False, "deadline_days": 30}
            ]
        }
        
        return forms.get(case_type, [])