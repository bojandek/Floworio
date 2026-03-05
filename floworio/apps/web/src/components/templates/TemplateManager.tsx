'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Save, Trash2, Copy, Plus, Settings } from 'lucide-react';

interface Template {
  id: string;
  name: string;
  chart_type: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

const CHART_TYPES = [
  { id: 'bar_race', label: 'Bar Race', icon: '📊' },
  { id: 'pie_race', label: 'Pie Race', icon: '🥧' },
  { id: 'line_chart', label: 'Line Chart', icon: '📈' },
  { id: 'area_chart', label: 'Area Chart', icon: '📉' },
  { id: 'world_map', label: 'World Map', icon: '🌍' },
];

export default function TemplateManager() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedType, setSelectedType] = useState<string>('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    chart_type: 'bar_race',
    description: '',
  });
  const [loading, setLoading] = useState(false);

  // Učitaj template-e
  useEffect(() => {
    loadTemplates();
  }, [selectedType]);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const url = selectedType
        ? `/api/templates/list?chart_type=${selectedType}`
        : '/api/templates/list';
      
      const response = await fetch(url);
      const data = await response.json();
      setTemplates(data.templates || []);
    } catch (error) {
      console.error('Error loading templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveTemplate = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/templates/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          config: {
            fps: 60,
            duration: 30,
            aspect_ratio: '16:9',
          },
          colors: {
            background: [255, 255, 255],
            text: [12, 27, 42],
            accent: [255, 215, 0],
          },
          styling: {
            title_font: 'Inter',
            title_size: 32,
            subtitle_font: 'Sans Serif',
            subtitle_size: 18,
          },
        }),
      });

      if (response.ok) {
        setFormData({ name: '', chart_type: 'bar_race', description: '' });
        setShowForm(false);
        loadTemplates();
      }
    } catch (error) {
      console.error('Error saving template:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTemplate = async (templateId: string) => {
    if (!confirm('Obriši ovaj template?')) return;

    try {
      setLoading(true);
      const response = await fetch(`/api/templates/${templateId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        loadTemplates();
      }
    } catch (error) {
      console.error('Error deleting template:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDuplicateTemplate = async (template: Template) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/templates/${template.id}`);
      const templateData = await response.json();

      // Spremi kao novi template sa "Copy" u imenu
      const newTemplate = {
        ...templateData,
        name: `${templateData.name} (Copy)`,
      };

      const saveResponse = await fetch('/api/templates/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTemplate),
      });

      if (saveResponse.ok) {
        loadTemplates();
      }
    } catch (error) {
      console.error('Error duplicating template:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-black mb-2">Template Manager</h1>
          <p className="text-gray-600">Kreiraj i upravljaj template-ima za različite tipove chart-a</p>
        </motion.div>

        {/* Chart Type Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <h2 className="text-lg font-semibold text-black mb-4">Filtriraj po tipu</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <button
              onClick={() => setSelectedType('')}
              className={`p-4 rounded-lg border-2 transition ${
                selectedType === ''
                  ? 'border-indigo-600 bg-indigo-50'
                  : 'border-gray-200 hover:border-indigo-300'
              }`}
            >
              <span className="text-2xl mb-2 block">📋</span>
              <span className="font-medium text-black">Svi</span>
            </button>
            {CHART_TYPES.map((type) => (
              <button
                key={type.id}
                onClick={() => setSelectedType(type.id)}
                className={`p-4 rounded-lg border-2 transition ${
                  selectedType === type.id
                    ? 'border-indigo-600 bg-indigo-50'
                    : 'border-gray-200 hover:border-indigo-300'
                }`}
              >
                <span className="text-2xl mb-2 block">{type.icon}</span>
                <span className="font-medium text-black text-sm">{type.label}</span>
              </button>
            ))}
          </div>
        </motion.div>

        {/* New Template Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <button
            onClick={() => setShowForm(!showForm)}
            className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold"
          >
            <Plus size={20} />
            Novi Template
          </button>
        </motion.div>

        {/* New Template Form */}
        {showForm && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg border border-gray-200 p-6 mb-8"
          >
            <h3 className="text-xl font-semibold text-black mb-4">Kreiraj novi template</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-black mb-2">Naziv</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="npr. Moj Bar Race Template"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-black mb-2">Tip Chart-a</label>
                <select
                  value={formData.chart_type}
                  onChange={(e) => setFormData({ ...formData, chart_type: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                >
                  {CHART_TYPES.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-black mb-2">Opis</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Opciono: Opis template-a"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 h-24"
                />
              </div>

              <div className="flex gap-2">
                <button
                  onClick={handleSaveTemplate}
                  disabled={!formData.name || loading}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                >
                  <Save size={18} />
                  Spremi Template
                </button>
                <button
                  onClick={() => setShowForm(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-black rounded-lg hover:bg-gray-50 transition"
                >
                  Otkaži
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Templates Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-600">Učitavanje...</p>
            </div>
          ) : templates.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
              <Settings size={48} className="mx-auto text-gray-400 mb-4" />
              <h3 className="text-xl font-semibold text-black mb-2">Nema template-a</h3>
              <p className="text-gray-600">Kreiraj prvi template da počneš</p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {templates.map((template, i) => (
                <motion.div
                  key={template.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition"
                >
                  <div className="mb-4">
                    <h3 className="text-lg font-semibold text-black mb-2">{template.name}</h3>
                    <p className="text-sm text-gray-600 mb-2">{template.description}</p>
                    <div className="inline-block px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-semibold">
                      {CHART_TYPES.find((t) => t.id === template.chart_type)?.label}
                    </div>
                  </div>

                  <div className="text-xs text-gray-500 mb-4">
                    <p>Kreirano: {new Date(template.created_at).toLocaleDateString()}</p>
                    <p>Ažurirano: {new Date(template.updated_at).toLocaleDateString()}</p>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => handleDuplicateTemplate(template)}
                      className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition text-sm font-medium"
                    >
                      <Copy size={16} />
                      Dupliraj
                    </button>
                    <button
                      onClick={() => handleDeleteTemplate(template.id)}
                      className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-red-50 text-red-600 rounded hover:bg-red-100 transition text-sm font-medium"
                    >
                      <Trash2 size={16} />
                      Obriši
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
