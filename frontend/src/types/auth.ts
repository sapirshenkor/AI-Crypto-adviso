export interface AuthUser {
  id: string
  name: string
  email: string
  created_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export type SignupResponse = AuthUser

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupCredentials {
  name: string
  email: string
  password: string
}
