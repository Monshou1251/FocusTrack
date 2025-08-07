<template>
    <div class="profile-info">
        <div class="avatar">
            <img :src="avatarUrl" alt="User avatar" referrerPolicy="no-referrer" />
        </div>
        <div class="userinfo">
            <div class="username">{{ username }}</div>
            <div class="email">{{ email }}</div>
        </div>
        <div class="date">
            <div class="day">{{ day }}</div>
            <div class="date-right-block">
                <div class="month">{{ month }}</div>
                <div class="week-day">{{ weekday }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth';
import { onMounted, ref } from 'vue';


const authStore = useAuthStore()

const username = authStore.username
const email = authStore.email
const avatarUrl = authStore.avatarUrl


const day = ref('')
const month = ref('')
const weekday = ref('')

onMounted(() => {
    const now = new Date()
    // const options = { month: 'long', weekday: 'long' }

    day.value = now.getDate()
    month.value = now.toLocaleDateString('en-US', { month: 'long' })
    weekday.value = now.toLocaleDateString('en-US', { weekday: 'long' })
})
</script>

<style scoped>
.profile-info {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
}

.avatar {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.userinfo {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
}

.username {
    font-size: 16px;
}

.email {
    font-size: 16px;
    color: var(--color-text-mute);
}

.date {
    width: 140px;
    height: 48px;
    display: flex;
    /* flex-direction: row; */
    justify-content: space-between;
    align-items: center;
    background-color: var(--color-background-raw);
    border-radius: var(--border-radius-8);
    padding: 4px;
}

.date-right-block {
    line-height: 1.1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding: 6px;
}

.day {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    background-color: #fff;
    color: var(--color-text-black);
    font-size: 22px;
    font-family: 'Bruno_Ace';
    border-radius: 6px;

}

.week-day {
    color: var(--color-text-mute);
    font-size: 16px;
}
</style>