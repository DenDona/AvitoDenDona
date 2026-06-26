import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'

export default function Header() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)

  const closeAll = () => { setMenuOpen(false); setSearchOpen(false) }

  const handleLogout = () => {
    logout()
    navigate('/')
    closeAll()
  }

  const submitSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const q = (e.currentTarget.elements.namedItem('q') as HTMLInputElement).value
    navigate(`/?q=${encodeURIComponent(q)}`)
    closeAll()
  }

  return (
    <header className="bg-white border-b border-avito-border sticky top-0 z-50 relative">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center gap-4">
        {/* Logo */}
        <Link to="/" className="flex-shrink-0" onClick={closeAll}>
          <span className="text-2xl font-bold">
            <span className="text-avito-blue">avi</span>
            <span className="text-avito-orange">to</span>
          </span>
        </Link>

        {/* Search (desktop) */}
        <form className="flex-1 hidden lg:flex gap-2" onSubmit={submitSearch}>
          <input name="q" className="input flex-1" placeholder="Поиск по объявлениям" />
          <button type="submit" className="btn-primary px-5">Найти</button>
        </form>

        {/* Nav (desktop) */}
        <nav className="hidden lg:flex items-center gap-3 text-sm flex-shrink-0 ml-auto">
          {user ? (
            <>
              <Link to="/favorites" className="text-avito-muted hover:text-avito-blue">♡ Избранное</Link>
              <Link to="/chat" className="text-avito-muted hover:text-avito-blue">💬 Сообщения</Link>
              <Link to="/profile" className="text-avito-muted hover:text-avito-blue font-medium">{user.username}</Link>
              <button onClick={handleLogout} className="text-avito-muted hover:text-red-500 text-xs">Выйти</button>
              <Link to="/posts/create" className="btn-orange text-sm py-1.5 px-3">+ Разместить</Link>
            </>
          ) : (
            <>
              <Link to="/login" className="text-avito-blue font-medium">Войти</Link>
              <Link to="/register" className="btn-primary text-sm py-1.5 px-3">Зарегистрироваться</Link>
            </>
          )}
        </nav>

        {/* Mobile controls */}
        <div className="flex items-center gap-1 lg:hidden ml-auto flex-shrink-0">
          <button
            aria-label="Поиск"
            onClick={() => { setSearchOpen(o => !o); setMenuOpen(false) }}
            className="p-2 text-avito-text text-lg"
          >
            🔍
          </button>
          {user && (
            <Link to="/posts/create" className="btn-orange text-xs py-1.5 px-2.5 whitespace-nowrap" onClick={closeAll}>
              + Подать
            </Link>
          )}
          <button
            aria-label="Меню"
            onClick={() => { setMenuOpen(o => !o); setSearchOpen(false) }}
            className="p-2 text-avito-text text-lg leading-none"
          >
            {menuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* Mobile search overlay */}
      {searchOpen && (
        <form
          className="lg:hidden absolute top-full left-0 right-0 bg-white border-b border-avito-border p-3 flex gap-2 shadow-md"
          onSubmit={submitSearch}
        >
          <input name="q" className="input flex-1" placeholder="Поиск по объявлениям" autoFocus />
          <button type="submit" className="btn-primary px-4">Найти</button>
        </form>
      )}

      {/* Mobile nav dropdown */}
      {menuOpen && (
        <nav className="lg:hidden absolute top-full left-0 right-0 bg-white border-b border-avito-border shadow-md px-4 py-3 flex flex-col gap-3 text-sm">
          {user ? (
            <>
              <Link to="/profile" className="font-medium text-avito-text" onClick={closeAll}>{user.username}</Link>
              <Link to="/favorites" className="text-avito-muted" onClick={closeAll}>♡ Избранное</Link>
              <Link to="/chat" className="text-avito-muted" onClick={closeAll}>💬 Сообщения</Link>
              <button onClick={handleLogout} className="text-left text-red-500">Выйти</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-avito-blue font-medium" onClick={closeAll}>Войти</Link>
              <Link to="/register" className="text-avito-blue font-medium" onClick={closeAll}>Зарегистрироваться</Link>
            </>
          )}
        </nav>
      )}
    </header>
  )
}
