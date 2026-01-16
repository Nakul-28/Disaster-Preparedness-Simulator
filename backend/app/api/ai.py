from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
from app.core.config import settings

router = APIRouter()

class AIActionRequest(BaseModel):
    """Request for AI action suggestion"""
    observation: List[float]
    simulation_id: Optional[str] = None

class AIActionResponse(BaseModel):
    """AI action suggestion response"""
    action: List[int]
    confidence: float
    explanation: str

class CompareRequest(BaseModel):
    """Request to compare human vs AI strategy"""
    observations: List[List[float]]
    human_actions: List[List[int]]

class CompareResponse(BaseModel):
    """Comparison results"""
    agreement_rate: float
    ai_actions: List[List[int]]
    total_steps: int
    differences: List[dict]

@router.post("/suggest-action", response_model=AIActionResponse)
async def suggest_action(request: AIActionRequest):
    """
    Get AI recommendation for the next action
    
    This endpoint communicates with the ML Engine to get the optimal
    action based on the current state observation.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ML_ENGINE_URL}/predict",
                json={
                    "observation": request.observation,
                    "simulation_id": request.simulation_id
                },
                timeout=5.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return AIActionResponse(
                    action=data["action"],
                    confidence=data["confidence"],
                    explanation=data["explanation"]
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="ML Engine error"
                )
                
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"ML Engine unavailable: {str(e)}"
        )

@router.post("/compare", response_model=CompareResponse)
async def compare_strategies(request: CompareRequest):
    """
    Compare human strategy against AI recommendations
    
    This analyzes a completed simulation to see how human decisions
    compared to what the AI would have done.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ML_ENGINE_URL}/evaluate",
                json={
                    "observations": request.observations,
                    "actions": request.human_actions
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Calculate differences
                differences = []
                for i, (human, ai) in enumerate(zip(request.human_actions, data["ai_actions"])):
                    if human[0] != ai[0]:  # Different action types
                        differences.append({
                            "timestep": i,
                            "human_action": human,
                            "ai_action": ai,
                            "action_type_match": False
                        })
                
                return CompareResponse(
                    agreement_rate=data["agreement_rate"],
                    ai_actions=data["ai_actions"],
                    total_steps=data["total_steps"],
                    differences=differences
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="ML Engine error"
                )
                
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"ML Engine unavailable: {str(e)}"
        )

@router.post("/explanation")
async def get_ai_explanation(request: AIActionRequest):
    """
    Get detailed explanation for AI's recommended action
    
    Provides reasoning, alternative actions, and confidence scores.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ML_ENGINE_URL}/explain",
                json={
                    "observation": request.observation,
                    "simulation_id": request.simulation_id
                },
                timeout=5.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="ML Engine error"
                )
                
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"ML Engine unavailable: {str(e)}"
        )

@router.get("/model/status")
async def get_model_status():
    """Get ML model status and information"""
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.ML_ENGINE_URL}/model/info",
                timeout=3.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="ML Engine error"
                )
                
    except httpx.RequestError as e:
        return {
            "model_loaded": False,
            "error": str(e),
            "status": "unavailable"
        }
