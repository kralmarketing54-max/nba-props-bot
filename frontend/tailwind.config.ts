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
                background: "var(--background)",
                foreground: "var(--foreground)",
                border: "var(--border)",
                nba: {
                    dark: "#0F172A", // slate-900
                    card: "rgba(30, 41, 59, 0.7)", // slate-800 with opacity for glassmorphism
                    primary: "#38bdf8", // sky-400
                    accent: "#818cf8", // indigo-400
                    over: "#10b981", // emerald-500
                    under: "#f43f5e", // rose-500
                }
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'glass-gradient': 'linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%)',
            },
        },
    },
    plugins: [],
};
export default config;
