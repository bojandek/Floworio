'use client';

import { useState } from 'react';
import TemplateManager from '@/components/templates/TemplateManager';

export default function TemplatesPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-3xl font-bold text-black">Templates</h1>
          <p className="text-gray-600 mt-2">Upravljaj template-ima za sve tipove chart-a</p>
        </div>
      </div>

      {/* Template Manager */}
      <TemplateManager />
    </div>
  );
}
