import { http } from '@/lib/http'

export interface Category {
  id: number
  name: string
}

export interface CategoriesResponse {
  categories: Category[]
}

const CATEGORY_ROOT = '/category'

export const CategoryApi = {
  getAll() {
    return http.get<CategoriesResponse>(`${CATEGORY_ROOT}/categories`)
  },

  create(payload: { name: string }) {
    return http.post<Category>(CATEGORY_ROOT, payload)
  },
  update(id: number, payload: { name: string }) {
    return http.patch<Category>(`${CATEGORY_ROOT}/${id}`, payload)
  },
  remove(id: number) {
    return http.delete<void>(`${CATEGORY_ROOT}/${id}`)
  }
}
