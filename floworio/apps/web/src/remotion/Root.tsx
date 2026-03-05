/**
 * Floworio — Remotion Root
 * Registers all video compositions
 */

import { Composition } from "remotion";
import { BarRaceComposition } from "./BarRace";

// Default props for preview in Remotion Studio
const defaultBarRaceProps = {
  frames: [
    {
      timestamp: "2020-12-31",
      values: { "United States": 21000, China: 14700, Japan: 5050, Germany: 3800, India: 2700 },
    },
    {
      timestamp: "2021-12-31",
      values: { "United States": 23000, China: 17700, Japan: 4940, Germany: 4260, India: 3180 },
    },
    {
      timestamp: "2022-12-31",
      values: { "United States": 25500, China: 18000, Japan: 4230, Germany: 4080, India: 3390 },
    },
  ],
  config: {
    title: "World GDP Rankings",
    subtitle: "in billions of USD",
    backgroundColor: "#0f1117",
    fontColor: "#ffffff",
    colors: {},
    numberOfBars: 5,
    unit: "B",
    timeIndicator: "year",
  },
  width: 1080,
  height: 1920,
  totalFrames: 90,
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="BarRace"
        component={BarRaceComposition as any}
        durationInFrames={90}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={defaultBarRaceProps}
      />
      <Composition
        id="BarRace_16x9"
        component={BarRaceComposition as any}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ ...defaultBarRaceProps, width: 1920, height: 1080 }}
      />
      <Composition
        id="BarRace_1x1"
        component={BarRaceComposition as any}
        durationInFrames={90}
        fps={30}
        width={1080}
        height={1080}
        defaultProps={{ ...defaultBarRaceProps, width: 1080, height: 1080 }}
      />
    </>
  );
};
