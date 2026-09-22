import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  sources?: Array<{
    content: string
    score: number
  }>
  created_at: string
}

export interface Conversation {
  id: number
  title: string
  created_at: string
  updated_at: string
  message_count?: number
}

export const useChatStore = defineStore('chat', () => {
  const currentConversationId = ref<number | null>(null)
  const conversations = ref<Conversation[]>([])
  const messages = ref<Message[]>([])
  const isStreaming = ref(false)

  const setCurrentConversation = (id: number) => {
    currentConversationId.value = id
  }

  const setConversations = (convs: Conversation[]) => {
    conversations.value = convs
  }

  const setMessages = (msgs: Message[]) => {
    messages.value = msgs
  }

  const addMessage = (message: Message) => {
    messages.value.push(message)
  }

  const updateLastMessage = (content: string) => {
    if (messages.value.length > 0) {
      const lastMessage = messages.value[messages.value.length - 1]
      lastMessage.content = content
    }
  }

  const setStreaming = (streaming: boolean) => {
    isStreaming.value = streaming
  }

  const reset = () => {
    currentConversationId.value = null
    messages.value = []
  }

  return {
    currentConversationId,
    conversations,
    messages,
    isStreaming,
    setCurrentConversation,
    setConversations,
    setMessages,
    addMessage,
    updateLastMessage,
    setStreaming,
    reset
  }
})
