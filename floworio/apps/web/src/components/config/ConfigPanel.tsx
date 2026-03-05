"use client";

import { useState } from "react";
import { useProjectStore } from "@/store/projectStore";
import toast from "react-hot-toast";

interface ConfigPanelProps {
  onComplete: () => void;
}

const CHART_TYPES = [
  { id: "bar_race", label: "Bar Race", icon: "📊", desc: "Animated ranking bars" },
  { id: "pie_race", label: "Pie Race", icon: "🥧", desc: "Animated pie chart" },
  { id: "line_chart", label: "Line Chart", icon: "📈", desc: "Animated line chart" },
  { id: "area_chart", label: "Area Chart", icon: "🏔️", desc: "Stacked area chart" },
  { id: "world_map", label: "World Map", icon: "🌍", desc: "Animated world map" },
] as const;

const ASPECT_RATIOS = [
  { id: "9:16", label: "9:16", desc: "TikTok / Reels", icon: "📱" },
  { id: "1:1", label: "1:1", desc: "Instagram Square", icon: "⬜" },
  { id: "16:9", label: "16:9", desc: "YouTube / Landscape", icon: "🖥️" },
  { id: "4:5", label: "4:5", desc: "Instagram Portrait", icon: "📷" },
] as const;

export function ConfigPanel({ onComplete }: ConfigPanelProps) {
  const { project, setConfig } = useProjectStore();
  const { config } = project;
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    if (!config.title) {
      toast.error("Please add a title for your video");
      return;
    }
    setSaving(true);
    await new Promise((r) => setTimeout(r, 500));
    setSaving(false);
    toast.success("Configuration saved!");
    onComplete();
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-1">Configure Your Video</h2>
        <p className="text-dark-400">Choose chart type, aspect ratio, and styling options</p>
      </div>

      {/* Chart Type */}
      <div className="glass rounded-xl p-6">
        <h3 className="text-sm font-semibold text-dark-300 mb-4 uppercase tracking-wider">
          Chart Type
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {CHART_TYPES.map((type) => (
            <button
              key={type.id}
              onClick={() => setConfig({ chartType: type.id })}
              className={`p-4 rounded-xl border text-center transition-all ${
                config.chartType === type.id
                  ? "border-brand-500 bg-brand-600/20 text-white"
                  : "border-white/10 hover:border-white/30 text-dark-300 hover:text-white"
              }`}
            >
              <div className="text-2xl mb-2">{type.icon}</div>
              <div className="text-xs font-medium">{type.label}</div>
              <div className="text-xs text-dark-500 mt-0.5">{type.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Aspect Ratio */}
      <div className="glass rounded-xl p-6">
        <h3 className="text-sm font-semibold text-dark-300 mb-4 uppercase tracking-wider">
          Aspect Ratio
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {ASPECT_RATIOS.map((ratio) => (
            <button
              key={ratio.id}
              onClick={() => setConfig({ aspectRatio: ratio.id })}
              className={`p-4 rounded-xl border text-center transition-all ${
                config.aspectRatio === ratio.id
                  ? "border-brand-500 bg-brand-600/20 text-white"
                  : "border-white/10 hover:border-white/30 text-dark-300 hover:text-white"
              }`}
            >
              <div className="text-2xl mb-2">{ratio.icon}</div>
              <div className="text-sm font-bold">{ratio.label}</div>
              <div className="text-xs text-dark-500 mt-0.5">{ratio.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Title & Subtitle */}
      <div className="glass rounded-xl p-6 space-y-4">
        <h3 className="text-sm font-semibold text-dark-300 mb-2 uppercase tracking-wider">
          Text & Labels
        </h3>
        <div>
          <label className="block text-sm text-dark-300 mb-1.5">Video Title *</label>
          <input
            type="text"
            value={config.title}
            onChange={(e) => setConfig({ title: e.target.value })}
            placeholder="e.g. Top 10 Countries by GDP 1990-2023"
            className="w-full bg-dark-800 border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-dark-500 focus:outline-none focus:border-brand-500 transition-colors"
          />
        </div>
        <div>
          <label className="block text-sm text-dark-300 mb-1.5">Subtitle</label>
          <input
            type="text"
            value={config.subtitle}
            onChange={(e) => setConfig({ subtitle: e.target.value })}
            placeholder="e.g. in billions of USD"
            className="w-full bg-dark-800 border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-dark-500 focus:outline-none focus:border-brand-500 transition-colors"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-dark-300 mb-1.5">Unit</label>
            <input
              type="text"
              value={config.unit}
              onChange={(e) => setConfig({ unit: e.target.value })}
              placeholder="e.g. %, $, kg"
              className="w-full bg-dark-800 border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-dark-500 focus:outline-none focus:border-brand-500 transition-colors"
            />
          </div>
          <div>
            <label className="block text-sm text-dark-300 mb-1.5">Time Format</label>
            <select
              value={config.timeIndicator}
              onChange={(e) => setConfig({ timeIndicator: e.target.value as "year" | "month" | "day" })}
              className="w-full bg-dark-800 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-brand-500 transition-colors"
            >
              <option value="year">Year (2023)</option>
              <option value="month">Month (Jan 2023)</option>
              <option value="day">Day (1 Jan 2023)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Duration & FPS */}
      <div className="glass rounded-xl p-6">
        <h3 className="text-sm font-semibold text-dark-300 mb-4 uppercase tracking-wider">
          Video Settings
        </h3>
        <div className="grid grid-cols-2 gap-6">
          <div>
            <label className="block text-sm text-dark-300 mb-1.5">
              Duration: <span className="text-white font-medium">{config.duration}s</span>
            </label>
            <input
              type="range"
              min={10}
              max={120}
              step={5}
              value={config.duration}
              onChange={(e) => setConfig({ duration: parseInt(e.target.value) })}
              className="w-full accent-brand-500"
            />
            <div className="flex justify-between text-xs text-dark-500 mt-1">
              <span>10s</span>
              <span>120s</span>
            </div>
          </div>
          <div>
            <label className="block text-sm text-dark-300 mb-1.5">
              FPS: <span className="text-white font-medium">{config.fps}</span>
            </label>
            <div className="flex gap-2">
              {[24, 30, 60].map((fps) => (
                <button
                  key={fps}
                  onClick={() => setConfig({ fps })}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-all ${
                    config.fps === fps
                      ? "border-brand-500 bg-brand-600/20 text-white"
                      : "border-white/10 text-dark-400 hover:text-white"
                  }`}
                >
                  {fps}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Number of bars (for bar race) */}
      {config.chartType === "bar_race" && (
        <div className="glass rounded-xl p-6">
          <h3 className="text-sm font-semibold text-dark-300 mb-4 uppercase tracking-wider">
            Bar Race Settings
          </h3>
          <div>
            <label className="block text-sm text-dark-300 mb-1.5">
              Number of bars: <span className="text-white font-medium">{config.numberOfBars}</span>
            </label>
            <input
              type="range"
              min={3}
              max={20}
              step={1}
              value={config.numberOfBars}
              onChange={(e) => setConfig({ numberOfBars: parseInt(e.target.value) })}
              className="w-full accent-brand-500"
            />
            <div className="flex justify-between text-xs text-dark-500 mt-1">
              <span>3</span>
              <span>20</span>
            </div>
          </div>
        </div>
      )}

      {/* Action */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white px-8 py-3 rounded-xl font-medium transition-colors flex items-center gap-2"
        >
          {saving ? "Saving..." : "Continue to AI Story →"}
        </button>
      </div>
    </div>
  );
}
