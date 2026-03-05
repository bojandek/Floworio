"use client";

import { useState } from "react";
import { useProjectStore } from "@/store/projectStore";
import toast from "react-hot-toast";

interface StoryPanelProps {
  onComplete: () => void;
}

const VOICES = [
  { id: "af_heart", label: "Heart (Female)", lang: "EN", style: "Warm & engaging" },
  { id: "af_bella", label: "Bella (Female)", lang: "EN", style: "Professional" },
  { id: "am_adam", label: "Adam (Male)", lang: "EN", style: "Deep & authoritative" },
  { id: "am_michael", label: "Michael (Male)", lang: "EN", style: "Friendly narrator" },
  { id: "bf_emma", label: "Emma (Female)", lang: "EN-GB", style: "British accent" },
  { id: "bm_george", label: "George (Male)", lang: "EN-GB", style: "British narrator" },
];

export function StoryPanel({ onComplete }: StoryPanelProps) {
  const { project, setProject } = useProjectStore();
  const [generating, setGenerating] = useState(false);
  const [generatingAudio, setGeneratingAudio] = useState(false);
  const [script, setScript] = useState(project.story?.script || "");
  const [selectedVoice, setSelectedVoice] = useState(project.story?.voiceId || "af_heart");
  const [audioUrl, setAudioUrl] = useState(project.story?.audioUrl || "");

  const generateStory = async () => {
    if (!project.dataId) {
      toast.error("No data loaded");
      return;
    }
    setGenerating(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/story/generate`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            data_id: project.dataId,
            title: project.config.title,
            chart_type: project.config.chartType,
            duration: project.config.duration,
          }),
        }
      );
      if (!response.ok) throw new Error("Story generation failed");
      const data = await response.json();
      setScript(data.script);
      toast.success("✍️ AI story generated!");
    } catch (error) {
      toast.error("Story generation failed. Check API connection.");
      console.error(error);
    } finally {
      setGenerating(false);
    }
  };

  const generateAudio = async () => {
    if (!script) {
      toast.error("Please write or generate a script first");
      return;
    }
    setGeneratingAudio(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/tts/generate`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: script,
            voice_id: selectedVoice,
          }),
        }
      );
      if (!response.ok) throw new Error("TTS failed");
      const data = await response.json();
      setAudioUrl(data.audio_url);
      toast.success("🎙️ Voiceover generated!");
    } catch (error) {
      toast.error("TTS generation failed. Check API connection.");
      console.error(error);
    } finally {
      setGeneratingAudio(false);
    }
  };

  const handleContinue = () => {
    if (!script) {
      toast.error("Please add a script or skip this step");
      return;
    }
    setProject({
      story: {
        script,
        voiceId: selectedVoice,
        audioUrl,
      },
    });
    toast.success("Story saved!");
    onComplete();
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-1">AI Story & Voiceover</h2>
        <p className="text-dark-400">
          Generate an AI-written narrative for your data, then add a voiceover using Kokoro TTS
        </p>
      </div>

      {/* AI Script Generation */}
      <div className="glass rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-dark-300 uppercase tracking-wider">
            ✍️ Script
          </h3>
          <button
            onClick={generateStory}
            disabled={generating}
            className="flex items-center gap-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {generating ? (
              <>
                <span className="animate-spin">⏳</span>
                Generating...
              </>
            ) : (
              <>✨ Generate with AI</>
            )}
          </button>
        </div>

        <textarea
          value={script}
          onChange={(e) => setScript(e.target.value)}
          placeholder="Your AI-generated script will appear here, or write your own narration...

Example: 'In 1990, the United States dominated global GDP rankings. But over the next three decades, a dramatic shift would unfold. China's rapid economic growth transformed the global landscape...'"
          rows={10}
          className="w-full bg-dark-800 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-dark-600 focus:outline-none focus:border-brand-500 transition-colors resize-none text-sm leading-relaxed"
        />

        <div className="flex items-center justify-between text-xs text-dark-500">
          <span>{script.length} characters</span>
          <span>~{Math.ceil(script.split(" ").length / 150)} min read</span>
        </div>
      </div>

      {/* Voice Selection */}
      <div className="glass rounded-xl p-6 space-y-4">
        <h3 className="text-sm font-semibold text-dark-300 uppercase tracking-wider">
          🎙️ Voice (Kokoro TTS — Open Source)
        </h3>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {VOICES.map((voice) => (
            <button
              key={voice.id}
              onClick={() => setSelectedVoice(voice.id)}
              className={`p-3 rounded-xl border text-left transition-all ${
                selectedVoice === voice.id
                  ? "border-brand-500 bg-brand-600/20"
                  : "border-white/10 hover:border-white/30"
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">{voice.lang === "EN-GB" ? "🇬🇧" : "🇺🇸"}</span>
                <span className="text-sm font-medium text-white">{voice.label}</span>
              </div>
              <div className="text-xs text-dark-400">{voice.style}</div>
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={generateAudio}
            disabled={generatingAudio || !script}
            className="flex items-center gap-2 bg-dark-700 hover:bg-dark-600 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-white/10"
          >
            {generatingAudio ? (
              <>
                <span className="animate-spin">⏳</span>
                Generating audio...
              </>
            ) : (
              <>🎵 Generate Voiceover</>
            )}
          </button>

          {audioUrl && (
            <div className="flex-1">
              <audio controls src={audioUrl} className="w-full h-8" />
            </div>
          )}
        </div>

        <div className="bg-dark-800/50 rounded-lg p-3 text-xs text-dark-400 border border-white/5">
          <strong className="text-dark-300">Powered by Kokoro TTS</strong> — Open-source, 82M parameter
          text-to-speech model. Runs locally on your server. No API costs.{" "}
          <a
            href="https://github.com/hexgrad/kokoro"
            target="_blank"
            rel="noopener noreferrer"
            className="text-brand-400 hover:underline"
          >
            GitHub ↗
          </a>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => onComplete()}
          className="text-dark-400 hover:text-white text-sm transition-colors"
        >
          Skip voiceover →
        </button>
        <button
          onClick={handleContinue}
          disabled={!script}
          className="bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white px-8 py-3 rounded-xl font-medium transition-colors"
        >
          Continue to Preview →
        </button>
      </div>
    </div>
  );
}
