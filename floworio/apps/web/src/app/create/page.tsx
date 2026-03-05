'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Upload, ChevronRight, FileUp, Settings, Sparkles, Video, Share2 } from 'lucide-react';

type Step = 'upload' | 'configure' | 'story' | 'preview' | 'publish';

export default function CreateProject() {
  const [currentStep, setCurrentStep] = useState<Step>('upload');
  const [fileName, setFileName] = useState<string>('');

  const steps: { id: Step; label: string; icon: any }[] = [
    { id: 'upload', label: 'Upload Data', icon: Upload },
    { id: 'configure', label: 'Configure', icon: Settings },
    { id: 'story', label: 'AI Story', icon: Sparkles },
    { id: 'preview', label: 'Preview', icon: Video },
    { id: 'publish', label: 'Publish', icon: Share2 },
  ];

  const stepIndex = steps.findIndex(s => s.id === currentStep);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-700 font-medium mb-4 inline-block">
            ← Back to Dashboard
          </Link>
          <h1 className="text-3xl font-bold text-black">Create New Project</h1>
        </div>
      </div>

      {/* Progress Steps */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            {steps.map((step, i) => {
              const isActive = step.id === currentStep;
              const isCompleted = steps.findIndex(s => s.id === currentStep) > i;
              const Icon = step.icon;

              return (
                <div key={step.id} className="flex items-center flex-1">
                  <motion.button
                    onClick={() => setCurrentStep(step.id)}
                    className={`flex items-center gap-3 px-4 py-2 rounded-lg transition ${
                      isActive
                        ? 'bg-indigo-100 text-indigo-700'
                        : isCompleted
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                    whileHover={{ scale: 1.05 }}
                  >
                    <Icon size={20} />
                    <span className="font-medium hidden sm:inline">{step.label}</span>
                  </motion.button>
                  {i < steps.length - 1 && (
                    <div className={`flex-1 h-1 mx-2 ${isCompleted ? 'bg-green-300' : 'bg-gray-200'}`} />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Step 1: Upload */}
        {currentStep === 'upload' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <div className="bg-white rounded-lg border border-gray-200 p-12">
              <h2 className="text-2xl font-bold text-black mb-2">Upload your data</h2>
              <p className="text-gray-600 mb-8">Excel, CSV, or paste your data. We'll handle the rest.</p>

              {/* Upload Area */}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-indigo-400 transition cursor-pointer bg-gray-50">
                <FileUp size={48} className="mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-black mb-2">Drag and drop your file</h3>
                <p className="text-gray-600 mb-4">or click to browse</p>
                <p className="text-sm text-gray-500">Supports .xlsx, .xls, .csv</p>
                <input
                  type="file"
                  accept=".xlsx,.xls,.csv"
                  onChange={(e) => {
                    if (e.target.files?.[0]) {
                      setFileName(e.target.files[0].name);
                    }
                  }}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <div className="mt-6 inline-block px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
                    Choose File
                  </div>
                </label>
              </div>

              {fileName && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3"
                >
                  <div className="w-10 h-10 bg-green-200 rounded-full flex items-center justify-center">
                    <span className="text-green-700 font-bold">✓</span>
                  </div>
                  <div>
                    <p className="font-semibold text-green-900">{fileName}</p>
                    <p className="text-sm text-green-700">Ready to configure</p>
                  </div>
                </motion.div>
              )}

              {/* Next Button */}
              <div className="mt-8 flex justify-end">
                <button
                  onClick={() => setCurrentStep('configure')}
                  disabled={!fileName}
                  className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                >
                  Next
                  <ChevronRight size={20} />
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Step 2: Configure */}
        {currentStep === 'configure' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <div className="bg-white rounded-lg border border-gray-200 p-12">
              <h2 className="text-2xl font-bold text-black mb-8">Configure your video</h2>

              <div className="space-y-6">
                {/* Chart Type */}
                <div>
                  <label className="block text-sm font-semibold text-black mb-3">Chart Type</label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {['Bar Race', 'Pie Race', 'Line Chart', 'Area Chart', 'World Map'].map((type) => (
                      <button
                        key={type}
                        className="p-4 border border-gray-200 rounded-lg hover:border-indigo-400 hover:bg-indigo-50 transition text-left"
                      >
                        <p className="font-medium text-black">{type}</p>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Aspect Ratio */}
                <div>
                  <label className="block text-sm font-semibold text-black mb-3">Aspect Ratio</label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {['16:9', '9:16', '1:1', '4:5'].map((ratio) => (
                      <button
                        key={ratio}
                        className="p-4 border border-gray-200 rounded-lg hover:border-indigo-400 hover:bg-indigo-50 transition text-center font-medium text-black"
                      >
                        {ratio}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Title & Subtitle */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-semibold text-black mb-2">Title</label>
                    <input
                      type="text"
                      placeholder="e.g., World GDP Rankings"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-black mb-2">Subtitle</label>
                    <input
                      type="text"
                      placeholder="e.g., 2020-2023"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>

                {/* Duration & FPS */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-semibold text-black mb-2">Duration (seconds)</label>
                    <input
                      type="number"
                      defaultValue="30"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-black mb-2">FPS</label>
                    <input
                      type="number"
                      defaultValue="30"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>
              </div>

              {/* Navigation */}
              <div className="mt-8 flex justify-between">
                <button
                  onClick={() => setCurrentStep('upload')}
                  className="px-6 py-3 border border-gray-300 text-black rounded-lg hover:bg-gray-50 transition font-semibold"
                >
                  Back
                </button>
                <button
                  onClick={() => setCurrentStep('story')}
                  className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold"
                >
                  Next
                  <ChevronRight size={20} />
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Step 3: AI Story */}
        {currentStep === 'story' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <div className="bg-white rounded-lg border border-gray-200 p-12">
              <h2 className="text-2xl font-bold text-black mb-2">Generate AI story</h2>
              <p className="text-gray-600 mb-8">Let AI write a compelling narration for your video</p>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-black mb-2">Tone</label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500">
                    <option>Engaging</option>
                    <option>Professional</option>
                    <option>Dramatic</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-black mb-2">Script Preview</label>
                  <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg min-h-32">
                    <p className="text-gray-600 italic">AI-generated script will appear here...</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <input type="checkbox" id="voiceover" className="w-4 h-4" defaultChecked />
                  <label htmlFor="voiceover" className="text-black font-medium">
                    Add Kokoro TTS voiceover
                  </label>
                </div>
              </div>

              {/* Navigation */}
              <div className="mt-8 flex justify-between">
                <button
                  onClick={() => setCurrentStep('configure')}
                  className="px-6 py-3 border border-gray-300 text-black rounded-lg hover:bg-gray-50 transition font-semibold"
                >
                  Back
                </button>
                <button
                  onClick={() => setCurrentStep('preview')}
                  className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold"
                >
                  Next
                  <ChevronRight size={20} />
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Step 4: Preview */}
        {currentStep === 'preview' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <div className="bg-white rounded-lg border border-gray-200 p-12">
              <h2 className="text-2xl font-bold text-black mb-8">Preview & Render</h2>

              <div className="aspect-video bg-gray-900 rounded-lg mb-8 flex items-center justify-center">
                <div className="text-center">
                  <Video size={48} className="text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400">Video preview will appear here</p>
                </div>
              </div>

              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg mb-8">
                <p className="text-blue-900">
                  <span className="font-semibold">Rendering in progress...</span> This may take a few minutes.
                </p>
              </div>

              {/* Navigation */}
              <div className="flex justify-between">
                <button
                  onClick={() => setCurrentStep('story')}
                  className="px-6 py-3 border border-gray-300 text-black rounded-lg hover:bg-gray-50 transition font-semibold"
                >
                  Back
                </button>
                <button
                  onClick={() => setCurrentStep('publish')}
                  className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold"
                >
                  Next
                  <ChevronRight size={20} />
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Step 5: Publish */}
        {currentStep === 'publish' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <div className="bg-white rounded-lg border border-gray-200 p-12">
              <h2 className="text-2xl font-bold text-black mb-8">Publish to social media</h2>

              <div className="space-y-4 mb-8">
                {['TikTok', 'Instagram Reels', 'YouTube Shorts', 'LinkedIn'].map((platform) => (
                  <label key={platform} className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" className="w-4 h-4" defaultChecked />
                    <span className="font-medium text-black">{platform}</span>
                  </label>
                ))}
              </div>

              <div>
                <label className="block text-sm font-semibold text-black mb-2">Caption</label>
                <textarea
                  placeholder="Add a caption for your video..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 h-24"
                />
              </div>

              {/* Navigation */}
              <div className="mt-8 flex justify-between">
                <button
                  onClick={() => setCurrentStep('preview')}
                  className="px-6 py-3 border border-gray-300 text-black rounded-lg hover:bg-gray-50 transition font-semibold"
                >
                  Back
                </button>
                <Link
                  href="/dashboard"
                  className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-semibold"
                >
                  Publish & Save
                  <ChevronRight size={20} />
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
