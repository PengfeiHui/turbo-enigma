<template>
  <div class="chat-container">
    <!-- 左侧会话列表 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <el-button @click="router.push('/dashboard')" :icon="HomeFilled" class="header-btn">
          返回首页
        </el-button>
        <el-button type="primary" @click="handleNewConversation" :icon="Plus" class="header-btn">
          新建会话
        </el-button>
      </div>

      <div class="conversation-list">
        <div
          v-for="conv in chatStore.conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: conv.id === chatStore.currentConversationId }"
          @click="handleSelectConversation(conv.id)"
        >
          <div class="conversation-title">{{ conv.title }}</div>
          <el-icon class="delete-icon" @click.stop="handleDeleteConversation(conv.id)">
            <Delete />
          </el-icon>
        </div>
      </div>

      <div class="sidebar-footer">
        <el-dropdown @command="handleCommand">
          <div class="user-info">
            <el-icon><User /></el-icon>
            <span>{{ userStore.user?.username }}</span>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-if="userStore.isAdmin()" command="kb">
                <el-icon><Document /></el-icon>
                知识库管理
              </el-dropdown-item>
              <el-dropdown-item command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 右侧对话区域 -->
    <div class="chat-main">
      <!-- 欢迎界面 -->
      <div v-if="!chatStore.currentConversationId" class="welcome-state">
        <div class="welcome-content">
          <div class="welcome-icon">
            <el-icon :size="80"><ChatDotSquare /></el-icon>
          </div>
          <h1>LongChain RAG 智能助手</h1>
          <p class="welcome-desc">基于知识库的智能问答系统，为您提供准确、专业的答案</p>

          <!-- 快捷提示词 -->
          <div class="prompt-suggestions">
            <h3>💡 试试这些问题</h3>
            <div class="prompt-grid">
              <el-card
                v-for="prompt in suggestedPrompts"
                :key="prompt.text"
                class="prompt-card"
                shadow="hover"
                @click="handlePromptClick(prompt.text)"
              >
                <div class="prompt-icon">{{ prompt.icon }}</div>
                <div class="prompt-text">{{ prompt.text }}</div>
              </el-card>
            </div>
          </div>

          <!-- 功能特性 -->
          <div class="features">
            <div class="feature-item">
              <el-icon :size="24" color="#409eff"><DocumentCopy /></el-icon>
              <span>多文档支持</span>
            </div>
            <div class="feature-item">
              <el-icon :size="24" color="#67c23a"><Connection /></el-icon>
              <span>上下文理解</span>
            </div>
            <div class="feature-item">
              <el-icon :size="24" color="#e6a23c"><Lightning /></el-icon>
              <span>实时流式输出</span>
            </div>
            <div class="feature-item">
              <el-icon :size="24" color="#f56c6c"><Collection /></el-icon>
              <span>来源追溯</span>
            </div>
          </div>
        </div>
      </div>

      <template v-else>
        <!-- 对话头部 -->
        <div class="chat-header">
          <div class="chat-title">
            <el-icon><ChatLineRound /></el-icon>
            <span>{{ currentConversationTitle }}</span>
          </div>
          <div class="chat-actions">
            <el-tooltip content="清空对话" placement="bottom">
              <el-button :icon="Delete" circle @click="handleClearMessages" />
            </el-tooltip>
            <el-tooltip content="导出对话" placement="bottom">
              <el-button :icon="Download" circle @click="handleExportChat" />
            </el-tooltip>
          </div>
        </div>

        <!-- 消息列表 -->
        <div ref="messageListRef" class="message-list">
          <!-- 空状态提示 -->
          <div v-if="chatStore.messages.length === 0" class="empty-messages">
            <el-icon :size="48" color="#909399"><ChatDotRound /></el-icon>
            <p>开始新的对话吧</p>
            <div class="quick-prompts">
              <el-tag
                v-for="quick in quickPrompts"
                :key="quick"
                @click="handleQuickPrompt(quick)"
                style="cursor: pointer; margin: 4px;"
              >
                {{ quick }}
              </el-tag>
            </div>
          </div>

          <div
            v-for="(msg, index) in chatStore.messages"
            :key="index"
            class="message-item"
            :class="msg.role"
          >
            <div class="message-avatar">
              <el-avatar v-if="msg.role === 'user'" :icon="UserFilled" />
              <el-avatar v-else>
                <el-icon><Cpu /></el-icon>
              </el-avatar>
            </div>
            <div class="message-bubble">
              <div class="message-header">
                <span class="message-role">{{ msg.role === 'user' ? '我' : 'AI 助手' }}</span>
                <span class="message-time">{{ formatMessageTime(msg.created_at) }}</span>
              </div>
              <div class="message-content" v-html="renderMarkdown(msg.content)"></div>

              <!-- 引用来源 -->
              <div v-if="msg.sources && msg.sources.length > 0" class="sources">
                <el-collapse accordion>
                  <el-collapse-item name="1">
                    <template #title>
                      <el-icon><Collection /></el-icon>
                      <span style="margin-left: 8px;">查看 {{ msg.sources.length }} 个引用来源</span>
                    </template>
                    <div
                      v-for="(source, idx) in msg.sources"
                      :key="idx"
                      class="source-item"
                    >
                      <div class="source-header">
                        <el-tag size="small" type="success">相似度: {{ (source.score * 100).toFixed(1) }}%</el-tag>
                      </div>
                      <div class="source-content">{{ source.content }}</div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </div>

              <!-- 消息操作 -->
              <div v-if="msg.role === 'assistant' && msg.content" class="message-actions">
                <el-tooltip content="复制" placement="top">
                  <el-button text :icon="CopyDocument" @click="handleCopy(msg.content)" />
                </el-tooltip>
                <el-tooltip content="重新生成" placement="top">
                  <el-button text :icon="RefreshRight" @click="handleRegenerate(index)" />
                </el-tooltip>
              </div>
            </div>
          </div>

          <!-- 加载中提示 -->
          <div v-if="chatStore.isStreaming" class="typing-indicator">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>AI 正在思考中...</span>
          </div>
        </div>

        <!-- 输入框 -->
        <div class="input-area">
          <div class="input-container">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="3"
              placeholder="输入您的问题... (按 Enter 发送，Shift + Enter 换行)"
              :disabled="chatStore.isStreaming"
              @keydown.enter.exact.prevent="handleSend"
              class="message-input"
            />
            <div class="input-toolbar">
              <div class="toolbar-left">
                <el-tooltip content="插入提示词模板" placement="top">
                  <el-dropdown @command="handleTemplateSelect">
                    <el-button text :icon="Tickets">
                      模板
                    </el-button>
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
              </div>
              <div class="toolbar-right">
                <el-button
                  type="primary"
                  :loading="chatStore.isStreaming"
                  :disabled="!inputMessage.trim()"
                  @click="handleSend"
                  :icon="Promotion"
                >
                  {{ chatStore.isStreaming ? '生成中...' : '发送' }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, User, Document, SwitchButton, HomeFilled, ChatDotSquare, DocumentCopy, Connection, Lightning, Collection, ChatLineRound, Download, ChatDotRound, UserFilled, Cpu, CopyDocument, RefreshRight, Loading, Tickets, Promotion } from '@element-plus/icons-vue'
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

