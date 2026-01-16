from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class LeaderboardEntry(BaseModel):
    """Leaderboard entry"""
    rank: int
    user_id: str
    username: str
    scenario_id: str
    score: float
    casualties: float
    evacuated: float
    evacuation_rate: float
    completed_at: datetime

class PerformanceStats(BaseModel):
    """User performance statistics"""
    total_simulations: int
    avg_score: float
    avg_casualties: float
    avg_evacuation_rate: float
    best_score: float
    scenarios_completed: int

# Mock leaderboard data
leaderboard_data = []

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    scenario_id: Optional[str] = None,
    limit: int = 10
):
    """
    Get leaderboard rankings
    
    Can be filtered by scenario_id, or show global rankings
    """
    
    # Filter by scenario if specified
    if scenario_id:
        entries = [e for e in leaderboard_data if e.scenario_id == scenario_id]
    else:
        entries = leaderboard_data
    
    # Sort by score (descending)
    entries = sorted(entries, key=lambda x: x.score, reverse=True)
    
    # Add ranks
    for i, entry in enumerate(entries):
        entry.rank = i + 1
    
    return entries[:limit]

@router.get("/user/{user_id}/stats", response_model=PerformanceStats)
async def get_user_stats(user_id: str):
    """Get performance statistics for a specific user"""
    
    user_entries = [e for e in leaderboard_data if e.user_id == user_id]
    
    if not user_entries:
        return PerformanceStats(
            total_simulations=0,
            avg_score=0,
            avg_casualties=0,
            avg_evacuation_rate=0,
            best_score=0,
            scenarios_completed=0
        )
    
    return PerformanceStats(
        total_simulations=len(user_entries),
        avg_score=sum(e.score for e in user_entries) / len(user_entries),
        avg_casualties=sum(e.casualties for e in user_entries) / len(user_entries),
        avg_evacuation_rate=sum(e.evacuation_rate for e in user_entries) / len(user_entries),
        best_score=max(e.score for e in user_entries),
        scenarios_completed=len(set(e.scenario_id for e in user_entries))
    )

@router.get("/scenarios/{scenario_id}/analytics")
async def get_scenario_analytics(scenario_id: str):
    """Get analytics for a specific scenario"""
    
    scenario_entries = [e for e in leaderboard_data if e.scenario_id == scenario_id]
    
    if not scenario_entries:
        return {
            "scenario_id": scenario_id,
            "total_attempts": 0,
            "avg_score": 0,
            "avg_casualties": 0,
            "avg_evacuation_rate": 0
        }
    
    return {
        "scenario_id": scenario_id,
        "total_attempts": len(scenario_entries),
        "avg_score": sum(e.score for e in scenario_entries) / len(scenario_entries),
        "avg_casualties": sum(e.casualties for e in scenario_entries) / len(scenario_entries),
        "avg_evacuation_rate": sum(e.evacuation_rate for e in scenario_entries) / len(scenario_entries),
        "best_score": max(e.score for e in scenario_entries),
        "completion_timeline": [
            {
                "date": e.completed_at.date().isoformat(),
                "attempts": 1
            } for e in scenario_entries
        ]
    }
