// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: `${API_BASE_URL}/auth/login`,
    REGISTER: `${API_BASE_URL}/auth/register`,
    ME: `${API_BASE_URL}/auth/me`,
    LOGOUT: `${API_BASE_URL}/auth/logout`,
  },
  
  // Agents
  AGENTS: {
    LIST: `${API_BASE_URL}/agents`,
    CREATE: `${API_BASE_URL}/agents`,
    GET: (id: number) => `${API_BASE_URL}/agents/${id}`,
    UPDATE: (id: number) => `${API_BASE_URL}/agents/${id}`,
    DELETE: (id: number) => `${API_BASE_URL}/agents/${id}`,
    EXECUTE: (id: number) => `${API_BASE_URL}/agents/${id}/execute`,
  },
  
  // Teams
  TEAMS: {
    LIST: `${API_BASE_URL}/teams`,
    CREATE: `${API_BASE_URL}/teams`,
    GET: (id: number) => `${API_BASE_URL}/teams/${id}`,
    UPDATE: (id: number) => `${API_BASE_URL}/teams/${id}`,
    DELETE: (id: number) => `${API_BASE_URL}/teams/${id}`,
    ADD_AGENT: (id: number) => `${API_BASE_URL}/teams/${id}/agents`,
    EXECUTE: (id: number) => `${API_BASE_URL}/teams/${id}/execute`,
  },
  
  // Chat
  CHAT: {
    WEBSOCKET: (agentId: number) => `${WS_BASE_URL}/chat/ws/${agentId}`,
  },
  
  // Analytics
  ANALYTICS: {
    DASHBOARD: `${API_BASE_URL}/analytics/dashboard`,
    PERFORMANCE: `${API_BASE_URL}/analytics/performance`,
    TRENDS: `${API_BASE_URL}/analytics/trends`,
  },
  
  // Workflows
  WORKFLOWS: {
    LIST: `${API_BASE_URL}/workflows`,
    CREATE: `${API_BASE_URL}/workflows`,
    GET: (id: number) => `${API_BASE_URL}/workflows/${id}`,
    DELETE: (id: number) => `${API_BASE_URL}/workflows/${id}`,
  },
  
  // Health
  HEALTH: `${API_BASE_URL}/health`,
};

// API Headers
export const getAuthHeaders = (token: string) => ({
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
});

export const getDefaultHeaders = () => ({
  'Content-Type': 'application/json',
});

// API Error Handling
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// API Response Types
export interface APIResponse<T = any> {
  data: T;
  message?: string;
  status: number;
}

// Environment Detection
export const isDevelopment = process.env.NODE_ENV === 'development';
export const isProduction = process.env.NODE_ENV === 'production';

// Logging
export const logAPI = (endpoint: string, method: string, data?: any) => {
  if (isDevelopment) {
    console.log(`API ${method} ${endpoint}`, data);
  }
}; 