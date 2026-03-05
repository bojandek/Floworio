"use client";

import { useState } from "react";
import { useProjectStore } from "@/store/projectStore";
import toast from "react-hot-toast";

const PLATFORMS = [
  {
    id: "tiktok",
    label: "TikTok",
    icon: "🎵",
    color: "from-pink-600 to-red-600",
    formats: ["9:16"],
    desc: "Best for 9:16 vertical videos",
  },
  {
    id: "instagram_reels",
    label: "Instagram Reels",
    icon: "📸",
    color: "from-purple-600 to-pink-600",
    formats: ["9:16", "1:1"],
    desc: "Reels & Feed posts",
  },
  {
    id: "youtube_shorts",
    label: "YouTube Shorts",
    icon: "▶️",
    color: "from-red-600 to-red-700",
    formats: ["9:16"],
    desc: "Shorts format",
  },
  {
    id: "youtube",
    label: "YouTube",
    icon: "📺",
    color: "from-red-500 to-red-600",
    formats: ["16:9"],
    desc: "Standard YouTube video",
  },
  {
    id: "linkedin",
    label: "LinkedIn",
    icon: "💼",
    color: "from-blue-600 to-blue-700",
    formats: ["16:9", "1:1", "4:5"],
    desc: "Professional network",
  },
  {
    id: "twitter",
    label: "X (Twitter)",
    icon: "🐦",
    color: "from-gray-700 to-gray-900",
    formats: ["16:9", "1:1"],
    desc: "Twitter/X video post",
  },
];

export function PublishPanel() {
  const { project } = useProjectStore();
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [caption, setCaption] = useState("");
  const [hashtags, setHashtags] = useState("");
  const [scheduleTime, setScheduleTime] = useState("");
  const [publishing, setPublishing] = useState(false);
  const [published, setPublished] = useState<string[]>([]);

  const togglePlatform = (id: string) => {
    setSelectedPlatforms((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  const generateCaption = async () => {
    if (!project.story?.script) {
      toast.error("No story script found. Go back and generate a story.");
      return;
    }
    // Use first 2 sentences of script as caption
    const sentences = project.story.script.split(". ").slice(0, 2).join(". ");
    setCaption(sentences + ".");
    setHashtags("#datavisualization #barrace #datascience #statistics #viral");
    toast.success("Caption generated from your story!");
  };

  const handlePublish = async () => {
    if (selectedPlatforms.length === 0) {
      toast.error("Select at least one platform");
      return;
    }
    if (!project.videoUrl) {
      toast.error("No video rendered yet. Go back and render your video.");
      return;
    }

    setPublishing(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/publish`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            video_url: project.videoUrl,
            platforms: selectedPlatforms,
            caption: caption + "\n\n" + hashtags,
            schedule_time: scheduleTime || null,
          }),
        }
      );

      if (!response.ok) throw new Error("Publish failed");
      const data = await response.json();

      setPublished(data.published_to || selectedPlatforms);
      toast.success(`🚀 Published to ${selectedPlatforms.length} platform(s)!`);
    } catch (error) {
      toast.error("Publishing failed. Check API connection and platform credentials.");
      console.error(error);
    } finally {
      setPublishing(false);
    }
  };

  const compatiblePlatforms = PLATFORMS.filter((p) =>
    p.formats.includes(project.config.aspectRatio)
  );

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold mb-1">Publish to Social Media</h2>
        <p className="text-dark-400">
          Select platforms and publish your video directly — or schedule for later
        </p>
      </div>

      {published.length > 0 && (
        <div className="glass rounded-xl p-6 border border-green-500/30 bg-green-500/5">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-2xl">🎉</span>
            <h3 className="text-lg font-bold text-green-400">Successfully Published!</h3>
          </div>
          <p className="text-dark-300 text-sm">
            Your video has been published to: {published.join(", ")}
          </p>
        </div>
      )}

      {/* Platform Selection */}
      <div className="glass rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-dark-300 uppercase tracking-wider">
            🚀 Select Platforms
          </h3>
          <span className="text-xs text-dark-500">
            Current format: <span className="text-brand-400">{project.config.aspectRatio}</span>
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {PLATFORMS.map((platform) => {
            const isCompatible = platform.formats.includes(project.config.aspectRatio);
            const isSelected = selectedPlatforms.includes(platform.id);

            return (
              <button
                key={platform.id}
                onClick={() => isCompatible && togglePlatform(platform.id)}
                disabled={!isCompatible}
                className={`p-4 rounded-xl border text-left transition-all relative ${
                  isSelected
                    ? "border-brand-500 bg-brand-600/20"
                    : isCompatible
                    ? "border-white/10 hover:border-white/30"
                    : "border-white/5 opacity-40 cursor-not-allowed"
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xl">{platform.icon}</span>
                  <span className="text-sm font-medium text-white">{platform.label}</span>
                  {isSelected && (
                    <span className="ml-auto text-brand-400 text-xs">✓</span>
                  )}
                </div>
                <div className="text-xs text-dark-400">{platform.desc}</div>
                {!isCompatible && (
                  <div className="text-xs text-dark-600 mt-1">
                    Needs: {platform.formats.join(" or ")}
                  </div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Caption & Hashtags */}
      <div className="glass rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-dark-300 uppercase tracking-wider">
            📝 Caption & Hashtags
          </h3>
          <button
            onClick={generateCaption}
            className="text-xs text-brand-400 hover:text-brand-300 transition-colors"
          >
            ✨ Generate from story
          </button>
        </div>

        <textarea
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
          placeholder="Write your caption here..."
          rows={4}
          className="w-full bg-dark-800 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-dark-600 focus:outline-none focus:border-brand-500 transition-colors resize-none text-sm"
        />

        <input
          type="text"
          value={hashtags}
          onChange={(e) => setHashtags(e.target.value)}
          placeholder="#datavisualization #barrace #datascience"
          className="w-full bg-dark-800 border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-dark-600 focus:outline-none focus:border-brand-500 transition-colors text-sm"
        />
      </div>

      {/* Schedule */}
      <div className="glass rounded-xl p-6">
        <h3 className="text-sm font-semibold text-dark-300 mb-4 uppercase tracking-wider">
          ⏰ Schedule (Optional)
        </h3>
        <div className="flex items-center gap-4">
          <input
            type="datetime-local"
            value={scheduleTime}
            onChange={(e) => setScheduleTime(e.target.value)}
            className="bg-dark-800 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-brand-500 transition-colors text-sm"
          />
          {scheduleTime && (
            <button
              onClick={() => setScheduleTime("")}
              className="text-dark-400 hover:text-white text-sm"
            >
              Clear (publish now)
            </button>
          )}
        </div>
        <p className="text-dark-500 text-xs mt-2">
          Leave empty to publish immediately. Set a time to schedule for later.
        </p>
      </div>

      {/* Publish Button */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-dark-400">
          {selectedPlatforms.length > 0 ? (
            <span>
              Publishing to:{" "}
              <span className="text-white">{selectedPlatforms.join(", ")}</span>
            </span>
          ) : (
            "No platforms selected"
          )}
        </div>
        <button
          onClick={handlePublish}
          disabled={publishing || selectedPlatforms.length === 0 || !project.videoUrl}
          className="bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white px-8 py-3 rounded-xl font-medium transition-colors flex items-center gap-2"
        >
          {publishing ? (
            <>
              <span className="animate-spin">⏳</span>
              Publishing...
            </>
          ) : scheduleTime ? (
            <>📅 Schedule Post</>
          ) : (
            <>🚀 Publish Now</>
          )}
        </button>
      </div>
    </div>
  );
}
