from typing import Dict, Any, List
from .base_agent import BaseAgent

class SmallClaimsAgent(BaseAgent):
    """Specialized agent for small claims court cases"""
    
    def __init__(self, llm_client):
        super().__init__(llm_client)
        self.agent_type = "small_claims"
        self.name = "Small Claims Specialist"
    
    def plan(self, case_context: str, memory: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create small claims case plan"""
        
        jurisdiction_info = self.get_jurisdiction_info(memory)
        key_facts = self.extract_key_facts(case_context)
        
        planning_prompt = f"""
        Create a strategy for this small claims case:
        
        Case: {case_context}
        Jurisdiction: {jurisdiction_info}
        Key Facts: {key_facts.get('extracted_facts', 'None extracted')}
        
        Consider:
        1. Damage calculation and documentation
        2. Evidence gathering (contracts, receipts, communications)
        3. Witness preparation
        4. Settlement negotiation opportunities
        5. Court presentation strategy
        
        Create a comprehensive action plan.
        """
        
        plan_text = self.llm_client.chat(planning_prompt)
        
        return [
            {
                "step": 1,
                "action": "Calculate Damages",
                "description": "Document all losses and calculate total claim amount",
                "estimated_time": "1 hour"
            },
            {
                "step": 2,
                "action": "Gather Evidence", 
                "description": "Collect contracts, receipts, photos, communications",
                "estimated_time": "3 hours"
            },
            {
                "step": 3,
                "action": "Attempt Settlement",
                "description": "Send demand letter and negotiate resolution",
                "estimated_time": "1 week"
            },
            {
                "step": 4,
                "action": "File Complaint",
                "description": "Prepare and file small claims complaint",
                "estimated_time": "2 hours"
            },
            {
                "step": 5,
                "action": "Prepare for Hearing",
                "description": "Organize evidence and practice presentation",
                "estimated_time": "4 hours"
            }
        ]
    
    def execute(self, plan: List[Dict[str, Any]], memory: Dict[str, Any]) -> Dict[str, Any]:
        """Execute small claims plan"""
        
        results = {
            "damage_calculation": self._calculate_damages(memory),
            "evidence_list": self._identify_evidence(memory),
            "settlement_analysis": self._analyze_settlement_options(memory),
            "filing_requirements": self._get_filing_requirements(memory),
            "success_probability": self._estimate_success_rate(memory)
        }
        
        return results
    
    def summarize(self, results: Dict[str, Any]) -> str:
        """Summarize small claims case"""
        
        total_damages = results.get("damage_calculation", {}).get("total", 0)
        success_rate = results.get("success_probability", 55)
        
        return f"""
        Small Claims Case Summary:
        
        I've prepared your small claims case with total damages of ${total_damages:,.2f}.
        Estimated success probability: {success_rate}%
        
        Completed actions:
        • Calculated and documented all damages
        • Identified required evidence and documentation
        • Analyzed settlement vs. litigation options
        • Prepared court filing requirements
        • Created hearing preparation checklist
        
        Recommendation: {"Proceed with filing" if success_rate > 60 else "Consider settlement negotiation first"}
        """
    
    def _calculate_damages(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate claim damages"""
        
        # Mock damage calculation - would parse from case description
        return {
            "direct_damages": 2500.00,
            "incidental_costs": 150.00,
            "court_fees": 75.00,
            "total": 2725.00,
            "breakdown": [
                {"item": "Unpaid invoice", "amount": 2500.00},
                {"item": "Late fees", "amount": 150.00},
                {"item": "Filing fees", "amount": 75.00}
            ]
        }
    
    def _identify_evidence(self, memory: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify required evidence"""
        
        return [
            {"type": "Contract", "description": "Original service agreement", "priority": "high"},
            {"type": "Invoice", "description": "Billing statement showing amount due", "priority": "high"},
            {"type": "Communications", "description": "Emails or letters requesting payment", "priority": "medium"},
            {"type": "Proof of Service", "description": "Evidence that services were completed", "priority": "high"},
            {"type": "Witness Testimony", "description": "Third-party confirmation of agreement", "priority": "medium"}
        ]
    
    def _analyze_settlement_options(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze settlement vs litigation"""
        
        return {
            "settlement_probability": 70,
            "recommended_settlement_range": {"min": 1800, "max": 2200},
            "litigation_costs": {"time": "2-4 months", "fees": 150, "uncertainty": "medium"},
            "recommendation": "Attempt settlement before filing"
        }
    
    def _get_filing_requirements(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Get jurisdiction-specific filing requirements"""
        
        jurisdiction = memory.get("preferences", {}).get("jurisdiction", "CA")
        
        requirements = {
            "CA": {
                "max_claim": 10000,
                "filing_fee": 75,
                "forms": ["SC-100", "SC-104"],
                "service_methods": ["Personal service", "Substituted service", "Certified mail"]
            }
        }
        
        return requirements.get(jurisdiction, requirements["CA"])
    
    def _estimate_success_rate(self, memory: Dict[str, Any]) -> int:
        """Estimate case success rate"""
        
        # Mock success rate calculation
        base_rate = 55
        
        # Would factor in evidence strength, defendant response history, etc.
        return base_rate