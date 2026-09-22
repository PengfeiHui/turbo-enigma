import { defineStore } from 'pinia'
import { ref } from 'vue'

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

    // 如果没有头像，从 localStorage 加载
    if (!user.value.avatar) {
      user.value.avatar = localStorage.getItem('userAvatar') || ''
    }

    localStorage.setItem('user', JSON.stringify(newUser))
  }

  const setAvatar = (avatarUrl: string) => {
    if (user.value) {
      user.value.avatar = avatarUrl
      localStorage.setItem('userAvatar', avatarUrl)
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
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
