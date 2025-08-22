import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for file uploads
})

export interface PaperUploadResponse {
  paper_id: string
  title: string
  message: string
}

export interface PaperSummary {
  paper_id: string
  title: string
  summary: string
  pros: string[]
  cons: string[]
  future_work: string[]
}

export interface ChatResponse {
  response: string
}

export async function uploadPaper(file: File): Promise<PaperUploadResponse> {
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await api.post('/upload-paper', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Upload failed')
    }
    throw error
  }
}

export async function uploadPaperFromURL(url: string): Promise<PaperUploadResponse> {
  const formData = new FormData()
  formData.append('url', url)

  try {
    const response = await api.post('/upload-paper', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'URL processing failed')
    }
    throw error
  }
}

export async function getPaperSummary(paperId: string): Promise<PaperSummary> {
  try {
    const response = await api.get(`/summary/${paperId}`)
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to get paper summary')
    }
    throw error
  }
}

export async function chatWithPaper(paperId: string, query: string): Promise<ChatResponse> {
  try {
    const response = await api.post(`/chat/${paperId}`, { query })
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Chat request failed')
    }
    throw error
  }
}

export async function exportPaper(paperId: string, format: 'pdf' | 'markdown'): Promise<void> {
  try {
    const response = await api.get(`/export/${paperId}/${format}`, {
      responseType: 'blob',
    })

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    
    // Get filename from response headers or use default
    const contentDisposition = response.headers['content-disposition']
    let filename = `paper-summary.${format}`
    
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="(.+)"/)
      if (filenameMatch) {
        filename = filenameMatch[1]
      }
    }
    
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Export failed')
    }
    throw error
  }
}
