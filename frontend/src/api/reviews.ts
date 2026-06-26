import api from './client'
import type { Review, RatingSummary } from '../types'

export const fetchReviews = (userId: number) =>
  api.get<Review[]>(`/reviews/users/${userId}`).then(r => r.data)

export const getRatingSummary = (userId: number) =>
  api.get<RatingSummary>(`/reviews/users/${userId}/rating`).then(r => r.data)

export const createReview = (userId: number, rating: number, text?: string) =>
  api.post<Review>(`/reviews/users/${userId}`, { rating, text }).then(r => r.data)