from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class DisasterType(str, Enum):
    EARTHQUAKE = "earthquake"
    FLOOD = "flood"
    CYCLONE = "cyclone"
    WILDFIRE = "wildfire"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

class Location(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)

class Shelter(BaseModel):
    id: str
    location: Location
    capacity: int
    current_occupancy: int = 0
    supplies: Dict[str, int] = {}

class Road(BaseModel):
    id: str
    start: Location
    end: Location
    status: float = Field(1.0, ge=0, le=1)  # 1.0 = fully operational, 0.0 = destroyed
    length_km: float

class Resource(BaseModel):
    id: str
    type: str  # ambulance, medical_team, supply_truck
    location: Location
    capacity: int
    current_load: int = 0

class Zone(BaseModel):
    id: str
    center: Location
    radius_km: float
    population: int
    evacuated: int = 0
    casualties: int = 0

class ScenarioConfig(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    disaster_type: DisasterType
    difficulty: DifficultyLevel
    
    # Spatial Configuration
    zones: List[Zone]
    shelters: List[Shelter]
    roads: List[Road]
    resources: List[Resource]
    
    # Temporal Configuration
    max_timesteps: int = 100
    timestep_minutes: int = 15  # Each step = 15 minutes
    
    # Disaster Parameters
    disaster_intensity: float = Field(..., ge=0, le=1)
    secondary_hazards: bool = False
    
    # Metadata
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Urban Earthquake Scenario",
                "description": "Magnitude 7.2 earthquake in dense urban area",
                "disaster_type": "earthquake",
                "difficulty": "medium",
                "zones": [],
                "shelters": [],
                "roads": [],
                "resources": [],
                "max_timesteps": 100,
                "disaster_intensity": 0.7
            }
        }
