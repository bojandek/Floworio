/**
 * Floworio — Bar Race Remotion Composition
 * Animated bar chart race using React + Remotion
 * Inspired by sjvisualizer's spring physics animation
 */

import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

interface FrameData {
  timestamp: string;
  values: Record<string, number>;
}

interface BarRaceProps {
  frames: FrameData[];
  config: {
    title: string;
    subtitle: string;
    backgroundColor: string;
    fontColor: string;
    colors: Record<string, string>;
    numberOfBars: number;
    unit: string;
    timeIndicator: string;
  };
  width: number;
  height: number;
  totalFrames: number;
}

// Default color palette (from sjvisualizer)
const DEFAULT_COLORS = [
  "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
  "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
  "#6272f1", "#a78bfa", "#60a5fa", "#34d399", "#f59e0b",
];

function formatValue(value: number, unit: string): string {
  if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(1)}B${unit}`;
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M${unit}`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K${unit}`;
  return `${value.toFixed(0)}${unit}`;
}

function getTimestamp(timestamp: string, timeIndicator: string): string {
  try {
    const date = new Date(timestamp);
    if (timeIndicator === "year") return String(date.getFullYear());
    if (timeIndicator === "month") {
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[date.getMonth()]} ${date.getFullYear()}`;
    }
    return date.toLocaleDateString();
  } catch {
    return timestamp;
  }
}

export const BarRaceComposition: React.FC<BarRaceProps> = ({
  frames,
  config,
  width,
  height,
  totalFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Get current frame data
  const frameIndex = Math.min(frame, frames.length - 1);
  const currentFrameData = frames[frameIndex];

  if (!currentFrameData) return null;

  const { values, timestamp } = currentFrameData;

  // Sort and get top N bars
  const sortedEntries = Object.entries(values)
    .filter(([, v]) => v > 0)
    .sort(([, a], [, b]) => b - a)
    .slice(0, config.numberOfBars);

  const maxValue = sortedEntries[0]?.[1] || 1;

  // Layout
  const padding = { top: height * 0.12, bottom: height * 0.08, left: width * 0.28, right: width * 0.08 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const barHeight = (chartHeight / config.numberOfBars) * 0.7;
  const barGap = (chartHeight / config.numberOfBars) * 0.3;

  // Color assignment
  const colorMap: Record<string, string> = {};
  let colorIndex = 0;
  Object.keys(values).forEach((key) => {
    if (config.colors[key]) {
      colorMap[key] = config.colors[key];
    } else {
      colorMap[key] = DEFAULT_COLORS[colorIndex % DEFAULT_COLORS.length];
      colorIndex++;
    }
  });

  // Entrance animation
  const entranceProgress = interpolate(frame, [0, fps * 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: config.backgroundColor || "#0f1117",
        fontFamily: "Inter, system-ui, sans-serif",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* Title */}
      <div
        style={{
          position: "absolute",
          top: height * 0.04,
          left: padding.left,
          right: padding.right,
          opacity: entranceProgress,
          transform: `translateY(${(1 - entranceProgress) * 20}px)`,
        }}
      >
        <div
          style={{
            fontSize: height * 0.045,
            fontWeight: 800,
            color: config.fontColor || "#ffffff",
            lineHeight: 1.2,
          }}
        >
          {config.title}
        </div>
        {config.subtitle && (
          <div
            style={{
              fontSize: height * 0.025,
              color: "rgba(255,255,255,0.5)",
              marginTop: 4,
            }}
          >
            {config.subtitle}
          </div>
        )}
      </div>

      {/* Timestamp */}
      <div
        style={{
          position: "absolute",
          top: height * 0.04,
          right: padding.right,
          fontSize: height * 0.07,
          fontWeight: 900,
          color: "rgba(255,255,255,0.15)",
          fontVariantNumeric: "tabular-nums",
        }}
      >
        {getTimestamp(timestamp, config.timeIndicator)}
      </div>

      {/* Bars */}
      <div
        style={{
          position: "absolute",
          top: padding.top,
          left: 0,
          right: 0,
          height: chartHeight,
        }}
      >
        {sortedEntries.map(([name, value], index) => {
          const barWidth = (value / maxValue) * chartWidth;
          const yPos = index * (barHeight + barGap);
          const color = colorMap[name] || DEFAULT_COLORS[0];

          // Spring animation for bar width
          const animatedWidth = interpolate(
            frame,
            [Math.max(0, frame - 5), frame],
            [barWidth * 0.95, barWidth],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );

          return (
            <div
              key={name}
              style={{
                position: "absolute",
                top: yPos,
                left: 0,
                width: "100%",
                height: barHeight,
                opacity: entranceProgress,
              }}
            >
              {/* Label */}
              <div
                style={{
                  position: "absolute",
                  right: width - padding.left + 8,
                  top: 0,
                  height: barHeight,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "flex-end",
                  width: padding.left - 16,
                  fontSize: Math.max(height * 0.018, 10),
                  fontWeight: 600,
                  color: config.fontColor || "#ffffff",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {name}
              </div>

              {/* Bar */}
              <div
                style={{
                  position: "absolute",
                  left: padding.left,
                  top: 0,
                  width: Math.max(animatedWidth, 2),
                  height: barHeight,
                  backgroundColor: color,
                  borderRadius: "0 6px 6px 0",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "flex-end",
                  paddingRight: 8,
                  transition: "width 0.1s ease",
                }}
              >
                {/* Value label */}
                <span
                  style={{
                    fontSize: Math.max(height * 0.016, 9),
                    fontWeight: 700,
                    color: "rgba(255,255,255,0.9)",
                    whiteSpace: "nowrap",
                  }}
                >
                  {formatValue(value, config.unit || "")}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Floworio watermark */}
      <div
        style={{
          position: "absolute",
          bottom: height * 0.02,
          right: padding.right,
          fontSize: height * 0.018,
          color: "rgba(255,255,255,0.2)",
          fontWeight: 600,
        }}
      >
        floworio.com
      </div>
    </div>
  );
};
