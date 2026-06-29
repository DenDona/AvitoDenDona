import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchReviews, getRatingSummary, createReview } from '../api/reviews'
import { fetchUser } from '../api/users'
import { useAuthStore } from '../store/auth'
import StarRating from '../components/StarRating'
import type { Review, RatingSummary, User } from '../types'

export default function UserPublicProfile() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuthStore()
  const [profile, setProfile] = useState<User | null>(null)
  const [reviews, setReviews] = useState<Review[]>([])
  const [rating, setRating] = useState<RatingSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [myRating, setMyRating] = useState(5)
  const [myText, setMyText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const userId = Number(id)

  useEffect(() => {
    if (!id) return
    Promise.all([fetchReviews(userId), getRatingSummary(userId), fetchUser(userId)])
      .then(([rev, rat, prof]) => { setReviews(rev); setRating(rat); setProfile(prof) })
      .finally(() => setLoading(false))
  }, [id])

  const handleReview = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      const r = await createReview(userId, myRating, myText || undefined)
      setReviews(prev => [r, ...prev])
      setSubmitted(true)
      setMyText('')
      const rat = await getRatingSummary(userId)
      setRating(rat)
    } catch { } finally { setSubmitting(false) }
  }

  const alreadyReviewed = reviews.some(r => r.from_user_id === user?.id)
  const canReview = user && user.id !== userId && !alreadyReviewed && !submitted

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="card p-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-avito-blue overflow-hidden flex items-center justify-center text-white text-2xl font-bold flex-shrink-0">
            {profile?.avatar_url ? (
              <img src={profile.avatar_url} alt="" className="w-full h-full object-cover" />
            ) : (
              profile?.username[0]?.toUpperCase() ?? userId
            )}
          </div>
          <div className="min-w-0">
            <h1 className="text-xl font-bold truncate">{profile?.username ?? `Продавец #${userId}`}</h1>
            {rating && (
              <div className="flex items-center gap-2 mt-1">
                <StarRating rating={rating.average_rating} />
                <span className="text-sm text-avito-muted">{rating.average_rating.toFixed(1)} ({rating.total_reviews} отзывов)</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {canReview && (
        <div className="card p-6">
          <h3 className="font-semibold mb-4">Оставить отзыв</h3>
          <form onSubmit={handleReview} className="space-y-4">
            <div>
              <label className="label">Оценка</label>
              <div className="flex gap-1">
                {[1,2,3,4,5].map(n => (
                  <button type="button" key={n} onClick={() => setMyRating(n)}
                    className={`text-2xl ${n <= myRating ? 'text-yellow-400' : 'text-gray-300'} hover:text-yellow-400 transition-colors`}>
                    ★
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="label">Комментарий (необязательно)</label>
              <textarea className="input resize-none" rows={3} value={myText} onChange={e => setMyText(e.target.value)} placeholder="Напишите о вашем опыте..." />
            </div>
            <button type="submit" disabled={submitting} className="btn-primary">
              {submitting ? 'Отправка...' : 'Отправить отзыв'}
            </button>
          </form>
        </div>
      )}

      <div className="card p-6">
        <h3 className="font-semibold mb-4">Отзывы ({reviews.length})</h3>
        {loading ? (
          <div className="space-y-3">{Array.from({length:3}).map((_,i) => <div key={i} className="h-16 bg-gray-100 rounded animate-pulse" />)}</div>
        ) : reviews.length === 0 ? (
          <p className="text-avito-muted text-sm">Отзывов пока нет</p>
        ) : (
          <div className="space-y-4">
            {reviews.map(r => (
              <div key={r.id} className="border-b border-avito-border pb-4 last:border-0">
                <div className="flex items-center gap-2 mb-1">
                  <div className="w-7 h-7 rounded-full bg-gray-200 flex items-center justify-center text-xs font-medium">{r.from_user_id}</div>
                  <StarRating rating={r.rating} />
                  <span className="text-xs text-avito-muted ml-auto">{new Date(r.created_at).toLocaleDateString('ru-RU')}</span>
                </div>
                {r.text && <p className="text-sm text-avito-text ml-9">{r.text}</p>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}