<template>
    <div class="weekly-chart">
        <Bar :data="chartData" :options="chartOptions" />
    </div>
</template>

<script setup>
import {
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    Title,
    Tooltip
} from 'chart.js'
import { getDay, parseISO } from 'date-fns'
import { Bar } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

// Входные данные: можно будет заменить на API-загрузку
const rawEntries = [
    { date: '2025-06-10', categoryId: 'abc123', category: 'Deep Work', color: '#42B883' },
    { date: '2025-06-11', categoryId: 'abc123', category: 'Deep Work', color: '#42B883' },
    { date: '2025-06-11', categoryId: 'xyz789', category: 'Reading', color: '#FF6F61' },
    { date: '2025-06-13', categoryId: 'xyz789', category: 'Reading', color: '#FF6F61' },
    { date: '2025-06-13', categoryId: 'xyz789', category: 'Reading', color: '#FF6F61' },
    { date: '2025-06-13', categoryId: 'xyz789', category: 'Reading', color: '#FF6F61' },
    { date: '2025-06-14', categoryId: 'xyz789', category: 'Reading', color: '#FF6F61' },
    { date: '2025-06-12', categoryId: 'abc123', category: 'Deep Work', color: '#42B883' }
]

// Группировка по дням недели (Пн - 0 ... Вс - 6)
const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const dayCounts = Array(7).fill(0)
const dayColors = Array(7).fill('#d3d3d3') // Цвет по умолчанию

// Считаем фокус по дням и запоминаем цвет самой частой категории
const categoryPerDay = Array(7).fill(null).map(() => ({}))

for (const entry of rawEntries) {
    const dayIndex = (getDay(parseISO(entry.date)) + 6) % 7 // Пн = 0
    dayCounts[dayIndex]++

    // Учитываем, сколько раз категория встречалась в этом дне
    if (!categoryPerDay[dayIndex][entry.category]) {
        categoryPerDay[dayIndex][entry.category] = { count: 1, color: entry.color }
    } else {
        categoryPerDay[dayIndex][entry.category].count++
    }
}

// Выбираем цвет самой популярной категории в каждом дне
for (let i = 0; i < 7; i++) {
    const categories = categoryPerDay[i]
    const mostFrequent = Object.entries(categories).sort((a, b) => b[1].count - a[1].count)[0]
    if (mostFrequent) {
        dayColors[i] = mostFrequent[1].color
    }
}

// Chart.js конфигурация
const chartData = {
    labels: dayNames,
    datasets: [
        {
            label: 'Focus Sessions',
            data: dayCounts,
            backgroundColor: dayColors
        }
    ]
}

const chartOptions = {
    responsive: true,
    plugins: {
        legend: { display: false }
    },
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                precision: 0
            }
        }
    }
}
</script>