// 当前会话标题
const currentConversationTitle = computed(() => {
  const conv = chatStore.conversations.find(c => c.id === chatStore.currentConversationId)
  return conv?.title || '新对话'
})

// 渲染 Markdown
const renderMarkdown = (content: string) => {
  return md.render(content)
}

// 加载会话列表
const loadConversations = async () => {
  try {
    const convs = await getConversations()
    chatStore.setConversations(convs)

    // 如果有会话且没有选中，选中第一个
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

  // 添加用户消息
  chatStore.addMessage({
    id: Date.now(),
    role: 'user',
    content: question,
    created_at: new Date().toISOString()
  })

  // 添加空的助手消息
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
      // 重新加载消息以获取 sources
      loadMessages(chatStore.currentConversationId!)
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
  }
}

// 监听消息变化，自动滚动
watch(
  () => chatStore.messages.length,
  () => {
    nextTick(() => scrollToBottom())
  }
)

// 格式化消息时间
const formatMessageTime = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`

  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 处理提示词点击
const handlePromptClick = async (prompt: string) => {
  // 如果没有当前会话，先创建一个
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

  // 找到上一条用户消息
  const userMessage = chatStore.messages[index - 1]
  if (userMessage.role !== 'user') return

  // 删除当前的助手消息
  chatStore.messages.splice(index, 1)

  // 重新发送
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

onMounted(() => {
  loadConversations()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background: #f5f5f5;
}

.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.header-btn {
  width: 100%;
  margin: 0 !important;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.conversation-item {
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s;
}

.conversation-item:hover {
  background: #f5f5f5;
}

.conversation-item.active {
  background: #ecf5ff;
  border-left: 3px solid #409eff;
}

.conversation-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}

.delete-icon {
  opacity: 0;
  transition: opacity 0.2s;
  color: #f56c6c;
}

.conversation-item:hover .delete-icon {
  opacity: 1;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #e5e5e5;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.user-info:hover {
  background: #f5f5f5;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

/* 欢迎界面 */
.welcome-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  overflow-y: auto;
}

.welcome-content {
  max-width: 800px;
  text-align: center;
}

.welcome-icon {
  color: #409eff;
  margin-bottom: 24px;
}

.welcome-content h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 16px;
}

.welcome-desc {
  font-size: 16px;
  color: #666;
  margin-bottom: 48px;
}

.prompt-suggestions {
  margin-bottom: 48px;
}

.prompt-suggestions h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 24px;
}

.prompt-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.prompt-card {
  cursor: pointer;
  transition: all 0.3s;
  text-align: left;
}

.prompt-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.prompt-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.prompt-text {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.features {
  display: flex;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

/* 对话头部 */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e5e5e5;
  background: white;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #f8f9fa;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 16px;
}

.empty-messages p {
  color: #909399;
  font-size: 14px;
}

.quick-prompts {
  margin-top: 16px;
}

.message-item {
  margin-bottom: 24px;
  display: flex;
  gap: 12px;
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

.message-avatar {
  flex-shrink: 0;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-bubble {
  max-width: 70%;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message-item.user .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 12px;
}

.message-role {
  font-weight: 600;
}

.message-item.user .message-role,
.message-item.user .message-time {
  color: rgba(255, 255, 255, 0.9);
}

.message-time {
  color: #999;
}

.message-content {
  line-height: 1.6;
  word-wrap: break-word;
}

.message-content :deep(p) {
  margin: 8px 0;
}

.message-content :deep(code) {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.message-content :deep(pre) {
  background: #f6f8fa;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
}

.message-content :deep(ul),
.message-content :deep(ol) {
  padding-left: 24px;
}

.sources {
  margin-top: 12px;
}

.source-item {
  margin-bottom: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
}

.source-header {
  margin-bottom: 8px;
}

.source-content {
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

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409eff;
  font-size: 14px;
}

/* 输入框 */
.input-area {
  padding: 20px 24px;
  border-top: 1px solid #e5e5e5;
  background: white;
}

.input-container {
  max-width: 100%;
}

.message-input {
  margin-bottom: 12px;
}

.input-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toolbar-left {
  display: flex;
  gap: 8px;
}

.toolbar-right {
  display: flex;
  gap: 8px;
}
</style>
