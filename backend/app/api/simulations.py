from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict
from app.models.simulation import (
    Simulation, SimulationConfig, SimulationStatus, 
    SimulationMode, Action, SimulationState, SimulationMetrics
)
from datetime import datetime
import uuid
import json
import httpx

router = APIRouter()

# In-memory storage (replace with MongoDB in production)
simulations_db = {}

# Active WebSocket connections
active_connections: Dict[str, WebSocket] = {}

@router.post("/start", response_model=Simulation)
async def start_simulation(config: SimulationConfig):
    """Initialize a new simulation"""
    simulation = Simulation(
        id=str(uuid.uuid4()),
        scenario_id=config.scenario_id,
        mode=config.mode,
        status=SimulationStatus.RUNNING,
        created_at=datetime.utcnow(),
        user_id=config.user_id
    )
    
    simulations_db[simulation.id] = simulation
    return simulation

@router.get("/{simulation_id}", response_model=Simulation)
async def get_simulation(simulation_id: str):
    """Get simulation details"""
    if simulation_id not in simulations_db:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return simulations_db[simulation_id]

@router.post("/{simulation_id}/step")
async def execute_step(simulation_id: str, action: Action):
    """Execute a single timestep with the given action"""
    if simulation_id not in simulations_db:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    simulation = simulations_db[simulation_id]
    
    if simulation.status != SimulationStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Simulation is not running")
    
    # Record action
    action.timestep = simulation.current_timestep
    simulation.actions.append(action)
    
    # Update timestep
    simulation.current_timestep += 1
    
    # Check if completed
    if simulation.current_timestep >= simulation.max_timesteps:
        simulation.status = SimulationStatus.COMPLETED
        simulation.completed_at = datetime.utcnow()
    
    # Notify via WebSocket if connected
    if simulation_id in active_connections:
        await active_connections[simulation_id].send_json({
            "type": "step_completed",
            "timestep": simulation.current_timestep,
            "action": action.dict()
        })
    
    return {
        "simulation_id": simulation_id,
        "timestep": simulation.current_timestep,
        "status": simulation.status
    }

@router.post("/{simulation_id}/actions")
async def submit_action(simulation_id: str, action: Action):
    """Submit an action for the current timestep"""
    return await execute_step(simulation_id, action)

@router.get("/{simulation_id}/state", response_model=SimulationState)
async def get_current_state(simulation_id: str):
    """Get current simulation state"""
    if simulation_id not in simulations_db:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    simulation = simulations_db[simulation_id]
    
    if not simulation.states:
        raise HTTPException(status_code=404, detail="No state data available")
    
    return simulation.states[-1]  # Return most recent state

@router.post("/{simulation_id}/reset")
async def reset_simulation(simulation_id: str):
    """Reset simulation to initial state"""
    if simulation_id not in simulations_db:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    simulation = simulations_db[simulation_id]
    simulation.current_timestep = 0
    simulation.actions = []
    simulation.states = []
    simulation.status = SimulationStatus.RUNNING
    
    return {"message": "Simulation reset successfully"}

@router.get("/{simulation_id}/metrics", response_model=SimulationMetrics)
async def get_simulation_metrics(simulation_id: str):
    """Get performance metrics for a simulation"""
    if simulation_id not in simulations_db:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    simulation = simulations_db[simulation_id]
    
    if simulation.status != SimulationStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Simulation not completed yet")
    
    # Calculate metrics from final state
    if simulation.states:
        final_state = simulation.states[-1]
        total_population = sum(final_state.zone_populations)
        
        metrics = SimulationMetrics(
            total_casualties=final_state.total_casualties,
            total_evacuated=final_state.total_evacuated,
            evacuation_rate=final_state.total_evacuated / total_population if total_population > 0 else 0,
            avg_response_time=simulation.current_timestep / len(simulation.actions) if simulation.actions else 0,
            resources_efficiency=0.85,  # Placeholder
            overall_score=1000 - (final_state.total_casualties * 10)
        )
        
        return metrics
    
    raise HTTPException(status_code=404, detail="No metrics available")

@router.get("/{simulation_id}/replay")
async def get_simulation_replay(simulation_id: str):
    """Get full simulation replay data"""
    if simulation_id not in simulations_db:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    simulation = simulations_db[simulation_id]
    
    return {
        "simulation_id": simulation_id,
        "scenario_id": simulation.scenario_id,
        "mode": simulation.mode,
        "total_timesteps": simulation.current_timestep,
        "actions": [action.dict() for action in simulation.actions],
        "states": [state.dict() for state in simulation.states]
    }

@router.websocket("/ws/{simulation_id}")
async def websocket_endpoint(websocket: WebSocket, simulation_id: str):
    """WebSocket endpoint for real-time simulation updates"""
    await websocket.accept()
    active_connections[simulation_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        del active_connections[simulation_id]
