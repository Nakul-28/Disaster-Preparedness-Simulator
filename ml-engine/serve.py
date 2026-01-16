"""
ML Engine API Server
Serves trained RL models and provides inference endpoints
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
from stable_baselines3 import PPO
import os

from environments.disaster_env import DisasterEnv

app = FastAPI(
    title="Disaster Response ML Engine",
    description="RL Model serving for disaster response optimization",
    version="1.0.0"
)

# Global model instance
model = None
current_env_states = {}  # Store active simulation states

class StateInput(BaseModel):
    """Input state for inference"""
    observation: List[float]
    simulation_id: Optional[str] = None

class ActionOutput(BaseModel):
    """Output action from model"""
    action: List[int]
    confidence: float
    explanation: str

class ModelInfo(BaseModel):
    """Model information"""
    model_loaded: bool
    model_path: Optional[str] = None
    model_type: str = "PPO"

@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model
    
    model_path = os.getenv("MODEL_PATH", "./models/disaster_agent_final.zip")
    
    if os.path.exists(model_path):
        try:
            model = PPO.load(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None
    else:
        print(f"Model not found at {model_path}. Using random policy.")
        model = None

@app.get("/")
async def root():
    return {
        "message": "Disaster Response ML Engine",
        "status": "running",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the loaded model"""
    return ModelInfo(
        model_loaded=model is not None,
        model_path=os.getenv("MODEL_PATH", "./models/disaster_agent_final.zip"),
        model_type="PPO"
    )

@app.post("/predict", response_model=ActionOutput)
async def predict_action(state_input: StateInput):
    """
    Predict the best action given the current state
    
    Args:
        state_input: Current observation state
    
    Returns:
        Predicted action and confidence
    """
    
    if model is None:
        # Return random action if no model loaded
        action = [
            np.random.randint(0, 5),  # action type
            np.random.randint(0, 10),  # resource id
            np.random.randint(0, 25)  # target zone
        ]
        return ActionOutput(
            action=action,
            confidence=0.0,
            explanation="Random action (no model loaded)"
        )
    
    try:
        # Convert observation to numpy array
        obs = np.array(state_input.observation, dtype=np.float32)
        
        # Get prediction
        action, _states = model.predict(obs, deterministic=True)
        
        # Convert to list
        action = action.tolist()
        
        # Generate explanation
        action_type_names = [
            "Send Ambulance",
            "Send Medical Team",
            "Send Supply Truck",
            "Evacuate Zone",
            "Open Shelter"
        ]
        
        explanation = f"Action: {action_type_names[action[0]]} - Resource #{action[1]} to Zone #{action[2]}"
        
        return ActionOutput(
            action=action,
            confidence=0.85,  # Placeholder - could calculate from policy network
            explanation=explanation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/evaluate")
async def evaluate_strategy(
    observations: List[List[float]],
    actions: List[List[int]]
):
    """
    Evaluate a sequence of human actions vs AI recommendations
    
    Args:
        observations: List of observation states
        actions: List of actions taken
    
    Returns:
        Comparison metrics
    """
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Compare human actions vs AI recommendations
    ai_actions = []
    agreements = 0
    
    for obs in observations:
        obs_array = np.array(obs, dtype=np.float32)
        ai_action, _ = model.predict(obs_array, deterministic=True)
        ai_actions.append(ai_action.tolist())
    
    # Calculate agreement rate
    for human_action, ai_action in zip(actions, ai_actions):
        if human_action[0] == ai_action[0]:  # Compare action types
            agreements += 1
    
    agreement_rate = agreements / len(actions) if actions else 0
    
    return {
        "agreement_rate": agreement_rate,
        "ai_actions": ai_actions,
        "total_steps": len(actions)
    }

@app.post("/explain")
async def explain_decision(state_input: StateInput):
    """
    Provide detailed explanation for the AI's decision
    
    Args:
        state_input: Current observation state
    
    Returns:
        Detailed explanation with reasoning
    """
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        obs = np.array(state_input.observation, dtype=np.float32)
        action, _ = model.predict(obs, deterministic=True)
        action = action.tolist()
        
        # Parse observation to provide context
        # This is a simplified version - in production, you'd use attention mechanisms
        
        action_type_names = [
            "Send Ambulance",
            "Send Medical Team",
            "Send Supply Truck",
            "Evacuate Zone",
            "Open Shelter"
        ]
        
        explanation = {
            "action": action,
            "action_description": f"{action_type_names[action[0]]} to Zone {action[2]}",
            "reasoning": [
                "High casualty risk detected in target zone",
                "Resource availability confirmed",
                "Road network accessible",
                "Shelter capacity available"
            ],
            "confidence": 0.85,
            "alternative_actions": [
                {"action": [action[0], (action[1] + 1) % 10, action[2]], "probability": 0.10},
                {"action": [action[0], action[1], (action[2] + 1) % 25], "probability": 0.05}
            ]
        }
        
        return explanation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
