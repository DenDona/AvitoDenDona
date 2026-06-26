import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'

export default function Header() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header className="bg-white border-b border-avito-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center gap-4">
        {/* Logo */}
        <Link to="/" className="flex-shrink-0">
          <span className="text-2xl font-bold">
            <span className="text-avito-blue">avi</span>
            <span className="text-avito-orange">to</span>
          </span>
        </Link>

        {/* Search */}
        <form
          className="flex-1 flex gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            const q = (e.currentTarget.elements.namedItem('q') as HTMLInputElement).value
            navigate(`/?q=${encodeURIComponent(q)}`)
          }}
        >
          <input
            name="q"
            className="input flex-1"
            placeholder="Поиск по объявлениям"
          />
          <button type="submit" className="btn-primary px-5">Найти</button>
        </form>

        {/* Nav */}
        <nav className="flex items-center gap-3 text-sm flex-shrink-0">
          {user ? (
            <>
              <Link to="/favorites" className="text-avito-muted hover:text-avito-blue">
                ♡ Избранное
              </Link>
              <Link to="/chat" className="text-avito-muted hover:text-avito-blue">
                💬 Сообщения
              </Link>
              <Link to="/profile" className="text-avito-muted hover:text-avito-blue font-medium">
                {user.username}
              </Link>
              <button onClick={handleLogout} className="text-avito-muted hover:text-red-500 text-xs">
                Выйти
              </button>
              <Link to="/posts/create" className="btn-orange text-sm py-1.5 px-3">
                + Разместить
              </Link>
            </>
          ) : (
            <>
              <Link to="/login" className="text-avito-blue font-medium">Войти</Link>
              <Link to="/register" className="btn-primary text-sm py-1.5 px-3">Зарегистрироваться</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}