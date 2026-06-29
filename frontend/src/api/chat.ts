import api from './client'
import type { Conversation, Message } from '../types'

export const fetchConversations = () =>
  api.get<Conversation[]>('/chat/conversations').then(r => r.data)

export const createConversation = (seller_id: number, post_id: number) =>
  api.post<Conversation>('/chat/conversations', { seller_id, post_id }).then(r => r.data)

export const fetchMessages = (conversationId: number) =>
  api.get<Message[]>(`/chat/conversations/${conversationId}/messages`).then(r => r.data)

export const sendMessage = (conversationId: number, text: string) =>
  api.post<Message>(`/chat/conversations/${conversationId}/messages`, { text }).then(r => r.data)