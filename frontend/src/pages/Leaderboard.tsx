import React, { useState } from 'react';
import { useLeaderboard } from '../hooks/useApi';

const Leaderboard: React.FC = () => {
    const [selectedScenario, setSelectedScenario] = useState<string | undefined>(undefined);
    const { leaderboard, loading } = useLeaderboard(selectedScenario);

    const getMedalEmoji = (rank: number): string => {
        if (rank === 1) return '🥇';
        if (rank === 2) return '🥈';
        if (rank === 3) return '🥉';
        return `#${rank}`;
    };

    return (
        <div className="container" style={{ paddingTop: 'var(--spacing-2xl)', paddingBottom: 'var(--spacing-2xl)' }}>
            <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-2xl)' }}>
                <h1 style={{ marginBottom: 'var(--spacing-md)' }}>🏆 Leaderboard</h1>
                <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)' }}>
                    Top performers in disaster response simulations
                </p>
            </div>

            {/* Filters */}
            <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: 'var(--spacing-md)', alignItems: 'end' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: 'var(--spacing-sm)', fontWeight: 500 }}>
                            Filter by Scenario
                        </label>
                        <select
                            value={selectedScenario || ''}
                            onChange={(e) => setSelectedScenario(e.target.value || undefined)}
                        >
                            <option value="">All Scenarios</option>
                            <option value="scenario1">Urban Earthquake</option>
                            <option value="scenario2">Coastal Flooding</option>
                            <option value="scenario3">Tropical Cyclone</option>
                        </select>
                    </div>
                    <button className="btn btn-secondary">
                        🔄 Refresh
                    </button>
                </div>
            </div>

            {/* Leaderboard Table */}
            {loading ? (
                <div className="card text-center">
                    <div className="spinner" style={{ margin: '0 auto' }}></div>
                    <p style={{ marginTop: 'var(--spacing-md)' }}>Loading leaderboard...</p>
                </div>
            ) : leaderboard.length === 0 ? (
                <div className="card text-center">
                    <p style={{ fontSize: '1.125rem' }}>No entries yet. Be the first to complete a simulation!</p>
                </div>
            ) : (
                <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ background: 'var(--bg-tertiary)', borderBottom: '1px solid var(--border-color)' }}>
                                <th style={{ padding: 'var(--spacing-md)', textAlign: 'left', fontWeight: 600 }}>Rank</th>
                                <th style={{ padding: 'var(--spacing-md)', textAlign: 'left', fontWeight: 600 }}>Player</th>
                                <th style={{ padding: 'var(--spacing-md)', textAlign: 'right', fontWeight: 600 }}>Score</th>
                                <th style={{ padding: 'var(--spacing-md)', textAlign: 'right', fontWeight: 600 }}>Evacuated</th>
                                <th style={{ padding: 'var(--spacing-md)', textAlign: 'right', fontWeight: 600 }}>Casualties</th>
                                <th style={{ padding: 'var(--spacing-md)', textAlign: 'right', fontWeight: 600 }}>Evac. Rate</th>
                                <th style={{ padding: 'var(--spacing-md)', textAlign: 'right', fontWeight: 600 }}>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {leaderboard.map((entry) => (
                                <tr
                                    key={entry.rank}
                                    style={{
                                        borderBottom: '1px solid var(--border-color)',
                                        transition: 'background var(--transition-fast)',
                                        background: entry.rank <= 3 ? 'rgba(59, 130, 246, 0.05)' : 'transparent'
                                    }}
                                    onMouseEnter={(e) => (e.currentTarget.style.background = 'var(--bg-hover)')}
                                    onMouseLeave={(e) => (e.currentTarget.style.background = entry.rank <= 3 ? 'rgba(59, 130, 246, 0.05)' : 'transparent')}
                                >
                                    <td style={{ padding: 'var(--spacing-md)' }}>
                                        <span style={{ fontSize: '1.25rem', fontWeight: 700 }}>
                                            {getMedalEmoji(entry.rank)}
                                        </span>
                                    </td>
                                    <td style={{ padding: 'var(--spacing-md)' }}>
                                        <div style={{ fontWeight: 600 }}>{entry.username}</div>
                                        <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                            {entry.scenario_id}
                                        </div>
                                    </td>
                                    <td style={{ padding: 'var(--spacing-md)', textAlign: 'right', fontWeight: 700, color: 'var(--color-secondary)' }}>
                                        {entry.score.toFixed(0)}
                                    </td>
                                    <td style={{ padding: 'var(--spacing-md)', textAlign: 'right' }}>
                                        {entry.evacuated.toFixed(0)}
                                    </td>
                                    <td style={{ padding: 'var(--spacing-md)', textAlign: 'right', color: 'var(--color-danger)' }}>
                                        {entry.casualties.toFixed(0)}
                                    </td>
                                    <td style={{ padding: 'var(--spacing-md)', textAlign: 'right' }}>
                                        <span className="badge badge-success">
                                            {(entry.evacuation_rate * 100).toFixed(1)}%
                                        </span>
                                    </td>
                                    <td style={{ padding: 'var(--spacing-md)', textAlign: 'right', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                        {new Date(entry.completed_at).toLocaleDateString()}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Stats Cards */}
            <div className="grid grid-3" style={{ marginTop: 'var(--spacing-2xl)' }}>
                {[
                    { label: 'Total Simulations', value: '1,245', icon: '🎮', color: 'var(--color-info)' },
                    { label: 'Active Players', value: '342', icon: '👥', color: 'var(--color-secondary)' },
                    { label: 'Lives Saved', value: '52.3K', icon: '❤️', color: 'var(--color-danger)' }
                ].map((stat, i) => (
                    <div key={i} className="card text-center">
                        <div style={{ fontSize: '3rem', marginBottom: 'var(--spacing-sm)' }}>{stat.icon}</div>
                        <div style={{ fontSize: '2rem', fontWeight: 700, color: stat.color, marginBottom: 'var(--spacing-xs)' }}>
                            {stat.value}
                        </div>
                        <div style={{ color: 'var(--text-muted)' }}>{stat.label}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Leaderboard;
