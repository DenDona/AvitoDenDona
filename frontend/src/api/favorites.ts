import api from './client'
import type { Favorite } from '../types'

export const fetchFavorites = () =>
  api.get<Favorite[]>('/favorites/').then(r => r.data)

export const addFavorite = (postId: number) =>
  api.post<Favorite>(`/favorites/${postId}`).then(r => r.data)

export const removeFavorite = (postId: number) =>
  api.delete(`/favorites/${postId}`)