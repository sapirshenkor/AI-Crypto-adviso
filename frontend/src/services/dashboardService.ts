import type { DashboardResponse } from '../types/dashboard'
import apiClient from './apiClient'

export async function getDashboard(): Promise<DashboardResponse> {
  const response = await apiClient.get<DashboardResponse>('/api/dashboard')
  return response.data
}
