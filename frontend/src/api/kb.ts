import request from '@/utils/request'

export interface KnowledgeBaseCreate {
  name: string
  description?: string
}

export interface KnowledgeBase {
  id: number
  name: string
  description?: string
  created_at: string
}

export interface Document {
  id: number
  kb_id: number
  filename: string
  chunk_count: number
  created_at: string
}

export interface DocumentListResponse {
  documents: Document[]
  total: number
}

export interface UploadResponse {
  message: string
  document_id: number
  filename: string
  chunk_count: number
}

// 创建知识库
export const createKnowledgeBase = (data: KnowledgeBaseCreate) => {
  return request.post<any, KnowledgeBase>('/kb/knowledge-bases', data)
}

// 获取知识库列表
export const getKnowledgeBases = () => {
  return request.get<any, KnowledgeBase[]>('/kb/knowledge-bases')
}

// 上传文档
export const uploadDocument = (file: File, kbId: number = 1) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('kb_id', kbId.toString())

  return request.post<any, UploadResponse>('/kb/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取文档列表
export const getDocuments = (kbId?: number) => {
  return request.get<any, DocumentListResponse>('/kb/documents', {
    params: kbId ? { kb_id: kbId } : {}
  })
}

// 删除文档
export const deleteDocument = (documentId: number) => {
  return request.delete(`/kb/documents/${documentId}`)
}
