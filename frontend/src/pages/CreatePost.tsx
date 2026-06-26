import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createPost, updatePost, fetchPost, fetchPostImages, addPostImage, deletePostImage } from '../api/posts'
import { fetchCategories } from '../api/categories'
import { uploadImage } from '../api/upload'
import { useAuthStore } from '../store/auth'
import type { Category, PostCondition, PostImage, PostStatus } from '../types'

const MAX_IMAGES = 8

export default function CreatePost() {
  const { id } = useParams<{ id: string }>()
  const isEdit = Boolean(id)
  const navigate = useNavigate()
  const { user } = useAuthStore()

  const [categories, setCategories] = useState<Category[]>([])
  const [images, setImages] = useState<string[]>([])
  const [existingImages, setExistingImages] = useState<PostImage[]>([])
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
  })

  useEffect(() => {
    if (!user) navigate('/login')
    fetchCategories().then(setCategories)
    if (isEdit && id) {
      const pid = Number(id)
      Promise.all([fetchPost(pid), fetchPostImages(pid)]).then(([p, imgs]) => {
        setForm({
          title: p.title,
          description: p.description || '',
          price: p.price != null ? String(p.price) : '',
          city: p.city || '',
          condition: p.condition || '',
          status: p.status,
          category_id: p.category_id ? String(p.category_id) : '',
        })
        setExistingImages(imgs)
        setImages(p.image_url ? [p.image_url, ...imgs.map(i => i.url)] : imgs.map(i => i.url))
      })
    }
  }, [])

  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }))

  const handleImageUpload = async (files: FileList) => {
    const list = Array.from(files).slice(0, MAX_IMAGES - images.length)
    if (list.length === 0) return
    setUploading(true)
    setError('')
    try {
      const urls = await Promise.all(list.map(uploadImage))
      setImages(prev => [...prev, ...urls])
    } catch {
      setError('Ошибка загрузки изображения')
    } finally {
      setUploading(false)
    }
  }

  const removeImage = (index: number) => {
    setImages(prev => prev.filter((_, i) => i !== index))
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
        image_url: images[0] || undefined,
      }
      const extraImages = images.slice(1)
      let postId: number
      if (isEdit && id) {
        postId = Number(id)
        await updatePost(postId, data)
        await Promise.all(existingImages.map(img => deletePostImage(postId, img.id)))
      } else {
        const p = await createPost(data)
        postId = p.id
      }
      await Promise.all(extraImages.map((url, i) => addPostImage(postId, url, i)))
      navigate(`/posts/${postId}`)
    } catch {
      setError('Ошибка сохранения')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-xl sm:text-2xl font-bold mb-6">{isEdit ? 'Редактировать объявление' : 'Новое объявление'}</h1>

      <form onSubmit={handleSubmit} className="card p-4 sm:p-6 space-y-5">
        {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>}

        <div>
          <label className="label">Заголовок *</label>
          <input className="input" value={form.title} onChange={e => set('title', e.target.value)} placeholder="Название товара или услуги" maxLength={64} required />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
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

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
          <label className="label">Фото {images.length > 0 && <span className="text-avito-muted font-normal">({images.length}/{MAX_IMAGES})</span>}</label>
          <p className="text-xs text-avito-muted mb-2">Первое фото будет обложкой объявления</p>
          <div className="grid grid-cols-3 sm:grid-cols-4 gap-3">
            {images.map((url, i) => (
              <div key={url + i} className="relative aspect-square rounded-lg overflow-hidden border border-avito-border group">
                <img src={url} alt="" className="w-full h-full object-cover" />
                {i === 0 && (
                  <span className="absolute bottom-1 left-1 bg-black/60 text-white text-[10px] px-1.5 py-0.5 rounded">Обложка</span>
                )}
                <button
                  type="button"
                  onClick={() => removeImage(i)}
                  aria-label="Удалить фото"
                  className="absolute top-1 right-1 w-6 h-6 rounded-full bg-black/60 text-white text-sm flex items-center justify-center hover:bg-red-500 transition-colors"
                >
                  ✕
                </button>
              </div>
            ))}
            {images.length < MAX_IMAGES && (
              <div
                className="aspect-square border-2 border-dashed border-avito-border rounded-lg flex items-center justify-center cursor-pointer hover:border-avito-blue transition-colors"
                onClick={() => document.getElementById('file-input')?.click()}
              >
                <div className="text-avito-muted text-center">
                  <div className="text-2xl">{uploading ? '⏳' : '📷'}</div>
                  <p className="text-xs mt-1">{uploading ? 'Загрузка...' : 'Добавить'}</p>
                </div>
              </div>
            )}
          </div>
          <input
            id="file-input"
            type="file"
            accept="image/*"
            multiple
            className="hidden"
            onChange={e => { if (e.target.files?.length) handleImageUpload(e.target.files); e.target.value = '' }}
          />
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