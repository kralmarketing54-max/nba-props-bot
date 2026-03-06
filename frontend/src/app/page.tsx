"use client";

import { useEffect, useState } from "react";
import { Search, Flame, TrendingUp, ShieldCheck } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

// Geçici mock veri (Backend bağlanana kadar görsel test amaçlı)
const MOCK_PROPS = [
    {
        id: 1,
        playerName: "LeBron James",
        teamLogo: "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg",
        market: "Points",
        line: 24.5,
        matchupGrade: "A+",
        hitRateL5: 80,
        evEdge: "+5.2%",
    },
    {
        id: 2,
        playerName: "Nikola Jokic",
        teamLogo: "https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg",
        market: "PRA",
        line: 52.5,
        matchupGrade: "A",
        hitRateL5: 100,
        evEdge: "+8.4%",
    },
    {
        id: 3,
        playerName: "Stephen Curry",
        teamLogo: "https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg",
        market: "Threes",
        line: 4.5,
        matchupGrade: "B",
        hitRateL5: 60,
        evEdge: "+1.1%",
    }
];

export default function Dashboard() {
    const [tgUser, setTgUser] = useState<any>(null);

    useEffect(() => {
        // Telegram objesine ulaşıldığından emin olmak için
        const WebApp = (window as any).Telegram?.WebApp;
        if (WebApp) {
            WebApp.ready();
            WebApp.expand(); // Tam ekran yer kapla
            const user = WebApp.initDataUnsafe?.user;
            if (user) {
                setTgUser(user);
            }
        }
    }, []);

    return (
        <div className="p-4 space-y-6">

            {/* Header */}
            <header className="flex items-center justify-between py-2">
                <div>
                    <h1 className="text-2xl font-bold font-outfit text-white tracking-tight">
                        NBA <span className="text-nba-primary">Statistics</span>
                    </h1>
                    <p className="text-sm text-slate-400 font-medium">
                        Welcome back, <span className="text-slate-200">{tgUser?.first_name || "Guest"}</span>
                    </p>
                </div>
                <div className="w-10 h-10 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center overflow-hidden">
                    {/* Avatar placeholder */}
                    <div className="text-nba-primary font-bold">{tgUser?.first_name?.[0] || "?"}</div>
                </div>
            </header>

            {/* Global Search Bar */}
            <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-slate-500" />
                </div>
                <input
                    type="text"
                    placeholder="Search by player or team..."
                    className="w-full bg-slate-800/50 border border-slate-700 rounded-2xl py-3.5 pl-10 pr-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-nba-primary/50 focus:border-nba-primary transition-all shadow-inner"
                />
            </div>

            {/* Recommended Best Picks */}
            <section>
                <div className="flex items-center gap-2 mb-4">
                    <Flame className="w-5 h-5 text-nba-over" />
                    <h2 className="text-lg font-semibold text-white font-outfit">Top AI Picks</h2>
                </div>

                <div className="space-y-4">
                    {MOCK_PROPS.map((prop, idx) => (
                        <motion.div
                            key={prop.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="glass-panel p-4 relative overflow-hidden active:scale-[0.98] transition-transform cursor-pointer"
                        >
                            {/* Soft glow based on grade */}
                            <div className="absolute -right-8 -top-8 w-24 h-24 bg-nba-primary/20 rounded-full blur-2xl"></div>

                            <div className="flex justify-between items-start">
                                <div className="flex gap-3">
                                    <div className="w-12 h-12 rounded-full bg-white/10 p-2 flex items-center justify-center shrink-0">
                                        <img src={prop.teamLogo} alt="Team" className="w-full h-full object-contain drop-shadow" />
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-white tracking-tight">{prop.playerName}</h3>
                                        <div className="flex items-center gap-2 mt-1">
                                            <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-white/10 text-slate-300">
                                                {prop.market}
                                            </span>
                                            <span className="text-sm font-bold text-white">
                                                O/U {prop.line}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex flex-col items-end">
                                    <div className="flex items-center gap-1 bg-emerald-500/20 px-2 py-1 rounded-lg border border-emerald-500/30">
                                        <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                                        <span className="font-bold text-sm text-emerald-400">{prop.matchupGrade}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Stats overview footer */}
                            <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between">
                                <div className="flex flex-col">
                                    <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-0.5">L5 Hit Rate</span>
                                    <div className="flex items-center gap-1.5">
                                        <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                            <div
                                                className={cn("h-full rounded-full", prop.hitRateL5 >= 80 ? "bg-nba-over" : "bg-nba-primary")}
                                                style={{ width: `${prop.hitRateL5}%` }}
                                            />
                                        </div>
                                        <span className="text-xs font-semibold text-slate-300">{prop.hitRateL5}%</span>
                                    </div>
                                </div>

                                <div className="flex items-center gap-1">
                                    <TrendingUp className="w-3.5 h-3.5 text-nba-accent" />
                                    <span className="text-xs font-bold text-nba-accent uppercase">Edge {prop.evEdge}</span>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </section>

        </div>
    );
}
