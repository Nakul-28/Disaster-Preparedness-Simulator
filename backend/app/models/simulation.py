from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class SimulationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class SimulationMode(str, Enum):
    MANUAL = "manual"
    AI_ASSISTED = "ai_assisted"
    AI_ONLY = "ai_only"
    COMPARISON = "comparison"

class Action(BaseModel):
    """Single action taken in simulation"""
    timestep: int
    action_type: int
    resource_id: int
    target_zone_id: int
    success: bool
    source: str = "human"  # "human" or "ai"

class SimulationState(BaseModel):
    """Snapshot of simulation state at a timestep"""
    timestep: int
    zone_populations: List[float]
    zone_evacuated: List[float]
    zone_casualties: List[float]
    shelter_occupancy: List[float]
    total_casualties: float
    total_evacuated: float
    observation: List[float]

class SimulationConfig(BaseModel):
    """Configuration for starting a simulation"""
    scenario_id: str
    mode: SimulationMode = SimulationMode.MANUAL
    user_id: Optional[str] = None

class Simulation(BaseModel):
    """Complete simulation record"""
    id: Optional[str] = None
    scenario_id: str
    mode: SimulationMode
    status: SimulationStatus = SimulationStatus.PENDING
    
    # Simulation data
    current_timestep: int = 0
    max_timesteps: int = 100
    
    actions: List[Action] = []
    states: List[SimulationState] = []
    
    # Final metrics
    final_casualties: Optional[float] = None
    final_evacuated: Optional[float] = None
    final_score: Optional[float] = None
    
    # Metadata
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    user_id: Optional[str] = None

class SimulationMetrics(BaseModel):
    """Performance metrics for a completed simulation"""
    total_casualties: float
    total_evacuated: float
    evacuation_rate: float
    avg_response_time: float
    resources_efficiency: float
    overall_score: float
    
    # Comparison with AI (if applicable)
    ai_casualties: Optional[float] = None
    ai_evacuated: Optional[float] = None
    performance_vs_ai: Optional[float] = None  # percentage difference
