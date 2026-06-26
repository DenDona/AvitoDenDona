import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login, getMe } from '../api/auth'
import { useAuthStore } from '../store/auth'

export default function Login() {
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()
  const [form, setForm] = useState({ login: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const { access_token } = await login(form)
      localStorage.setItem('token', access_token)
      const user = await getMe()
      setAuth(user, access_token)
      navigate('/')
    } catch {
      setError('Неверный логин или пароль')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-12">
      <div className="text-center mb-8">
        <span className="text-4xl font-bold"><span className="text-avito-blue">avi</span><span className="text-avito-orange">to</span></span>
        <p className="text-avito-muted text-sm mt-2">Вход в аккаунт</p>
      </div>
      <div className="card p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>}
          <div>
            <label className="label">Логин или email</label>
            <input className="input" value={form.login} onChange={e => setForm(f => ({ ...f, login: e.target.value }))} required autoFocus />
          </div>
          <div>
            <label className="label">Пароль</label>
            <input className="input" type="password" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} required />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full py-3 text-base mt-2">
            {loading ? 'Вход...' : 'Войти'}
          </button>
        </form>
        <p className="text-center text-sm text-avito-muted mt-4">
          Нет аккаунта?{' '}
          <Link to="/register" className="text-avito-blue hover:underline">Зарегистрироваться</Link>
        </p>
      </div>
    </div>
  )
}