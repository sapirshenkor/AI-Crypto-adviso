import type {
  AuthUser,
  LoginCredentials,
  LoginResponse,
  SignupCredentials,
  SignupResponse,
} from '../types/auth'
import apiClient from './apiClient'

export async function signup(
  credentials: SignupCredentials,
): Promise<SignupResponse> {
  const response = await apiClient.post<SignupResponse>(
    '/api/auth/signup',
    credentials,
  )
  return response.data
}

export async function login(
  credentials: LoginCredentials,
): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>(
    '/api/auth/login',
    credentials,
  )
  return response.data
}

export async function getCurrentUser(): Promise<AuthUser> {
  const response = await apiClient.get<AuthUser>('/api/auth/me')
  return response.data
}
