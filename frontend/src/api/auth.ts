import api from './client'
import type { User } from '../types'

export const register = (data: { username: string; email?: string; password: string }) =>
  api.post<User>('/auth/register', data).then(r => r.data)

export const login = (data: { login: string; password: string }) =>
  api.post<{ access_token: string; token_type: string }>('/auth/login', data).then(r => r.data)

export const getMe = () => api.get<User>('/auth/me').then(r => r.data)

export const updateProfile = (data: { phone?: string; avatar_url?: string }) =>
  api.patch<User>('/users/me', data).then(r => r.data)