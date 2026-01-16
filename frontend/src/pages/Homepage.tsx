import React from 'react';
import { useNavigate } from 'react-router-dom';

const Homepage: React.FC = () => {
    const navigate = useNavigate();

    const features = [
        {
            icon: '🎯',
            title: 'Interactive Simulation',
            description: 'Make real-time decisions in realistic disaster scenarios'
        },
        {
            icon: '🤖',
            title: 'AI-Powered Training',
            description: 'Learn from AI recommendations trained on optimal strategies'
        },
        {
            icon: '📊',
            title: 'Performance Analytics',
            description: 'Track your progress and compare with others'
        },
        {
            icon: '🏆',
            title: 'Leaderboards',
            description: 'Compete with emergency planners worldwide'
        }
    ];

    return (
        <div style={{ paddingTop: 'var(--spacing-2xl)' }}>
            {/* Hero Section */}
            <section className="container text-center" style={{ paddingBottom: 'var(--spacing-2xl)' }}>
                <h1 style={{
                    fontSize: '3.5rem',
                    background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    marginBottom: 'var(--spacing-lg)'
                }}>
                    Master Disaster Response
                </h1>
                <p style={{
                    fontSize: '1.25rem',
                    color: 'var(--text-secondary)',
                    maxWidth: '800px',
                    margin: '0 auto var(--spacing-2xl)',
                    lineHeight: 1.8
                }}>
                    Train your emergency response skills with AI-powered simulations.
                    Make critical decisions, save lives, and learn from the best strategies.
                </p>
                <div style={{ display: 'flex', gap: 'var(--spacing-md)', justifyContent: 'center', flexWrap: 'wrap' }}>
                    <button
                        className="btn btn-primary"
                        onClick={() => navigate('/scenarios')}
                        style={{ fontSize: '1.125rem', padding: 'var(--spacing-md) var(--spacing-xl)' }}
                    >
                        Start Training
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={() => navigate('/leaderboard')}
                        style={{ fontSize: '1.125rem', padding: 'var(--spacing-md) var(--spacing-xl)' }}
                    >
                        View Leaderboard
                    </button>
                </div>
            </section>

            {/* Features Grid */}
            <section className="container" style={{ paddingBottom: 'var(--spacing-2xl)' }}>
                <div className="grid grid-4" style={{ gap: 'var(--spacing-lg)' }}>
                    {features.map((feature, index) => (
                        <div
                            key={index}
                            className="card fade-in"
                            style={{
                                textAlign: 'center',
                                animationDelay: `${index * 100}ms`
                            }}
                        >
                            <div style={{ fontSize: '3rem', marginBottom: 'var(--spacing-md)' }}>
                                {feature.icon}
                            </div>
                            <h3 style={{ marginBottom: 'var(--spacing-sm)', fontSize: '1.25rem' }}>
                                {feature.title}
                            </h3>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.9375rem' }}>
                                {feature.description}
                            </p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Scenario Types */}
            <section className="container" style={{ paddingBottom: 'var(--spacing-2xl)' }}>
                <h2 className="text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
                    Disaster Scenarios
                </h2>
                <div className="grid grid-3">
                    {[
                        { type: 'Earthquake', emoji: '🌋', color: '#ef4444' },
                        { type: 'Flood', emoji: '🌊', color: '#3b82f6' },
                        { type: 'Cyclone', emoji: '🌪️', color: '#8b5cf6' }
                    ].map((scenario, index) => (
                        <div
                            key={index}
                            className="card"
                            style={{
                                background: `linear-gradient(135deg, ${scenario.color}22 0%, transparent 100%)`,
                                borderLeft: `4px solid ${scenario.color}`,
                                cursor: 'pointer'
                            }}
                            onClick={() => navigate('/scenarios')}
                        >
                            <div style={{ fontSize: '3rem', marginBottom: 'var(--spacing-sm)' }}>
                                {scenario.emoji}
                            </div>
                            <h3>{scenario.type}</h3>
                            <p style={{ color: 'var(--text-muted)' }}>
                                Practice response strategies for {scenario.type.toLowerCase()} disasters
                            </p>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            <section
                style={{
                    background: 'linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%)',
                    padding: 'var(--spacing-2xl) 0',
                    textAlign: 'center'
                }}
            >
                <div className="container">
                    <h2 style={{ marginBottom: 'var(--spacing-md)', fontSize: '2rem' }}>
                        Ready to Make a Difference?
                    </h2>
                    <p style={{ fontSize: '1.125rem', marginBottom: 'var(--spacing-xl)', maxWidth: '600px', margin: '0 auto var(--spacing-xl)' }}>
                        Join emergency planners worldwide in honing disaster response skills
                    </p>
                    <button
                        className="btn btn-primary"
                        onClick={() => navigate('/scenarios')}
                        style={{
                            fontSize: '1.125rem',
                            padding: 'var(--spacing-md) var(--spacing-2xl)',
                            background: 'white',
                            color: '#1e3a8a'
                        }}
                    >
                        Begin Simulation
                    </button>
                </div>
            </section>
        </div>
    );
};

export default Homepage;
