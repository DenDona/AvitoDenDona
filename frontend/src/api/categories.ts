import api from './client'
import type { Category } from '../types'

export const fetchCategories = () =>
  api.get<Category[]>('/categories/').then(r => r.data)

export const fetchCategory = (id: number) =>
  api.get<Category>(`/categories/${id}`).then(r => r.data)

export const createCategory = (data: { name: string; parent_id?: number }) =>
  api.post<Category>('/categories/', data).then(r => r.data)

export const deleteCategory = (id: number) =>
  api.delete(`/categories/${id}`)