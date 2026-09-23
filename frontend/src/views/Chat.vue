<template>
  <div class="modern-chat">
    <!-- 左侧会话列表 -->
    <aside class="chat-sidebar">
      <div class="sidebar-header">
        <button class="back-btn" @click="router.push('/dashboard')">
          <el-icon><ArrowLeft /></el-icon>
        </button>
        <button class="new-chat-btn" @click="handleNewConversation">
          <el-icon><Plus /></el-icon>
          <span>新对话</span>
        </button>
      </div>

      <div class="conversations-list">
        <div
          v-for="conv in chatStore.conversations"
          :key="conv.id"
          class="conversation-card"
          :class="{ active: conv.id === chatStore.currentConversationId }"
          @click="handleSelectConversation(conv.id)"
        >
          <div class="conv-icon">
            <el-icon><ChatLineRound /></el-icon>
          </div>
          <div class="conv-content">
            <div class="conv-title">{{ conv.title }}</div>
            <div class="conv-time">{{ formatTime(conv.updated_at) }}</div>
          </div>
          <button class="conv-delete" @click.stop="handleDeleteConversation(conv.id)">
            <el-icon><Delete /></el-icon>
          </button>
        </div>
      </div>

      <div class="sidebar-footer">
        <el-dropdown @command="handleCommand" trigger="click" placement="top-start">
          <div class="user-profile">
            <el-avatar :size="40" :src="userStore.user?.avatar" :icon="UserFilled" />
            <div class="profile-info">
              <div class="profile-name">{{ userStore.user?.username }}</div>
              <div class="profile-role">{{ userStore.isAdmin() ? '管理员' : '用户' }}</div>
            </div>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="avatar">
                <el-icon><UserFilled /></el-icon>
                更换头像
              </el-dropdown-item>
              <el-dropdown-item command="settings">
                <el-icon><Setting /></el-icon>
                个人中心
              </el-dropdown-item>
              <el-dropdown-item v-if="userStore.isAdmin()" command="kb" divided>
                <el-icon><Document /></el-icon>
                知识库管理
              </el-dropdown-item>
              <el-dropdown-item command="logout" divided>
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </aside>

    <!-- 右侧对话区域 -->
    <main class="chat-main">
      <!-- 欢迎页面 -->
      <div v-if="!chatStore.currentConversationId" class="welcome-view">
        <div class="welcome-container">
          <div class="welcome-icon">
            <svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="60" cy="60" r="50" fill="url(#gradient1)" opacity="0.2"/>
              <path d="M40 50h40M40 60h40M40 70h25" stroke="url(#gradient1)" stroke-width="4" stroke-linecap="round"/>
              <defs>
                <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#667eea"/>
                  <stop offset="100%" style="stop-color:#764ba2"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 class="welcome-title">开始新的对话</h1>
          <p class="welcome-desc">基于强大的知识库，为您提供准确、专业的答案</p>

          <!-- 建议问题 -->
          <div class="suggestions">
            <div
              v-for="prompt in suggestedPrompts"
              :key="prompt.text"
              class="suggestion-card"
              @click="handlePromptClick(prompt.text)"
            >
              <div class="suggestion-icon">{{ prompt.icon }}</div>
              <div class="suggestion-text">{{ prompt.text }}</div>
            </div>
          </div>

          <!-- 功能特性 -->
          <div class="features-badges">
            <div class="feature-badge">
              <el-icon><DocumentCopy /></el-icon>
              <span>多文档支持</span>
            </div>
            <div class="feature-badge">
              <el-icon><Connection /></el-icon>
              <span>上下文理解</span>
            </div>
            <div class="feature-badge">
              <el-icon><Lightning /></el-icon>
              <span>实时流式</span>
            </div>
            <div class="feature-badge">
              <el-icon><Collection /></el-icon>
              <span>来源追溯</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 对话视图 -->
      <template v-else>
        <!-- 对话头部 -->
        <header class="chat-header">
          <div class="header-info">
            <h2 class="chat-title">{{ currentConversationTitle }}</h2>
            <div class="chat-meta">
              <span>{{ chatStore.messages.length }} 条消息</span>
            </div>
          </div>
          <div class="header-actions">
            <el-tooltip content="清空对话" placement="bottom">
              <button class="action-btn" @click="handleClearMessages">
                <el-icon><Delete /></el-icon>
              </button>
            </el-tooltip>
            <el-tooltip content="导出对话" placement="bottom">
              <button class="action-btn" @click="handleExportChat">
                <el-icon><Download /></el-icon>
              </button>
            </el-tooltip>
          </div>
        </header>

        <!-- 消息列表 -->
        <div ref="messageListRef" class="messages-container">
          <!-- 空状态 -->
          <div v-if="chatStore.messages.length === 0" class="empty-messages">
            <div class="empty-icon">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <p>开始新的对话吧</p>
            <div class="quick-starts">
              <button
                v-for="quick in quickPrompts"
                :key="quick"
                class="quick-start-btn"
                @click="handleQuickPrompt(quick)"
              >
                {{ quick }}
              </button>
            </div>
          </div>

          <!-- 消息列表 -->
          <div
            v-for="(msg, index) in chatStore.messages"
            :key="index"
            class="message-wrapper"
            :class="msg.role"
          >
            <div class="message-avatar">
              <el-avatar
                v-if="msg.role === 'user'"
                :size="36"
                :src="userStore.user?.avatar"
                :icon="UserFilled"
              />
              <div v-else class="ai-avatar">
                <el-icon><Cpu /></el-icon>
              </div>
            </div>

            <div class="message-box">
              <div class="message-header">
                <span class="sender-name">{{ msg.role === 'user' ? userStore.user?.username : 'AI 助手' }}</span>
                <span class="message-time">{{ formatMessageTime(msg.created_at) }}</span>
              </div>

              <div class="message-body" v-html="renderMarkdown(msg.content)"></div>

              <!-- 引用来源 -->
              <div v-if="msg.sources && msg.sources.length > 0" class="sources-section">
                <el-collapse accordion>
                  <el-collapse-item>
                    <template #title>
                      <div class="sources-title">
                        <el-icon><Collection /></el-icon>
                        <span>{{ msg.sources.length }} 个引用来源</span>
                      </div>
                    </template>
                    <div class="sources-list">
                      <div
                        v-for="(source, idx) in msg.sources"
                        :key="idx"
                        class="source-card"
                      >
                        <div class="source-score">
                          <el-icon><TrendCharts /></el-icon>
                          <span>{{ (source.score * 100).toFixed(0) }}%</span>
                        </div>
                        <div class="source-text">{{ source.content }}</div>
                      </div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </div>

              <!-- 消息操作 -->
              <div v-if="msg.role === 'assistant' && msg.content" class="message-actions">
                <button class="msg-action-btn" @click="handleCopy(msg.content)">
                  <el-icon><CopyDocument /></el-icon>
                  <span>复制</span>
                </button>
                <button class="msg-action-btn" @click="handleRegenerate(index)">
                  <el-icon><RefreshRight /></el-icon>
                  <span>重新生成</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 加载中 -->
          <div v-if="chatStore.isStreaming" class="typing-wrapper">
            <div class="message-avatar">
              <div class="ai-avatar">
                <el-icon><Cpu /></el-icon>
              </div>
            </div>
            <div class="typing-indicator">
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-wrapper">
          <div class="input-container">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="1"
              :autosize="{ minRows: 1, maxRows: 6 }"
              placeholder="输入您的问题..."
              :disabled="chatStore.isStreaming"
              @keydown.enter.exact.prevent="handleSend"
              class="message-input"
            />

            <div class="input-actions">
              <el-tooltip content="提示词模板" placement="top">
                <el-dropdown @command="handleTemplateSelect" trigger="click">
                  <button class="input-action-btn">
                    <el-icon><Tickets /></el-icon>
                  </button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item
                        v-for="tpl in promptTemplates"
                        :key="tpl.name"
                        :command="tpl.template"
                      >
                        {{ tpl.name }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </el-tooltip>

              <button
                class="send-btn"
                :disabled="!inputMessage.trim() || chatStore.isStreaming"
                @click="handleSend"
              >
                <el-icon v-if="chatStore.isStreaming"><Loading /></el-icon>
                <el-icon v-else><Promotion /></el-icon>
              </button>
            </div>
          </div>

          <div class="input-hint">
            按 Enter 发送，Shift + Enter 换行
          </div>
        </div>
      </template>
    </main>

    <!-- 更换头像对话框 -->
    <el-dialog
      v-model="avatarDialogVisible"
      title="更换头像"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="avatar-dialog-content">
        <div class="current-avatar">
          <el-avatar :size="100" :src="userStore.user?.avatar" :icon="UserFilled" />
          <p>当前头像</p>
        </div>

        <el-divider />

        <div class="upload-section">
          <h4>上传自定义头像</h4>
          <el-upload
            ref="uploadRef"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :http-request="handleAvatarUpload"
            accept="image/*"
            drag
          >
            <el-icon class="el-icon--upload"><Upload /></el-icon>
            <div class="el-upload__text">
              将图片拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 JPG、PNG 格式，文件大小不超过 2MB
              </div>
            </template>
          </el-upload>
        </div>

        <el-divider />

        <div class="preset-section">
          <h4>选择预设头像</h4>
          <div class="preset-avatars">
            <div
              v-for="(avatar, index) in presetAvatars"
              :key="index"
              class="preset-avatar-item"
              @click="handleSelectPresetAvatar(avatar)"
            >
              <el-avatar :size="64" :src="avatar" />
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="avatarDialogVisible = false">取消</el-button>
        <el-button type="danger" plain @click="handleRemoveAvatar" v-if="userStore.user?.avatar">
          移除头像
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Delete,
  Document,
  SwitchButton,
  ChatDotSquare,
  DocumentCopy,
  Connection,
  Lightning,
  Collection,
  Download,
  ChatDotRound,
  UserFilled,
  Cpu,
  CopyDocument,
  RefreshRight,
  Loading,
  Tickets,
  Promotion,
  Setting,
  ArrowLeft,
  Upload,
  ChatLineRound,
  TrendCharts
} from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import {
  createConversation,
  getConversations,
  getMessages,
  deleteConversation,
  askQuestion
} from '@/api/chat'

