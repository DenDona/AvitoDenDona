import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchFavorites } from '../api/favorites'
import { fetchPost } from '../api/posts'
import PostCard from '../components/PostCard'
import { useAuthStore } from '../store/auth'
import type { Post } from '../types'

export default function Favorites() {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    fetchFavorites()
      .then(favs => Promise.all(favs.map(f => fetchPost(f.post_id))))
      .then(setPosts)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Избранное</h1>
      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
          {Array.from({ length: 4 }).map((_, i) => <div key={i} className="card animate-pulse h-60" />)}
        </div>
      ) : posts.length === 0 ? (
        <div className="text-center py-20 text-avito-muted">
          <div className="text-5xl mb-4">♡</div>
          <p className="text-lg">В избранном пока ничего нет</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
          {posts.map(p => <PostCard key={p.id} post={p} />)}
        </div>
      )}
    </div>
  )
}
