# Frontend Development

Comprehensive guide to ProtoScribe's Next.js frontend, including architecture, components, and development patterns.

## Frontend Overview

ProtoScribe's frontend is built with Next.js 14, React, TypeScript, and Tailwind CSS, providing a modern, responsive, and performant user interface for clinical trial protocol optimization.

### Technology Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for utility-first design
- **UI Components**: Custom components with Headless UI
- **State Management**: React hooks and Context API
- **API Client**: Custom fetch wrapper with error handling
- **Build Tool**: Webpack (via Next.js)

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout component
│   ├── page.tsx           # Home page
│   └── editor/            # Editor page
│       └── page.tsx
├── components/            # Reusable UI components
│   ├── ui/               # Base UI components
│   ├── protocol/         # Protocol-specific components
│   └── analysis/         # Analysis-related components
├── lib/                  # Utility libraries
│   ├── api.ts           # API client functions
│   ├── utils.ts         # Helper utilities
│   └── types.ts         # TypeScript type definitions
├── hooks/               # Custom React hooks
├── styles/              # Additional CSS modules
└── public/              # Static assets
```

## Core Components

### Layout Components

#### Root Layout
```typescript
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ProtoScribe - Clinical Trial Protocol AI Optimizer',
  description: 'Optimize your clinical trial protocols with AI-powered analysis and CONSORT/SPIRIT compliance checking.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white shadow-sm border-b">
            {/* Navigation component */}
          </nav>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
```

#### Navigation Component
```typescript
// components/ui/Navigation.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'

const navigationItems = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Editor', href: '/editor', icon: DocumentTextIcon },
  { name: 'Protocols', href: '/protocols', icon: FolderIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
]

export function Navigation() {
  const pathname = usePathname()

  return (
    <nav className="flex space-x-8">
      {navigationItems.map((item) => {
        const isActive = pathname === item.href
        return (
          <Link
            key={item.name}
            href={item.href}
            className={cn(
              'flex items-center px-3 py-2 text-sm font-medium rounded-md',
              isActive
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
            )}
          >
            <item.icon className="w-4 h-4 mr-2" />
            {item.name}
          </Link>
        )
      })}
    </nav>
  )
}
```

### Protocol Components

#### Protocol Upload
```typescript
// components/protocol/ProtocolUpload.tsx
'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { uploadProtocol } from '@/lib/api'
import { Button } from '@/components/ui/Button'
import { Progress } from '@/components/ui/Progress'

interface ProtocolUploadProps {
  onUploadComplete: (protocol: Protocol) => void
}

export function ProtocolUpload({ onUploadComplete }: ProtocolUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    setUploading(true)
    setProgress(0)

    try {
      const protocol = await uploadProtocol(file, {
        onProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          setProgress(percentCompleted)
        }
      })

      onUploadComplete(protocol)
    } catch (error) {
      console.error('Upload failed:', error)
      // Handle error (show toast, etc.)
    } finally {
      setUploading(false)
      setProgress(0)
    }
  }, [onUploadComplete])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md']
    },
    maxFiles: 1,
    maxSize: 50 * 1024 * 1024, // 50MB
  })

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={cn(
          'border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors',
          isDragActive
            ? 'border-blue-400 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        )}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">Uploading...</p>
            <Progress value={progress} className="w-full" />
          </div>
        ) : (
          <div className="space-y-4">
            <DocumentArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
            <div>
              <p className="text-lg font-medium text-gray-900">
                {isDragActive ? 'Drop your protocol here' : 'Upload protocol'}
              </p>
              <p className="text-sm text-gray-600">
                PDF, DOCX, TXT, or MD files up to 50MB
              </p>
            </div>
            <Button variant="outline">Choose File</Button>
          </div>
        )}
      </div>
    </div>
  )
}
```

#### Protocol Card
```typescript
// components/protocol/ProtocolCard.tsx
import Link from 'next/link'
import { formatDistanceToNow } from 'date-fns'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/Card'

interface ProtocolCardProps {
  protocol: Protocol
  onDelete?: (id: string) => void
}

