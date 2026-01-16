"""
Training script for the Disaster Response RL Agent
Uses PPO (Proximal Policy Optimization) from Stable-Baselines3
"""

import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.monitor import Monitor
import torch

# Import our custom environment
from environments.disaster_env import DisasterEnv

def create_env():
    """Create and return the disaster environment"""
    return DisasterEnv(
        grid_size=10,
        num_zones=25,
        num_shelters=5,
        num_resources=10,
        max_timesteps=100,
        disaster_intensity=0.5
    )

def train_agent(
    total_timesteps: int = 500_000,
    save_dir: str = "./models",
    tensorboard_log: str = "./logs"
):
    """
    Train the RL agent
    
    Args:
        total_timesteps: Total number of timesteps to train
        save_dir: Directory to save models
        tensorboard_log: Directory for tensorboard logs
    """
    
    # Create directories
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(tensorboard_log, exist_ok=True)
    
    # Create vectorized environment (parallel training)
    env = make_vec_env(create_env, n_envs=4)
    
    # Create evaluation environment
    eval_env = Monitor(create_env())
    
    # Configure callbacks
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=f"{save_dir}/best",
        log_path=f"{save_dir}/eval",
        eval_freq=10000,
        deterministic=True,
        render=False
    )
    
    checkpoint_callback = CheckpointCallback(
        save_freq=50000,
        save_path=f"{save_dir}/checkpoints",
        name_prefix="disaster_agent"
    )
    
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Training on: {device}")
    
    # Create PPO agent
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        clip_range_vf=None,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        tensorboard_log=tensorboard_log,
        device=device,
        verbose=1
    )
    
    print("Starting training...")
    print(f"Total timesteps: {total_timesteps:,}")
    
    # Train the agent
    model.learn(
        total_timesteps=total_timesteps,
        callback=[eval_callback, checkpoint_callback],
        progress_bar=True
    )
    
    # Save final model
    final_model_path = f"{save_dir}/disaster_agent_final"
    model.save(final_model_path)
    print(f"\nTraining complete! Final model saved to: {final_model_path}")
    
    return model

def test_agent(model_path: str, num_episodes: int = 10):
    """
    Test a trained agent
    
    Args:
        model_path: Path to the saved model
        num_episodes: Number of episodes to test
    """
    
    # Load the model
    model = PPO.load(model_path)
    
    # Create environment
    env = create_env()
    
    total_rewards = []
    total_casualties_list = []
    total_evacuated_list = []
    
    for episode in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward
            done = terminated or truncated
        
        total_rewards.append(episode_reward)
        total_casualties_list.append(info['total_casualties'])
        total_evacuated_list.append(info['total_evacuated'])
        
        print(f"Episode {episode + 1}: Reward={episode_reward:.2f}, "
              f"Casualties={info['total_casualties']:.1f}, "
              f"Evacuated={info['total_evacuated']:.0f}")
    
    print(f"\n=== Test Results (Average over {num_episodes} episodes) ===")
    print(f"Average Reward: {sum(total_rewards)/len(total_rewards):.2f}")
    print(f"Average Casualties: {sum(total_casualties_list)/len(total_casualties_list):.1f}")
    print(f"Average Evacuated: {sum(total_evacuated_list)/len(total_evacuated_list):.0f}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train or test Disaster Response RL Agent")
    parser.add_argument("--mode", type=str, choices=["train", "test"], default="train",
                       help="Mode: train or test")
    parser.add_argument("--timesteps", type=int, default=500_000,
                       help="Total timesteps for training")
    parser.add_argument("--model", type=str, default="./models/disaster_agent_final",
                       help="Path to model for testing")
    parser.add_argument("--episodes", type=int, default=10,
                       help="Number of episodes for testing")
    
    args = parser.parse_args()
    
    if args.mode == "train":
        train_agent(total_timesteps=args.timesteps)
    else:
        test_agent(model_path=args.model, num_episodes=args.episodes)
