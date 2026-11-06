import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark technical workstation palette
        background: {
          DEFAULT: "#090A0F",
          secondary: "#0D0F14",
          tertiary: "#131620",
        },
        surface: {
          DEFAULT: "#131620",
          elevated: "#1A1E2A",
          overlay: "#1E2333",
        },
        border: {
          DEFAULT: "#1E2333",
          subtle: "#2A2F3E",
          focus: "#06B6D4",
        },
        text: {
          PRIMARY: "#F8FAFC",
          secondary: "#94A3B8",
          muted: "#64748B",
          inverse: "#090A0F",
        },
        accent: {
          cyan: "#06B6D4",
          cyanDim: "#0891B2",
          emerald: "#10B981",
          emeraldDim: "#059669",
          amber: "#F59E0B",
          amberDim: "#D97706",
          rose: "#F43F5E",
          roseDim: "#E11D48",
        },
        status: {
          success: "#10B981",
          warning: "#F59E0B",
          error: "#F43F5E",
          info: "#06B6D4",
        },
      },
      fontFamily: {
        sans: ["Geist", "Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
        display: ["Geist", "Inter", "system-ui", "sans-serif"],
      },
      fontSize: {
        "display-xl": ["4.5rem", { lineHeight: "1.1", letterSpacing: "-0.02em" }],
        "display-lg": ["3.5rem", { lineHeight: "1.15", letterSpacing: "-0.02em" }],
        "display-md": ["2.5rem", { lineHeight: "1.2", letterSpacing: "-0.01em" }],
        "display-sm": ["1.875rem", { lineHeight: "1.25", letterSpacing: "-0.01em" }],
        "heading-xl": ["1.5rem", { lineHeight: "1.3", letterSpacing: "-0.01em" }],
        "heading-lg": ["1.25rem", { lineHeight: "1.35", letterSpacing: "-0.01em" }],
        "heading-md": ["1.125rem", { lineHeight: "1.4", letterSpacing: "0" }],
        "heading-sm": ["1rem", { lineHeight: "1.45", letterSpacing: "0" }],
        "body-lg": ["1.125rem", { lineHeight: "1.6" }],
        "body-md": ["1rem", { lineHeight: "1.6" }],
        "body-sm": ["0.875rem", { lineHeight: "1.55" }],
        "body-xs": ["0.75rem", { lineHeight: "1.5" }],
        "caption": ["0.6875rem", { lineHeight: "1.5", letterSpacing: "0.02em" }],
      },
      spacing: {
        "space-1": "0.25rem",  // 4px
        "space-2": "0.5rem",   // 8px
        "space-3": "0.75rem",  // 12px
        "space-4": "1rem",     // 16px
        "space-5": "1.25rem",  // 20px
        "space-6": "1.5rem",   // 24px
        "space-8": "2rem",     // 32px
        "space-10": "2.5rem",  // 40px
        "space-12": "3rem",    // 48px
        "space-16": "4rem",    // 64px
        "space-20": "5rem",    // 80px
        "space-24": "6rem",    // 96px
      },
      borderRadius: {
        "radius-sm": "4px",
        "radius-md": "8px",
        "radius-lg": "12px",
        "radius-xl": "16px",
        "radius-full": "9999px",
      },
      boxShadow: {
        "shadow-sm": "0 1px 2px 0 rgba(0, 0, 0, 0.3)",
        "shadow-md": "0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3)",
        "shadow-lg": "0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.3)",
        "shadow-xl": "0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.3)",
        "shadow-glow-cyan": "0 0 20px rgba(6, 182, 212, 0.15)",
        "shadow-glow-emerald": "0 0 20px rgba(16, 185, 129, 0.15)",
      },
      transitionDuration: {
        "fast": "100ms",
        "normal": "200ms",
        "slow": "300ms",
      },
      transitionTimingFunction: {
        "ease-out-expo": "cubic-bezier(0.16, 1, 0.3, 1)",
        "ease-spring": "cubic-bezier(0.34, 1.56, 0.64, 1)",
      },
      animation: {
        "fade-in": "fadeIn 200ms ease-out forwards",
        "slide-up": "slideUp 300ms ease-out-expo forwards",
        "slide-down": "slideDown 300ms ease-out-expo forwards",
        "scale-in": "scaleIn 200ms ease-out-expo forwards",
        "pulse-soft": "pulseSoft 2s ease-in-out infinite",
        "shimmer": "shimmer 2s linear infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideDown: {
          "0%": { opacity: "0", transform: "translateY(-8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.96)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.6" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
        "beam-cyan": "radial-gradient(ellipse 80% 50% at 50% 0%, rgba(6, 182, 212, 0.15) 0%, transparent 70%)",
        "beam-emerald": "radial-gradient(ellipse 80% 50% at 50% 0%, rgba(16, 185, 129, 0.15) 0%, transparent 70%)",
        "mesh-gradient": "linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, transparent 50%), linear-gradient(225deg, rgba(16, 185, 129, 0.08) 0%, transparent 50%)",
      },
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
  ],
};

export default config;