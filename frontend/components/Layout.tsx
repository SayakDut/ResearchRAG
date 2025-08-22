import { ReactNode } from 'react'
import Link from 'next/link'
import { FileText, Github } from 'lucide-react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center gap-2 font-bold text-xl text-gray-900">
              <div className="p-2 bg-primary-600 rounded-lg">
                <FileText className="w-5 h-5 text-white" />
              </div>
              Research<span className="text-primary-600">RAG</span>
            </Link>
            
            <div className="flex items-center gap-4">
              <Link
                href="/"
                className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
              >
                Upload Paper
              </Link>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              Built with Next.js, FastAPI, and OpenRouter AI
            </p>
            <p className="text-sm">
              ResearchRAG - AI-Powered Research Paper Analysis
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
