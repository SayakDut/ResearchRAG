import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import { Download, MessageCircle, FileText, ThumbsUp, ThumbsDown, Lightbulb } from 'lucide-react'
import Layout from '@/components/Layout'
import ChatBox from '@/components/ChatBox'
import { getPaperSummary, exportPaper } from '@/lib/api'

interface PaperData {
  paper_id: string
  title: string
  summary: string
  pros: string[]
  cons: string[]
  future_work: string[]
}

export default function PaperPage() {
  const router = useRouter()
  const { id } = router.query
  const [paper, setPaper] = useState<PaperData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'summary' | 'chat'>('summary')

  useEffect(() => {
    if (id && typeof id === 'string') {
      loadPaper(id)
    }
  }, [id])

  const loadPaper = async (paperId: string) => {
    try {
      setLoading(true)
      const data = await getPaperSummary(paperId)
      setPaper(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load paper')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (format: 'pdf' | 'markdown') => {
    if (!paper) return
    
    try {
      await exportPaper(paper.paper_id, format)
    } catch (err) {
      console.error('Export failed:', err)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading paper analysis...</p>
          </div>
        </div>
      </Layout>
    )
  }

  if (error || !paper) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Paper Not Found</h2>
            <p className="text-gray-600 mb-6">{error || 'The requested paper could not be found.'}</p>
            <button
              onClick={() => router.push('/')}
              className="btn-primary"
            >
              Upload Another Paper
            </button>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <>
      <Head>
        <title>{paper.title} - ResearchRAG</title>
      </Head>
      
      <Layout>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-6xl mx-auto px-4 py-8">
            {/* Header */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">{paper.title}</h1>
              
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={() => handleExport('pdf')}
                  className="flex items-center gap-2 btn-secondary"
                >
                  <Download className="w-4 h-4" />
                  Export PDF
                </button>
                <button
                  onClick={() => handleExport('markdown')}
                  className="flex items-center gap-2 btn-secondary"
                >
                  <Download className="w-4 h-4" />
                  Export Markdown
                </button>
              </div>
            </div>

            {/* Tabs */}
            <div className="bg-white rounded-lg shadow-md">
              <div className="border-b border-gray-200">
                <nav className="flex">
                  <button
                    onClick={() => setActiveTab('summary')}
                    className={`flex items-center gap-2 px-6 py-4 font-medium border-b-2 transition-colors ${
                      activeTab === 'summary'
                        ? 'border-primary-600 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    <FileText className="w-4 h-4" />
                    Analysis
                  </button>
                  <button
                    onClick={() => setActiveTab('chat')}
                    className={`flex items-center gap-2 px-6 py-4 font-medium border-b-2 transition-colors ${
                      activeTab === 'chat'
                        ? 'border-primary-600 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    <MessageCircle className="w-4 h-4" />
                    Chat
                  </button>
                </nav>
              </div>

              <div className="p-6">
                {activeTab === 'summary' ? (
                  <div className="space-y-8">
                    {/* Summary */}
                    <section>
                      <h2 className="text-2xl font-bold text-gray-900 mb-4">Summary</h2>
                      <div className="prose max-w-none">
                        <p className="text-gray-700 leading-relaxed">{paper.summary}</p>
                      </div>
                    </section>

                    <div className="grid md:grid-cols-2 gap-8">
                      {/* Strengths */}
                      <section>
                        <div className="flex items-center gap-2 mb-4">
                          <ThumbsUp className="w-5 h-5 text-green-600" />
                          <h2 className="text-xl font-bold text-gray-900">Strengths</h2>
                        </div>
                        <ul className="space-y-3">
                          {paper.pros.map((pro, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                              <span className="text-gray-700">{pro}</span>
                            </li>
                          ))}
                        </ul>
                      </section>

                      {/* Weaknesses */}
                      <section>
                        <div className="flex items-center gap-2 mb-4">
                          <ThumbsDown className="w-5 h-5 text-red-600" />
                          <h2 className="text-xl font-bold text-gray-900">Weaknesses</h2>
                        </div>
                        <ul className="space-y-3">
                          {paper.cons.map((con, index) => (
                            <li key={index} className="flex items-start gap-3">
                              <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                              <span className="text-gray-700">{con}</span>
                            </li>
                          ))}
                        </ul>
                      </section>
                    </div>

                    {/* Future Work */}
                    <section>
                      <div className="flex items-center gap-2 mb-4">
                        <Lightbulb className="w-5 h-5 text-yellow-600" />
                        <h2 className="text-xl font-bold text-gray-900">Future Work</h2>
                      </div>
                      <ul className="space-y-3">
                        {paper.future_work.map((work, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0"></div>
                            <span className="text-gray-700">{work}</span>
                          </li>
                        ))}
                      </ul>
                    </section>
                  </div>
                ) : (
                  <ChatBox paperId={paper.paper_id} />
                )}
              </div>
            </div>
          </div>
        </div>
      </Layout>
    </>
  )
}
