// src/store/categories.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref<string[]>(['First Focus', 'Second Focus'])

  const selectedCategory = ref<string | null>(categories.value[0] ?? null)

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

  const addCategory = () => {
    if (categories.value.length < pastelColors.length) {
      categories.value.push(`New category ${categories.value.length + 1}`)
    } else {
      alert('Maximum categories reached.')
    }
  }

  const deleteCategory = (index: number) => {
    categories.value.splice(index, 1)
  }

  const updateCategory = (index: number, newName: string) => {
    categories.value[index] = newName.trim()
  }

  const getColorByIndex = (index: number): string => pastelColors[index % pastelColors.length]

  return {
    categories,
    pastelColors,
    addCategory,
    deleteCategory,
    updateCategory,
    getColorByIndex,
    selectedCategory
  }
})