const router = useRouter()
const userStore = useUserStore()
const chatStore = useChatStore()

const messageListRef = ref<HTMLElement>()
const inputMessage = ref('')
const md = new MarkdownIt()
const avatarDialogVisible = ref(false)

// 建议的提示词
const suggestedPrompts = [
  { icon: '📝', text: '总结最近上传的文档内容' },
  { icon: '🔍', text: '搜索关于产品功能的详细说明' },
  { icon: '💡', text: '解释技术文档中的核心概念' },
  { icon: '📊', text: '对比不同产品的特性和参数' },
]

// 快速提示词
const quickPrompts = [
  '介绍一下知识库的内容',
  '最新的文档有哪些',
  '帮我总结重点信息',
]

// 提示词模板
const promptTemplates = [
  { name: '总结文档', template: '请帮我总结文档《》的核心内容，包括：\n1. 主要观点\n2. 关键信息\n3. 结论建议' },
  { name: '对比分析', template: '请对比分析以下内容：\n1. \n2. \n\n重点关注它们的异同点和优劣势。' },
  { name: '深度解释', template: '请详细解释""这个概念，包括：\n1. 定义和背景\n2. 应用场景\n3. 相关示例' },
  { name: '提取信息', template: '从文档中提取以下信息：\n1. \n2. \n3. ' },
]

