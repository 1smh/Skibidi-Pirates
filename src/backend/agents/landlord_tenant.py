from typing import Dict, Any, List
from .base_agent import BaseAgent

class LandlordTenantAgent(BaseAgent):
    """Specialized agent for landlord-tenant disputes"""
    
    def __init__(self, llm_client):
        super().__init__(llm_client)
        self.agent_type = "landlord_tenant"
        self.name = "Landlord-Tenant Specialist"
    
    def plan(self, case_context: str, memory: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create landlord-tenant case plan"""
        
        jurisdiction_info = self.get_jurisdiction_info(memory)
        key_facts = self.extract_key_facts(case_context)
        
        planning_prompt = f"""
        Create a strategy for this landlord-tenant dispute:
        
        Case: {case_context}
        Jurisdiction: {jurisdiction_info}
        Key Facts: {key_facts.get('extracted_facts', 'None extracted')}
        
        Consider:
        1. Lease agreement analysis
        2. Tenant rights and landlord obligations
        3. Security deposit laws
        4. Habitability requirements
        5. Eviction procedures and defenses
        6. Rent control regulations
        
        Create a detailed action plan.
        """
        
        plan_text = self.llm_client.chat(planning_prompt)
        
        return [
            {
                "step": 1,
                "action": "Analyze Lease Agreement",
                "description": "Review lease terms and identify relevant provisions",
                "estimated_time": "1 hour"
            },
            {
                "step": 2,
                "action": "Research Tenant Rights",
                "description": "Identify applicable tenant protection laws",
                "estimated_time": "2 hours"
            },
            {
                "step": 3,
                "action": "Document Property Conditions",
                "description": "Gather evidence of property issues or conditions",
                "estimated_time": "1 hour"
            },
            {
                "step": 4,
                "action": "Calculate Damages",
                "description": "Determine financial impact and potential claims",
                "estimated_time": "1 hour"
            },
            {
                "step": 5,
                "action": "Prepare Response Strategy",
                "description": "Develop approach for negotiations or court",
                "estimated_time": "2 hours"
            }
        ]
    
    def execute(self, plan: List[Dict[str, Any]], memory: Dict[str, Any]) -> Dict[str, Any]:
        """Execute landlord-tenant plan"""
        
        results = {
            "lease_analysis": self._analyze_lease(memory),
            "tenant_rights": self._research_tenant_rights(memory),
            "property_documentation": self._document_conditions(memory),
            "financial_analysis": self._calculate_financial_impact(memory),
            "success_probability": self._estimate_outcome(memory)
        }
        
        return results
    
    def summarize(self, results: Dict[str, Any]) -> str:
        """Summarize landlord-tenant case"""
        
        success_rate = results.get("success_probability", 45)
        key_issues = results.get("lease_analysis", {}).get("key_issues", [])
        
        return f"""
        Landlord-Tenant Case Summary:
        
        I've analyzed your landlord-tenant dispute. Success probability: {success_rate}%
        
        Key findings:
        • Lease agreement reviewed for relevant provisions
        • Tenant rights and protections identified
        • Property conditions documented
        • Financial impact calculated
        • Response strategy developed
        
        Primary issues: {', '.join(key_issues[:3]) if key_issues else 'Standard landlord-tenant dispute'}
        
        Next steps: {"Consider negotiation first" if success_rate < 60 else "Strong case for formal action"}
        """
    
    def _analyze_lease(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze lease agreement"""
        
        # Mock lease analysis - would parse uploaded lease document
        return {
            "lease_type": "Standard residential lease",
            "term": "12 months",
            "rent_amount": 2500,
            "security_deposit": 2500,
            "key_provisions": [
                "Maintenance responsibilities",
                "Security deposit terms",
                "Notice requirements"
            ],
            "key_issues": [
                "Unclear maintenance obligations",
                "Excessive security deposit retention"
            ],
            "potential_violations": [
                "Improper notice period",
                "Unlawful deposit deductions"
            ]
        }
    
    def _research_tenant_rights(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Research applicable tenant rights"""
        
        jurisdiction = memory.get("preferences", {}).get("jurisdiction", "CA")
        
        tenant_rights = {
            "CA": {
                "habitability_warranty": True,
                "security_deposit_limit": "2x monthly rent",
                "notice_period": "30 days for month-to-month",
                "rent_control": "Varies by city",
                "key_protections": [
                    "Just cause eviction requirements",
                    "Security deposit return timeline (21 days)",
                    "Right to habitable premises",
                    "Protection from retaliatory eviction"
                ]
            }
        }
        
        return tenant_rights.get(jurisdiction, tenant_rights["CA"])
    
    def _document_conditions(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Document property conditions"""
        
        # Mock property documentation
        return {
            "inspection_date": "2024-01-15",
            "conditions_noted": [
                {"area": "Kitchen", "issue": "Leaking faucet", "severity": "medium"},
                {"area": "Bathroom", "issue": "Mold in shower", "severity": "high"},
                {"area": "Living room", "issue": "Damaged flooring", "severity": "low"}
            ],
            "photos_needed": ["Water damage", "Safety hazards", "General conditions"],
            "witness_statements": ["Maintenance requests", "Landlord communications"]
        }
    
    def _calculate_financial_impact(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate financial damages"""
        
        return {
            "security_deposit_dispute": 2500,
            "temporary_housing_costs": 800,
            "property_damage": 300,
            "lost_use_of_deposit": 100,
            "total_potential_recovery": 3700,
            "itemized_damages": [
                {"item": "Improperly retained security deposit", "amount": 2500},
                {"item": "Temporary housing during repairs", "amount": 800},
                {"item": "Personal property damage", "amount": 300},
                {"item": "Interest and penalties", "amount": 100}
            ]
        }
    
    def _estimate_outcome(self, memory: Dict[str, Any]) -> int:
        """Estimate case outcome probability"""
        
        # Mock outcome estimation
        base_rate = 45  # Landlord-tenant cases can be complex
        
        # Would factor in evidence strength, jurisdiction tenant-friendliness, etc.
        return base_rate