export type UserRole = 'employees' | 'moderator' | 'administrator'
export type PostStatus = 'active' | 'sold' | 'archived' | 'moderation'
export type PostCondition = 'new' | 'used'

export interface User {
  id: number
  username: string
  email: string | null
  phone: string | null
  avatar_url: string | null
}

export interface Category {
  id: number
  name: string
  parent_id: number | null
  created_at: string
}

export interface Post {
  id: number
  title: string
  description: string | null
  image_url: string | null
  price: number | null
  city: string | null
  status: PostStatus
  condition: PostCondition | null
  category_id: number | null
  created_by_id: number
  created_at: string
  updated_at: string | null
  deleted_at: string | null
}

export interface PaginatedPosts {
  items: Post[]
  total: number
  page: number
  limit: number
}

export interface PostImage {
  id: number
  post_id: number
  url: string
  order: number
}

export interface Favorite {
  id: number
  user_id: number
  post_id: number
  created_at: string
}

export interface Conversation {
  id: number
  buyer_id: number
  seller_id: number
  post_id: number
  created_at: string
}

export interface Message {
  id: number
  conversation_id: number
  sender_id: number
  text: string
  is_read: boolean
  created_at: string
}

export interface Review {
  id: number
  from_user_id: number
  to_user_id: number
  rating: number
  text: string | null
  created_at: string
}

export interface RatingSummary {
  to_user_id: number
  average_rating: number
  total_reviews: number
}

export interface PostFilters {
  category_id?: number
  city?: string
  min_price?: number
  max_price?: number
  condition?: PostCondition
  status?: PostStatus
  q?: string
  page?: number
  limit?: number
}