// 预设头像
const presetAvatars = [
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Aneka',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Luna',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Max',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Sophie',
  'https://api.dicebear.com/7.x/avataaars/svg?seed=Oliver',
  'https://api.dicebear.com/7.x/bottts/svg?seed=Felix',
  'https://api.dicebear.com/7.x/bottts/svg?seed=Aneka',
]

// 当前会话标题
const currentConversationTitle = computed(() => {
  const conv = chatStore.conversations.find(c => c.id === chatStore.currentConversationId)
  return conv?.title || '新对话'
})

// 渲染 Markdown
const renderMarkdown = (content: string) => {
  return md.render(content)
}

// 格式化时间
const formatTime = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / 86400000)

  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
}

// 格式化消息时间
const formatMessageTime = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 加载会话列表
const loadConversations = async () => {
  try {
    const convs = await getConversations()
    chatStore.setConversations(convs)

    if (convs.length > 0 && !chatStore.currentConversationId) {
      handleSelectConversation(convs[0].id)
    }
  } catch (error) {
    console.error('Failed to load conversations:', error)
  }
}

// 加载消息
const loadMessages = async (conversationId: number) => {
  try {
    const res = await getMessages(conversationId)
    chatStore.setMessages(res.messages)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to load messages:', error)
  }
}

