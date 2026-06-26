import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { fetchMessages, sendMessage } from '../api/chat'
import { useAuthStore } from '../store/auth'
import type { Message } from '../types'

export default function ChatRoom() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user, token } = useAuthStore()
  const [messages, setMessages] = useState<Message[]>([])
  const [text, setText] = useState('')
  const [sending, setSending] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!user || !id) { navigate('/login'); return }
    const cid = Number(id)
    fetchMessages(cid).then(setMessages)

    const apiUrl = import.meta.env.VITE_API_URL ?? '/v1'
    const wsBase = apiUrl.replace(/^https?/, (p) => (p === 'https' ? 'wss' : 'ws'))
    const ws = new WebSocket(`${wsBase}/chat/ws/${cid}?token=${token}`)
    wsRef.current = ws
    ws.onmessage = (e) => {
      try {
        const msg = JSON.parse(e.data) as Message
        setMessages(prev => [...prev, msg])
      } catch {}
    }
    return () => ws.close()
  }, [id])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!text.trim() || !id) return
    setSending(true)
    try {
      const msg = await sendMessage(Number(id), text.trim())
      setMessages(prev => [...prev, msg])
      setText('')
    } finally { setSending(false) }
  }

  return (
    <div className="max-w-2xl mx-auto flex flex-col" style={{ height: 'calc(100vh - 120px)' }}>
      <div className="card flex flex-col flex-1 overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b border-avito-border flex items-center gap-3">
          <button onClick={() => navigate('/chat')} className="text-avito-muted hover:text-avito-blue">← Назад</button>
          <h2 className="font-semibold">Диалог #{id}</h2>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.length === 0 && (
            <div className="text-center text-avito-muted text-sm py-8">Сообщений пока нет</div>
          )}
          {messages.map(m => {
            const isMe = m.sender_id === user?.id
            return (
              <div key={m.id} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-xs lg:max-w-sm rounded-2xl px-4 py-2.5 text-sm ${isMe ? 'bg-avito-blue text-white rounded-br-sm' : 'bg-gray-100 text-avito-text rounded-bl-sm'}`}>
                  <p>{m.text}</p>
                  <p className={`text-xs mt-1 ${isMe ? 'text-blue-200' : 'text-avito-muted'}`}>
                    {new Date(m.created_at).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
                    {isMe && <span className="ml-1">{m.is_read ? '✓✓' : '✓'}</span>}
                  </p>
                </div>
              </div>
            )
          })}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSend} className="p-4 border-t border-avito-border flex gap-3">
          <input
            className="input flex-1"
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="Сообщение..."
            disabled={sending}
            autoFocus
          />
          <button type="submit" disabled={sending || !text.trim()} className="btn-primary px-5">
            Отправить
          </button>
        </form>
      </div>
    </div>
  )
}