export interface ComSimulation {
  id: number;
  name: string;
  parameters: number[];
  configuration: Record<string, any>;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

export interface SimulationHistory {
  id: number;
  simulation: number;
  execution_time: number;
  status: string;
  error_message: string | null;
  created_at: string;
  updated_at: string;
} 