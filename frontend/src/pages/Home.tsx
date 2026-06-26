import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { fetchPosts } from '../api/posts'
import { fetchCategories } from '../api/categories'
import PostCard from '../components/PostCard'
import type { Post, Category, PostCondition } from '../types'

const CITIES = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Нижний Новгород', 'Краснодар']

export default function Home() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [posts, setPosts] = useState<Post[]>([])
  const [total, setTotal] = useState(0)
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)

  const page = Number(searchParams.get('page') || 1)
  const q = searchParams.get('q') || ''
  const categoryId = searchParams.get('category_id') ? Number(searchParams.get('category_id')) : undefined
  const city = searchParams.get('city') || undefined
  const minPrice = searchParams.get('min_price') ? Number(searchParams.get('min_price')) : undefined
  const maxPrice = searchParams.get('max_price') ? Number(searchParams.get('max_price')) : undefined
  const condition = (searchParams.get('condition') as PostCondition) || undefined

  useEffect(() => {
    fetchCategories().then(setCategories).catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    fetchPosts({ page, q: q || undefined, category_id: categoryId, city, min_price: minPrice, max_price: maxPrice, condition, limit: 20 })
      .then(d => { setPosts(d.items); setTotal(d.total) })
      .finally(() => setLoading(false))
  }, [searchParams.toString()])

  const set = (key: string, value: string | undefined) => {
    const p = new URLSearchParams(searchParams)
    if (value) p.set(key, value)
    else p.delete(key)
    p.delete('page')
    setSearchParams(p)
  }

  const totalPages = Math.ceil(total / 20)

  return (
    <div className="flex gap-6">
      {/* Sidebar */}
      <aside className="w-60 flex-shrink-0 space-y-4">
        <div className="card p-4 space-y-3">
          <h3 className="font-semibold text-sm text-avito-muted uppercase tracking-wide">Категории</h3>
          <button
            onClick={() => set('category_id', undefined)}
            className={`block w-full text-left text-sm py-1 px-2 rounded hover:bg-blue-50 transition-colors ${!categoryId ? 'text-avito-blue font-medium bg-blue-50' : 'text-avito-text'}`}
          >
            Все категории
          </button>
          {categories.map(c => (
            <button
              key={c.id}
              onClick={() => set('category_id', String(c.id))}
              className={`block w-full text-left text-sm py-1 px-2 rounded hover:bg-blue-50 transition-colors ${categoryId === c.id ? 'text-avito-blue font-medium bg-blue-50' : 'text-avito-text'}`}
            >
              {c.name}
            </button>
          ))}
        </div>

        <div className="card p-4 space-y-3">
          <h3 className="font-semibold text-sm text-avito-muted uppercase tracking-wide">Цена, ₽</h3>
          <div className="flex gap-2">
            <input
              className="input text-xs"
              placeholder="От"
              type="number"
              defaultValue={minPrice}
              onBlur={e => set('min_price', e.target.value || undefined)}
            />
            <input
              className="input text-xs"
              placeholder="До"
              type="number"
              defaultValue={maxPrice}
              onBlur={e => set('max_price', e.target.value || undefined)}
            />
          </div>
        </div>

        <div className="card p-4 space-y-3">
          <h3 className="font-semibold text-sm text-avito-muted uppercase tracking-wide">Город</h3>
          <select className="input text-sm" value={city || ''} onChange={e => set('city', e.target.value || undefined)}>
            <option value="">Все города</option>
            {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="card p-4 space-y-3">
          <h3 className="font-semibold text-sm text-avito-muted uppercase tracking-wide">Состояние</h3>
          <select className="input text-sm" value={condition || ''} onChange={e => set('condition', e.target.value as PostCondition || undefined)}>
            <option value="">Любое</option>
            <option value="new">Новый</option>
            <option value="used">Б/у</option>
          </select>
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-lg font-semibold">
            {q ? `Результаты по «${q}»` : 'Объявления'}
            <span className="text-avito-muted font-normal text-sm ml-2">{total.toLocaleString('ru-RU')} шт.</span>
          </h1>
        </div>

        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="aspect-[4/3] bg-gray-200" />
                <div className="p-3 space-y-2">
                  <div className="h-5 bg-gray-200 rounded w-3/4" />
                  <div className="h-4 bg-gray-200 rounded" />
                  <div className="h-3 bg-gray-200 rounded w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-20 text-avito-muted">
            <div className="text-5xl mb-4">🔍</div>
            <p className="text-lg">Объявления не найдены</p>
            <p className="text-sm mt-1">Попробуйте изменить фильтры</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {posts.map(post => <PostCard key={post.id} post={post} />)}
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center gap-2 mt-8">
            {Array.from({ length: Math.min(totalPages, 10) }).map((_, i) => {
              const p = i + 1
              return (
                <button
                  key={p}
                  onClick={() => { const s = new URLSearchParams(searchParams); s.set('page', String(p)); setSearchParams(s) }}
                  className={`w-9 h-9 rounded-lg text-sm font-medium transition-colors ${p === page ? 'bg-avito-blue text-white' : 'bg-white border border-avito-border hover:border-avito-blue text-avito-text'}`}
                >
                  {p}
                </button>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}