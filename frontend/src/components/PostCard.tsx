import { Link } from 'react-router-dom'
import type { Post } from '../types'

const NO_IMAGE = 'https://via.placeholder.com/300x200?text=Нет+фото'

const CONDITION_LABELS: Record<string, string> = { new: 'Новый', used: 'Б/у' }
const STATUS_COLORS: Record<string, string> = {
  active: 'text-green-600',
  sold: 'text-red-500',
  archived: 'text-gray-400',
  moderation: 'text-yellow-600',
}

export default function PostCard({ post }: { post: Post }) {
  return (
    <Link to={`/posts/${post.id}`} className="card block hover:shadow-md transition-shadow overflow-hidden group">
      <div className="aspect-[4/3] overflow-hidden bg-gray-100">
        <img
          src={post.image_url || NO_IMAGE}
          alt={post.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => { (e.target as HTMLImageElement).src = NO_IMAGE }}
        />
      </div>
      <div className="p-3">
        <div className="font-semibold text-lg text-avito-blue">
          {post.price != null ? `${Number(post.price).toLocaleString('ru-RU')} ₽` : 'Договорная'}
        </div>
        <div className="text-sm text-avito-text line-clamp-2 mt-0.5">{post.title}</div>
        <div className="flex items-center justify-between mt-2 text-xs text-avito-muted">
          <span>{post.city || 'Россия'}</span>
          <span>{new Date(post.created_at).toLocaleDateString('ru-RU')}</span>
        </div>
        {post.condition && (
          <span className="inline-block mt-1 text-xs bg-gray-100 text-avito-muted rounded px-1.5 py-0.5">
            {CONDITION_LABELS[post.condition]}
          </span>
        )}
        {post.status !== 'active' && (
          <span className={`block text-xs mt-1 font-medium ${STATUS_COLORS[post.status]}`}>
            {post.status === 'sold' ? 'Продано' : post.status === 'archived' ? 'Архив' : 'На проверке'}
          </span>
        )}
      </div>
    </Link>
  )
}