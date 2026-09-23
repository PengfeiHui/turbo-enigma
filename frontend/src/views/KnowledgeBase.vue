<template>
  <div class="kb-container">
    <div class="kb-header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <h2>知识库管理</h2>
      </div>
      <div class="header-right">
        <el-button @click="folderDialogVisible = true" :icon="FolderAdd">
          新建分类
        </el-button>
        <el-button type="primary" @click="uploadDialogVisible = true" :icon="Upload">
          上传文档
        </el-button>
      </div>
    </div>

    <div class="kb-main">
      <!-- 左侧分类列表 -->
      <div class="category-sidebar">
        <div class="category-header">
          <span>文档分类</span>
        </div>
        <div class="category-list">
          <div
            class="category-item"
            :class="{ active: currentCategory === null }"
            @click="selectCategory(null)"
          >
            <el-icon><Folder /></el-icon>
            <span>全部文档</span>
            <span class="count">{{ totalCount }}</span>
          </div>
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-item"
            :class="{ active: currentCategory === category.id }"
            @click="selectCategory(category.id)"
          >
            <el-icon><Folder /></el-icon>
            <span>{{ category.name }}</span>
            <span class="count">{{ category.docCount || 0 }}</span>
            <el-dropdown @command="(cmd) => handleCategoryAction(cmd, category)" trigger="click" class="category-actions">
              <el-icon class="more-icon" @click.stop><MoreFilled /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="rename">
                    <el-icon><Edit /></el-icon>
                    重命名
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" divided>
                    <el-icon><Delete /></el-icon>
                    删除分类
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>

      <!-- 右侧文档列表 -->
      <div class="document-area">
        <div class="document-toolbar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索文档名称..."
            :prefix-icon="Search"
            clearable
            style="width: 300px"
          />
          <div class="view-mode">
            <el-radio-group v-model="viewMode" size="small">
              <el-radio-button value="grid">
                <el-icon><Grid /></el-icon>
              </el-radio-button>
              <el-radio-button value="list">
                <el-icon><List /></el-icon>
              </el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <!-- 网格视图 -->
        <div v-if="viewMode === 'grid'" class="document-grid" v-loading="loading">
          <el-card
            v-for="doc in filteredDocuments"
            :key="doc.id"
            class="document-card"
            shadow="hover"
          >
            <div class="doc-icon">
              <el-icon :size="48"><Document /></el-icon>
            </div>
            <div class="doc-info">
              <div class="doc-name" :title="doc.filename">{{ doc.filename }}</div>
              <div class="doc-meta">
                <span>{{ doc.chunk_count }} 个文本块</span>
                <span>{{ formatDate(doc.created_at) }}</span>
              </div>
            </div>
            <div class="doc-actions">
              <el-button
                type="primary"
                size="small"
                text
                @click="moveDocument(doc)"
              >
                移动
              </el-button>
              <el-button
                type="danger"
                size="small"
                text
                @click="handleDelete(doc.id)"
              >
                删除
              </el-button>
            </div>
          </el-card>
          <el-empty v-if="filteredDocuments.length === 0 && !loading" description="暂无文档" />
        </div>

        <!-- 列表视图 -->
        <el-table
          v-else
          :data="filteredDocuments"
          v-loading="loading"
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="filename" label="文件名" min-width="250">
            <template #default="{ row }">
              <div style="display: flex; align-items: center; gap: 8px;">
                <el-icon><Document /></el-icon>
                <span>{{ row.filename }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" width="150">
            <template #default="{ row }">
              <el-tag v-if="row.categoryName" size="small">{{ row.categoryName }}</el-tag>
              <span v-else style="color: #999;">未分类</span>
            </template>
          </el-table-column>
          <el-table-column prop="chunk_count" label="文本块" width="100" />
          <el-table-column prop="created_at" label="上传时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="moveDocument(row)">
                移动
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleDelete(row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 新建分类对话框 -->
    <el-dialog
      v-model="folderDialogVisible"
      :title="editingCategory ? '重命名分类' : '新建分类'"
      width="400px"
    >
      <el-form :model="folderForm" label-width="80px">
        <el-form-item label="分类名称">
          <el-input
            v-model="folderForm.name"
            placeholder="请输入分类名称"
            maxlength="20"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="folderDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveCategory">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 上传文档对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传文档"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form label-width="80px">
        <el-form-item label="选择分类">
          <el-select v-model="uploadForm.categoryId" placeholder="请选择分类（可选）" clearable style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :limit="20"
        :on-exceed="handleExceed"
        :on-change="handleFileChange"
        :on-remove="handleFileRemove"
        drag
        accept=".pdf,.docx,.txt"
        multiple
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 PDF、DOCX、TXT 格式，单个文件不超过 10MB<br/>
            可同时选择多个文件（最多 20 个）
          </div>
        </template>
      </el-upload>

      <template #footer>
        <div v-if="uploading" style="margin-bottom: 16px; text-align: left;">
          <div style="margin-bottom: 8px;">
            正在上传: {{ currentUploadFile }}
          </div>
          <el-progress :percentage="uploadProgress" />
        </div>
        <div>
          <el-button @click="uploadDialogVisible = false" :disabled="uploading">取消</el-button>
          <el-button
            type="primary"
            :loading="uploading"
            :disabled="selectedFiles.length === 0"
            @click="handleUpload"
          >
            {{ uploading ? `上传中 (${uploadProgress}%)` : `确定上传 (${selectedFiles.length} 个文件)` }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 移动文档对话框 -->
    <el-dialog v-model="moveDialogVisible" title="移动文档" width="400px">
      <el-form label-width="80px">
        <el-form-item label="目标分类">
          <el-select v-model="moveForm.categoryId" placeholder="请选择目标分类" clearable style="width: 100%">
            <el-option label="未分类" :value="null" />
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="moveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleMoveDocument">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadInstance, UploadProps } from 'element-plus'
import {
  ArrowLeft,
  Upload,
  Delete,
  UploadFilled,
  Folder,
  FolderAdd,
  Document,
  Search,
  Grid,
  List,
  MoreFilled,
  Edit
} from '@element-plus/icons-vue'
import { getDocuments, uploadDocument, deleteDocument } from '@/api/kb'
import type { Document as DocType } from '@/api/kb'

const router = useRouter()
const uploadRef = ref<UploadInstance>()

const loading = ref(false)
const uploading = ref(false)
const uploadDialogVisible = ref(false)
const folderDialogVisible = ref(false)
const moveDialogVisible = ref(false)
const documents = ref<DocType[]>([])
const selectedFiles = ref<File[]>([])
const uploadProgress = ref(0)
const currentUploadFile = ref('')
const searchKeyword = ref('')
const viewMode = ref<'grid' | 'list'>('grid')
const currentCategory = ref<string | null>(null)
const editingCategory = ref<any>(null)

// 分类数据（临时使用 localStorage，后续可以改为后端API）
const categories = ref<any[]>([])

// 表单
const folderForm = ref({
  name: ''
})

const uploadForm = ref({
  categoryId: null as string | null
})

const moveForm = ref({
  categoryId: null as string | null
})

const movingDocument = ref<DocType | null>(null)

// 计算属性
const totalCount = computed(() => documents.value.length)

const filteredDocuments = computed(() => {
  let result = documents.value

  // 按分类筛选
  if (currentCategory.value !== null) {
    result = result.filter(doc => (doc as any).categoryId === currentCategory.value)
  }

  // 按关键词搜索
  if (searchKeyword.value) {
    result = result.filter(doc =>
      doc.filename.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }

  return result
})

// 返回
const goBack = () => {
  router.push('/dashboard')
}

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / 86400000)

  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString('zh-CN')
}

// 加载分类
const loadCategories = () => {
  const stored = localStorage.getItem('kb_categories')
  if (stored) {
    categories.value = JSON.parse(stored)
  }
  updateCategoryCounts()
}

// 保存分类
const saveCategories = () => {
  localStorage.setItem('kb_categories', JSON.stringify(categories.value))
}

// 更新分类文档数量
const updateCategoryCounts = () => {
  categories.value.forEach(cat => {
    cat.docCount = documents.value.filter((doc: any) => doc.categoryId === cat.id).length
  })
}

// 选择分类
const selectCategory = (id: string | null) => {
  currentCategory.value = id
}

// 分类操作
const handleCategoryAction = (command: string, category: any) => {
  if (command === 'rename') {
    editingCategory.value = category
    folderForm.value.name = category.name
    folderDialogVisible.value = true
  } else if (command === 'delete') {
    handleDeleteCategory(category)
  }
}

// 保存分类
const handleSaveCategory = () => {
  if (!folderForm.value.name.trim()) {
    ElMessage.warning('请输入分类名称')
    return
  }

  if (editingCategory.value) {
    // 重命名
    editingCategory.value.name = folderForm.value.name
    ElMessage.success('分类已重命名')
  } else {
    // 新建
    const newCategory = {
      id: Date.now().toString(),
      name: folderForm.value.name,
      docCount: 0
    }
    categories.value.push(newCategory)
    ElMessage.success('分类已创建')
  }

  saveCategories()
  folderDialogVisible.value = false
  folderForm.value.name = ''
  editingCategory.value = null
}

// 删除分类
const handleDeleteCategory = async (category: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除分类"${category.name}"吗？分类下的文档将移至未分类。`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 将该分类下的文档移至未分类
    documents.value.forEach((doc: any) => {
      if (doc.categoryId === category.id) {
        doc.categoryId = null
        doc.categoryName = null
      }
    })
    saveDocumentCategories()

    // 删除分类
    const index = categories.value.findIndex(c => c.id === category.id)
    if (index > -1) {
      categories.value.splice(index, 1)
    }
    saveCategories()

    if (currentCategory.value === category.id) {
      currentCategory.value = null
    }

    ElMessage.success('分类已删除')
  } catch (error) {
    // 取消删除
  }
}

// 加载文档列表
const loadDocuments = async () => {
  loading.value = true
  try {
    const res = await getDocuments()
    documents.value = res.documents

    // 加载文档分类信息
    const stored = localStorage.getItem('doc_categories')
    if (stored) {
      const docCategories = JSON.parse(stored)
      documents.value.forEach((doc: any) => {
        if (docCategories[doc.id]) {
          doc.categoryId = docCategories[doc.id].categoryId
          doc.categoryName = docCategories[doc.id].categoryName
        }
      })
    }

    updateCategoryCounts()
  } catch (error) {
    console.error('Failed to load documents:', error)
  } finally {
    loading.value = false
  }
}

// 保存文档分类信息
const saveDocumentCategories = () => {
  const docCategories: any = {}
  documents.value.forEach((doc: any) => {
    if (doc.categoryId) {
      docCategories[doc.id] = {
        categoryId: doc.categoryId,
        categoryName: doc.categoryName
      }
    }
  })
  localStorage.setItem('doc_categories', JSON.stringify(docCategories))
}

// 文件选择
const handleFileChange: UploadProps['onChange'] = (uploadFile) => {
  if (uploadFile.raw) {
    selectedFiles.value.push(uploadFile.raw)
  }
}

// 文件移除
const handleFileRemove: UploadProps['onRemove'] = (uploadFile) => {
  const index = selectedFiles.value.findIndex(f => f.name === uploadFile.name)
  if (index > -1) {
    selectedFiles.value.splice(index, 1)
  }
}

// 文件超出限制
const handleExceed: UploadProps['onExceed'] = (files) => {
  ElMessage.warning(`最多只能选择 20 个文件`)
}

// 上传文档
const handleUpload = async () => {
  if (selectedFiles.value.length === 0) {
    ElMessage.warning('请先选择文件')
    return
  }

  const oversizeFiles = selectedFiles.value.filter(f => f.size > 10 * 1024 * 1024)
  if (oversizeFiles.length > 0) {
    ElMessage.error(`以下文件超过 10MB：${oversizeFiles.map(f => f.name).join(', ')}`)
    return
  }

  uploading.value = true
  uploadProgress.value = 0

  let successCount = 0
  let failCount = 0

  try {
    for (let i = 0; i < selectedFiles.value.length; i++) {
      const file = selectedFiles.value[i]
      currentUploadFile.value = file.name
      uploadProgress.value = Math.round(((i + 1) / selectedFiles.value.length) * 100)

      try {
        const res = await uploadDocument(file)

        // 保存分类信息
        if (uploadForm.value.categoryId) {
          const category = categories.value.find(c => c.id === uploadForm.value.categoryId)
          const docCategories = JSON.parse(localStorage.getItem('doc_categories') || '{}')
          docCategories[res.document_id] = {
            categoryId: uploadForm.value.categoryId,
            categoryName: category?.name || ''
          }
          localStorage.setItem('doc_categories', JSON.stringify(docCategories))
        }

        successCount++
      } catch (error) {
        console.error(`❌ ${file.name} 上传失败:`, error)
        failCount++
      }
    }

    if (failCount === 0) {
      ElMessage.success(`全部上传成功！共 ${successCount} 个文件`)
    } else {
      ElMessage.warning(`上传完成：成功 ${successCount} 个，失败 ${failCount} 个`)
    }

    uploadDialogVisible.value = false
    uploadRef.value?.clearFiles()
    selectedFiles.value = []
    uploadForm.value.categoryId = null
    await loadDocuments()
  } catch (error) {
    console.error('Upload error:', error)
  } finally {
    uploading.value = false
    uploadProgress.value = 0
    currentUploadFile.value = ''
  }
}

// 移动文档
const moveDocument = (doc: DocType) => {
  movingDocument.value = doc
  moveForm.value.categoryId = (doc as any).categoryId || null
  moveDialogVisible.value = true
}

// 确认移动文档
const handleMoveDocument = () => {
  if (!movingDocument.value) return

  const doc: any = movingDocument.value
  doc.categoryId = moveForm.value.categoryId

  if (moveForm.value.categoryId) {
    const category = categories.value.find(c => c.id === moveForm.value.categoryId)
    doc.categoryName = category?.name || ''
  } else {
    doc.categoryName = null
  }

  saveDocumentCategories()
  updateCategoryCounts()

  moveDialogVisible.value = false
  movingDocument.value = null
  ElMessage.success('文档已移动')
}

// 删除文档
const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个文档吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteDocument(id)
    ElMessage.success('文档已删除')
    await loadDocuments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete document:', error)
    }
  }
}

onMounted(() => {
  loadCategories()
  loadDocuments()
})
</script>

<style scoped>
.kb-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.kb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.header-right {
  display: flex;
  gap: 12px;
}

.kb-main {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 左侧分类 */
.category-sidebar {
  width: 240px;
  background: white;
  border-right: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
}

.category-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e5e5e5;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.category-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  margin-bottom: 4px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  color: #606266;
  font-size: 14px;
  position: relative;
}

.category-item:hover {
  background: #f5f7fa;
}

.category-item.active {
  background: #ecf5ff;
  color: #409eff;
  font-weight: 500;
}

.category-item .count {
  margin-left: auto;
  font-size: 12px;
  color: #909399;
  background: #f4f4f5;
  padding: 2px 8px;
  border-radius: 10px;
}

.category-item.active .count {
  background: #409eff;
  color: white;
}

.category-actions {
  opacity: 0;
  transition: opacity 0.2s;
}

.category-item:hover .category-actions {
  opacity: 1;
}

.more-icon {
  padding: 4px;
  border-radius: 4px;
  cursor: pointer;
}

.more-icon:hover {
  background: rgba(0, 0, 0, 0.05);
}

/* 右侧文档区域 */
.document-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.document-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

.view-mode {
  display: flex;
  gap: 8px;
}

.document-grid {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  align-content: start;
}

.document-card {
  cursor: pointer;
  transition: all 0.3s;
  padding: 20px;
}

.document-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.doc-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
  color: #409eff;
}

.doc-info {
  margin-bottom: 12px;
}

.doc-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.doc-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.doc-actions {
  display: flex;
  gap: 8px;
  justify-content: center;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.el-upload__tip {
  color: #999;
  font-size: 12px;
  margin-top: 8px;
}
</style>