// 新建会话
const handleNewConversation = async () => {
  try {
    const conv = await createConversation({ title: '新对话' })
    await loadConversations()
    handleSelectConversation(conv.id)
    ElMessage.success('会话创建成功')
  } catch (error) {
    console.error('Failed to create conversation:', error)
  }
}

// 选择会话
const handleSelectConversation = (id: number) => {
  chatStore.setCurrentConversation(id)
  loadMessages(id)
}

// 删除会话
const handleDeleteConversation = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个会话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteConversation(id)
    ElMessage.success('会话已删除')

    if (chatStore.currentConversationId === id) {
      chatStore.reset()
    }

    await loadConversations()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete conversation:', error)
    }
  }
}

// 发送消息
const handleSend = async () => {
  if (!inputMessage.value.trim() || !chatStore.currentConversationId) return

  const question = inputMessage.value.trim()
  inputMessage.value = ''

  chatStore.addMessage({
    id: Date.now(),
    role: 'user',
    content: question,
    created_at: new Date().toISOString()
  })

  chatStore.addMessage({
    id: Date.now() + 1,
    role: 'assistant',
    content: '',
    created_at: new Date().toISOString()
  })

  await nextTick()
  scrollToBottom()

  chatStore.setStreaming(true)

  let fullContent = ''

  askQuestion(
    question,
    chatStore.currentConversationId,
    (chunk: string) => {
      fullContent += chunk
      chatStore.updateLastMessage(fullContent)
      scrollToBottom()
    },
    () => {
      chatStore.setStreaming(false)
      loadMessages(chatStore.currentConversationId!)
      loadConversations()
    },
    (error: string) => {
      chatStore.setStreaming(false)
      ElMessage.error(error)
    }
  )
}

// 滚动到底部
const scrollToBottom = () => {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

// 下拉菜单命令
const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  } else if (command === 'kb') {
    router.push('/kb-manage')
  } else if (command === 'settings') {
    router.push('/settings')
  } else if (command === 'avatar') {
    avatarDialogVisible.value = true
  }
}

// 处理提示词点击
const handlePromptClick = async (prompt: string) => {
  if (!chatStore.currentConversationId) {
    await handleNewConversation()
  }
  inputMessage.value = prompt
  await nextTick()
  handleSend()
}

// 处理快速提示词
const handleQuickPrompt = (prompt: string) => {
  inputMessage.value = prompt
}

// 处理模板选择
const handleTemplateSelect = (template: string) => {
  inputMessage.value = template
}

// 复制消息
const handleCopy = async (content: string) => {
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}

// 重新生成
const handleRegenerate = async (index: number) => {
  if (index < 1) return

  const userMessage = chatStore.messages[index - 1]
  if (userMessage.role !== 'user') return

  chatStore.messages.splice(index, 1)

  const question = userMessage.content

  chatStore.addMessage({
    id: Date.now(),
    role: 'assistant',
    content: '',
    created_at: new Date().toISOString()
  })

  await nextTick()
  scrollToBottom()

  chatStore.setStreaming(true)

  let fullContent = ''

  askQuestion(
    question,
    chatStore.currentConversationId!,
    (chunk: string) => {
      fullContent += chunk
      chatStore.updateLastMessage(fullContent)
      scrollToBottom()
    },
    () => {
      chatStore.setStreaming(false)
      loadMessages(chatStore.currentConversationId!)
      loadConversations()
    },
    (error: string) => {
      chatStore.setStreaming(false)
      ElMessage.error(error)
    }
  )
}

