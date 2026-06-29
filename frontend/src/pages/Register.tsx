import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register, login, getMe } from '../api/auth'
import { useAuthStore } from '../store/auth'

export default function Register() {
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()
  const [form, setForm] = useState({ username: '', email: '', password: '', confirm: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (form.password !== form.confirm) { setError('Пароли не совпадают'); return }
    setLoading(true)
    setError('')
    try {
      await register({ username: form.username, email: form.email || undefined, password: form.password })
      const { access_token } = await login({ login: form.username, password: form.password })
      localStorage.setItem('token', access_token)
      const user = await getMe()
      setAuth(user, access_token)
      navigate('/')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Ошибка регистрации')
    } finally {
      setLoading(false)
    }
  }

  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }))

  return (
    <div className="max-w-sm mx-auto mt-12">
      <div className="text-center mb-8">
        <span className="text-4xl font-bold"><span className="text-avito-blue">avi</span><span className="text-avito-orange">to</span></span>
        <p className="text-avito-muted text-sm mt-2">Регистрация</p>
      </div>
      <div className="card p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>}
          <div>
            <label className="label">Имя пользователя</label>
            <input className="input" value={form.username} onChange={e => set('username', e.target.value)} required autoFocus />
          </div>
          <div>
            <label className="label">Email (необязательно)</label>
            <input className="input" type="email" value={form.email} onChange={e => set('email', e.target.value)} />
          </div>
          <div>
            <label className="label">Пароль</label>
            <input className="input" type="password" value={form.password} onChange={e => set('password', e.target.value)} required minLength={6} />
          </div>
          <div>
            <label className="label">Повторите пароль</label>
            <input className="input" type="password" value={form.confirm} onChange={e => set('confirm', e.target.value)} required />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full py-3 text-base mt-2">
            {loading ? 'Регистрация...' : 'Создать аккаунт'}
          </button>
        </form>
        <p className="text-center text-sm text-avito-muted mt-4">
          Уже есть аккаунт?{' '}
          <Link to="/login" className="text-avito-blue hover:underline">Войти</Link>
        </p>
      </div>
    </div>
  )
}