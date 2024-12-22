export interface SParameter {
  id: number;
  file: number;
  frequency: number;
  value: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ParameterHistory {
  id: number;
  parameter: number;
  operation: string;
  details: Record<string, any>;
  created_at: string;
  updated_at: string;
}