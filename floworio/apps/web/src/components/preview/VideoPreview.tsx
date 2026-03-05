"use client";

import { useState, useEffect } from "react";
import { useProjectStore } from "@/store/projectStore";
import toast from "react-hot-toast";

interface VideoPreviewProps {
  onComplete: () => void;
}

export function VideoPreview({ onComplete }: VideoPreviewProps) {
  const { project, setProject } = useProjectStore();
  const [rendering, setRendering] = useState(false);
  const [renderProgress, setRenderProgress] = useState(0);
  const [renderStatus, setRenderStatus] = useState("");

  const startRender = async () => {
    if (!project.dataId) {
      toast.error("No data loaded");
      return;
    }
    setRendering(true);
    setRenderProgress(0);
    setRenderStatus("Initializing render...");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/render/start`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            data_id: project.dataId,
            config: project.config,
            story: project.story,
          }),
        }
      );

      if (!response.ok) throw new Error("Render failed to start");
      const data = await response.json();
      const jobId = data.job_id;

      setProject({ renderJobId: jobId, status: "rendering" });

      // Poll for progress
      const pollInterval = setInterval(async () => {
        try {
          const statusRes = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/render/status/${jobId}`
          );
          const statusData = await statusRes.json();

          setRenderProgress(statusData.progress || 0);
          setRenderStatus(statusData.message || "Rendering...");

          if (statusData.status === "completed") {
            clearInterval(pollInterval);
            setRendering(false);
            setProject({
              videoUrl: statusData.video_url,
              status: "ready",
            });
            toast.success("🎬 Video rendered successfully!");
          } else if (statusData.status === "failed") {
            clearInterval(pollInterval);
            setRendering(false);
            toast.error("Render failed: " + statusData.error);
          }
        } catch {
          clearInterval(pollInterval);
          setRendering(false);
          toast.error("Lost connection to render server");
        }
      }, 2000);
    } catch (error) {
      setRendering(false);
      toast.error("Failed to start render. Check API connection.");
      console.error(error);
    }
  };

  const aspectRatioClass = {
    "9:16": "aspect-[9/16] max-h-[600px]",
    "1:1": "aspect-square max-h-[500px]",
    "16:9": "aspect-video max-h-[400px]",
    "4:5": "aspect-[4/5] max-h-[550px]",
  }[project.config.aspectRatio] || "aspect-video";

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-1">Preview & Render</h2>
        <p className="text-dark-400">
          Render your video using Remotion — server-side React-based video rendering
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Video Preview Area */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-dark-300 uppercase tracking-wider">
            🎬 Video Preview
          </h3>

          <div className={`${aspectRatioClass} w-full mx-auto max-w-sm`}>
            {project.videoUrl ? (
              <video
                src={project.videoUrl}
                controls
                className="w-full h-full rounded-xl object-cover"
              />
            ) : (
              <div className="w-full h-full rounded-xl glass flex flex-col items-center justify-center gap-4">
                {rendering ? (
                  <>
                    <div className="text-4xl animate-spin">⚙️</div>
                    <div className="text-center">
                      <p className="text-white font-medium mb-2">{renderStatus}</p>
                      <div className="w-48 bg-dark-800 rounded-full h-2">
                        <div
                          className="progress-animated h-2 rounded-full transition-all duration-500"
                          style={{ width: `${renderProgress}%` }}
                        />
                      </div>
                      <p className="text-dark-400 text-sm mt-2">{renderProgress}%</p>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="text-5xl">🎬</div>
                    <p className="text-dark-400 text-sm text-center">
                      Click &quot;Render Video&quot; to generate your animated video
                    </p>
                  </>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Render Settings & Info */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-dark-300 uppercase tracking-wider">
            ⚙️ Render Settings
          </h3>

          {/* Summary */}
          <div className="glass rounded-xl p-5 space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-dark-400">Chart Type</span>
              <span className="text-white capitalize">{project.config.chartType.replace("_", " ")}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-dark-400">Aspect Ratio</span>
              <span className="text-white">{project.config.aspectRatio}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-dark-400">Duration</span>
              <span className="text-white">{project.config.duration}s</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-dark-400">FPS</span>
              <span className="text-white">{project.config.fps}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-dark-400">Total Frames</span>
              <span className="text-white">{project.config.duration * project.config.fps}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-dark-400">Voiceover</span>
              <span className={project.story?.audioUrl ? "text-green-400" : "text-dark-500"}>
                {project.story?.audioUrl ? "✅ Included" : "Not added"}
              </span>
            </div>
          </div>

          {/* Remotion Info */}
          <div className="bg-dark-800/50 rounded-lg p-4 text-xs text-dark-400 border border-white/5">
            <strong className="text-dark-300">Powered by Remotion</strong> — React-based programmatic
            video creation. Renders your data animations server-side as high-quality MP4.{" "}
            <a
              href="https://github.com/remotion-dev/remotion"
              target="_blank"
              rel="noopener noreferrer"
              className="text-brand-400 hover:underline"
            >
              GitHub ↗
            </a>
          </div>

          {/* Render Button */}
          {!project.videoUrl ? (
            <button
              onClick={startRender}
              disabled={rendering}
              className="w-full bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white py-3 rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
            >
              {rendering ? (
                <>
                  <span className="animate-spin">⚙️</span>
                  Rendering... {renderProgress}%
                </>
              ) : (
                <>🎬 Render Video</>
              )}
            </button>
          ) : (
            <div className="space-y-3">
              <a
                href={project.videoUrl}
                download
                className="w-full bg-green-600 hover:bg-green-500 text-white py-3 rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
              >
                ⬇️ Download MP4
              </a>
              <button
                onClick={startRender}
                className="w-full bg-dark-700 hover:bg-dark-600 text-white py-2.5 rounded-xl text-sm font-medium transition-colors border border-white/10"
              >
                🔄 Re-render
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Continue */}
      <div className="flex justify-end">
        <button
          onClick={onComplete}
          disabled={!project.videoUrl}
          className="bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white px-8 py-3 rounded-xl font-medium transition-colors"
        >
          Continue to Publish →
        </button>
      </div>
    </div>
  );
}
