export interface DashboardData {
  name: string;
  plan: 'FREE' | 'PRO';
  daily_usage?: number;     // Optional, only for FREE
  remaining_attempts?: number; // Optional, only for FREE
}