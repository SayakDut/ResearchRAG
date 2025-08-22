import { useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import { Upload, Link as LinkIcon, FileText, Zap } from 'lucide-react'
import FileUpload from '@/components/FileUpload'
import URLInput from '@/components/URLInput'
import Layout from '@/components/Layout'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'upload' | 'url'>('upload')
  const router = useRouter()

  const handlePaperProcessed = (paperId: string) => {
    router.push(`/paper/${paperId}`)
  }

  return (
    <>
      <Head>
        <title>ResearchRAG - Upload Research Papers</title>
      </Head>
      
      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
          {/* Hero Section */}
          <div className="pt-20 pb-16">
            <div className="max-w-4xl mx-auto px-4 text-center">
              <div className="flex justify-center mb-6">
                <div className="p-3 bg-primary-600 rounded-full">
                  <FileText className="w-8 h-8 text-white" />
                </div>
              </div>
              
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                Research<span className="text-primary-600">RAG</span>
              </h1>
              
              <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                AI-powered research paper analysis. Upload PDFs or provide URLs to get instant summaries, 
                pros/cons analysis, and chat with your papers using advanced RAG technology.
              </p>
              
              <div className="flex flex-wrap justify-center gap-6 mb-12">
                <div className="flex items-center gap-2 text-gray-700">
                  <Zap className="w-5 h-5 text-primary-600" />
                  <span>Instant AI Summaries</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <FileText className="w-5 h-5 text-primary-600" />
                  <span>Pros & Cons Analysis</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <LinkIcon className="w-5 h-5 text-primary-600" />
                  <span>Interactive Chat</span>
                </div>
              </div>
            </div>
          </div>

          {/* Upload Section */}
          <div className="max-w-2xl mx-auto px-4 pb-20">
            <div className="card p-8">
              <div className="flex border-b border-gray-200 mb-6">
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`flex items-center gap-2 px-4 py-2 font-medium border-b-2 transition-colors ${
                    activeTab === 'upload'
                      ? 'border-primary-600 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Upload className="w-4 h-4" />
                  Upload PDF
                </button>
                <button
                  onClick={() => setActiveTab('url')}
                  className={`flex items-center gap-2 px-4 py-2 font-medium border-b-2 transition-colors ${
                    activeTab === 'url'
                      ? 'border-primary-600 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <LinkIcon className="w-4 h-4" />
                  Paper URL
                </button>
              </div>

              {activeTab === 'upload' ? (
                <FileUpload onPaperProcessed={handlePaperProcessed} />
              ) : (
                <URLInput onPaperProcessed={handlePaperProcessed} />
              )}
            </div>
          </div>
        </div>
      </Layout>
    </>
  )
}
