'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Upload, FileText, CheckCircle, AlertCircle, Clock } from 'lucide-react'

export default function HomePage() {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [analysisStatus, setAnalysisStatus] = useState<'idle' | 'uploading' | 'analyzing' | 'complete'>('idle')

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setAnalysisStatus('uploading')
    
    // Simulate upload progress
    for (let i = 0; i <= 100; i += 10) {
      setUploadProgress(i)
      await new Promise(resolve => setTimeout(resolve, 100))
    }
    
    setAnalysisStatus('analyzing')
    
    // Simulate analysis
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setAnalysisStatus('complete')
  }

  return (
    <div className="container mx-auto py-8 px-4">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          ProtoScribe
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Clinical Trial Protocol AI Optimizer
        </p>
        <p className="text-lg text-gray-500 max-w-3xl mx-auto">
          Accelerate and standardize protocol drafting by automatically identifying missing 
          or under-specified elements and suggesting high-quality text aligned with CONSORT/SPIRIT guidelines.
        </p>
      </div>

      {/* Upload Section */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Upload Protocol Document
          </CardTitle>
          <CardDescription>
            Upload your protocol document (PDF, DOCX, or TXT) to get started with AI-powered analysis.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileUpload}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer flex flex-col items-center gap-4"
            >
              <FileText className="h-12 w-12 text-gray-400" />
              <div>
                <p className="text-lg font-medium">Click to upload</p>
                <p className="text-sm text-gray-500">or drag and drop</p>
                <p className="text-xs text-gray-400 mt-2">PDF, DOCX, TXT up to 50MB</p>
              </div>
            </label>
          </div>

          {analysisStatus !== 'idle' && (
            <div className="mt-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">
                  {analysisStatus === 'uploading' && 'Uploading...'}
                  {analysisStatus === 'analyzing' && 'Analyzing protocol...'}
                  {analysisStatus === 'complete' && 'Analysis complete!'}
                </span>
                <span className="text-sm text-gray-500">
                  {analysisStatus === 'uploading' && `${uploadProgress}%`}
                  {analysisStatus === 'analyzing' && 'Processing'}
                  {analysisStatus === 'complete' && '100%'}
                </span>
              </div>
              <Progress value={analysisStatus === 'complete' ? 100 : uploadProgress} className="w-full" />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Results Section */}
      {analysisStatus === 'complete' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Compliance Score</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">85.5%</div>
              <p className="text-xs text-gray-500">
                CONSORT/SPIRIT compliance
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Missing Items</CardTitle>
              <AlertCircle className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">7</div>
              <p className="text-xs text-gray-500">
                Items need attention
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Suggestions</CardTitle>
              <Clock className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">12</div>
              <p className="text-xs text-gray-500">
                AI-generated improvements
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              Compliance Checking
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              Automatic validation against CONSORT and SPIRIT guidelines with detailed scoring and item-by-item analysis.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-600" />
              AI-Powered Suggestions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              Get intelligent suggestions for missing or incomplete protocol elements with example text and explanations.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-purple-600" />
              Interactive Review
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              Side-by-side editor with accept/edit/reject workflow for efficient protocol improvement.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Footer */}
      <div className="text-center mt-12 pt-8 border-t border-gray-200">
        <p className="text-gray-500">
          ProtoScribe v0.1.0 - Clinical Trial Protocol AI Optimizer
        </p>
        <div className="flex justify-center gap-4 mt-4">
          <Badge variant="outline">CONSORT 2010</Badge>
          <Badge variant="outline">SPIRIT 2013</Badge>
          <Badge variant="outline">AI-Powered</Badge>
        </div>
      </div>
    </div>
  )
}
