import api from './client'

export const uploadImage = async (file: File): Promise<string> => {
  const form = new FormData()
  form.append('file', file)
  const res = await api.post<{ url: string }>('/upload/image', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data.url
}