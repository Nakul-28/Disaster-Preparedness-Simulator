import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useSimulation } from '../hooks/useApi';
import apiClient from '../services/api';
import type { AIActionResponse } from '../types';

const SimulationPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const { simulation, loading, refetch } = useSimulation(id || null);
    const [aiSuggestion, setAiSuggestion] = useState<AIActionResponse | null>(null);
    const [selectedAction, setSelectedAction] = useState({
        actionType: 0,
        resourceId: 0,
        targetZone: 0
    });
    const [isPlaying, setIsPlaying] = useState(false);

    const actionTypeNames = [
        'Send Ambulance',
        'Send Medical Team',
        'Send Supply Truck',
        'Evacuate Zone',
        'Open Shelter'
    ];

    const handleGetAISuggestion = async () => {
        if (!simulation) return;

        try {
            // Mock observation for now
            const mockObservation = new Array(100).fill(0).map(() => Math.random());
            const suggestion = await apiClient.suggestAction(mockObservation, id);
            setAiSuggestion(suggestion);
        } catch (error) {
            console.error('Failed to get AI suggestion:', error);
        }
    };

    const handleSubmitAction = async () => {
        if (!id) return;

        try {
            await apiClient.submitAction(id, {
                timestep: simulation?.current_timestep || 0,
                action_type: selectedAction.actionType,
                resource_id: selectedAction.resourceId,
                target_zone_id: selectedAction.targetZone,
                success: true,
                source: 'human'
            });
            refetch();
            setAiSuggestion(null);
        } catch (error) {
            console.error('Failed to submit action:', error);
        }
    };

    if (loading || !simulation) {
        return (
            <div className="container" style={{ paddingTop: 'var(--spacing-2xl)', textAlign: 'center' }}>
                <div className="spinner" style={{ margin: '0 auto' }}></div>
                <p style={{ marginTop: 'var(--spacing-md)' }}>Loading simulation...</p>
            </div>
        );
    }

    const progress = (simulation.current_timestep / simulation.max_timesteps) * 100;

    return (
        <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
            {/* Top Bar */}
            <div style={{
                background: 'var(--bg-secondary)',
                borderBottom: '1px solid var(--border-color)',
                padding: 'var(--spacing-md) var(--spacing-lg)'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h2 style={{ marginBottom: 'var(--spacing-xs)' }}>Simulation in Progress</h2>
                        <div style={{ display: 'flex', gap: 'var(--spacing-lg)', alignItems: 'center' }}>
                            <span className="badge badge-primary">
                                Step {simulation.current_timestep}/{simulation.max_timesteps}
                            </span>
                            <span className="badge" style={{ background: simulation.status === 'running' ? 'var(--color-secondary)' : 'var(--color-warning)', color: 'white' }}>
                                {simulation.status}
                            </span>
                        </div>
                    </div>
                    <div style={{ display: 'flex', gap: 'var(--spacing-md)' }}>
                        <button
                            className="btn btn-secondary"
                            onClick={() => setIsPlaying(!isPlaying)}
                        >
                            {isPlaying ? '⏸️ Pause' : '▶️ Play'}
                        </button>
                        <button className="btn btn-secondary">
                            🔄 Reset
                        </button>
                    </div>
                </div>
                {/* Progress Bar */}
                <div style={{
                    marginTop: 'var(--spacing-md)',
                    background: 'var(--bg-tertiary)',
                    border- radius: '9999px',
                height: '8px',
                overflow: 'hidden'
        }}>
                <div style={{
                    width: `${progress}%`,
                    height: '100%',
                    background: 'linear-gradient(90deg, var(--color-primary) 0%, var(--color-secondary) 100%)',
                    transition: 'width var(--transition-normal)'
                }} />
            </div>
        </div>

      {/* Main Content */ }
    <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1fr 400px' }}>
        {/* Map/Visualization Area */}
        <div style={{
            background: 'var(--bg-primary)',
            padding: 'var(--spacing-lg)',
            display: 'flex',
            flexDirection: 'column'
        }}>
            <div className="card" style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#1a1f2e' }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '4rem', marginBottom: 'var(--spacing-md)' }}>
                        🗺️
                    </div>
                    <h3>Simulation Map</h3>
                    <p style={{ color: 'var(--text-muted)' }}>
                        Interactive disaster zone visualization will appear here
                    </p>
                </div>
            </div>

            {/* Metrics Bar */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--spacing-md)', marginTop: 'var(--spacing-md)' }}>
                {[
                    { label: 'Casualties', value: simulation.final_casualties || 0, color: 'var(--color-danger)', icon: '⚠️' },
                    { label: 'Evacuated', value: simulation.final_evacuated || 0, color: 'var(--color-secondary)', icon: '✅' },
                    { label: 'Resources Used', value: simulation.actions.length, color: 'var(--color-info)', icon: '🚑' },
                    { label: 'Score', value: simulation.final_score || 0, color: 'var(--color-warning)', icon: '🏆' }
                ].map((metric, i) => (
                    <div key={i} className="card" style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '1.5rem' }}>{metric.icon}</div>
                        <div style={{ fontSize: '1.5rem', fontWeight: 700, color: metric.color, marginBottom: 'var(--spacing-xs)' }}>
                            {metric.value}
                        </div>
                        <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                            {metric.label}
                        </div>
                    </div>
                ))}
            </div>
        </div>

        {/* Control Panel */}
        <div style={{
            background: 'var(--bg-secondary)',
            borderLeft: '1px solid var(--border-color)',
            padding: 'var(--spacing-lg)',
            overflowY: 'auto'
        }}>
            <h3 style={{ marginBottom: 'var(--spacing-lg)' }}>Control Panel</h3>

            {/* AI Suggestion */}
            {aiSuggestion && (
                <div className="card" style={{
                    marginBottom: 'var(--spacing-lg)',
                    background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, transparent 100%)',
                    borderLeft: '4px solid #8b5cf6'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-md)' }}>
                        <span style={{ fontSize: '1.5rem' }}>🤖</span>
                        <h4 style={{ marginBottom: 0 }}>AI Recommendation</h4>
                    </div>
                    <p style={{ marginBottom: 'var(--spacing-md)', color: 'var(--text-secondary)' }}>
                        {aiSuggestion.explanation}
                    </p>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span className="badge" style={{ background: '#8b5cf6', color: 'white' }}>
                            {(aiSuggestion.confidence * 100).toFixed(0)}% confident
                        </span>
                        <button
                            className="btn btn-primary"
                            onClick={() => {
                                setSelectedAction({
                                    actionType: aiSuggestion.action[0],
                                    resourceId: aiSuggestion.action[1],
                                    targetZone: aiSuggestion.action[2]
                                });
                            }}
                            style={{ fontSize: '0.875rem', padding: 'var(--spacing-xs) var(--spacing-md)' }}
                        >
                            Use This Action
                        </button>
                    </div>
                </div>
            )}

            <button
                className="btn btn-secondary"
                onClick={handleGetAISuggestion}
                style={{ width: '100%', marginBottom: 'var(--spacing-lg)' }}
            >
                🤖 Get AI Suggestion
            </button>

            {/* Action Selection */}
            <div className="card">
                <h4 style={{ marginBottom: 'var(--spacing-md)' }}>Select Action</h4>

                <div style={{ marginBottom: 'var(--spacing-md)' }}>
                    <label style={{ display: 'block', marginBottom: 'var(--spacing-sm)', fontWeight: 500 }}>
                        Action Type
                    </label>
                    <select
                        value={selectedAction.actionType}
                        onChange={(e) => setSelectedAction({ ...selectedAction, actionType: parseInt(e.target.value) })}
                    >
                        {actionTypeNames.map((name, i) => (
                            <option key={i} value={i}>{name}</option>
                        ))}
                    </select>
                </div>

                <div style={{ marginBottom: 'var(--spacing-md)' }}>
                    <label style={{ display: 'block', marginBottom: 'var(--spacing-sm)', fontWeight: 500 }}>
                        Resource ID
                    </label>
                    <input
                        type="number"
                        min="0"
                        max="9"
                        value={selectedAction.resourceId}
                        onChange={(e) => setSelectedAction({ ...selectedAction, resourceId: parseInt(e.target.value) })}
                    />
                </div>

                <div style={{ marginBottom: 'var(--spacing-md)' }}>
                    <label style={{ display: 'block', marginBottom: 'var(--spacing-sm)', fontWeight: 500 }}>
                        Target Zone
                    </label>
                    <input
                        type="number"
                        min="0"
                        max="24"
                        value={selectedAction.targetZone}
                        onChange={(e) => setSelectedAction({ ...selectedAction, targetZone: parseInt(e.target.value) })}
                    />
                </div>

                <button
                    className="btn btn-primary"
                    onClick={handleSubmitAction}
                    style={{ width: '100%' }}
                >
                    Execute Action
                </button>
            </div>

            {/* Action History */}
            <div className="card" style={{ marginTop: 'var(--spacing-lg)' }}>
                <h4 style={{ marginBottom: 'var(--spacing-md)' }}>Action History</h4>
                <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                    {simulation.actions.length === 0 ? (
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No actions yet</p>
                    ) : (
                        simulation.actions.map((action, i) => (
                            <div key={i} style={{
                                padding: 'var(--spacing-sm)',
                                background: 'var(--bg-tertiary)',
                                borderRadius: 'var(--border-radius)',
                                marginBottom: 'var(--spacing-sm)',
                                fontSize: '0.875rem'
                            }}>
                                <div style={{ fontWeight: 600 }}>Step {action.timestep}</div>
                                <div style={{ color: 'var(--text-muted)' }}>
                                    {actionTypeNames[action.action_type]} → Zone {action.target_zone_id}
                                </div>
                                <span className="badge" style={{
                                    marginTop: 'var(--spacing-xs)',
                                    background: action.source === 'ai' ? '#8b5cf6' : 'var(--color-primary)'
                                }}>
                                    {action.source}
                                </span>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    </div>
    </div >
  );
};

export default SimulationPage;
