import { useState, useEffect } from 'react';
import apiClient from '../services/api';
import type { Scenario, DisasterType, DifficultyLevel } from '../types';

export const useScenarios = (
    disasterType?: DisasterType,
    difficulty?: DifficultyLevel
) => {
    const [scenarios, setScenarios] = useState<Scenario[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const fetchScenarios = async () => {
            try {
                setLoading(true);
                const data = await apiClient.listScenarios(disasterType, difficulty);
                setScenarios(data);
                setError(null);
            } catch (err) {
                setError(err as Error);
            } finally {
                setLoading(false);
            }
        };

        fetchScenarios();
    }, [disasterType, difficulty]);

    return { scenarios, loading, error };
};

export const useSimulation = (simulationId: string | null) => {
    const [simulation, setSimulation] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        if (!simulationId) return;

        const fetchSimulation = async () => {
            try {
                setLoading(true);
                const data = await apiClient.getSimulation(simulationId);
                setSimulation(data);
                setError(null);
            } catch (err) {
                setError(err as Error);
            } finally {
                setLoading(false);
            }
        };

        fetchSimulation();
    }, [simulationId]);

    return {
        simulation, loading, error, refetch: () => {
            if (simulationId) {
                apiClient.getSimulation(simulationId).then(setSimulation);
            }
        }
    };
};

export const useLeaderboard = (scenarioId?: string, limit: number = 10) => {
    const [leaderboard, setLeaderboard] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                setLoading(true);
                const data = await apiClient.getLeaderboard(scenarioId, limit);
                setLeaderboard(data);
                setError(null);
            } catch (err) {
                setError(err as Error);
            } finally {
                setLoading(false);
            }
        };

        fetchLeaderboard();
    }, [scenarioId, limit]);

    return { leaderboard, loading, error };
};
