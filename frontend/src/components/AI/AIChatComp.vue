<template>
    <div class="ai-chat">
        <TopPanel title="AI Assistant" :showButton="false" />

        <div class="chat-container">
            <!-- Messages -->
            <div class="messages" ref="messagesContainer">
                <div v-for="message in messages" :key="message.id" class="message" :class="message.type">
                    <div class="message-content">
                        <div class="message-icon">
                            <svg-icon v-if="message.type === 'ai'" type="mdi" :path="mdiRobot" />
                            <svg-icon v-else type="mdi" :path="mdiAccount" />
                        </div>
                        <div class="message-text">{{ message.text }}</div>
                    </div>
                    <div class="message-time">{{ formatTime(message.timestamp) }}</div>
                </div>
            </div>

            <!-- Input area -->
            <div class="input-area">
                <div class="input-container">
                    <input v-model="newMessage" @keyup.enter="sendMessage" @keyup.esc="clearInput"
                        placeholder="Ask about productivity, focus tips..." class="message-input" :disabled="isLoading"
                        ref="messageInput" />
                    <button @click="sendMessage" class="send-button" :disabled="!newMessage.trim() || isLoading">
                        <svg-icon v-if="isLoading" type="mdi" :path="mdiLoading" class="loading-icon" />
                        <svg-icon v-else type="mdi" :path="mdiSend" />
                    </button>
                </div>

                <!-- Quick suggestions -->
                <div class="suggestions">
                    <button v-for="suggestion in suggestions" :key="suggestion" @click="sendSuggestion(suggestion)"
                        class="suggestion-btn" :disabled="isLoading">
                        {{ suggestion }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiAccount, mdiLoading, mdiRobot, mdiSend } from '@mdi/js'
import { nextTick, onMounted, ref, watch } from 'vue'
import TopPanel from '../TopPanel/TopPanelComp.vue'

interface Message {
    id: number
    type: 'user' | 'ai'
    text: string
    timestamp: Date
}

const messages = ref<Message[]>([
    {
        id: 1,
        type: 'ai',
        text: "Hi! I'm your productivity assistant. Ask me about focus techniques, time management, or how to improve your work sessions!",
        timestamp: new Date()
    }
])

const newMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref<HTMLElement>()
const messageInput = ref<HTMLInputElement>()

const suggestions = [
    "How to stay focused?",
    "Best time for deep work?",
    "How long should I work?",
    "Tips for breaks?"
]

const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    })
}

const scrollToBottom = async () => {
    await nextTick()
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
}

const sendMessage = async () => {
    if (!newMessage.value.trim() || isLoading.value) return

    const userMessage: Message = {
        id: Date.now(),
        type: 'user',
        text: newMessage.value,
        timestamp: new Date()
    }

    messages.value.push(userMessage)
    const userText = newMessage.value
    newMessage.value = ''
    isLoading.value = true

    await scrollToBottom()

    // Simulate AI response (replace with actual AI API call)
    setTimeout(() => {
        const aiResponse = generateAIResponse(userText)
        const aiMessage: Message = {
            id: Date.now() + 1,
            type: 'ai',
            text: aiResponse,
            timestamp: new Date()
        }
        messages.value.push(aiMessage)
        isLoading.value = false
        scrollToBottom()
    }, 1000 + Math.random() * 2000) // Random delay 1-3 seconds
}

const sendSuggestion = (suggestion: string) => {
    newMessage.value = suggestion
    sendMessage()
}

const clearInput = () => {
    newMessage.value = ''
}

const generateAIResponse = (userText: string): string => {
    const text = userText.toLowerCase()

    if (text.includes('focus') || text.includes('concentrate')) {
        return "Try the Pomodoro technique: 25 minutes of focused work followed by a 5-minute break. Eliminate distractions by putting your phone in another room and using website blockers."
    }

    if (text.includes('time') && text.includes('work')) {
        return "Your most productive hours are typically 9-11 AM and 2-4 PM. Schedule your most challenging tasks during these windows. For deep work, aim for 90-minute sessions."
    }

    if (text.includes('long') || text.includes('duration')) {
        return "For most people, 25-45 minute work sessions work best. Start with 25 minutes and gradually increase. Take 5-15 minute breaks between sessions to maintain focus."
    }

    if (text.includes('break') || text.includes('rest')) {
        return "Take breaks every 25-45 minutes. Use breaks to stretch, walk around, or do something completely different. Avoid screens during breaks to give your brain a rest."
    }

    if (text.includes('productive') || text.includes('efficient')) {
        return "Track your energy levels throughout the day. Schedule important tasks during your peak hours. Use time blocking and eliminate multitasking for better results."
    }

    return "Great question! I'm here to help you optimize your productivity. Try asking about focus techniques, time management, or work session planning. What specific area would you like to improve?"
}

onMounted(() => {
    scrollToBottom()
})

watch(messages, () => {
    scrollToBottom()
}, { deep: true })
</script>

<style scoped>
.ai-chat {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    min-width: 0;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    gap: 12px;
    padding: 12px;
    overflow-y: auto;
}

.messages {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 8px;
    background: var(--color-background-soft);
    border-radius: 8px;
    border: 1px solid var(--color-border);
    min-height: 0;
    /* Allow shrinking */
    max-height: auto;

}

.message {
    display: flex;
    flex-direction: column;

    gap: 4px;
}

.message.user {
    align-items: flex-end;
}

.message.ai {
    align-items: flex-start;
}

.message-content {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    max-width: 85%;
    padding: 8px 12px;
    border-radius: 12px;
    background: var(--color-background);
    border: 1px solid var(--color-border);
}

.message.user .message-content {
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
}

.message-icon {
    flex-shrink: 0;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 2px;
}

.message.user .message-icon {
    color: rgba(255, 255, 255, 0.8);
}

.message.ai .message-icon {
    color: var(--color-primary);
}

.message-text {
    font-size: 13px;
    line-height: 1.4;
    word-wrap: break-word;
}

.message-time {
    font-size: 10px;
    color: var(--color-text-mute);
    margin: 0 4px;
}

.input-area {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.input-container {
    display: flex;
    gap: 8px;
    align-items: center;
}

.message-input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid var(--color-border);
    border-radius: 20px;
    background: var(--color-background);
    color: var(--color-text);
    font-size: 13px;
    outline: none;
    transition: all 0.2s ease;
}

.message-input:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

.message-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.send-button {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 50%;
    background: var(--color-primary);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
}

.send-button:hover:not(:disabled) {
    background: var(--color-primary-dark);
    transform: scale(1.05);
}

.send-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.loading-icon {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.suggestion-btn {
    padding: 4px 8px;
    border: 1px solid var(--color-border);
    border-radius: 12px;
    background: var(--color-background-soft);
    color: var(--color-text);
    font-size: 11px;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.suggestion-btn:hover:not(:disabled) {
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
}

.suggestion-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Scrollbar styling */
.messages::-webkit-scrollbar {
    width: 4px;
}

.messages::-webkit-scrollbar-track {
    background: transparent;
}

.messages::-webkit-scrollbar-thumb {
    background: var(--color-border);
    border-radius: 2px;
}

.messages::-webkit-scrollbar-thumb:hover {
    background: var(--color-text-mute);
}
</style>
