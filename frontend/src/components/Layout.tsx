import { Outlet } from 'react-router-dom'
import Header from './Header'

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-6">
        <Outlet />
      </main>
      <footer className="bg-white border-t border-avito-border py-6 text-center text-xs text-avito-muted">
        © 2026 DenDona Avito
      </footer>
    </div>
  )
}