from typing import Dict, Any
import random
import json

def simulate_case_outcome(case_description: str, memory: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate case outcome using heuristics and past case data"""
    
    # Get past cases for comparison
    past_cases = memory.get("past_cases", [])
    jurisdiction = memory.get("preferences", {}).get("jurisdiction", "CA")
    
    # Basic heuristic scoring
    base_win_rate = 50
    
    # Adjust based on jurisdiction (mock data)
    jurisdiction_modifiers = {
        "CA": 10,   # More favorable
        "NY": 5,
        "TX": -5,
        "FL": 0
    }
    
    win_probability = base_win_rate + jurisdiction_modifiers.get(jurisdiction, 0)
    
    # Analyze case type for additional modifiers
    case_lower = case_description.lower()
    
    if "traffic" in case_lower or "ticket" in case_lower:
        win_probability += 15  # Traffic tickets often winnable
    elif "small claims" in case_lower:
        win_probability += 5   # Moderate win rate
    elif "landlord" in case_lower or "tenant" in case_lower:
        win_probability -= 10  # More complex, harder to win
    
    # Add some randomness but keep it realistic
    win_probability += random.randint(-15, 15)
    win_probability = max(20, min(90, win_probability))  # Clamp between 20-90%
    
    # Determine best strategy based on case type and win probability
    strategies = {
        "high": ["Aggressive litigation", "Demand full compensation", "Take to trial"],
        "medium": ["Negotiate settlement", "Mediation", "Limited litigation"], 
        "low": ["Settlement focus", "Damage control", "Alternative resolution"]
    }
    
    if win_probability >= 70:
        strategy_category = "high"
    elif win_probability >= 50:
        strategy_category = "medium"
    else:
        strategy_category = "low"
    
    best_strategy = random.choice(strategies[strategy_category])
    
    # Identify risk factors
    risk_factors = []
    if win_probability < 60:
        risk_factors.append("Weak evidence")
    if "complex" in case_description.lower():
        risk_factors.append("Legal complexity")
    if len(past_cases) == 0:
        risk_factors.append("No case history")
    
    # Estimate duration based on case complexity
    durations = {
        "traffic": "2-4 weeks",
        "small claims": "1-3 months", 
        "landlord": "3-6 months",
        "contract": "2-8 months",
        "personal injury": "6-18 months"
    }
    
    estimated_duration = "2-6 months"  # Default
    for case_type, duration in durations.items():
        if case_type in case_lower:
            estimated_duration = duration
            break
    
    return {
        "win_probability": win_probability,
        "best_strategy": best_strategy,
        "risk_factors": risk_factors if risk_factors else ["Standard legal risks"],
        "estimated_duration": estimated_duration,
        "confidence_level": "medium" if 40 <= win_probability <= 70 else "high" if win_probability > 70 else "low",
        "similar_cases": len([c for c in past_cases if calculate_case_similarity(case_description, c.get("description", "")) > 0.5])
    }

def calculate_case_similarity(case1: str, case2: str) -> float:
    """Calculate similarity between two case descriptions"""
    
    # Simple keyword-based similarity
    words1 = set(case1.lower().split())
    words2 = set(case2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def get_outcome_statistics(case_type: str, jurisdiction: str = "CA") -> Dict[str, Any]:
    """Get mock outcome statistics for case type and jurisdiction"""
    
    # Mock statistical data - in reality this would come from legal databases
    base_stats = {
        "traffic_ticket": {"win_rate": 0.65, "avg_fine_reduction": 0.40},
        "small_claims": {"win_rate": 0.55, "avg_recovery": 0.70},
        "landlord_tenant": {"win_rate": 0.45, "avg_damages": 0.60},
        "contract": {"win_rate": 0.50, "avg_settlement": 0.65}
    }
    
    jurisdiction_multipliers = {
        "CA": 1.1,
        "NY": 1.05,
        "TX": 0.95,
        "FL": 1.0
    }
    
    stats = base_stats.get(case_type, base_stats["small_claims"])
    multiplier = jurisdiction_multipliers.get(jurisdiction, 1.0)
    
    return {
        "win_rate": min(0.9, stats["win_rate"] * multiplier),
        "average_outcome": stats.get("avg_fine_reduction", stats.get("avg_recovery", 0.6)),
        "sample_size": random.randint(50, 500),  # Mock sample size
        "data_currency": "Last 12 months"
    }