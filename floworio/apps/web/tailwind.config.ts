import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f4ff",
          100: "#e0e9ff",
          200: "#c7d7fe",
          300: "#a5bbfc",
          400: "#8196f8",
          500: "#6272f1",
          600: "#4f52e5",
          700: "#4240ca",
          800: "#3737a3",
          900: "#323381",
          950: "#1e1d4c",
        },
        dark: {
          50: "#f6f6f7",
          100: "#e1e3e7",
          200: "#c3c7cf",
          300: "#9da3af",
          400: "#777f8e",
          500: "#5c6474",
          600: "#494f5e",
          700: "#3c414e",
          800: "#333843",
          900: "#1a1d24",
          950: "#0f1117",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-in-out",
        "slide-up": "slideUp 0.3s ease-out",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
