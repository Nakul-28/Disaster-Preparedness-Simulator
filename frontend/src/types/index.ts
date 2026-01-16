/**
 * TypeScript types and interfaces for the Disaster Preparedness Simulator
 */

export enum DisasterType {
    EARTHQUAKE = "earthquake",
    FLOOD = "flood",
    CYCLONE = "cyclone",
    WILDFIRE = "wildfire"
}

export enum DifficultyLevel {
    EASY = "easy",
    MEDIUM = "medium",
    HARD = "hard",
    EXPERT = "expert"
}

export enum SimulationStatus {
    PENDING = "pending",
    RUNNING = "running",
    PAUSED = "paused",
    COMPLETED = "completed",
    FAILED = "failed"
}

export enum SimulationMode {
    MANUAL = "manual",
    AI_ASSISTED = "ai_assisted",
    AI_ONLY = "ai_only",
    COMPARISON = "comparison"
}

export interface Location {
    lat: number;
    lon: number;
}

export interface Zone {
    id: string;
    center: Location;
    radius_km: number;
    population: number;
    evacuated: number;
    casualties: number;
}

export interface Shelter {
    id: string;
    location: Location;
    capacity: number;
    current_occupancy: number;
    supplies: Record<string, number>;
}

export interface Resource {
    id: string;
    type: string;
    location: Location;
    capacity: number;
    current_load: number;
}

export interface Road {
    id: string;
    start: Location;
    end: Location;
    status: number;
    length_km: number;
}

export interface Scenario {
    id?: string;
    name: string;
    description: string;
    disaster_type: DisasterType;
    difficulty: DifficultyLevel;
    zones: Zone[];
    shelters: Shelter[];
    roads: Road[];
    resources: Resource[];
    max_timesteps: number;
    timestep_minutes: number;
    disaster_intensity: number;
    secondary_hazards: boolean;
    created_at?: string;
    created_by?: string;
}

export interface Action {
    timestep: number;
    action_type: number;
    resource_id: number;
    target_zone_id: number;
    success: boolean;
    source: "human" | "ai";
}

export interface SimulationState {
    timestep: number;
    zone_populations: number[];
    zone_evacuated: number[];
    zone_casualties: number[];
    shelter_occupancy: number[];
    total_casualties: number;
    total_evacuated: number;
    observation: number[];
}

export interface Simulation {
    id?: string;
    scenario_id: string;
    mode: SimulationMode;
    status: SimulationStatus;
    current_timestep: number;
    max_timesteps: number;
    actions: Action[];
    states: SimulationState[];
    final_casualties?: number;
    final_evacuated?: number;
    final_score?: number;
    created_at?: string;
    completed_at?: string;
    user_id?: string;
}

export interface SimulationMetrics {
    total_casualties: number;
    total_evacuated: number;
    evacuation_rate: number;
    avg_response_time: number;
    resources_efficiency: number;
    overall_score: number;
    ai_casualties?: number;
    ai_evacuated?: number;
    performance_vs_ai?: number;
}

export interface AIActionResponse {
    action: number[];
    confidence: number;
    explanation: string;
}

export interface LeaderboardEntry {
    rank: number;
    user_id: string;
    username: string;
    scenario_id: string;
    score: number;
    casualties: number;
    evacuated: number;
    evacuation_rate: number;
    completed_at: string;
}

export interface PerformanceStats {
    total_simulations: number;
    avg_score: number;
    avg_casualties: number;
    avg_evacuation_rate: number;
    best_score: number;
    scenarios_completed: number;
}
