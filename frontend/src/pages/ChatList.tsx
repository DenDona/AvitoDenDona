import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { fetchConversations } from '../api/chat'
import { useAuthStore } from '../store/auth'
import type { Conversation } from '../types'

export default function ChatList() {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [convs, setConvs] = useState<Conversation[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    fetchConversations().then(setConvs).finally(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Сообщения</h1>
      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => <div key={i} className="card h-16 animate-pulse" />)}
        </div>
      ) : convs.length === 0 ? (
        <div className="text-center py-20 text-avito-muted">
          <div className="text-5xl mb-4">💬</div>
          <p className="text-lg">Нет активных диалогов</p>
        </div>
      ) : (
        <div className="space-y-2">
          {convs.map(c => (
            <Link key={c.id} to={`/chat/${c.id}`} className="card p-4 flex items-center gap-4 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-full bg-avito-blue flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                {user?.id === c.buyer_id ? c.seller_id : c.buyer_id}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium">
                  {user?.id === c.buyer_id ? `Продавец #${c.seller_id}` : `Покупатель #${c.buyer_id}`}
                </p>
                <p className="text-xs text-avito-muted">Объявление #{c.post_id}</p>
              </div>
              <span className="text-xs text-avito-muted flex-shrink-0">
                {new Date(c.created_at).toLocaleDateString('ru-RU')}
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}