export function ProtocolCard({ protocol, onDelete }: ProtocolCardProps) {
  const statusColors = {
    processing: 'yellow',
    ready: 'green',
    error: 'red'
  } as const

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <h3 className="font-semibold text-lg line-clamp-2">
            {protocol.title}
          </h3>
          <Badge variant={statusColors[protocol.status]}>
            {protocol.status}
          </Badge>
        </div>
        {protocol.description && (
          <p className="text-sm text-gray-600 line-clamp-2">
            {protocol.description}
          </p>
        )}
      </CardHeader>

      <CardContent className="pb-3">
        <div className="space-y-2 text-sm text-gray-500">
          <div className="flex items-center justify-between">
            <span>File size:</span>
            <span>{formatFileSize(protocol.file_size)}</span>
          </div>
          <div className="flex items-center justify-between">
            <span>Created:</span>
            <span>{formatDistanceToNow(new Date(protocol.created_at))} ago</span>
          </div>
        </div>
      </CardContent>

      <CardFooter className="pt-3 space-x-2">
        <Button asChild variant="outline" size="sm">
          <Link href={`/protocols/${protocol.id}`}>
            View
          </Link>
        </Button>
        {protocol.status === 'ready' && (
          <>
            <Button asChild size="sm">
              <Link href={`/editor?protocol=${protocol.id}`}>
                Edit
              </Link>
            </Button>
            <Button asChild variant="outline" size="sm">
              <Link href={`/analyze?protocol=${protocol.id}`}>
                Analyze
              </Link>
            </Button>
          </>
        )}
        {onDelete && (
          <Button
            variant="destructive"
            size="sm"
            onClick={() => onDelete(protocol.id)}
          >
            Delete
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}
```

### Analysis Components

#### Analysis Dashboard
```typescript
// components/analysis/AnalysisDashboard.tsx
'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Progress } from '@/components/ui/Progress'
import { Badge } from '@/components/ui/Badge'

interface AnalysisDashboardProps {
  protocolId: string
}

export function AnalysisDashboard({ protocolId }: AnalysisDashboardProps) {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchAnalysis() {
      try {
        const result = await getAnalysisResults(protocolId)
        setAnalysis(result)
      } catch (error) {
        console.error('Failed to fetch analysis:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchAnalysis()
  }, [protocolId])

  if (loading) {
    return <div>Loading analysis...</div>
  }

  if (!analysis) {
    return <div>No analysis available</div>
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {/* Overall Score */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Overall Score</CardTitle>
          <TrophyIcon className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{analysis.results.overall_score}/100</div>
          <Progress value={analysis.results.overall_score} className="mt-2" />
          <p className="text-xs text-muted-foreground mt-2">
            {getScoreDescription(analysis.results.overall_score)}
          </p>
        </CardContent>
      </Card>

      {/* CONSORT Score */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">CONSORT Compliance</CardTitle>
          <CheckCircleIcon className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{analysis.results.consort_score}/100</div>
          <Progress value={analysis.results.consort_score} className="mt-2" />
          <Badge
            variant={analysis.results.consort_score >= 80 ? 'success' : 'warning'}
            className="mt-2"
          >
            {analysis.results.consort_score >= 80 ? 'Compliant' : 'Needs Work'}
          </Badge>
        </CardContent>
      </Card>

      {/* SPIRIT Score */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">SPIRIT Compliance</CardTitle>
          <DocumentCheckIcon className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{analysis.results.spirit_score}/100</div>
          <Progress value={analysis.results.spirit_score} className="mt-2" />
          <Badge
            variant={analysis.results.spirit_score >= 80 ? 'success' : 'warning'}
            className="mt-2"
          >
            {analysis.results.spirit_score >= 80 ? 'Compliant' : 'Needs Work'}
          </Badge>
        </CardContent>
      </Card>

      {/* Categories Overview */}
      <Card className="md:col-span-2 lg:col-span-3">
        <CardHeader>
          <CardTitle>Categories Breakdown</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {Object.entries(analysis.results.categories).map(([category, data]) => (
              <div key={category} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium capitalize">
                    {category.replace('_', ' ')}
                  </span>
                  <Badge variant={getStatusVariant(data.status)}>
                    {data.status.replace('_', ' ')}
                  </Badge>
                </div>
                <Progress value={data.score} />
                <span className="text-xs text-muted-foreground">
                  {data.score}/100
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
```

#### Suggestions Panel
```typescript
// components/analysis/SuggestionsPanel.tsx
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Textarea } from '@/components/ui/Textarea'

interface SuggestionsPanelProps {
  suggestions: Suggestion[]
  onSuggestionUpdate: (suggestionId: string, action: string, content?: string) => void
}

export function SuggestionsPanel({ suggestions, onSuggestionUpdate }: SuggestionsPanelProps) {
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editContent, setEditContent] = useState('')

  const groupedSuggestions = suggestions.reduce((acc, suggestion) => {
    if (!acc[suggestion.type]) {
      acc[suggestion.type] = []
    }
    acc[suggestion.type].push(suggestion)
    return acc
  }, {} as Record<string, Suggestion[]>)

  const priorityOrder = ['critical', 'improvement', 'style']
  const sortedGroups = priorityOrder.filter(type => groupedSuggestions[type])

  return (
    <div className="space-y-6">
      {sortedGroups.map(type => (
        <div key={type}>
          <h3 className="text-lg font-semibold mb-3 capitalize">
            {type} Suggestions ({groupedSuggestions[type].length})
          </h3>
          <div className="space-y-4">
            {groupedSuggestions[type].map(suggestion => (
              <SuggestionCard
                key={suggestion.id}
                suggestion={suggestion}
                isEditing={editingId === suggestion.id}
                editContent={editContent}
                onEdit={(content) => {
                  setEditingId(suggestion.id)
                  setEditContent(content)
                }}
                onSave={() => {
                  onSuggestionUpdate(suggestion.id, 'accept', editContent)
                  setEditingId(null)
                  setEditContent('')
                }}
                onCancel={() => {
                  setEditingId(null)
                  setEditContent('')
                }}
                onAccept={() => onSuggestionUpdate(suggestion.id, 'accept')}
                onReject={() => onSuggestionUpdate(suggestion.id, 'reject')}
                onEditContentChange={setEditContent}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function SuggestionCard({ 
  suggestion, 
  isEditing, 
  editContent, 
  onEdit, 
  onSave, 
  onCancel, 
  onAccept, 
  onReject,
  onEditContentChange 
}: SuggestionCardProps) {
  const typeColors = {
    critical: 'destructive',
    improvement: 'warning',
    style: 'secondary'
  } as const

  return (
    <Card className="border-l-4 border-l-blue-500">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <Badge variant={typeColors[suggestion.type]}>
                {suggestion.type}
              </Badge>
              <Badge variant="outline">
                {suggestion.section}
              </Badge>
              <span className="text-xs text-muted-foreground">
                {Math.round(suggestion.confidence * 100)}% confidence
              </span>
            </div>
            <CardTitle className="text-base">
              {suggestion.priority} Priority
            </CardTitle>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {isEditing ? (
          <div className="space-y-3">
            <Textarea
              value={editContent}
              onChange={(e) => onEditContentChange(e.target.value)}
              placeholder="Edit the suggestion..."
              rows={4}
            />
            <div className="flex space-x-2">
              <Button onClick={onSave} size="sm">
                Save
              </Button>
              <Button onClick={onCancel} variant="outline" size="sm">
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <>
            <p className="text-sm">{suggestion.content}</p>
            <div className="flex space-x-2">
              <Button
                onClick={onAccept}
                size="sm"
                className="bg-green-600 hover:bg-green-700"
              >
                ✓ Accept
              </Button>
              <Button
                onClick={() => onEdit(suggestion.content)}
                variant="outline"
                size="sm"
              >
                ✏️ Edit
              </Button>
              <Button
                onClick={onReject}
                variant="destructive"
                size="sm"
              >
                ✗ Reject
              </Button>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
```

## State Management

### React Context for Global State

```typescript
// lib/context/ProtocolContext.tsx
'use client'

import { createContext, useContext, useReducer, ReactNode } from 'react'

interface ProtocolState {
  protocols: Protocol[]
  currentProtocol: Protocol | null
  analyses: Record<string, AnalysisResult>
  loading: boolean
  error: string | null
}

type ProtocolAction =
  | { type: 'SET_PROTOCOLS'; protocols: Protocol[] }
  | { type: 'ADD_PROTOCOL'; protocol: Protocol }
  | { type: 'UPDATE_PROTOCOL'; protocol: Protocol }
  | { type: 'DELETE_PROTOCOL'; id: string }
  | { type: 'SET_CURRENT_PROTOCOL'; protocol: Protocol | null }
  | { type: 'SET_ANALYSIS'; protocolId: string; analysis: AnalysisResult }
  | { type: 'SET_LOADING'; loading: boolean }
  | { type: 'SET_ERROR'; error: string | null }

const ProtocolContext = createContext<{
  state: ProtocolState
  dispatch: React.Dispatch<ProtocolAction>
} | null>(null)

function protocolReducer(state: ProtocolState, action: ProtocolAction): ProtocolState {
  switch (action.type) {
    case 'SET_PROTOCOLS':
      return { ...state, protocols: action.protocols, loading: false }
    
    case 'ADD_PROTOCOL':
      return { 
        ...state, 
        protocols: [...state.protocols, action.protocol] 
      }
    
    case 'UPDATE_PROTOCOL':
      return {
        ...state,
        protocols: state.protocols.map(p => 
          p.id === action.protocol.id ? action.protocol : p
        ),
        currentProtocol: state.currentProtocol?.id === action.protocol.id 
          ? action.protocol 
          : state.currentProtocol
      }
    
    case 'DELETE_PROTOCOL':
      return {
        ...state,
        protocols: state.protocols.filter(p => p.id !== action.id),
        currentProtocol: state.currentProtocol?.id === action.id 
          ? null 
          : state.currentProtocol
      }
    
    case 'SET_CURRENT_PROTOCOL':
      return { ...state, currentProtocol: action.protocol }
    
    case 'SET_ANALYSIS':
      return {
        ...state,
        analyses: {
          ...state.analyses,
          [action.protocolId]: action.analysis
        }
      }
    
    case 'SET_LOADING':
      return { ...state, loading: action.loading }
    
    case 'SET_ERROR':
      return { ...state, error: action.error, loading: false }
    
    default:
      return state
  }
}

export function ProtocolProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(protocolReducer, {
    protocols: [],
    currentProtocol: null,
    analyses: {},
    loading: false,
    error: null
  })

  return (
    <ProtocolContext.Provider value={{ state, dispatch }}>
      {children}
    </ProtocolContext.Provider>
  )
}

export function useProtocol() {
  const context = useContext(ProtocolContext)
  if (!context) {
    throw new Error('useProtocol must be used within a ProtocolProvider')
  }
  return context
}
```

### Custom Hooks

```typescript
// hooks/useProtocols.ts
import { useEffect } from 'react'
import { useProtocol } from '@/lib/context/ProtocolContext'
import { getProtocols } from '@/lib/api'

export function useProtocols() {
  const { state, dispatch } = useProtocol()

  useEffect(() => {
    async function fetchProtocols() {
      dispatch({ type: 'SET_LOADING', loading: true })
      try {
        const protocols = await getProtocols()
        dispatch({ type: 'SET_PROTOCOLS', protocols })
      } catch (error) {
        dispatch({ type: 'SET_ERROR', error: error.message })
      }
    }

    if (state.protocols.length === 0 && !state.loading) {
      fetchProtocols()
    }
  }, [state.protocols.length, state.loading, dispatch])

  const createProtocol = async (file: File, metadata: { title: string; description?: string }) => {
    try {
      const protocol = await uploadProtocol(file, metadata)
      dispatch({ type: 'ADD_PROTOCOL', protocol })
      return protocol
    } catch (error) {
      dispatch({ type: 'SET_ERROR', error: error.message })
      throw error
    }
  }

  const deleteProtocol = async (id: string) => {
    try {
      await deleteProtocolApi(id)
      dispatch({ type: 'DELETE_PROTOCOL', id })
    } catch (error) {
      dispatch({ type: 'SET_ERROR', error: error.message })
      throw error
    }
  }

  return {
    protocols: state.protocols,
    loading: state.loading,
    error: state.error,
    createProtocol,
    deleteProtocol
  }
}

// hooks/useAnalysis.ts
export function useAnalysis(protocolId: string) {
  const { state, dispatch } = useProtocol()
  const analysis = state.analyses[protocolId]

  const startAnalysis = async (options: AnalysisOptions) => {
    try {
      dispatch({ type: 'SET_LOADING', loading: true })
      const result = await analyzeProtocol(protocolId, options)
      dispatch({ type: 'SET_ANALYSIS', protocolId, analysis: result })
      return result
    } catch (error) {
      dispatch({ type: 'SET_ERROR', error: error.message })
      throw error
    }
  }

  const refreshAnalysis = async () => {
    try {
      const result = await getAnalysisResults(protocolId)
      dispatch({ type: 'SET_ANALYSIS', protocolId, analysis: result })
      return result
    } catch (error) {
      dispatch({ type: 'SET_ERROR', error: error.message })
      throw error
    }
  }

  return {
    analysis,
    loading: state.loading,
    error: state.error,
    startAnalysis,
    refreshAnalysis
  }
}
```

## API Integration

### API Client

```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class APIError extends Error {
  constructor(public status: number, message: string, public details?: any) {
    super(message)
    this.name = 'APIError'
  }
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  const response = await fetch(url, config)

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new APIError(
      response.status,
      errorData.message || `HTTP ${response.status}`,
      errorData
    )
  }

  return response.json()
}

// Protocol API functions
export async function getProtocols(): Promise<Protocol[]> {
  const data = await apiRequest<{ protocols: Protocol[] }>('/api/protocols/')
  return data.protocols
}

export async function getProtocol(id: string): Promise<Protocol> {
  return apiRequest<Protocol>(`/api/protocols/${id}`)
}

export async function uploadProtocol(
  file: File,
  metadata: { title: string; description?: string },
  options?: { onProgress?: (progress: ProgressEvent) => void }
): Promise<Protocol> {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('title', metadata.title)
  if (metadata.description) {
    formData.append('description', metadata.description)
  }

  const xhr = new XMLHttpRequest()
  
  return new Promise((resolve, reject) => {
    xhr.upload.addEventListener('progress', (e) => {
      if (options?.onProgress) {
        options.onProgress(e)
      }
    })

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText))
      } else {
        reject(new APIError(xhr.status, 'Upload failed'))
      }
    })

    xhr.addEventListener('error', () => {
      reject(new APIError(0, 'Network error'))
    })

    xhr.open('POST', `${API_BASE_URL}/api/protocols/`)
    xhr.send(formData)
  })
}

export async function analyzeProtocol(
  protocolId: string,
  options: AnalysisOptions
): Promise<AnalysisResult> {
  return apiRequest<AnalysisResult>(`/api/protocols/${protocolId}/analyze`, {
    method: 'POST',
    body: JSON.stringify(options),
  })
}

export async function getAnalysisResults(protocolId: string): Promise<AnalysisResult> {
  return apiRequest<AnalysisResult>(`/api/protocols/${protocolId}/results`)
}

export async function updateSuggestion(
  suggestionId: string,
  update: { status: string; user_comment?: string; modified_content?: string }
): Promise<Suggestion> {
  return apiRequest<Suggestion>(`/api/suggestions/${suggestionId}`, {
    method: 'PUT',
    body: JSON.stringify(update),
  })
}
```

## Styling and Theming

### Tailwind Configuration

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        success: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
        },
        destructive: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
  ],
}
```

### Component Variants

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Button variants using cva (class-variance-authority)
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'underline-offset-4 hover:underline text-primary',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-3 rounded-md',
        lg: 'h-11 px-8 rounded-md',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button'
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
```

## Performance Optimization

### Code Splitting and Lazy Loading

```typescript
// Dynamic imports for large components
import dynamic from 'next/dynamic'

const AnalysisDashboard = dynamic(
  () => import('@/components/analysis/AnalysisDashboard'),
  {
    loading: () => <div>Loading analysis...</div>,
    ssr: false, // Disable SSR for client-only components
  }
)

const ProtocolEditor = dynamic(
  () => import('@/components/protocol/ProtocolEditor'),
  {
    loading: () => <div>Loading editor...</div>,
  }
)
```

### Image Optimization

```typescript
import Image from 'next/image'

// Optimized images with Next.js Image component
export function ProtocolPreview({ protocol }: { protocol: Protocol }) {
  return (
    <div className="relative aspect-[4/3] rounded-lg overflow-hidden">
      <Image
        src={`/api/protocols/${protocol.id}/thumbnail`}
        alt={protocol.title}
        fill
        className="object-cover"
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        priority={false} // Only set true for above-the-fold images
      />
    </div>
  )
}
```

### Memoization

```typescript
import { useMemo, useCallback } from 'react'

export function SuggestionsList({ suggestions }: { suggestions: Suggestion[] }) {
  // Memoize expensive calculations
  const groupedSuggestions = useMemo(() => {
    return suggestions.reduce((acc, suggestion) => {
      if (!acc[suggestion.type]) {
        acc[suggestion.type] = []
      }
      acc[suggestion.type].push(suggestion)
      return acc
    }, {} as Record<string, Suggestion[]>)
  }, [suggestions])

  // Memoize event handlers
  const handleSuggestionUpdate = useCallback((id: string, action: string) => {
    // Handle suggestion update
  }, [])

  return (
    <div>
      {/* Render grouped suggestions */}
    </div>
  )
}
```

## Testing

### Component Testing with Jest and Testing Library

```typescript
// __tests__/components/ProtocolCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { ProtocolCard } from '@/components/protocol/ProtocolCard'

const mockProtocol: Protocol = {
  id: 'test-1',
  title: 'Test Protocol',
  description: 'Test description',
  status: 'ready',
  file_size: 1024,
  created_at: '2024-01-15T10:30:00Z',
  updated_at: '2024-01-15T10:30:00Z',
}

describe('ProtocolCard', () => {
  it('renders protocol information correctly', () => {
    render(<ProtocolCard protocol={mockProtocol} />)
    
    expect(screen.getByText('Test Protocol')).toBeInTheDocument()
    expect(screen.getByText('Test description')).toBeInTheDocument()
    expect(screen.getByText('ready')).toBeInTheDocument()
  })

  it('calls onDelete when delete button is clicked', () => {
    const mockOnDelete = jest.fn()
    render(<ProtocolCard protocol={mockProtocol} onDelete={mockOnDelete} />)
    
    const deleteButton = screen.getByText('Delete')
    fireEvent.click(deleteButton)
    
    expect(mockOnDelete).toHaveBeenCalledWith('test-1')
  })

  it('shows edit button only when protocol is ready', () => {
    render(<ProtocolCard protocol={mockProtocol} />)
    expect(screen.getByText('Edit')).toBeInTheDocument()

    const processingProtocol = { ...mockProtocol, status: 'processing' }
    render(<ProtocolCard protocol={processingProtocol} />)
    expect(screen.queryByText('Edit')).not.toBeInTheDocument()
  })
})
```

### Integration Testing

```typescript
// __tests__/integration/protocol-workflow.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ProtocolProvider } from '@/lib/context/ProtocolContext'
import { ProtocolUpload } from '@/components/protocol/ProtocolUpload'

// Mock API functions
jest.mock('@/lib/api', () => ({
  uploadProtocol: jest.fn().mockResolvedValue({
    id: 'new-protocol',
    title: 'Uploaded Protocol',
    status: 'processing',
  }),
}))

describe('Protocol Upload Workflow', () => {
  it('uploads protocol and updates UI', async () => {
    const mockOnComplete = jest.fn()
    
    render(
      <ProtocolProvider>
        <ProtocolUpload onUploadComplete={mockOnComplete} />
      </ProtocolProvider>
    )

    const file = new File(['protocol content'], 'protocol.pdf', {
      type: 'application/pdf',
    })

    const input = screen.getByRole('textbox', { hidden: true })
    fireEvent.change(input, { target: { files: [file] } })

    await waitFor(() => {
      expect(mockOnComplete).toHaveBeenCalledWith(
        expect.objectContaining({
          id: 'new-protocol',
          title: 'Uploaded Protocol',
        })
      )
    })
  })
})
```

## Deployment

### Build Configuration

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost', 'api.protoscribe.app'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  // Enable static export for GitHub Pages
  output: process.env.NODE_ENV === 'production' ? 'export' : undefined,
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for static export
  },
}

module.exports = nextConfig
```

### GitHub Actions Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: npm ci
      working-directory: frontend
    
    - name: Build
      run: npm run build
      working-directory: frontend
      env:
        NEXT_PUBLIC_API_URL: https://api.protoscribe.app
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: frontend/out
```

!!! tip "Development Tips"
    - Use TypeScript for better development experience and fewer runtime errors
    - Implement proper error boundaries to handle unexpected errors gracefully
    - Use React DevTools and Next.js DevTools for debugging
    - Set up Prettier and ESLint for consistent code formatting

!!! warning "Performance Considerations"
    - Avoid unnecessary re-renders with React.memo and useMemo
    - Implement virtual scrolling for large lists
    - Use Next.js Image component for optimized images
    - Monitor bundle size and split large components

!!! info "Accessibility"
    - Use semantic HTML elements
    - Implement proper ARIA labels and roles
    - Ensure keyboard navigation works correctly
    - Test with screen readers and other assistive technologies
