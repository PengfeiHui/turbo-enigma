<template>
  <div class="modern-dashboard">
    <!-- 顶部导航 -->
    <nav class="top-nav">
      <div class="nav-content">
        <div class="brand">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" opacity="0.3"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <span class="brand-text">LongChain RAG</span>
        </div>

        <div class="nav-actions">
          <button class="nav-btn" @click="router.push('/chat')">
            <el-icon><ChatDotSquare /></el-icon>
            <span>开始对话</span>
          </button>

          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-menu">
              <el-avatar :size="36" :src="userStore.user?.avatar" :icon="UserFilled" />
              <span class="username">{{ userStore.user?.username }}</span>
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
    </nav>

    <!-- 主要内容 -->
    <div class="dashboard-main">
      <!-- 欢迎区域 -->
      <section class="welcome-section">
        <div class="welcome-content">
          <h1 class="greeting">
            {{ getGreeting() }}，<span class="highlight">{{ userStore.user?.username }}</span>
          </h1>
          <p class="tagline">基于知识库的智能对话系统，让信息触手可及</p>
        </div>

        <!-- 统计卡片 - 现代化设计 -->
        <div class="stats-cards">
          <div class="stat-card stat-primary">
            <div class="stat-content">
              <div class="stat-label">对话次数</div>
              <div class="stat-value">{{ stats.conversations }}</div>
            </div>
            <div class="stat-icon">
              <el-icon><ChatDotRound /></el-icon>
            </div>
          </div>

          <div class="stat-card stat-success">
            <div class="stat-content">
              <div class="stat-label">消息总数</div>
              <div class="stat-value">{{ stats.messages }}</div>
            </div>
            <div class="stat-icon">
              <el-icon><ChatLineRound /></el-icon>
            </div>
          </div>

          <template v-if="userStore.isAdmin()">
            <div class="stat-card stat-warning">
              <div class="stat-content">
                <div class="stat-label">知识文档</div>
                <div class="stat-value">{{ stats.documents }}</div>
              </div>
              <div class="stat-icon">
                <el-icon><Document /></el-icon>
              </div>
            </div>

            <div class="stat-card stat-info">
              <div class="stat-content">
                <div class="stat-label">文本块数</div>
                <div class="stat-value">{{ stats.chunks }}</div>
              </div>
              <div class="stat-icon">
                <el-icon><Grid /></el-icon>
              </div>
            </div>
          </template>
        </div>
      </section>

      <!-- 快速操作区域 -->
      <section class="quick-actions">
        <h2 class="section-title">快速开始</h2>
        <div class="action-grid">
          <div class="action-card action-chat" @click="router.push('/chat')">
            <div class="action-bg"></div>
            <div class="action-content">
              <div class="action-icon">
                <el-icon><ChatDotSquare /></el-icon>
              </div>
              <h3>智能对话</h3>
              <p>与 AI 开始新的对话</p>
            </div>
          </div>

          <div v-if="userStore.isAdmin()" class="action-card action-kb" @click="router.push('/kb-manage')">
            <div class="action-bg"></div>
            <div class="action-content">
              <div class="action-icon">
                <el-icon><FolderOpened /></el-icon>
              </div>
              <h3>知识库</h3>
              <p>管理文档和知识</p>
            </div>
          </div>

          <div class="action-card action-history" @click="router.push('/history')">
            <div class="action-bg"></div>
            <div class="action-content">
              <div class="action-icon">
                <el-icon><Clock /></el-icon>
              </div>
              <h3>历史记录</h3>
              <p>查看过往对话</p>
            </div>
          </div>

          <div class="action-card action-settings" @click="router.push('/settings')">
            <div class="action-bg"></div>
            <div class="action-content">
              <div class="action-icon">
                <el-icon><Setting /></el-icon>
              </div>
              <h3>系统设置</h3>
              <p>个性化配置</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 最近对话 -->
      <section class="recent-section">
        <div class="section-header">
          <h2 class="section-title">最近对话</h2>
          <button class="view-all-btn" @click="router.push('/chat')">
            查看全部
            <el-icon><ArrowRight /></el-icon>
          </button>
        </div>

        <div v-loading="loading" class="recent-list">
          <div
            v-for="conv in recentConversations"
            :key="conv.id"
            class="recent-item"
            @click="goToConversation(conv.id)"
          >
            <div class="recent-icon">
              <el-icon><ChatLineRound /></el-icon>
            </div>
            <div class="recent-info">
              <div class="recent-title">{{ conv.title }}</div>
              <div class="recent-time">{{ formatTime(conv.updated_at) }}</div>
            </div>
            <div class="recent-arrow">
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>

          <div v-if="recentConversations.length === 0 && !loading" class="empty-recent">
            <el-icon :size="48"><ChatDotRound /></el-icon>
            <p>暂无对话记录</p>
            <button class="start-btn" @click="router.push('/chat')">开始第一次对话</button>
          </div>
        </div>
      </section>
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
const avatarDialogVisible = ref(false)

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

