import request from '@/utils/request'

export interface LoginData {
  account: string  // 改为账号
  password: string
}

export interface RegisterData {
  username: string
  password: string
}

export interface UserResponse {
  id: number
  username: string
  account: string  // 添加账号字段
  role: string
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserResponse
}

export interface ChangePasswordData {
  old_password: string
  new_password: string
}

// 用户登录
export const login = (data: LoginData) => {
  return request.post<any, TokenResponse>('/auth/login', data)
}

// 用户注册
export const register = (data: RegisterData) => {
  return request.post<any, UserResponse>('/auth/register', data)
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get<any, UserResponse>('/auth/me')
}

// 修改密码
export const changePassword = (data: ChangePasswordData) => {
  return request.post<any, { message: string }>('/auth/change-password', data)
}
