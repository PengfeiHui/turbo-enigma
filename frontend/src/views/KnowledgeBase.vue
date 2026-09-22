<template>
  <div class="kb-container">
    <div class="kb-header">
      <div class="header-left">
        <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
        <h2>知识库管理</h2>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="dialogVisible = true" :icon="Upload">
          上传文档
        </el-button>
      </div>
    </div>

    <div class="kb-content">
      <el-table :data="documents" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="filename" label="文件名" min-width="200" />
        <el-table-column prop="chunk_count" label="分块数量" width="120" />
        <el-table-column prop="created_at" label="上传时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row.id)"
              :icon="Delete"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="documents.length === 0 && !loading" class="empty-state">
        <el-empty description="暂无文档，请上传文档到知识库" />
      </div>
    </div>

    <!-- 上传对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="上传文档"
      width="500px"
      :close-on-click-modal="false"
    >
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
          <el-button @click="dialogVisible = false" :disabled="uploading">取消</el-button>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, genFileId } from 'element-plus'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { ArrowLeft, Upload, Delete, UploadFilled } from '@element-plus/icons-vue'
import { getDocuments, uploadDocument, deleteDocument } from '@/api/kb'
import type { Document } from '@/api/kb'

const router = useRouter()
const uploadRef = ref<UploadInstance>()

const loading = ref(false)
const uploading = ref(false)
const dialogVisible = ref(false)
const documents = ref<Document[]>([])
const selectedFiles = ref<File[]>([])
const uploadProgress = ref(0)
const currentUploadFile = ref('')

// 返回
const goBack = () => {
  router.push('/dashboard')
}

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 加载文档列表
const loadDocuments = async () => {
  loading.value = true
  try {
    const res = await getDocuments()
    documents.value = res.documents
  } catch (error) {
    console.error('Failed to load documents:', error)
  } finally {
    loading.value = false
  }
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
  ElMessage.warning(`最多只能选择 20 个文件，当前选择了 ${files.length + selectedFiles.value.length} 个`)
}

// 上传文档（批量）
const handleUpload = async () => {
  if (selectedFiles.value.length === 0) {
    ElMessage.warning('请先选择文件')
    return
  }

  // 检查文件大小（10MB）
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
        console.log(`✅ ${file.name} 上传成功，已分割为 ${res.chunk_count} 个文本块`)
        successCount++
      } catch (error) {
        console.error(`❌ ${file.name} 上传失败:`, error)
        failCount++
      }
    }

    // 显示结果
    if (failCount === 0) {
      ElMessage.success(`全部上传成功！共 ${successCount} 个文件`)
    } else {
      ElMessage.warning(`上传完成：成功 ${successCount} 个，失败 ${failCount} 个`)
    }

    dialogVisible.value = false
    uploadRef.value?.clearFiles()
    selectedFiles.value = []
    await loadDocuments()
  } catch (error) {
    console.error('Upload error:', error)
  } finally {
    uploading.value = false
    uploadProgress.value = 0
    currentUploadFile.value = ''
  }
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
}

.kb-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.el-upload__tip {
  color: #999;
  font-size: 12px;
  margin-top: 8px;
}
</style>
