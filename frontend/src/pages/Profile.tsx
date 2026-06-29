import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getMe, updateProfile } from '../api/auth'
import { uploadImage } from '../api/upload'
import { useAuthStore } from '../store/auth'

export default function Profile() {
  const navigate = useNavigate()
  const { user, setUser, logout } = useAuthStore()
  const [form, setForm] = useState({ phone: '', avatar_url: '' })
  const [saving, setSaving] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    setForm({ phone: user.phone || '', avatar_url: user.avatar_url || '' })
  }, [user])

  const handleAvatarUpload = async (file: File) => {
    setUploading(true)
    try {
      const url = await uploadImage(file)
      setForm(f => ({ ...f, avatar_url: url }))
    } finally { setUploading(false) }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    try {
      await updateProfile({ phone: form.phone || undefined, avatar_url: form.avatar_url || undefined })
      const updated = await getMe()
      setUser(updated)
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } finally { setSaving(false) }
  }

  if (!user) return null

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Профиль</h1>

      <div className="card p-6">
        <form onSubmit={handleSubmit} className="space-y-5">
          {success && <div className="bg-green-50 text-green-700 text-sm p-3 rounded-lg">Профиль обновлён</div>}

          <div className="flex items-center gap-4">
            <div
              className="w-20 h-20 rounded-full overflow-hidden bg-avito-blue flex items-center justify-center cursor-pointer hover:opacity-90 transition-opacity flex-shrink-0"
              onClick={() => document.getElementById('avatar-input')?.click()}
            >
              {form.avatar_url ? (
                <img src={form.avatar_url} alt="" className="w-full h-full object-cover" />
              ) : (
                <span className="text-white text-2xl font-bold">{user.username[0].toUpperCase()}</span>
              )}
            </div>
            <div>
              <p className="font-semibold text-lg">{user.username}</p>
              <p className="text-sm text-avito-muted">{user.email}</p>
              <button
                type="button"
                disabled={uploading}
                onClick={() => document.getElementById('avatar-input')?.click()}
                className="text-xs text-avito-blue hover:underline mt-1"
              >
                {uploading ? 'Загрузка...' : 'Изменить фото'}
              </button>
              <input id="avatar-input" type="file" accept="image/*" className="hidden"
                onChange={e => e.target.files?.[0] && handleAvatarUpload(e.target.files[0])} />
            </div>
          </div>

          <div>
            <label className="label">Телефон</label>
            <input className="input" type="tel" value={form.phone} onChange={e => setForm(f => ({ ...f, phone: e.target.value }))} placeholder="+7 (999) 000-00-00" />
          </div>

          <button type="submit" disabled={saving} className="btn-primary w-full py-3">
            {saving ? 'Сохранение...' : 'Сохранить'}
          </button>
        </form>
      </div>

      <div className="card p-6">
        <h2 className="font-semibold mb-3">Безопасность</h2>
        <button onClick={() => { logout(); navigate('/') }} className="text-red-500 text-sm hover:underline">Выйти из аккаунта</button>
      </div>
    </div>
  )
}
