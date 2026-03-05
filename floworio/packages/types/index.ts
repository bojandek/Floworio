/**
 * Floworio — Shared TypeScript Types
 * Used by both Next.js frontend and any TypeScript consumers
 * These mirror the Python Pydantic models in apps/api/routers/
 */

// ============================================================
// DATA TYPES
// ============================================================

export interface FrameData {
  timestamp: string;
  values: Record<string, number>;
}

export interface DateRange {
  start: string;
  end: string;
}

export interface UploadResponse {
  data_id: string;
  filename: string;
  columns: string[];
  rows: number;
  date_range: DateRange;
  preview: Array<{ date: string } & Record<string, number>>;
  message: string;
}

export interface DataResponse {
  data_id: string;
  columns: string[];
  frames: FrameData[];
  total_frames: number;
}

// ============================================================
// CONFIG TYPES
// ============================================================

export type ChartType = "bar_race" | "pie_race" | "line_chart" | "area_chart" | "world_map";
export type AspectRatio = "16:9" | "9:16" | "1:1" | "4:5";
export type TimeIndicator = "year" | "month" | "day";

export interface VideoConfig {
  chartType: ChartType;
  aspectRatio: AspectRatio;
  duration: number;
  fps: number;
  title: string;
  subtitle: string;
  backgroundColor: string;
  fontColor: string;
  colors: Record<string, string>;
  numberOfBars: number;
  unit: string;
  timeIndicator: TimeIndicator;
  brandingLogo?: string;
}

// ============================================================
// STORY TYPES
// ============================================================

export interface StoryRequest {
  data_id: string;
  title: string;
  chart_type: ChartType;
  duration: number;
  language?: string;
  tone?: "engaging" | "professional" | "dramatic";
}

export interface StoryResponse {
  script: string;
  word_count: number;
  estimated_duration: number;
  key_insights: string[];
}

export interface TTSRequest {
  text: string;
  voice_id?: string;
  speed?: number;
}

export interface TTSResponse {
  audio_url: string;
  duration: number;
  voice_id: string;
}

export interface VoiceOption {
  id: string;
  name: string;
}

// ============================================================
// RENDER TYPES
// ============================================================

export type RenderStatus = "pending" | "rendering" | "completed" | "failed";

export interface RenderRequest {
  data_id: string;
  config: VideoConfig;
  story?: {
    script?: string;
    voiceId?: string;
    audioUrl?: string;
  };
}

export interface RenderStartResponse {
  job_id: string;
  status: RenderStatus;
  message: string;
}

export interface RenderStatusResponse {
  job_id: string;
  status: RenderStatus;
  progress: number;
  message: string;
  video_url?: string;
  error?: string;
}

// ============================================================
// PUBLISH TYPES
// ============================================================

export type SocialPlatform =
  | "tiktok"
  | "instagram_reels"
  | "youtube_shorts"
  | "youtube"
  | "linkedin"
  | "twitter";

export interface PublishRequest {
  video_url: string;
  platforms: SocialPlatform[];
  caption: string;
  hashtags?: string;
  schedule_time?: string;
}

export interface PlatformResult {
  platform: SocialPlatform;
  success: boolean;
  post_url?: string;
  error?: string;
}

export interface PublishResponse {
  published_to: SocialPlatform[];
  results: PlatformResult[];
  scheduled: boolean;
  schedule_time?: string;
}

export interface PlatformInfo {
  id: SocialPlatform;
  name: string;
  configured: boolean;
  formats: AspectRatio[];
  docs: string;
}

// ============================================================
// PROJECT STATE (matches Zustand store)
// ============================================================

export type ProjectStatus =
  | "idle"
  | "uploading"
  | "processing"
  | "generating_story"
  | "rendering"
  | "ready"
  | "publishing"
  | "published";

export interface Project {
  id?: string;
  dataId?: string;
  fileName?: string;
  columns?: string[];
  dateRange?: DateRange;
  config: VideoConfig;
  story?: {
    script: string;
    voiceId: string;
    audioUrl?: string;
  };
  renderJobId?: string;
  videoUrl?: string;
  status: ProjectStatus;
}

// ============================================================
// API CLIENT HELPERS
// ============================================================

export interface ApiError {
  detail: string;
  status: number;
}

export function isApiError(error: unknown): error is ApiError {
  return typeof error === "object" && error !== null && "detail" in error;
}