// 清空消息
const handleClearMessages = async () => {
  try {
    await ElMessageBox.confirm('确定要清空当前对话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    chatStore.setMessages([])
    ElMessage.success('对话已清空')
  } catch (error) {
    // 取消操作
  }
}

// 导出对话
const handleExportChat = () => {
  const messages = chatStore.messages.map(msg => ({
    角色: msg.role === 'user' ? '用户' : 'AI助手',
    内容: msg.content,
    时间: new Date(msg.created_at).toLocaleString('zh-CN')
  }))

  const content = messages.map(msg =>
    `【${msg.角色}】${msg.时间}\n${msg.内容}\n`
  ).join('\n---\n\n')

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `对话记录_${new Date().toLocaleDateString()}.txt`
  a.click()
  URL.revokeObjectURL(url)

  ElMessage.success('对话已导出')
}

// 头像上传前检查
const beforeAvatarUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 处理头像上传
const handleAvatarUpload = (options: any) => {
  const file = options.file
  const reader = new FileReader()

  reader.onload = (e) => {
    const avatarUrl = e.target?.result as string
    userStore.setAvatar(avatarUrl)
    ElMessage.success('头像已更新')
    avatarDialogVisible.value = false
  }

  reader.readAsDataURL(file)
}

// 选择预设头像
const handleSelectPresetAvatar = (url: string) => {
  userStore.setAvatar(url)
  ElMessage.success('头像已更新')
  avatarDialogVisible.value = false
}

// 移除头像
const handleRemoveAvatar = () => {
  userStore.setAvatar('')
  ElMessage.success('头像已移除')
  avatarDialogVisible.value = false
}

// 监听消息变化
watch(
  () => chatStore.messages.length,
  () => {
    nextTick(() => scrollToBottom())
  }
)

onMounted(() => {
  loadConversations()
})
</script>

<style scoped>
.modern-chat {
  display: flex;
  height: 100vh;
  background: #f8f9ff;
}

/* 左侧边栏 */
.chat-sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e8ecf1;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  display: flex;
  gap: 8px;
  border-bottom: 1px solid #e8ecf1;
}

.back-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: #f5f7fa;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  color: #666;
}

.back-btn:hover {
  background: #e8ecf1;
  color: #333;
}

.new-chat-btn {
  flex: 1;
  height: 40px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.new-chat-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.conversation-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin-bottom: 4px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.conversation-card:hover {
  background: #f8f9ff;
}

.conversation-card.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-left: 3px solid #667eea;
}

.conv-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.conv-content {
  flex: 1;
  min-width: 0;
}

.conv-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-time {
  font-size: 12px;
  color: #999;
}

.conv-delete {
  opacity: 0;
  width: 28px;
  height: 28px;
  border: none;
  background: #fee;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #f56c6c;
  cursor: pointer;
  transition: all 0.2s;
}

.conversation-card:hover .conv-delete {
  opacity: 1;
}

.conv-delete:hover {
  background: #f56c6c;
  color: white;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #e8ecf1;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.user-profile:hover {
  background: #f8f9ff;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.profile-role {
  font-size: 12px;
  color: #999;
}

/* 右侧主区域 */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f8f9ff;
}

