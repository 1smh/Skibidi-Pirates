import json
import os
from typing import Dict, Any
from pathlib import Path

MEMORY_FILE = "storage/user_memory.json"

def ensure_storage_exists():
    """Ensure storage directory and files exist"""
    os.makedirs("storage", exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump({}, f)

def load_memory(user_id: str) -> Dict[str, Any]:
    """Load user memory from JSON file"""
    ensure_storage_exists()
    
    try:
        with open(MEMORY_FILE, "r") as f:
            all_memory = json.load(f)
        
        return all_memory.get(user_id, {
            "best_plans": [],
            "past_cases": [],
            "conversations": [],
            "preferences": {
                "jurisdiction": "CA",
                "language": "plain_english"
            }
        })
    except Exception as e:
        print(f"Error loading memory: {e}")
        return {
            "best_plans": [],
            "past_cases": [],
            "conversations": [],
            "preferences": {
                "jurisdiction": "CA", 
                "language": "plain_english"
            }
        }

def save_memory(user_id: str, memory: Dict[str, Any]) -> None:
    """Save user memory to JSON file"""
    ensure_storage_exists()
    
    try:
        # Load existing memory
        with open(MEMORY_FILE, "r") as f:
            all_memory = json.load(f)
        
        # Update user's memory
        all_memory[user_id] = memory
        
        # Save back to file
        with open(MEMORY_FILE, "w") as f:
            json.dump(all_memory, f, indent=2)
            
    except Exception as e:
        print(f"Error saving memory: {e}")

def get_case_history(user_id: str, case_type: str = None) -> list:
    """Get case history for similarity matching"""
    memory = load_memory(user_id)
    cases = memory.get("past_cases", [])
    
    if case_type:
        cases = [case for case in cases if case.get("type") == case_type]
    
    return cases

def add_case_to_history(user_id: str, case_data: Dict[str, Any]) -> None:
    """Add a completed case to history"""
    memory = load_memory(user_id)
    memory.setdefault("past_cases", []).append(case_data)
    save_memory(user_id, memory)