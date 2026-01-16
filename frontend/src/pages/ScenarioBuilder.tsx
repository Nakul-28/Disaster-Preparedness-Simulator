import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useScenarios } from '../hooks/useApi';
import apiClient from '../services/api';
import type { DisasterType, DifficultyLevel, SimulationMode } from '../types';

const ScenarioBuilder: React.FC = () => {
    const navigate = useNavigate();
    const { scenarios, loading } = useScenarios();
    const [filter, setFilter] = useState<{
        disasterType?: DisasterType;
        difficulty?: DifficultyLevel;
    }>({});
    const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
    const [mode, setMode] = useState<SimulationMode>('manual' as SimulationMode);

    const handleStartSimulation = async () => {
        if (!selectedScenario) return;

        try {
            const simulation = await apiClient.startSimulation(selectedScenario, mode);
            navigate(`/simulation/${simulation.id}`);
        } catch (error) {
            console.error('Failed to start simulation:', error);
            alert('Failed to start simulation. Please try again.');
        }
    };

    const difficultyColors: Record<DifficultyLevel, string> = {
        easy: '#10b981',
        medium: '#f59e0b',
        hard: '#ef4444',
        expert: '#8b5cf6'
    };

    return (
        <div className="container" style={{ paddingTop: 'var(--spacing-2xl)', paddingBottom: 'var(--spacing-2xl)' }}>
            <h1 style={{ marginBottom: 'var(--spacing-xl)' }}>Choose Your Scenario</h1>

            {/* Filters */}
            <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
                <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Filters</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--spacing-md)' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: 'var(--spacing-sm)', fontWeight: 500 }}>
                            Disaster Type
                        </label>
                        <select
                            value={filter.disasterType || ''}
                            onChange={(e) => setFilter({ ...filter, disasterType: e.target.value as DisasterType || undefined })}
                        >
                            <option value="">All Types</option>
                            <option value="earthquake">Earthquake</option>
                            <option value="flood">Flood</option>
                            <option value="cyclone">Cyclone</option>
                            <option value="wildfire">Wildfire</option>
                        </select>
                    </div>
                    <div>
                        <label style={{ display: 'block', marginBottom: 'var(--spacing-sm)', fontWeight: 500 }}>
                            Difficulty
                        </label>
                        <select
                            value={filter.difficulty || ''}
                            onChange={(e) => setFilter({ ...filter, difficulty: e.target.value as DifficultyLevel || undefined })}
                        >
                            <option value="">All Difficulties</option>
                            <option value="easy">Easy</option>
                            <option value="medium">Medium</option>
                            <option value="hard">Hard</option>
                            <option value="expert">Expert</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Simulation Mode Selection */}
            {selectedScenario && (
                <div className="card" style={{ marginBottom: 'var(--spacing-xl)', background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%)', borderLeft: '4px solid var(--color-primary)' }}>
                    <h3 style={{ marginBottom: 'var(--spacing-md)' }}>Simulation Mode</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--spacing-md)' }}>
                        {[
                            { value: 'manual', label: 'Manual Only', icon: '👤', desc: 'You make all decisions' },
                            { value: 'ai_assisted', label: 'AI Assisted', icon: '🤝', desc: 'Get AI recommendations' },
                            { value: 'comparison', label: 'Comparison', icon: '⚖️', desc: 'Compare with AI' }
                        ].map((m) => (
                            <div
                                key={m.value}
                                onClick={() => setMode(m.value as SimulationMode)}
                                style={{
                                    padding: 'var(--spacing-md)',
                                    border: `2px solid ${mode === m.value ? 'var(--color-primary)' : 'var(--border-color)'}`,
                                    borderRadius: 'var(--border-radius)',
                                    cursor: 'pointer',
                                    transition: 'all var(--transition-fast)',
                                    background: mode === m.value ? 'rgba(59, 130, 246, 0.1)' : 'transparent'
                                }}
                            >
                                <div style={{ fontSize: '2rem', marginBottom: 'var(--spacing-sm)' }}>{m.icon}</div>
                                <div style={{ fontWeight: 600, marginBottom: 'var(--spacing-xs)' }}>{m.label}</div>
                                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{m.desc}</div>
                            </div>
                        ))}
                    </div>
                    <button
                        className="btn btn-primary"
                        onClick={handleStartSimulation}
                        style={{ marginTop: 'var(--spacing-lg)', width: '100%' }}
                    >
                        Start Simulation
                    </button>
                </div>
            )}

            {/* Scenarios Grid */}
            {loading ? (
                <div style={{ textAlign: 'center', padding: 'var(--spacing-2xl)' }}>
                    <div className="spinner" style={{ margin: '0 auto' }}></div>
                    <p style={{ marginTop: 'var(--spacing-md)' }}>Loading scenarios...</p>
                </div>
            ) : scenarios.length === 0 ? (
                <div className="card text-center">
                    <p style={{ fontSize: '1.125rem' }}>No scenarios available yet. Check back soon!</p>
                </div>
            ) : (
                <div className="grid grid-3">
                    {scenarios.map((scenario) => (
                        <div
                            key={scenario.id}
                            className={`card ${selectedScenario === scenario.id ? 'selected-scenario' : ''}`}
                            onClick={() => setSelectedScenario(scenario.id!)}
                            style={{
                                cursor: 'pointer',
                                border: selectedScenario === scenario.id ? '2px solid var(--color-primary)' : '1px solid var(--border-color)',
                                transform: selectedScenario === scenario.id ? 'scale(1.02)' : 'none'
                            }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 'var(--spacing-md)' }}>
                                <h3 style={{ marginBottom: 0 }}>{scenario.name}</h3>
                                <span
                                    className="badge"
                                    style={{ background: difficultyColors[scenario.difficulty], color: 'white' }}
                                >
                                    {scenario.difficulty}
                                </span>
                            </div>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.9375rem', marginBottom: 'var(--spacing-md)' }}>
                                {scenario.description}
                            </p>
                            <div style={{ display: 'flex', gap: 'var(--spacing-sm)', flexWrap: 'wrap' }}>
                                <span className="badge badge-primary" style={{ textTransform: 'capitalize' }}>
                                    {scenario.disaster_type}
                                </span>
                                <span className="badge" style={{ background: 'var(--bg-tertiary)', color: 'var(--text-secondary)' }}>
                                    {scenario.max_timesteps} steps
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ScenarioBuilder;
