<template>
  <div class="settings-container">
    <div class="settings-header">
      <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
      <h2>系统设置</h2>
    </div>

    <div class="settings-content">
      <el-tabs v-model="activeTab" class="settings-tabs">
        <!-- 个人信息 -->
        <el-tab-pane label="个人信息" name="profile">
          <el-card shadow="never">
            <el-form :model="profileForm" label-width="100px">
              <el-form-item label="用户名">
                <el-input v-model="profileForm.username" disabled />
              </el-form-item>
              <el-form-item label="角色">
                <el-tag :type="userStore.isAdmin() ? 'danger' : 'primary'">
                  {{ userStore.isAdmin() ? '管理员' : '普通用户' }}
                </el-tag>
              </el-form-item>
              <el-form-item label="注册时间">
                <span>{{ formatDate(userStore.user?.created_at || '') }}</span>
              </el-form-item>
            </el-form>
          </el-card>
        </el-tab-pane>

        <!-- 模型参数 -->
        <el-tab-pane label="模型参数" name="model">
          <el-card shadow="never">
            <el-form :model="modelForm" label-width="120px">
              <el-form-item label="温度 (Temperature)">
                <el-slider
                  v-model="modelForm.temperature"
                  :min="0"
                  :max="1"
                  :step="0.1"
                  show-input
                  :input-size="'small'"
                />
                <div class="form-hint">控制回答的随机性，值越高越随机，越低越确定</div>
              </el-form-item>

              <el-form-item label="最大 Token 数">
                <el-input-number
                  v-model="modelForm.maxTokens"
                  :min="100"
                  :max="4000"
                  :step="100"
                />
                <div class="form-hint">单次回答的最大长度</div>
              </el-form-item>

              <el-form-item label="检索文档数量">
                <el-input-number
                  v-model="modelForm.topK"
                  :min="1"
                  :max="10"
                  :step="1"
                />
                <div class="form-hint">从知识库检索的相关文档数量</div>
              </el-form-item>

              <el-form-item label="相似度阈值">
                <el-slider
                  v-model="modelForm.similarityThreshold"
                  :min="0"
                  :max="1"
                  :step="0.05"
                  show-input
                  :input-size="'small'"
                />
                <div class="form-hint">只使用相似度高于此阈值的文档</div>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="saveModelSettings">保存设置</el-button>
                <el-button @click="resetModelSettings">重置默认</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-tab-pane>

        <!-- 界面设置 -->
        <el-tab-pane label="界面设置" name="ui">
          <el-card shadow="never">
            <el-form :model="uiForm" label-width="120px">
              <el-form-item label="主题模式">
                <el-radio-group v-model="uiForm.theme">
                  <el-radio label="light">浅色</el-radio>
                  <el-radio label="dark">深色</el-radio>
                  <el-radio label="auto">跟随系统</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="字体大小">
                <el-radio-group v-model="uiForm.fontSize">
                  <el-radio label="small">小</el-radio>
                  <el-radio label="medium">中</el-radio>
                  <el-radio label="large">大</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="显示来源">
                <el-switch v-model="uiForm.showSources" />
                <div class="form-hint">在回答中显示知识库引用来源</div>
              </el-form-item>

              <el-form-item label="Markdown 渲染">
                <el-switch v-model="uiForm.enableMarkdown" />
                <div class="form-hint">启用消息的 Markdown 格式渲染</div>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="saveUISettings">保存设置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-tab-pane>

        <!-- 关于 -->
        <el-tab-pane label="关于" name="about">
          <el-card shadow="never">
            <div class="about-content">
              <div class="about-logo">
                <el-icon :size="64"><ChatDotSquare /></el-icon>
              </div>
              <h2>LongChain RAG 系统</h2>
              <p class="version">版本 1.0.0</p>
              <el-divider />
              <div class="about-info">
                <h3>技术栈</h3>
                <div class="tech-tags">
                  <el-tag>FastAPI</el-tag>
                  <el-tag type="success">Vue 3</el-tag>
                  <el-tag type="warning">TypeScript</el-tag>
                  <el-tag type="danger">ChromaDB</el-tag>
                  <el-tag type="info">Docker</el-tag>
                </div>

                <h3 style="margin-top: 24px;">功能特性</h3>
                <ul class="feature-list">
                  <li>基于 RAG 的智能问答系统</li>
                  <li>支持多种文档格式（PDF、DOCX、TXT）</li>
                  <li>自动文档分块和向量化</li>
                  <li>多轮对话上下文理解</li>
                  <li>实时流式输出</li>
                  <li>知识库管理功能</li>
                </ul>

                <h3 style="margin-top: 24px;">开源协议</h3>
                <p>MIT License</p>
              </div>
            </div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, ChatDotSquare } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('profile')

const profileForm = ref({
  username: '',
})

const modelForm = ref({
  temperature: 0.7,
  maxTokens: 2000,
  topK: 5,
  similarityThreshold: 0.6,
})

const uiForm = ref({
  theme: 'light',
  fontSize: 'medium',
  showSources: true,
  enableMarkdown: true,
})

// 返回
const goBack = () => {
  router.push('/dashboard')
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 保存模型设置
const saveModelSettings = () => {
  localStorage.setItem('modelSettings', JSON.stringify(modelForm.value))
  ElMessage.success('模型参数已保存')
}

// 重置模型设置
const resetModelSettings = () => {
  modelForm.value = {
    temperature: 0.7,
    maxTokens: 2000,
    topK: 5,
    similarityThreshold: 0.6,
  }
  ElMessage.success('已重置为默认值')
}

// 保存界面设置
const saveUISettings = () => {
  localStorage.setItem('uiSettings', JSON.stringify(uiForm.value))
  ElMessage.success('界面设置已保存')
}

// 加载设置
const loadSettings = () => {
  profileForm.value.username = userStore.user?.username || ''

  const savedModelSettings = localStorage.getItem('modelSettings')
  if (savedModelSettings) {
    modelForm.value = JSON.parse(savedModelSettings)
  }

  const savedUISettings = localStorage.getItem('uiSettings')
  if (savedUISettings) {
    uiForm.value = JSON.parse(savedUISettings)
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.settings-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

.settings-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.settings-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.settings-tabs {
  background: white;
  padding: 24px;
  border-radius: 8px;
}

.form-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.about-content {
  text-align: center;
  padding: 24px;
}

.about-logo {
  margin-bottom: 16px;
  color: #409eff;
}

.about-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.version {
  color: #999;
  font-size: 14px;
  margin-bottom: 24px;
}

.about-info {
  text-align: left;
}

.about-info h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
  color: #333;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.feature-list {
  margin: 12px 0;
  padding-left: 24px;
  line-height: 2;
  color: #666;
}

.feature-list li {
  list-style-type: disc;
}
</style>