/* 欢迎视图 */
.welcome-view {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.welcome-container {
  max-width: 600px;
  text-align: center;
}

.welcome-icon {
  margin-bottom: 24px;
}

.welcome-icon svg {
  width: 120px;
  height: 120px;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.welcome-desc {
  font-size: 16px;
  color: #666;
  margin: 0 0 40px 0;
}

.suggestions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 40px;
}

.suggestion-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: left;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.suggestion-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.suggestion-icon {
  font-size: 28px;
  margin-bottom: 12px;
}

.suggestion-text {
  font-size: 14px;
  color: #333;
  line-height: 1.6;
}

.features-badges {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.feature-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* 对话头部 */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: white;
  border-bottom: 1px solid #e8ecf1;
}

.header-info {
  flex: 1;
}

.chat-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.chat-meta {
  font-size: 13px;
  color: #999;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  color: #666;
}

.action-btn:hover {
  background: #667eea;
  color: white;
}

/* 消息容器 */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.empty-icon {
  font-size: 64px;
  color: #ddd;
  margin-bottom: 16px;
}

.empty-messages p {
  font-size: 14px;
  color: #999;
  margin: 0 0 24px 0;
}

.quick-starts {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.quick-start-btn {
  padding: 10px 20px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.quick-start-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f8f9ff;
}

/* 消息包装器 */
.message-wrapper {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-wrapper.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.ai-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.message-box {
  max-width: 70%;
  background: white;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.message-wrapper.user .message-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.sender-name {
  font-size: 13px;
  font-weight: 600;
}

.message-wrapper.user .sender-name {
  color: rgba(255, 255, 255, 0.9);
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-wrapper.user .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.message-body {
  line-height: 1.7;
  word-wrap: break-word;
  color: #1a1a1a;
  font-size: 14px;
}

.message-body :deep(p) {
  margin: 8px 0;
  color: #1a1a1a;
}

.message-wrapper.user .message-body :deep(p) {
  color: white;
}

.message-body :deep(code) {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  color: #e83e8c;
}

.message-wrapper.user .message-body :deep(code) {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.message-body :deep(pre) {
  background: #f6f8fa;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
}

.message-body :deep(pre code) {
  background: transparent;
  color: #1a1a1a;
}

.message-body :deep(ul),
.message-body :deep(ol) {
  padding-left: 24px;
  color: #1a1a1a;
}

.message-body :deep(li) {
  color: #1a1a1a;
  margin: 4px 0;
}

.message-body :deep(strong) {
  color: #1a1a1a;
  font-weight: 600;
}

.message-body :deep(h1),
.message-body :deep(h2),
.message-body :deep(h3),
.message-body :deep(h4),
.message-body :deep(h5),
.message-body :deep(h6) {
  color: #1a1a1a;
  margin: 12px 0 8px 0;
  font-weight: 600;
}

.sources-section {
  margin-top: 12px;
}

.sources-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #666;
}

.sources-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

.source-card {
  background: #f8f9ff;
  border-radius: 8px;
  padding: 12px;
  border-left: 3px solid #667eea;
}

.source-score {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #667eea;
  margin-bottom: 8px;
  font-weight: 600;
}

.source-text {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}

.message-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.msg-action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.msg-action-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f8f9ff;
}

/* 输入中指示器 */
.typing-wrapper {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 16px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #667eea;
  animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  30% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 输入区域 */
.input-wrapper {
  padding: 20px 24px;
  background: white;
  border-top: 1px solid #e8ecf1;
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: #f8f9ff;
  border-radius: 16px;
  padding: 12px 16px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.input-container:focus-within {
  border-color: #667eea;
  background: white;
}

.message-input {
  flex: 1;
}

.message-input :deep(.el-textarea__inner) {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 0;
  resize: none;
  font-size: 14px;
  line-height: 1.6;
}

.message-input :deep(.el-textarea__inner):focus {
  box-shadow: none;
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-action-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  color: #999;
}

.input-action-btn:hover {
  background: #e8ecf1;
  color: #667eea;
}

.send-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
  text-align: center;
}

/* 头像对话框 */
.avatar-dialog-content {
  padding: 20px 0;
}

.current-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.current-avatar p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.upload-section,
.preset-section {
  margin: 20px 0;
}

.upload-section h4,
.preset-section h4 {
  margin: 0 0 16px 0;
  font-size: 15px;
  color: #333;
}

.preset-avatars {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.preset-avatar-item {
  cursor: pointer;
  transition: transform 0.2s;
  display: flex;
  justify-content: center;
}

.preset-avatar-item:hover {
  transform: scale(1.1);
}
</style>
