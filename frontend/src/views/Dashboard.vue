<template>
  <div class="dashboard">
    <div class="header">
      <h1>LongChain RAG 系统</h1>
      <div class="user-section">
        <el-dropdown @command="handleCommand" trigger="click">
          <div class="user-info">
            <el-avatar :size="32" :src="userStore.user?.avatar" :icon="UserFilled" />
            <span>{{ userStore.user?.username }}</span>
            <el-icon><ArrowDown /></el-icon>
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
              <el-dropdown-item command="logout" divided>
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon conversations">
            <el-icon :size="32"><ChatDotRound /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.conversations }}</div>
            <div class="stat-label">会话数量</div>
          </div>
        </el-card>

        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon messages">
            <el-icon :size="32"><ChatLineRound /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.messages }}</div>
            <div class="stat-label">消息数量</div>
          </div>
        </el-card>

        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon documents">
            <el-icon :size="32"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.documents }}</div>
            <div class="stat-label">知识库文档</div>
          </div>
        </el-card>

        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon chunks">
            <el-icon :size="32"><Grid /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.chunks }}</div>
            <div class="stat-label">文本块总数</div>
          </div>
        </el-card>
      </div>

      <!-- 功能入口 -->
      <div class="features-grid">
        <el-card class="feature-card" shadow="hover" @click="router.push('/chat')">
          <div class="feature-icon chat">
            <el-icon :size="48"><ChatDotSquare /></el-icon>
          </div>
          <h3>智能对话</h3>
          <p>基于知识库的智能问答，支持上下文理解和多轮对话</p>
          <el-button type="primary" text>开始对话 →</el-button>
        </el-card>

        <el-card class="feature-card" shadow="hover" @click="router.push('/kb-manage')" v-if="userStore.isAdmin()">
          <div class="feature-icon kb">
            <el-icon :size="48"><FolderOpened /></el-icon>
          </div>
          <h3>知识库管理</h3>
          <p>上传、管理文档，自动分块和向量化，构建专属知识库</p>
          <el-button type="primary" text>管理知识库 →</el-button>
        </el-card>

        <el-card class="feature-card" shadow="hover" @click="router.push('/history')">
          <div class="feature-icon history">
            <el-icon :size="48"><Clock /></el-icon>
          </div>
          <h3>历史记录</h3>
          <p>查看和管理所有对话历史，支持搜索和导出功能</p>
          <el-button type="primary" text>查看历史 →</el-button>
        </el-card>

        <el-card class="feature-card" shadow="hover" @click="router.push('/settings')">
          <div class="feature-icon settings">
            <el-icon :size="48"><Setting /></el-icon>
          </div>
          <h3>系统设置</h3>
          <p>配置模型参数、调整回答风格、管理个人信息</p>
          <el-button type="primary" text>进入设置 →</el-button>
        </el-card>
      </div>

      <!-- 最近对话 -->
      <el-card class="recent-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>最近对话</span>
            <el-button text type="primary" @click="router.push('/chat')">
              查看全部 →
            </el-button>
          </div>
        </template>
        <div v-loading="loading" class="recent-list">
          <div
            v-for="conv in recentConversations"
            :key="conv.id"
            class="recent-item"
            @click="goToConversation(conv.id)"
          >
            <div class="recent-info">
              <div class="recent-title">{{ conv.title }}</div>
              <div class="recent-time">{{ formatTime(conv.updated_at) }}</div>
            </div>
            <el-icon class="recent-arrow"><ArrowRight /></el-icon>
          </div>
          <el-empty v-if="recentConversations.length === 0 && !loading" description="暂无对话记录" />
        </div>
      </el-card>
    </div>

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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  UserFilled,
  ArrowDown,
  SwitchButton,
  ChatDotRound,
  ChatLineRound,
  Document,
  Grid,
  ChatDotSquare,
  FolderOpened,
  Clock,
  Setting,
  ArrowRight,
  Upload
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getConversations } from '@/api/chat'
import { getDocuments } from '@/api/kb'
import type { Conversation } from '@/api/chat'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const recentConversations = ref<Conversation[]>([])
const stats = ref({
  conversations: 0,
  messages: 0,
  documents: 0,
  chunks: 0
})

// 加载统计数据
const loadStats = async () => {
  loading.value = true
  try {
    // 加载会话
    const conversations = await getConversations()
    stats.value.conversations = conversations.length

    // 计算消息总数
    stats.value.messages = conversations.reduce((sum, conv) => sum + (conv.message_count || 0), 0)

    // 最近5个会话
    recentConversations.value = conversations.slice(0, 5)

    // 加载文档（仅管理员）
    if (userStore.isAdmin()) {
      const docs = await getDocuments()
      stats.value.documents = docs.documents.length
      stats.value.chunks = docs.documents.reduce((sum, doc) => sum + doc.chunk_count, 0)
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatTime = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString('zh-CN')
}

// 跳转到对话
const goToConversation = (id: number) => {
  router.push(`/chat?conversation=${id}`)
}

// 下拉菜单命令
const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  } else if (command === 'settings') {
    router.push('/settings')
  } else if (command === 'avatar') {
    showAvatarDialog()
  }
}

// 预设头像列表
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

const avatarDialogVisible = ref(false)
const uploadRef = ref()

// 显示头像对话框
const showAvatarDialog = () => {
  avatarDialogVisible.value = true
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

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 40px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header h1 {
  margin: 0;
  font-size: 24px;
  color: white;
  font-weight: 600;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.3);
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  display: flex;
  gap: 16px;
  padding: 24px;
  cursor: pointer;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon.conversations {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.messages {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.documents {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.chunks {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.feature-card {
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.feature-icon.chat {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.feature-icon.kb {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.feature-icon.history {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.feature-icon.settings {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.feature-card h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: #333;
}

.feature-card p {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  min-height: 42px;
}

.recent-card {
  margin-bottom: 40px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
}

.recent-list {
  min-height: 200px;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.recent-item:hover {
  background: #f5f5f5;
}

.recent-info {
  flex: 1;
}

.recent-title {
  font-size: 15px;
  color: #333;
  margin-bottom: 4px;
}

.recent-time {
  font-size: 13px;
  color: #999;
}

.recent-arrow {
  color: #999;
  transition: transform 0.2s;
}

.recent-item:hover .recent-arrow {
  transform: translateX(4px);
  color: #409eff;
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

.el-upload__tip {
  color: #999;
  font-size: 12px;
  margin-top: 8px;
}
</style>
