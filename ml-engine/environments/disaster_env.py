"""
Custom OpenAI Gym Environment for Disaster Response Simulation
This environment simulates disaster scenarios where an agent must allocate
resources, evacuate populations, and minimize casualties.
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import IntEnum
import json

class ActionType(IntEnum):
    """Types of actions the agent can take"""
    SEND_AMBULANCE = 0
    SEND_MEDICAL_TEAM = 1
    SEND_SUPPLY_TRUCK = 2
    EVACUATE_ZONE = 3
    OPEN_SHELTER = 4

class DisasterEnv(gym.Env):
    """
    Disaster Response Environment
    
    State Space:
        - Grid-based map (NxN zones)
        - Population per zone
        - Casualties per zone
        - Shelter status (capacity, occupancy)
        - Resource locations and availability
        - Road network status
        - Current timestep
    
    Action Space:
        - Discrete actions for resource allocation
        - Each action specifies: [action_type, resource_id, target_zone_id]
    
    Reward:
        - Large penalty for casualties
        - Reward for successful evacuations
        - Small penalty for resource usage
        - Bonus for efficiency
    """
    
    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 4}
    
    def __init__(
        self,
        grid_size: int = 10,
        num_zones: int = 25,
        num_shelters: int = 5,
        num_resources: int = 10,
        max_timesteps: int = 100,
        disaster_intensity: float = 0.5,
        render_mode: Optional[str] = None
    ):
        super().__init__()
        
        self.grid_size = grid_size
        self.num_zones = num_zones
        self.num_shelters = num_shelters
        self.num_resources = num_resources
        self.max_timesteps = max_timesteps
        self.disaster_intensity = disaster_intensity
        self.render_mode = render_mode
        
        # Initialize state dimensions
        self.state_dim = self._calculate_state_dim()
        
        # Define action space
        # Actions: [action_type (5 types), resource_id, target_zone_id]
        self.action_space = spaces.MultiDiscrete([
            5,  # action type
            self.num_resources,  # which resource
            self.num_zones  # target zone
        ])
        
        # Define observation space
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(self.state_dim,),
            dtype=np.float32
        )
        
        # Initialize environment state
        self.reset()
    
    def _calculate_state_dim(self) -> int:
        """Calculate the total dimension of the state vector"""
        dim = 0
        dim += self.num_zones * 3  # population, evacuated, casualties per zone
        dim += self.num_shelters * 2  # capacity, occupancy per shelter
        dim += self.num_resources * 3  # location (x,y), availability
        dim += self.num_zones * self.num_zones  # road network status matrix
        dim += 1  # current timestep
        return dim
    
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[np.ndarray, dict]:
        """Reset the environment to initial state"""
        super().reset(seed=seed)
        
        self.current_step = 0
        
        # Initialize zones with populations
        self.zone_populations = self.np_random.integers(100, 1000, size=self.num_zones).astype(np.float32)
        self.zone_evacuated = np.zeros(self.num_zones, dtype=np.float32)
        self.zone_casualties = np.zeros(self.num_zones, dtype=np.float32)
        
        # Initialize zone risk levels (affected by disaster)
        self.zone_risk = self.np_random.random(self.num_zones).astype(np.float32) * self.disaster_intensity
        
        # Initialize shelters
        self.shelter_capacity = self.np_random.integers(200, 500, size=self.num_shelters).astype(np.float32)
        self.shelter_occupancy = np.zeros(self.num_shelters, dtype=np.float32)
        
        # Initialize resources (x, y, available)
        self.resource_positions = self.np_random.random((self.num_resources, 2)).astype(np.float32)
        self.resource_available = np.ones(self.num_resources, dtype=np.float32)
        
        # Initialize road network (fully operational at start)
        self.road_network = np.ones((self.num_zones, self.num_zones), dtype=np.float32)
        
        # Metrics
        self.total_casualties = 0
        self.total_evacuated = 0
        self.resources_used = 0
        
        observation = self._get_observation()
        info = self._get_info()
        
        return observation, info
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, dict]:
        """
        Execute one timestep of the environment
        
        Args:
            action: [action_type, resource_id, target_zone_id]
        
        Returns:
            observation, reward, terminated, truncated, info
        """
        action_type, resource_id, target_zone = action
        
        # Execute action
        action_success = self._execute_action(action_type, resource_id, target_zone)
        
        # Update disaster progression
        self._update_disaster()
        
        # Calculate casualties based on risk and unprotected population
        new_casualties = self._calculate_casualties()
        self.total_casualties += new_casualties
        
        # Calculate reward
        reward = self._calculate_reward(new_casualties, action_success)
        
        # Increment timestep
        self.current_step += 1
        
        # Check termination conditions
        terminated = self.current_step >= self.max_timesteps
        truncated = False
        
        observation = self._get_observation()
        info = self._get_info()
        
        return observation, reward, terminated, truncated, info
    
    def _execute_action(self, action_type: int, resource_id: int, target_zone: int) -> bool:
        """Execute the specified action"""
        if not self.resource_available[resource_id]:
            return False
        
        if action_type == ActionType.EVACUATE_ZONE:
            # Evacuate population from zone to nearest shelter
            evacuees = min(
                self.zone_populations[target_zone] - self.zone_evacuated[target_zone],
                50  # Max 50 people per action
            )
            
            if evacuees > 0:
                # Find shelter with capacity
                for i in range(self.num_shelters):
                    available_capacity = self.shelter_capacity[i] - self.shelter_occupancy[i]
                    if available_capacity > 0:
                        actual_evacuees = min(evacuees, available_capacity)
                        self.zone_evacuated[target_zone] += actual_evacuees
                        self.shelter_occupancy[i] += actual_evacuees
                        self.total_evacuated += actual_evacuees
                        self.resources_used += 1
                        return True
        
        elif action_type in [ActionType.SEND_AMBULANCE, ActionType.SEND_MEDICAL_TEAM, ActionType.SEND_SUPPLY_TRUCK]:
            # Send resource to zone (reduces risk temporarily)
            self.zone_risk[target_zone] *= 0.9  # 10% risk reduction
            self.resources_used += 1
            return True
        
        return False
    
    def _update_disaster(self):
        """Update disaster progression (increase risk over time)"""
        # Disaster intensifies slightly each timestep
        self.zone_risk = np.clip(
            self.zone_risk * 1.02,  # 2% increase per step
            0, 1
        )
        
        # Road network degradation
        degradation = self.np_random.random((self.num_zones, self.num_zones)) * 0.01
        self.road_network = np.clip(self.road_network - degradation, 0, 1)
    
    def _calculate_casualties(self) -> float:
        """Calculate casualties for this timestep"""
        casualties = 0
        for i in range(self.num_zones):
            unprotected = self.zone_populations[i] - self.zone_evacuated[i]
            zone_casualties = unprotected * self.zone_risk[i] * 0.01  # 1% casualty rate per risk unit
            self.zone_casualties[i] += zone_casualties
            casualties += zone_casualties
        return casualties
    
    def _calculate_reward(self, casualties: float, action_success: bool) -> float:
        """Calculate reward for this timestep"""
        reward = 0
        
        # Heavy penalty for casualties
        reward -= casualties * 100
        
        # Reward for evacuations (saved lives)
        evacuation_rate = self.total_evacuated / self.zone_populations.sum()
        reward += evacuation_rate * 50
        
        # Small penalty for resource usage
        reward -= self.resources_used * 0.1
        
        # Penalty for failed actions
        if not action_success:
            reward -= 5
        
        # Bonus for efficiency (high evacuation, low casualties)
        if evacuation_rate > 0.8 and self.total_casualties < 10:
            reward += 100
        
        return reward
    
    def _get_observation(self) -> np.ndarray:
        """Get current observation (normalized state)"""
        obs = []
        
        # Zone information (normalized)
        obs.extend(self.zone_populations / 1000.0)
        obs.extend(self.zone_evacuated / 1000.0)
        obs.extend(self.zone_casualties / 100.0)
        
        # Shelter information (normalized)
        obs.extend(self.shelter_capacity / 500.0)
        obs.extend(self.shelter_occupancy / 500.0)
        
        # Resource information
        obs.extend(self.resource_positions.flatten())
        obs.extend(self.resource_available)
        
        # Road network (flattened)
        obs.extend(self.road_network.flatten())
        
        # Timestep (normalized)
        obs.append(self.current_step / self.max_timesteps)
        
        return np.array(obs, dtype=np.float32)
    
    def _get_info(self) -> dict:
        """Get additional information about current state"""
        return {
            'timestep': self.current_step,
            'total_casualties': float(self.total_casualties),
            'total_evacuated': float(self.total_evacuated),
            'evacuation_rate': float(self.total_evacuated / self.zone_populations.sum()),
            'resources_used': self.resources_used,
            'average_risk': float(self.zone_risk.mean())
        }
    
    def render(self):
        """Render the environment (optional)"""
        if self.render_mode == "human":
            print(f"\n=== Timestep {self.current_step}/{self.max_timesteps} ===")
            print(f"Casualties: {self.total_casualties:.1f}")
            print(f"Evacuated: {self.total_evacuated:.0f}/{self.zone_populations.sum():.0f}")
            print(f"Average Risk: {self.zone_risk.mean():.2f}")
    
    def close(self):
        """Clean up resources"""
        pass


# Register the environment
gym.register(
    id='DisasterResponse-v0',
    entry_point='environments.disaster_env:DisasterEnv',
    max_episode_steps=100,
)
