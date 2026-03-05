import { create } from "zustand";

export interface ProjectConfig {
  chartType: "bar_race" | "pie_race" | "line_chart" | "area_chart" | "world_map";
  aspectRatio: "16:9" | "9:16" | "1:1" | "4:5";
  duration: number; // seconds
  fps: number;
  title: string;
  subtitle: string;
  backgroundColor: string;
  fontColor: string;
  colors: Record<string, string>;
  numberOfBars: number;
  unit: string;
  timeIndicator: "year" | "month" | "day";
  brandingLogo?: string;
}

export interface Project {
  id?: string;
  dataId?: string;
  fileName?: string;
  columns?: string[];
  dateRange?: { start: string; end: string };
  config: ProjectConfig;
  story?: {
    script: string;
    voiceId: string;
    audioUrl?: string;
  };
  renderJobId?: string;
  videoUrl?: string;
  status: "idle" | "uploading" | "processing" | "generating_story" | "rendering" | "ready" | "publishing" | "published";
}

interface ProjectStore {
  project: Project;
  setProject: (updates: Partial<Project>) => void;
  setConfig: (updates: Partial<ProjectConfig>) => void;
  resetProject: () => void;
}

const defaultConfig: ProjectConfig = {
  chartType: "bar_race",
  aspectRatio: "9:16",
  duration: 30,
  fps: 30,
  title: "",
  subtitle: "",
  backgroundColor: "#0f1117",
  fontColor: "#ffffff",
  colors: {},
  numberOfBars: 10,
  unit: "",
  timeIndicator: "year",
};

const defaultProject: Project = {
  config: defaultConfig,
  status: "idle",
};

export const useProjectStore = create<ProjectStore>((set) => ({
  project: defaultProject,
  setProject: (updates) =>
    set((state) => ({
      project: { ...state.project, ...updates },
    })),
  setConfig: (updates) =>
    set((state) => ({
      project: {
        ...state.project,
        config: { ...state.project.config, ...updates },
      },
    })),
  resetProject: () => set({ project: defaultProject }),
}));
