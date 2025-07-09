'use client'

import { useState, useEffect } from 'react'
import { 
  FileText, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  ThumbsUp, 
  ThumbsDown, 
  Edit3,
  RotateCcw,
  Eye,
  Settings,
  Download,
  Upload,
  Zap,
  Loader2
} from 'lucide-react'
import { apiClient, type ProtocolAnalysis, type Suggestion } from '@/lib/api'

export default function ProtocolEditor() {
  const [analysis, setAnalysis] = useState<ProtocolAnalysis | null>(null)
  const [selectedSuggestion, setSelectedSuggestion] = useState<Suggestion | null>(null)
  const [editingText, setEditingText] = useState<string>('')
  const [showOriginal, setShowOriginal] = useState(false)
  const [filterType, setFilterType] = useState<string>('all')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [protocolId] = useState('protocol_123') // Default to existing protocol

  // Load analysis data
  useEffect(() => {
    loadAnalysis()
  }, [])

  const loadAnalysis = async () => {
    try {
      setError(null)
      setIsAnalyzing(true)
      const analysisData = await apiClient.getFormattedAnalysis(protocolId)
      setAnalysis(analysisData)
    } catch (err) {
      console.error('Error loading analysis:', err)
      setError('Failed to load analysis. Using mock data.')
      // Fallback to mock data
      setAnalysis({
        protocol_id: protocolId,
        overall_score: 85.5,
        component_scores: {
          consort_compliance: 88.0,
          spirit_compliance: 83.0,
          clarity_score: 82.5,
          consistency_score: 89.0
        },
        suggestions: [
          {
            id: 'sug_1',
            type: 'missing_item',
            section: 'Methods',
            issue: 'Missing primary outcome definition',
            suggested_text: 'The primary outcome is the change in systolic blood pressure from baseline to 12 weeks, measured using a standardized sphygmomanometer in the seated position after 5 minutes of rest.',
            explanation: 'CONSORT guidelines require a clear definition of primary outcomes with specific measurement methods and timing.',
            confidence: 0.92,
            status: 'pending',
            guideline: 'CONSORT 6a'
          },
          {
            id: 'sug_2',
            type: 'clarity',
            section: 'Participants',
            issue: 'Inclusion criteria could be more specific',
            suggested_text: 'Adults aged 18-65 years with hypertension (systolic BP ≥140 mmHg or diastolic BP ≥90 mmHg on two separate occasions) who are not currently taking antihypertensive medications.',
            explanation: 'More specific criteria help ensure consistent participant selection and improve reproducibility.',
            confidence: 0.78,
            status: 'pending'
          },
          {
            id: 'sug_3',
            type: 'consistency',
            section: 'Statistical Analysis',
            issue: 'Sample size calculation inconsistent with stated power',
            suggested_text: 'Based on a two-sided alpha of 0.05, power of 80%, and expected difference of 10 mmHg (SD=15), we require 36 participants per group. Accounting for 20% dropout, we will recruit 45 participants per group (total N=90).',
            explanation: 'The current sample size calculation shows 90% power but the methods section mentions 80% power.',
            confidence: 0.85,
            status: 'pending'
          }
        ],
        executive_summary: 'This protocol demonstrates good overall compliance with CONSORT/SPIRIT guidelines with a score of 85.5%. Key strengths include well-defined study design and comprehensive statistical analysis plan. Primary areas for improvement include more specific outcome definitions and consistency in power calculations.',
        analysis_provider: 'mock',
        analyzed_at: new Date().toISOString()
      })
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleSuggestionAction = (suggestionId: string, action: 'accept' | 'reject' | 'modify') => {
    if (!analysis) return

    const updatedSuggestions = analysis.suggestions.map(sug => 
      sug.id === suggestionId 
        ? { ...sug, status: action === 'modify' ? 'modified' : action === 'accept' ? 'accepted' : 'rejected' }
        : sug
    )

    setAnalysis({
      ...analysis,
      suggestions: updatedSuggestions
    })

    if (action === 'modify') {
      const suggestion = analysis.suggestions.find(s => s.id === suggestionId)
      if (suggestion) {
        setSelectedSuggestion(suggestion)
        setEditingText(suggestion.suggested_text)
      }
    }
  }

  const runComprehensiveAnalysis = async () => {
    setIsAnalyzing(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 3000))
    setIsAnalyzing(false)
    // In real implementation, this would call the API and update the analysis
  }

  const filteredSuggestions = analysis?.suggestions.filter(sug => 
    filterType === 'all' || sug.type === filterType
  ) || []

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'accepted': return 'text-green-600 bg-green-50'
      case 'rejected': return 'text-red-600 bg-red-50'
      case 'modified': return 'text-blue-600 bg-blue-50'
      default: return 'text-orange-600 bg-orange-50'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'missing_item': return <AlertCircle className="h-4 w-4" />
      case 'clarity': return <Eye className="h-4 w-4" />
      case 'consistency': return <CheckCircle className="h-4 w-4" />
      default: return <FileText className="h-4 w-4" />
    }
  }

  if (!analysis) {
    return <div className="flex items-center justify-center h-64">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Protocol Editor</h1>
              <p className="text-sm text-gray-500">Interactive AI-powered protocol review</p>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={runComprehensiveAnalysis}
                disabled={isAnalyzing}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
              >
                {isAnalyzing ? (
                  <>
                    <Clock className="h-4 w-4 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Zap className="h-4 w-4 mr-2" />
                    Re-analyze
                  </>
                )}
              </button>
              <button className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                <Download className="h-4 w-4 mr-2" />
                Export
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Panel - Protocol Overview */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Protocol Score</h2>
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">{analysis.overall_score}%</div>
                <p className="text-sm text-gray-500">Overall Compliance</p>
              </div>
              
              <div className="mt-6 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">CONSORT</span>
                  <span className="text-sm font-medium">{analysis.component_scores.consort_compliance}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${analysis.component_scores.consort_compliance}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">SPIRIT</span>
                  <span className="text-sm font-medium">{analysis.component_scores.spirit_compliance}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full" 
                    style={{ width: `${analysis.component_scores.spirit_compliance}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Clarity</span>
                  <span className="text-sm font-medium">{analysis.component_scores.clarity_score}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-purple-600 h-2 rounded-full" 
                    style={{ width: `${analysis.component_scores.clarity_score}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Executive Summary */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Executive Summary</h2>
              <p className="text-sm text-gray-600 leading-relaxed">{analysis.executive_summary}</p>
            </div>
          </div>

          {/* Center Panel - Suggestions List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">
                    Suggestions ({filteredSuggestions.length})
                  </h2>
                  <select
                    value={filterType}
                    onChange={(e) => setFilterType(e.target.value)}
                    className="text-sm border border-gray-300 rounded-md px-3 py-1"
                  >
                    <option value="all">All Types</option>
                    <option value="missing_item">Missing Items</option>
                    <option value="clarity">Clarity</option>
                    <option value="consistency">Consistency</option>
                  </select>
                </div>
              </div>

              <div className="max-h-96 overflow-y-auto">
                {filteredSuggestions.map((suggestion) => (
                  <div
                    key={suggestion.id}
                    className={`p-4 border-b border-gray-200 cursor-pointer hover:bg-gray-50 ${
                      selectedSuggestion?.id === suggestion.id ? 'bg-blue-50 border-blue-200' : ''
                    }`}
                    onClick={() => setSelectedSuggestion(suggestion)}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        {getTypeIcon(suggestion.type)}
                        <span className="text-sm font-medium text-gray-900">{suggestion.section}</span>
                        {suggestion.guideline && (
                          <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                            {suggestion.guideline}
                          </span>
                        )}
                      </div>
                      <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(suggestion.status)}`}>
                        {suggestion.status}
                      </span>
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-2">{suggestion.issue}</p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        <div className="w-16 bg-gray-200 rounded-full h-1">
                          <div 
                            className="bg-blue-600 h-1 rounded-full" 
                            style={{ width: `${suggestion.confidence * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-xs text-gray-500">
                          {Math.round(suggestion.confidence * 100)}%
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Panel - Suggestion Details */}
          <div className="lg:col-span-1">
            {selectedSuggestion ? (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Suggestion Details</h3>
                  <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(selectedSuggestion.status)}`}>
                    {selectedSuggestion.status}
                  </span>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Issue</label>
                    <p className="text-sm text-gray-600 mt-1">{selectedSuggestion.issue}</p>
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-700">Explanation</label>
                    <p className="text-sm text-gray-600 mt-1">{selectedSuggestion.explanation}</p>
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-sm font-medium text-gray-700">Suggested Text</label>
                      <button
                        onClick={() => setShowOriginal(!showOriginal)}
                        className="text-xs text-blue-600 hover:text-blue-800"
                      >
                        {showOriginal ? 'Show Suggestion' : 'Show Original'}
                      </button>
                    </div>
                    
                    {selectedSuggestion.status === 'modified' ? (
                      <textarea
                        value={editingText}
                        onChange={(e) => setEditingText(e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-md text-sm"
                        rows={6}
                      />
                    ) : (
                      <div className="p-3 bg-gray-50 border border-gray-200 rounded-md text-sm text-gray-700">
                        {selectedSuggestion.suggested_text}
                      </div>
                    )}
                  </div>

                  {selectedSuggestion.status === 'pending' && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleSuggestionAction(selectedSuggestion.id, 'accept')}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                      >
                        <ThumbsUp className="h-4 w-4 mr-1" />
                        Accept
                      </button>
                      <button
                        onClick={() => handleSuggestionAction(selectedSuggestion.id, 'modify')}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                      >
                        <Edit3 className="h-4 w-4 mr-1" />
                        Modify
                      </button>
                      <button
                        onClick={() => handleSuggestionAction(selectedSuggestion.id, 'reject')}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                      >
                        <ThumbsDown className="h-4 w-4 mr-1" />
                        Reject
                      </button>
                    </div>
                  )}

                  {selectedSuggestion.status === 'modified' && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => {
                          // Save the modified text
                          handleSuggestionAction(selectedSuggestion.id, 'accept')
                          setEditingText('')
                        }}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                      >
                        Save Changes
                      </button>
                      <button
                        onClick={() => {
                          setEditingText(selectedSuggestion.suggested_text)
                          handleSuggestionAction(selectedSuggestion.id, 'pending')
                        }}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                      >
                        <RotateCcw className="h-4 w-4 mr-1" />
                        Reset
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
                <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>Select a suggestion to view details and make edits</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
