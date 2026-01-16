/**
 * API Client for Disaster Preparedness Simulator
 * Handles all communication with the backend API
 */

import axios, { AxiosInstance } from 'axios';
import type {
    Scenario,
    Simulation,
    Action,
    SimulationMetrics,
    AIActionResponse,
    LeaderboardEntry,
    PerformanceStats,
    DisasterType,
    DifficultyLevel,
    SimulationMode
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }

    // ===== Scenario Endpoints =====

    async createScenario(scenario: Scenario): Promise<Scenario> {
        const response = await this.client.post('/api/scenarios/', scenario);
        return response.data;
    }

    async listScenarios(
        disaster_type?: DisasterType,
        difficulty?: DifficultyLevel
    ): Promise<Scenario[]> {
        const params = new URLSearchParams();
        if (disaster_type) params.append('disaster_type', disaster_type);
        if (difficulty) params.append('difficulty', difficulty);

        const response = await this.client.get('/api/scenarios/', { params });
        return response.data;
    }

    async getScenario(id: string): Promise<Scenario> {
        const response = await this.client.get(`/api/scenarios/${id}`);
        return response.data;
    }

    async updateScenario(id: string, scenario: Scenario): Promise<Scenario> {
        const response = await this.client.put(`/api/scenarios/${id}`, scenario);
        return response.data;
    }

    async deleteScenario(id: string): Promise<void> {
        await this.client.delete(`/api/scenarios/${id}`);
    }

    async getTemplates(): Promise<any[]> {
        const response = await this.client.get('/api/scenarios/templates/list');
        return response.data;
    }

    // ===== Simulation Endpoints =====

    async startSimulation(scenarioId: string, mode: SimulationMode): Promise<Simulation> {
        const response = await this.client.post('/api/simulations/start', {
            scenario_id: scenarioId,
            mode,
        });
        return response.data;
    }

    async getSimulation(id: string): Promise<Simulation> {
        const response = await this.client.get(`/api/simulations/${id}`);
        return response.data;
    }

    async submitAction(simulationId: string, action: Action): Promise<any> {
        const response = await this.client.post(
            `/api/simulations/${simulationId}/actions`,
            action
        );
        return response.data;
    }

    async getCurrentState(simulationId: string): Promise<any> {
        const response = await this.client.get(
            `/api/simulations/${simulationId}/state`
        );
        return response.data;
    }

    async resetSimulation(simulationId: string): Promise<void> {
        await this.client.post(`/api/simulations/${simulationId}/reset`);
    }

    async getMetrics(simulationId: string): Promise<SimulationMetrics> {
        const response = await this.client.get(
            `/api/simulations/${simulationId}/metrics`
        );
        return response.data;
    }

    async getReplay(simulationId: string): Promise<any> {
        const response = await this.client.get(
            `/api/simulations/${simulationId}/replay`
        );
        return response.data;
    }

    // ===== AI Endpoints =====

    async suggestAction(observation: number[], simulationId?: string): Promise<AIActionResponse> {
        const response = await this.client.post('/api/ai/suggest-action', {
            observation,
            simulation_id: simulationId,
        });
        return response.data;
    }

    async compareStrategies(
        observations: number[][],
        humanActions: number[][]
    ): Promise<any> {
        const response = await this.client.post('/api/ai/compare', {
            observations,
            human_actions: humanActions,
        });
        return response.data;
    }

    async getAIExplanation(observation: number[], simulationId?: string): Promise<any> {
        const response = await this.client.post('/api/ai/explanation', {
            observation,
            simulation_id: simulationId,
        });
        return response.data;
    }

    async getModelStatus(): Promise<any> {
        const response = await this.client.get('/api/ai/model/status');
        return response.data;
    }

    // ===== Analytics Endpoints =====

    async getLeaderboard(
        scenarioId?: string,
        limit: number = 10
    ): Promise<LeaderboardEntry[]> {
        const params = new URLSearchParams();
        if (scenarioId) params.append('scenario_id', scenarioId);
        params.append('limit', limit.toString());

        const response = await this.client.get('/api/analytics/leaderboard', { params });
        return response.data;
    }

    async getUserStats(userId: string): Promise<PerformanceStats> {
        const response = await this.client.get(`/api/analytics/user/${userId}/stats`);
        return response.data;
    }

    async getScenarioAnalytics(scenarioId: string): Promise<any> {
        const response = await this.client.get(
            `/api/analytics/scenarios/${scenarioId}/analytics`
        );
        return response.data;
    }

    // ===== Health Check =====

    async healthCheck(): Promise<any> {
        const response = await this.client.get('/health');
        return response.data;
    }
}

export default new ApiClient();
