<template>
  <div class="chat-container">
    <!-- 左侧会话列表 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <el-button @click="router.push('/dashboard')" :icon="HomeFilled" class="header-button">
          返回首页
        </el-button>
        <el-button type="primary" @click="handleNewConversation" :icon="Plus" class="header-button">
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
      <div v-if="!chatStore.currentConversationId" class="empty-state">
        <el-empty description="请选择或创建一个会话开始对话" />
      </div>

      <template v-else>
        <!-- 消息列表 -->
        <div ref="messageListRef" class="message-list">
          <div
            v-for="(msg, index) in chatStore.messages"
            :key="index"
            class="message-item"
            :class="msg.role"
          >
            <div class="message-bubble">
              <div class="message-content" v-html="renderMarkdown(msg.content)"></div>

              <!-- 引用来源 -->
              <div v-if="msg.sources && msg.sources.length > 0" class="sources">
                <el-collapse accordion>
                  <el-collapse-item title="查看引用来源" name="1">
                    <div
                      v-for="(source, idx) in msg.sources"
                      :key="idx"
                      class="source-item"
                    >
                      <div class="source-header">
                        <el-tag size="small">相似度: {{ (source.score * 100).toFixed(1) }}%</el-tag>
                      </div>
                      <div class="source-content">{{ source.content }}</div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入框 -->
        <div class="input-area">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题..."
            :disabled="chatStore.isStreaming"
            @keydown.enter.exact.prevent="handleSend"
          />
          <el-button
            type="primary"
            :loading="chatStore.isStreaming"
            :disabled="!inputMessage.trim()"
            @click="handleSend"
          >
            {{ chatStore.isStreaming ? '生成中...' : '发送' }}
          </el-button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, User, Document, SwitchButton, HomeFilled } from '@element-plus/icons-vue'
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

.header-button {
  width: 100%;
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

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message-item {
  margin-bottom: 20px;
  display: flex;
}

.message-item.user {
  justify-content: flex-end;
}

.message-item.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  word-wrap: break-word;
}

.message-item.user .message-bubble {
  background: #409eff;
  color: white;
}

.message-item.assistant .message-bubble {
  background: #f5f5f5;
  color: #333;
}

.message-content {
  line-height: 1.6;
}

.message-content :deep(p) {
  margin: 0;
}

.sources {
  margin-top: 12px;
}

.source-item {
  margin-bottom: 12px;
  padding: 12px;
  background: white;
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

.input-area {
  padding: 20px;
  border-top: 1px solid #e5e5e5;
  display: flex;
  gap: 12px;
  background: white;
}

.input-area .el-textarea {
  flex: 1;
}
</style>
