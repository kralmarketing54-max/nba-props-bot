import type { Metadata, Viewport } from "next";
import { Inter, Outfit } from "next/font/google";
import Script from "next/script";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], variable: '--font-inter' });
const outfit = Outfit({ subsets: ["latin"], variable: '--font-outfit' });

export const metadata: Metadata = {
    title: "NBA Player Props Analytics",
    description: "Advanced NBA Player Props Analytics for Telegram",
};

export const viewport: Viewport = {
    width: "device-width",
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="dark">
            <head>
                {/* Telegram Web App SDK */}
                <Script src="https://telegram.org/js/telegram-web-app.js" strategy="beforeInteractive" />
            </head>
            <body className={cn(inter.variable, outfit.variable, "font-sans antialiased bg-[#0B1121] text-slate-50")}>
                <main className="max-w-md mx-auto min-h-screen relative pb-20">
                    {children}
                </main>
            </body>
        </html>
    );
}
