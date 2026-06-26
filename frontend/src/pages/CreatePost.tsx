import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createPost, updatePost, fetchPost } from '../api/posts'
import { fetchCategories } from '../api/categories'
import { uploadImage } from '../api/upload'
import { useAuthStore } from '../store/auth'
import type { Category, PostCondition, PostStatus } from '../types'

export default function CreatePost() {
  const { id } = useParams<{ id: string }>()
  const isEdit = Boolean(id)
  const navigate = useNavigate()
  const { user } = useAuthStore()

  const [categories, setCategories] = useState<Category[]>([])
  const [uploading, setUploading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const [form, setForm] = useState({
    title: '',
    description: '',
    price: '',
    city: '',
    condition: '' as PostCondition | '',
    status: 'active' as PostStatus,
    category_id: '' as string,
    image_url: '',
  })

  useEffect(() => {
    if (!user) navigate('/login')
    fetchCategories().then(setCategories)
    if (isEdit && id) {
      fetchPost(Number(id)).then(p => {
        setForm({
          title: p.title,
          description: p.description || '',
          price: p.price != null ? String(p.price) : '',
          city: p.city || '',
          condition: p.condition || '',
          status: p.status,
          category_id: p.category_id ? String(p.category_id) : '',
          image_url: p.image_url || '',
        })
      })
    }
  }, [])

  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }))

  const handleImageUpload = async (file: File) => {
    setUploading(true)
    try { set('image_url', await uploadImage(file)) }
    catch { setError('Ошибка загрузки изображения') }
    finally { setUploading(false) }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.title.trim()) { setError('Введите заголовок'); return }
    setSaving(true)
    setError('')
    try {
      const data = {
        title: form.title,
        description: form.description || undefined,
        price: form.price ? Number(form.price) : undefined,
        city: form.city || undefined,
        condition: form.condition || undefined,
        status: form.status,
        category_id: form.category_id ? Number(form.category_id) : undefined,
        image_url: form.image_url || undefined,
      }
      if (isEdit && id) {
        await updatePost(Number(id), data)
        navigate(`/posts/${id}`)
      } else {
        const p = await createPost(data)
        navigate(`/posts/${p.id}`)
      }
    } catch {
      setError('Ошибка сохранения')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">{isEdit ? 'Редактировать объявление' : 'Новое объявление'}</h1>

      <form onSubmit={handleSubmit} className="card p-6 space-y-5">
        {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>}

        <div>
          <label className="label">Заголовок *</label>
          <input className="input" value={form.title} onChange={e => set('title', e.target.value)} placeholder="Название товара или услуги" maxLength={64} required />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="label">Категория</label>
            <select className="input" value={form.category_id} onChange={e => set('category_id', e.target.value)}>
              <option value="">Выберите категорию</option>
              {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>
          <div>
            <label className="label">Состояние</label>
            <select className="input" value={form.condition} onChange={e => set('condition', e.target.value)}>
              <option value="">Не указано</option>
              <option value="new">Новый</option>
              <option value="used">Б/у</option>
            </select>
          </div>
        </div>

        <div>
          <label className="label">Описание</label>
          <textarea className="input resize-none" rows={5} value={form.description} onChange={e => set('description', e.target.value)} placeholder="Опишите товар подробнее" />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="label">Цена, ₽</label>
            <input className="input" type="number" min={0} value={form.price} onChange={e => set('price', e.target.value)} placeholder="0 — договорная" />
          </div>
          <div>
            <label className="label">Местонахождение</label>
            <input className="input" value={form.city} onChange={e => set('city', e.target.value)} placeholder="Например: Москва" />
          </div>
        </div>

        {isEdit && (
          <div>
            <label className="label">Статус</label>
            <select className="input" value={form.status} onChange={e => set('status', e.target.value as PostStatus)}>
              <option value="active">Активно</option>
              <option value="sold">Продано</option>
              <option value="archived">Архив</option>
            </select>
          </div>
        )}

        <div>
          <label className="label">Фото</label>
          <div className="border-2 border-dashed border-avito-border rounded-xl p-6 text-center cursor-pointer hover:border-avito-blue transition-colors"
            onClick={() => document.getElementById('file-input')?.click()}>
            {form.image_url ? (
              <img src={form.image_url} alt="" className="h-40 mx-auto object-contain rounded-lg" />
            ) : (
              <div className="text-avito-muted">
                <div className="text-3xl mb-2">📷</div>
                <p className="text-sm">{uploading ? 'Загрузка...' : 'Нажмите чтобы загрузить фото'}</p>
              </div>
            )}
            <input id="file-input" type="file" accept="image/*" className="hidden"
              onChange={e => e.target.files?.[0] && handleImageUpload(e.target.files[0])} />
          </div>
          {form.image_url && (
            <input className="input mt-2 text-xs" value={form.image_url} onChange={e => set('image_url', e.target.value)} placeholder="URL изображения" />
          )}
        </div>

        <div className="flex gap-3 pt-2">
          <button type="submit" disabled={saving || uploading} className="btn-primary flex-1 py-3 text-base">
            {saving ? 'Сохранение...' : isEdit ? 'Сохранить' : 'Разместить объявление'}
          </button>
          <button type="button" onClick={() => navigate(-1)} className="btn-secondary px-6">Отмена</button>
        </div>
      </form>
    </div>
  )
}