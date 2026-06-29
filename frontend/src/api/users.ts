import api from './client'
import type { User } from '../types'

export const fetchUser = (id: number) => api.get<User>(`/users/${id}`).then(r => r.data)
