from fastapi import APIRouter, HTTPException
from typing import List
from app.models.scenario import ScenarioConfig, DisasterType, DifficultyLevel
from datetime import datetime
import uuid

router = APIRouter()

# In-memory storage (replace with MongoDB in production)
scenarios_db = {}

@router.post("/", response_model=ScenarioConfig)
async def create_scenario(scenario: ScenarioConfig):
    """Create a new disaster scenario"""
    scenario.id = str(uuid.uuid4())
    scenario.created_at = datetime.utcnow()
    scenarios_db[scenario.id] = scenario
    return scenario

@router.get("/", response_model=List[ScenarioConfig])
async def list_scenarios(
    disaster_type: DisasterType = None,
    difficulty: DifficultyLevel = None
):
    """List all scenarios with optional filtering"""
    scenarios = list(scenarios_db.values())
    
    if disaster_type:
        scenarios = [s for s in scenarios if s.disaster_type == disaster_type]
    if difficulty:
        scenarios = [s for s in scenarios if s.difficulty == difficulty]
    
    return scenarios

@router.get("/{scenario_id}", response_model=ScenarioConfig)
async def get_scenario(scenario_id: str):
    """Get a specific scenario by ID"""
    if scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenarios_db[scenario_id]

@router.put("/{scenario_id}", response_model=ScenarioConfig)
async def update_scenario(scenario_id: str, scenario: ScenarioConfig):
    """Update an existing scenario"""
    if scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario.id = scenario_id
    scenarios_db[scenario_id] = scenario
    return scenario

@router.delete("/{scenario_id}")
async def delete_scenario(scenario_id: str):
    """Delete a scenario"""
    if scenario_id not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    del scenarios_db[scenario_id]
    return {"message": "Scenario deleted successfully"}

@router.get("/templates/list")
async def list_templates():
    """Get pre-built scenario templates"""
    templates = [
        {
            "id": "urban_earthquake",
            "name": "Urban Earthquake",
            "description": "Magnitude 7.2 earthquake in dense urban area",
            "disaster_type": "earthquake",
            "difficulty": "medium"
        },
        {
            "id": "coastal_flood",
            "name": "Coastal Flooding",
            "description": "Hurricane-driven coastal flooding",
            "disaster_type": "flood",
            "difficulty": "hard"
        },
        {
            "id": "tropical_cyclone",
            "name": "Tropical Cyclone",
            "description": "Category 4 cyclone approaching coastal city",
            "disaster_type": "cyclone",
            "difficulty": "expert"
        }
    ]
    return templates