// 获取问候语
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  if (hour < 22) return '晚上好'
  return '夜深了'
}

// 加载统计数据
const loadStats = async () => {
  loading.value = true
  try {
    const conversations = await getConversations()
    stats.value.conversations = conversations.length
    stats.value.messages = conversations.reduce((sum, conv) => sum + (conv.message_count || 0), 0)
    recentConversations.value = conversations.slice(0, 5)

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
    avatarDialogVisible.value = true
  }
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
.modern-dashboard {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%);
}

/* 顶部导航 */
.top-nav {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand-icon svg {
  width: 20px;
  height: 20px;
}

.brand-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px 6px 6px;
  background: #f5f7fa;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s;
}

.user-menu:hover {
  background: #e8ecf1;
}

.username {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

/* 主要内容 */
.dashboard-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 32px;
}

/* 欢迎区域 */
.welcome-section {
  margin-bottom: 48px;
}

.welcome-content {
  margin-bottom: 32px;
}

.greeting {
  font-size: 36px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.highlight {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.tagline {
  font-size: 16px;
  color: #666;
  margin: 0;
}

/* 统计卡片 - 现代化 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  max-width: 900px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.stat-card.stat-primary {
  border-color: #667eea;
}

.stat-card.stat-primary .stat-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.stat-success {
  border-color: #42d392;
}

.stat-card.stat-success .stat-icon {
  background: linear-gradient(135deg, #42d392 0%, #37b67e 100%);
}

.stat-card.stat-warning {
  border-color: #ffb648;
}

.stat-card.stat-warning .stat-icon {
  background: linear-gradient(135deg, #ffb648 0%, #ffa726 100%);
}

.stat-card.stat-info {
  border-color: #4fc3f7;
}

.stat-card.stat-info .stat-icon {
  background: linear-gradient(135deg, #4fc3f7 0%, #29b6f6 100%);
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

/* 快速操作 */
.quick-actions {
  margin-bottom: 48px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 24px 0;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.action-card {
  position: relative;
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.action-bg {
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  opacity: 0.1;
  transition: all 0.4s;
}

.action-card:hover .action-bg {
  transform: scale(1.3);
  opacity: 0.15;
}

.action-chat .action-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.action-kb .action-bg {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.action-history .action-bg {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.action-settings .action-bg {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.action-content {
  position: relative;
  z-index: 1;
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  font-size: 24px;
  color: white;
}

.action-chat .action-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.action-kb .action-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.action-history .action-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.action-settings .action-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.action-card h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.action-card p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* 最近对话 */
.recent-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.view-all-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.view-all-btn:hover {
  background: #f5f7fa;
  border-color: #667eea;
  color: #667eea;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.recent-item:hover {
  background: #f8f9ff;
}

.recent-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  flex-shrink: 0;
}

.recent-info {
  flex: 1;
  min-width: 0;
}

.recent-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-time {
  font-size: 13px;
  color: #888;
}

.recent-arrow {
  color: #ccc;
  font-size: 18px;
  transition: all 0.3s;
}

.recent-item:hover .recent-arrow {
  color: #667eea;
  transform: translateX(4px);
}

.empty-recent {
  text-align: center;
  padding: 48px 24px;
}

.empty-recent .el-icon {
  color: #ddd;
  margin-bottom: 16px;
}

.empty-recent p {
  font-size: 14px;
  color: #999;
  margin: 0 0 24px 0;
}

.start-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
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

/* 骨架屏样式 */
.skeleton-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 8px;
}

.skeleton-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  flex-shrink: 0;
}

.skeleton-content {
  flex: 1;
}

.skeleton-line {
  height: 14px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  border-radius: 4px;
  animation: shimmer 1.5s ease-in-out infinite;
  margin-bottom: 8px;
}

.skeleton-line.short {
  width: 60%;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
