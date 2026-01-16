# 🚨 Disaster Preparedness Simulator

**An AI-driven decision-support platform for optimizing emergency response strategies.**

This project simulates disaster scenarios (e.g., urban earthquakes) to train emergency planners. It utilizes a custom Python Gym environment and Reinforcement Learning (RL) to compare human decision-making against AI-optimized strategies for resource allocation.

---

## 🎯 Problem vs. Solution

| Current Challenges | Our Solution |
| :--- | :--- |
| **Reactive:** Resources deployed inefficiently after disaster strikes. | **Proactive:** Data-driven simulation to plan and test strategies beforehand. |
| **Static:** Planning relies on fixed guidelines or tabletop exercises. | **Dynamic:** Realistic `Gym` environment capturing population movement. |
| **No Feedback:** Hard to evaluate the impact of decisions. | **Analytics:** Real-time feedback on casualties, shelter usage, and efficiency. |

---

## 🛠 Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend** | React (Web Interface, Map Visualizations) |
| **Simulation** | Python, Custom OpenAI Gym Environment |
| **AI / ML** | Stable-Baselines3 / Ray RLlib (PPO/Q-Learning) |
| **Database** | MongoDB (Scenario & Outcome storage) |

---

## ⚙️ System Architecture

![alt text](<images/System Architecture.png>)



## 🚀 Key Features
Scenario Configuration: Customize disaster severity (Magnitude 7+ Earthquake), population size, and infrastructure damage.

Resource Management: Allocate ambulances, medical teams, and shelters.

Dual Modes:

Manual Mode: User acts as the commander.

AI Mode: RL Agent allocates resources to minimize casualties.

Outcome Metrics: Tracks survival rates, response time, and logistics costs.

## 📦 Installation & Setup
Prerequisites
Node.js & npm

Python 3.8+

MongoDB (Local or Atlas URI)

1. Clone the Repository
Bash

git clone [https://github.com/Nakul-28/disaster-simulator.git](https://github.com/Nakul-28/disaster-simulator.git)
cd disaster-simulator
2. Backend & Simulation Setup
Bash

cd backend
pip install -r requirements.txt
# Set up env variables (DB connection)
echo "MONGO_URI=your_connection_string" > .env
python main.py
3. Frontend Setup
Bash

cd frontend
npm install
npm start
## 🧠 AI Agent Details
The AI is trained using Reinforcement Learning with the following parameters:

State Space: Population distribution, road status, resource availability.

Action Space: Dispatch teams, allocate supplies, open shelters.

Reward Function:

- (+) Positive reward for every person safely sheltered.

- (-) Penalties for casualties, unmet demand, and high logistics costs.

## 🤝 Contributing
- Fork the Project

- Create your Feature Branch (git checkout -b feature/AmazingFeature)

- Commit your Changes (git commit -m 'Add some AmazingFeature')

- Push to the Branch (git push origin feature/AmazingFeature)

- Open a Pull Request