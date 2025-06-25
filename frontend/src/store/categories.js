import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref(['First Focus', 'Second Focus'])

  const selectedCategory = ref(categories.value[0] ?? null)

  const pastelColors = [
    '#ffcd4b', // тёплый жёлтый
    '#FF6F61', // кораллово-красный
    '#F58EA8', // мягкий розовый
    '#6EC1E4', // голубой
    '#42B883', // мятно-зелёный
    '#A7D676', // светло-зелёный
    '#A78BFA', // мягкий фиолетовый
    '#80CBC4' // бирюзовый
  ]

  const addCategory = () => {
    if (categories.value.length < pastelColors.length) {
      categories.value.push(`New category ${categories.value.length + 1}`)
    } else {
      alert('Maximum categories reached.')
    }
  }

  const deleteCategory = (index) => {
    categories.value.splice(index, 1)
  }

  const updateCategory = (index, newName) => {
    categories.value[index] = newName.trim()
  }

  const getColorByIndex = (index) => pastelColors[index % pastelColors.length]

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
