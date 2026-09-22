import request from '@/utils/request'
import type { Conversation, Message } from '@/stores/chat'

export interface ConversationCreate {
  title?: string
}

export interface MessageListResponse {
  messages: Message[]
  total: number
  page: number
  page_size: number
}

// 创建会话
export const createConversation = (data: ConversationCreate) => {
  return request.post<any, Conversation>('/conversations', data)
}

// 获取会话列表
export const getConversations = () => {
  return request.get<any, Conversation[]>('/conversations')
}

// 获取会话消息
export const getMessages = (conversationId: number, page = 1, pageSize = 50) => {
  return request.get<any, MessageListResponse>(`/conversations/${conversationId}/messages`, {
    params: { page, page_size: pageSize }
  })
}

// 删除会话
export const deleteConversation = (conversationId: number) => {
  return request.delete(`/conversations/${conversationId}`)
}

// 问答（流式）- 使用 fetch API 支持 POST 的 SSE
export const askQuestion = async (
  question: string,
  conversationId: number,
  onChunk: (chunk: string) => void,
  onDone: () => void,
  onError: (error: string) => void
) => {
  const token = localStorage.getItem('token')

  try {
    const response = await fetch('/api/chat/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        question,
        conversation_id: conversationId
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('无法读取响应流')
    }

    let buffer = ''  // 缓冲区，用于处理不完整的数据

    while (true) {
      const { done, value } = await reader.read()

      if (done) {
        break
      }

      // 解码新数据并添加到缓冲区
      buffer += decoder.decode(value, { stream: true })

      // 按行分割
      const lines = buffer.split('\n')

      // 保留最后一个可能不完整的行
      buffer = lines.pop() || ''

      // 处理完整的行
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const jsonStr = line.slice(6).trim()
            if (jsonStr) {
              const data = JSON.parse(jsonStr)

              if (data.done) {
                onDone()
                return
              } else if (data.chunk) {
                onChunk(data.chunk)
              } else if (data.error) {
                onError(data.error)
                return
              }
            }
          } catch (e) {
            console.error('Failed to parse SSE data:', line, e)
          }
        }
      }
    }

    // 处理可能剩余的数据
    if (buffer.trim()) {
      console.log('Remaining buffer:', buffer)
    }

    onDone()
  } catch (error) {
    console.error('Stream error:', error)
    onError('连接失败，请重试')
  }
}
