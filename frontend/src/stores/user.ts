import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useChatStore } from './chat'

export interface User {
  id: number
  username: string
  role: string
  created_at: string
  avatar?: string
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const user = ref<User | null>(null)
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      user.value = JSON.parse(userStr)
    } catch (e) {
      console.error('Failed to parse user from localStorage', e)
    }
  }

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUser = (newUser: User) => {
    user.value = newUser

    // 从 localStorage 加载该用户的头像
    const userAvatarKey = `userAvatar_${newUser.id}`
    const savedAvatar = localStorage.getItem(userAvatarKey)
    if (savedAvatar) {
      user.value.avatar = savedAvatar
    }

    localStorage.setItem('user', JSON.stringify(user.value))
  }

  const setAvatar = (avatarUrl: string) => {
    if (user.value) {
      user.value.avatar = avatarUrl
      // 按用户 ID 存储头像
      const userAvatarKey = `userAvatar_${user.value.id}`
      localStorage.setItem(userAvatarKey, avatarUrl)
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    // 注意：不删除 userAvatar_xxx，保留各用户的头像

    // 清理聊天状态
    const chatStore = useChatStore()
    chatStore.clearAll()
  }

  const isAdmin = () => {
    return user.value?.role === 'admin'
  }

  return {
    token,
    user,
    setToken,
    setUser,
    setAvatar,
    logout,
    isAdmin
  }
})
