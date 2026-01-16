"""
Environment Setup Verification Script
Checks if all required environment files exist and are properly configured
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing")
        return False

def check_env_variable(filepath, var_name):
    """Check if a specific variable exists in an env file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if var_name in content and not content.split(var_name)[1].split('\n')[0].strip().startswith('#'):
                return True
    except:
        pass
    return False

def main():
    print("=" * 60)
    print("🔍 Disaster Preparedness Simulator - Environment Check")
    print("=" * 60)
    print()
    
    project_root = Path(__file__).parent
    all_good = True
    
    # Check backend .env
    print("📦 BACKEND Configuration")
    print("-" * 60)
    backend_env = project_root / "backend" / ".env"
    if check_file_exists(backend_env, "Backend .env file"):
        required_vars = ["MONGODB_URL", "ML_ENGINE_URL", "ENVIRONMENT"]
        for var in required_vars:
            if check_env_variable(backend_env, var):
                print(f"  ✓ {var} configured")
            else:
                print(f"  ✗ {var} missing or commented")
                all_good = False
    else:
        all_good = False
    print()
    
    # Check frontend .env
    print("🎨 FRONTEND Configuration")
    print("-" * 60)
    frontend_env = project_root / "frontend" / ".env"
    if check_file_exists(frontend_env, "Frontend .env file"):
        required_vars = ["VITE_API_URL", "VITE_WS_URL"]
        for var in required_vars:
            if check_env_variable(frontend_env, var):
                print(f"  ✓ {var} configured")
            else:
                print(f"  ✗ {var} missing or commented")
                all_good = False
    else:
        all_good = False
    print()
    
    # Check ML Engine .env
    print("🤖 ML ENGINE Configuration")
    print("-" * 60)
    ml_env = project_root / "ml-engine" / ".env"
    if check_file_exists(ml_env, "ML Engine .env file"):
        required_vars = ["MODEL_PATH", "ENVIRONMENT"]
        for var in required_vars:
            if check_env_variable(ml_env, var):
                print(f"  ✓ {var} configured")
            else:
                print(f"  ✗ {var} missing or commented")
                all_good = False
    else:
        all_good = False
    print()
    
    # Check for required directories
    print("📁 Directory Structure")
    print("-" * 60)
    check_file_exists(project_root / "backend" / "app", "Backend app directory")
    check_file_exists(project_root / "frontend" / "src", "Frontend src directory")
    check_file_exists(project_root / "ml-engine" / "environments", "ML Engine environments")
    print()
    
    # Check for requirements files
    print("📋 Dependency Files")
    print("-" * 60)
    check_file_exists(project_root / "backend" / "requirements.txt", "Backend requirements.txt")
    check_file_exists(project_root / "frontend" / "package.json", "Frontend package.json")
    check_file_exists(project_root / "ml-engine" / "requirements.txt", "ML Engine requirements.txt")
    print()
    
    # Check for Docker files
    print("🐳 Docker Configuration")
    print("-" * 60)
    check_file_exists(project_root / "docker-compose.yml", "Docker Compose file")
    check_file_exists(project_root / "backend" / "Dockerfile", "Backend Dockerfile")
    check_file_exists(project_root / "frontend" / "Dockerfile", "Frontend Dockerfile")
    check_file_exists(project_root / "ml-engine" / "Dockerfile", "ML Engine Dockerfile")
    print()
    
    # Final summary
    print("=" * 60)
    if all_good:
        print("✨ All environment files are properly configured!")
        print()
        print("Next steps:")
        print("1. Start MongoDB: docker-compose up mongodb -d")
        print("2. Install dependencies (see README.md)")
        print("3. Train ML model: cd ml-engine && python train_agent.py")
        print("4. Start services: docker-compose up")
        return 0
    else:
        print("⚠️  Some environment files are missing or incomplete")
        print()
        print("Please check the issues above and fix them.")
        print("See docs/ENVIRONMENT_SETUP.md for more details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
