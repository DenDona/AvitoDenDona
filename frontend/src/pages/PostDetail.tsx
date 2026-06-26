import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { fetchPost, fetchPostImages, deletePost } from '../api/posts'
import { addFavorite, removeFavorite, fetchFavorites } from '../api/favorites'
import { createConversation } from '../api/chat'
import { fetchReviews, getRatingSummary } from '../api/reviews'
import { fetchUser } from '../api/users'
import { useAuthStore } from '../store/auth'
import StarRating from '../components/StarRating'
import type { Post, PostImage, Review, RatingSummary, User } from '../types'
import { NO_IMAGE } from '../lib/placeholder'

const CONDITION_LABELS: Record<string, string> = { new: 'Новый', used: 'Б/у' }
const STATUS_LABELS: Record<string, string> = { active: 'Активно', sold: 'Продано', archived: 'Архив', moderation: 'На проверке' }

export default function PostDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuthStore()

  const [post, setPost] = useState<Post | null>(null)
  const [images, setImages] = useState<PostImage[]>([])
  const [activeImg, setActiveImg] = useState(0)
  const [isFav, setIsFav] = useState(false)
  const [reviews, setReviews] = useState<Review[]>([])
  const [rating, setRating] = useState<RatingSummary | null>(null)
  const [seller, setSeller] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [chatLoading, setChatLoading] = useState(false)

  useEffect(() => {
    if (!id) return
    const pid = Number(id)
    Promise.all([
      fetchPost(pid),
      fetchPostImages(pid),
    ]).then(([p, imgs]) => {
      setPost(p)
      setImages(imgs)
      return Promise.all([
        fetchReviews(p.created_by_id),
        getRatingSummary(p.created_by_id),
        fetchUser(p.created_by_id),
      ])
    }).then(([rev, rat, sel]) => {
      setReviews(rev)
      setRating(rat)
      setSeller(sel)
    }).finally(() => setLoading(false))

    if (user) {
      fetchFavorites().then(favs => setIsFav(favs.some(f => f.post_id === pid)))
    }
  }, [id, user])

  const allImages = post?.image_url
    ? [{ url: post.image_url }, ...images.map(i => ({ url: i.url }))]
    : images.map(i => ({ url: i.url }))

  const toggleFav = async () => {
    if (!post) return
    if (isFav) { await removeFavorite(post.id); setIsFav(false) }
    else { await addFavorite(post.id); setIsFav(true) }
  }

  const handleChat = async () => {
    if (!post || !user) { navigate('/login'); return }
    setChatLoading(true)
    const conv = await createConversation(post.created_by_id, post.id)
    navigate(`/chat/${conv.id}`)
  }

  const handleDelete = async () => {
    if (!post || !confirm('Удалить объявление?')) return
    await deletePost(post.id)
    navigate('/')
  }

  if (loading) return <div className="animate-pulse space-y-4"><div className="h-96 bg-gray-200 rounded-xl" /></div>
  if (!post) return <div className="text-center py-20 text-avito-muted">Объявление не найдено</div>

  const isOwner = user?.id === post.created_by_id

  return (
    <div className="flex flex-col lg:flex-row gap-6 lg:gap-8">
      {/* Left */}
      <div className="flex-1 min-w-0 space-y-6">
        {/* Images */}
        <div className="card overflow-hidden">
          <div className="aspect-video bg-gray-100">
            <img
              src={allImages[activeImg]?.url || NO_IMAGE}
              alt={post.title}
              className="w-full h-full object-contain"
              onError={(e) => { (e.target as HTMLImageElement).src = NO_IMAGE }}
            />
          </div>
          {allImages.length > 1 && (
            <div className="flex gap-2 p-3 overflow-x-auto">
              {allImages.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setActiveImg(i)}
                  className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-colors ${i === activeImg ? 'border-avito-blue' : 'border-transparent'}`}
                >
                  <img src={img.url} alt="" className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Title & Info */}
        <div className="card p-4 sm:p-6">
          <div className="flex flex-col-reverse sm:flex-row sm:items-start sm:justify-between gap-2 sm:gap-4">
            <div className="min-w-0">
              <h1 className="text-xl sm:text-2xl font-bold break-words">{post.title}</h1>
              <div className="flex items-center gap-2 sm:gap-3 mt-1 text-xs sm:text-sm text-avito-muted flex-wrap">
                <span>{post.city || 'Россия'}</span>
                <span>•</span>
                <span>{new Date(post.created_at).toLocaleDateString('ru-RU')}</span>
                {post.condition && <><span>•</span><span>{CONDITION_LABELS[post.condition]}</span></>}
                {post.status !== 'active' && (
                  <><span>•</span><span className="text-red-500">{STATUS_LABELS[post.status]}</span></>
                )}
              </div>
            </div>
            <div className="text-xl sm:text-2xl font-bold text-avito-blue flex-shrink-0">
              {post.price != null ? `${Number(post.price).toLocaleString('ru-RU')} ₽` : 'Договорная'}
            </div>
          </div>

          {post.description && (
            <div className="mt-4 pt-4 border-t border-avito-border">
              <h3 className="font-semibold mb-2">Описание</h3>
              <p className="text-sm text-avito-text leading-relaxed whitespace-pre-wrap">{post.description}</p>
            </div>
          )}
        </div>

        {/* Seller Reviews */}
        {reviews.length > 0 && (
          <div className="card p-6">
            <div className="flex items-center gap-3 mb-4">
              <h3 className="font-semibold">Отзывы о продавце</h3>
              {rating && (
                <div className="flex items-center gap-1">
                  <StarRating rating={rating.average_rating} />
                  <span className="text-sm text-avito-muted">{rating.average_rating.toFixed(1)} ({rating.total_reviews})</span>
                </div>
              )}
            </div>
            <div className="space-y-3">
              {reviews.slice(0, 5).map(r => (
                <div key={r.id} className="border-b border-avito-border pb-3 last:border-0">
                  <div className="flex items-center gap-2 mb-1">
                    <StarRating rating={r.rating} />
                    <span className="text-xs text-avito-muted">{new Date(r.created_at).toLocaleDateString('ru-RU')}</span>
                  </div>
                  {r.text && <p className="text-sm text-avito-text">{r.text}</p>}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Right sidebar */}
      <div className="w-full lg:w-72 flex-shrink-0 space-y-4">
        <div className="card p-4 space-y-3">
          {isOwner ? (
            <>
              <Link to={`/posts/${post.id}/edit`} className="btn-primary w-full block text-center">Редактировать</Link>
              <button onClick={handleDelete} className="w-full border border-red-300 text-red-500 px-4 py-2 rounded-lg text-sm hover:bg-red-50 transition-colors">Удалить</button>
            </>
          ) : (
            <>
              <button onClick={handleChat} disabled={chatLoading} className="btn-primary w-full">
                {chatLoading ? 'Загрузка...' : 'Написать продавцу'}
              </button>
              <button onClick={toggleFav} className={`w-full border px-4 py-2 rounded-lg text-sm transition-colors ${isFav ? 'border-red-300 text-red-500 bg-red-50' : 'border-avito-border text-avito-muted hover:border-avito-blue hover:text-avito-blue'}`}>
                {isFav ? '♥ В избранном' : '♡ Добавить в избранное'}
              </button>
            </>
          )}
        </div>

        <div className="card p-4">
          <h3 className="font-semibold mb-3 text-sm">Продавец</h3>
          <Link to={`/users/${post.created_by_id}`} className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <div className="w-10 h-10 rounded-full bg-avito-blue overflow-hidden flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
              {seller?.avatar_url ? (
                <img src={seller.avatar_url} alt="" className="w-full h-full object-cover" />
              ) : (
                seller?.username[0]?.toUpperCase() ?? post.created_by_id
              )}
            </div>
            <div className="min-w-0">
              <p className="text-sm font-medium truncate">{seller?.username ?? `Продавец #${post.created_by_id}`}</p>
              {rating && rating.total_reviews > 0 && (
                <div className="flex items-center gap-1 mt-0.5">
                  <StarRating rating={rating.average_rating} />
                  <span className="text-xs text-avito-muted">({rating.total_reviews})</span>
                </div>
              )}
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
}