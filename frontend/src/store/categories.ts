// src/store/categories.ts
import { Category, CategoryApi } from '@/api/category'
import { defineStore } from 'pinia'
import { ref } from 'vue'

// Base URL is configured in the shared HTTP client

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref<Category[]>([])
  const isLoading = ref(false)
  const isLoaded = ref(false)
  const selectedCategory = ref<Category | null>(null)

  const pastelColors = [
    '#ffcd4b',
    '#FF6F61',
    '#F58EA8',
    '#6EC1E4',
    '#42B883',
    '#A7D676',
    '#A78BFA',
    '#80CBC4'
  ]

  const addCategory = async (name?: string) => {
    if (categories.value.length < pastelColors.length) {
      try {
        const categoryName = name || `New category ${categories.value.length + 1}`
        const res = await CategoryApi.create({ name: categoryName })

        // Add the new category from the server response
        categories.value.push(res.data)

        // If this is the first category, select it
        if (categories.value.length === 1) {
          selectedCategory.value = res.data
        }

        return res.data
      } catch (error) {
        console.error('Failed to create category:', error)
        throw error
      }
    } else {
      throw new Error('Maximum categories reached.')
    }
  }

  const deleteCategory = async (index: number) => {
    const category = categories.value[index]
    if (!category) return

    try {
      await CategoryApi.remove(category.id)
      categories.value.splice(index, 1)

      // Update selected category if the deleted one was selected
      if (
        selectedCategory.value &&
        !categories.value.find((c) => c.id === selectedCategory.value?.id)
      ) {
        selectedCategory.value = categories.value[0] ?? null
      }
    } catch (error) {
      console.error('Failed to delete category:', error)
      throw error
    }
  }

  const updateCategory = async (index: number, newName: string) => {
    const category = categories.value[index]
    if (!category) return

    try {
      const res = await CategoryApi.update(category.id, { name: newName.trim() })
      categories.value[index] = res.data

      // Update selected category if it was the edited one
      if (selectedCategory.value?.id === category.id) {
        selectedCategory.value = res.data
      }
    } catch (error) {
      console.error('Failed to update category:', error)
      throw error
    }
  }

  const fetchCategories = async () => {
    isLoading.value = true
    try {
      const res = await CategoryApi.getAll()
      categories.value = res.data.categories
      selectedCategory.value = categories.value[0] ?? null
      isLoaded.value = true
    } catch (e) {
      console.log(e)
      isLoading.value = false
    } finally {
      isLoading.value = false
    }
  }

  const getColorByIndex = (index: number): string => pastelColors[index % pastelColors.length]

  return {
    categories,
    pastelColors,
    addCategory,
    deleteCategory,
    updateCategory,
    getColorByIndex,
    fetchCategories,
    selectedCategory,
    isLoading,
    isLoaded
  }
})
