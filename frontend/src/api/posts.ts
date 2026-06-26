import api from './client'
import type { Post, PaginatedPosts, PostFilters, PostImage } from '../types'

export const fetchPosts = (filters: PostFilters = {}) =>
  api.get<PaginatedPosts>('/posts/', { params: filters }).then(r => r.data)

export const fetchPost = (id: number) =>
  api.get<Post>(`/posts/${id}`).then(r => r.data)

export const createPost = (data: Partial<Post>) =>
  api.post<Post>('/posts/', data).then(r => r.data)

export const updatePost = (id: number, data: Partial<Post>) =>
  api.patch<Post>(`/posts/${id}`, data).then(r => r.data)

export const deletePost = (id: number) =>
  api.delete(`/posts/${id}`)

export const fetchPostImages = (postId: number) =>
  api.get<PostImage[]>(`/posts/${postId}/images/`).then(r => r.data)

export const addPostImage = (postId: number, url: string, order = 0) =>
  api.post<PostImage>(`/posts/${postId}/images/`, { url, order }).then(r => r.data)

export const deletePostImage = (postId: number, imageId: number) =>
  api.delete(`/posts/${postId}/images/${imageId}`)