import { useState } from 'react'
import { Link as LinkIcon, Loader2 } from 'lucide-react'
import { uploadPaperFromURL } from '@/lib/api'

interface URLInputProps {
  onPaperProcessed: (paperId: string) => void
}

export default function URLInput({ onPaperProcessed }: URLInputProps) {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!url.trim()) {
      setError('Please enter a valid URL')
      return
    }

    try {
      setLoading(true)
      setError(null)
      
      const result = await uploadPaperFromURL(url.trim())
      onPaperProcessed(result.paper_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process URL')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <LinkIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Enter Paper URL
        </h3>
        <p className="text-gray-600">
          Provide a link to a research paper (arXiv, PDF URL, etc.)
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
            Paper URL
          </label>
          <input
            type="url"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://arxiv.org/abs/2301.00001 or https://example.com/paper.pdf"
            className="input-field"
            disabled={loading}
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !url.trim()}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Processing paper...
            </>
          ) : (
            <>
              <LinkIcon className="w-4 h-4" />
              Analyze Paper
            </>
          )}
        </button>
      </form>

      <div className="text-sm text-gray-500 space-y-2">
        <p className="font-medium">Supported sources:</p>
        <ul className="list-disc list-inside space-y-1 ml-4">
          <li>arXiv papers (arxiv.org/abs/...)</li>
          <li>Direct PDF URLs</li>
          <li>Research paper web pages</li>
        </ul>
      </div>
    </div>
  )
}
