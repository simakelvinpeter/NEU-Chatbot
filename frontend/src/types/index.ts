export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  avatar?: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  language?: string;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  timestamp: string;
}

export interface QuickLink {
  id: string;
  label: string;
  icon: string;
  url: string;
  active?: boolean;
}

export interface ApiError {
  detail: string;
  status_code: number;
}
