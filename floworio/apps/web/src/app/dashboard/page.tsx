'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Plus, Play, Trash2, Share2, Clock, BarChart3 } from 'lucide-react';

interface Project {
  id: string;
  title: string;
  status: 'draft' | 'rendering' | 'completed' | 'published';
  createdAt: string;
  videoUrl?: string;
  thumbnail?: string;
}

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([
    {
      id: '1',
      title: 'World GDP Rankings 2020-2023',
      status: 'completed',
      createdAt: '2 days ago',
      videoUrl: '#',
      thumbnail: 'https://via.placeholder.com/300x200?text=GDP+Rankings',
    },
    {
      id: '2',
      title: 'Tech Stock Performance',
      status: 'rendering',
      createdAt: '1 hour ago',
    },
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'rendering':
        return 'bg-blue-100 text-blue-800';
      case 'published':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'rendering':
        return <Clock size={16} className="animate-spin" />;
      case 'completed':
        return <Play size={16} />;
      case 'published':
        return <Share2 size={16} />;
      default:
        return <BarChart3 size={16} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-black">Dashboard</h1>
              <p className="text-gray-600 mt-2">Create and manage your data videos</p>
            </div>
            <Link
              href="/create"
              className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold"
            >
              <Plus size={20} />
              New Project
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid md:grid-cols-4 gap-6 mb-12"
        >
          {[
            { label: 'Total Videos', value: '12', color: 'bg-blue-50 border-blue-200' },
            { label: 'This Month', value: '5', color: 'bg-green-50 border-green-200' },
            { label: 'Published', value: '8', color: 'bg-purple-50 border-purple-200' },
            { label: 'Views', value: '24.5K', color: 'bg-orange-50 border-orange-200' },
          ].map((stat, i) => (
            <div key={i} className={`p-6 rounded-lg border ${stat.color}`}>
              <p className="text-gray-600 text-sm font-medium">{stat.label}</p>
              <p className="text-3xl font-bold text-black mt-2">{stat.value}</p>
            </div>
          ))}
        </motion.div>

        {/* Projects Grid */}
        <div>
          <h2 className="text-2xl font-bold text-black mb-6">Your Projects</h2>
          
          {projects.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-12 bg-white rounded-lg border border-gray-200"
            >
              <BarChart3 size={48} className="mx-auto text-gray-400 mb-4" />
              <h3 className="text-xl font-semibold text-black mb-2">No projects yet</h3>
              <p className="text-gray-600 mb-6">Create your first data video to get started</p>
              <Link
                href="/create"
                className="inline-block px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
              >
                Create Project
              </Link>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {projects.map((project, i) => (
                <motion.div
                  key={project.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-lg transition"
                >
                  {/* Thumbnail */}
                  <div className="relative aspect-video bg-gray-200 overflow-hidden">
                    {project.thumbnail ? (
                      <img
                        src={project.thumbnail}
                        alt={project.title}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-300 to-gray-400">
                        <BarChart3 size={40} className="text-gray-600" />
                      </div>
                    )}
                    
                    {/* Status Badge */}
                    <div className={`absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1 ${getStatusColor(project.status)}`}>
                      {getStatusIcon(project.status)}
                      {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
                    </div>

                    {/* Play Button (if completed) */}
                    {project.status === 'completed' && (
                      <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 hover:opacity-100 transition">
                        <button className="w-12 h-12 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition">
                          <Play size={24} className="text-indigo-600 ml-1" />
                        </button>
                      </div>
                    )}
                  </div>

                  {/* Content */}
                  <div className="p-4">
                    <h3 className="font-semibold text-black mb-2 line-clamp-2">{project.title}</h3>
                    <p className="text-sm text-gray-600 mb-4">Created {project.createdAt}</p>

                    {/* Actions */}
                    <div className="flex gap-2">
                      <Link
                        href={`/edit/${project.id}`}
                        className="flex-1 px-3 py-2 bg-indigo-50 text-indigo-600 rounded hover:bg-indigo-100 transition text-sm font-medium text-center"
                      >
                        Edit
                      </Link>
                      {project.status === 'completed' && (
                        <button className="flex-1 px-3 py-2 bg-green-50 text-green-600 rounded hover:bg-green-100 transition text-sm font-medium">
                          Publish
                        </button>
                      )}
                      <button className="px-3 py-2 bg-red-50 text-red-600 rounded hover:bg-red-100 transition">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
