"use client";

import { useEffect, useState } from "react";
import { ArrowLeft, TrendingUp, ShieldAlert, Star, Share2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import PlayerChart from "@/components/PlayerChart";

// Geçici statik data
const MOCK_ANALYTICS = {
    player: { name: "LeBron James", team: "LAL", photo: "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png" },
    market: "Points",
    line: 24.5,
    hitRates: {
        l5: {
            hit_rate: 80, history: [
                { game_id: "1", date: "Mar 4", opponent: "DEN", value: 26, is_hit: true },
                { game_id: "2", date: "Mar 2", opponent: "MIA", value: 31, is_hit: true },
                { game_id: "3", date: "Feb 28", opponent: "LAC", value: 22, is_hit: false },
                { game_id: "4", date: "Feb 26", opponent: "PHX", value: 28, is_hit: true },
                { game_id: "5", date: "Feb 24", opponent: "SAS", value: 30, is_hit: true },
            ]
        },
        season: { hit_rate: 65, total: 54 }
    },
    matchup_grade: { grade: "A+", score: 88, breakdown: { def_rating_score: 18 } },
    prediction: { expected_value: 12.5, hit_probability: 68.2, edge: "+4.1%" },
    splits: { home_avg: 26.2, away_avg: 23.8, h2h_avg: 28.0 }
};

export default function PlayerAnalyticsPage({ params }: { params: { id: string } }) {
    const router = useRouter();
    const [isFavorite, setIsFavorite] = useState(false);

    // Normalde fetch() ile params.id kullanılarak backend'den veri çekilir.
    const data = MOCK_ANALYTICS;

    return (
        <div className="pb-10 font-sans">
            {/* Header (Back button + Actions) */}
            <header className="sticky top-0 z-50 glass-panel border-x-0 border-t-0 rounded-none px-4 py-3 flex items-center justify-between">
                <button onClick={() => router.back()} className="w-10 h-10 flex items-center justify-center rounded-full bg-white/5 hover:bg-white/10 transition-colors">
                    <ArrowLeft className="w-5 h-5 text-white" />
                </button>
                <div className="flex gap-2">
                    <button
                        onClick={() => setIsFavorite(!isFavorite)}
                        className={cn("w-10 h-10 flex items-center justify-center rounded-full transition-colors", isFavorite ? "bg-amber-500/20 text-amber-500" : "bg-white/5 text-slate-300 hover:bg-white/10")}
                    >
                        <Star className={cn("w-5 h-5", isFavorite && "fill-current")} />
                    </button>
                    <button className="w-10 h-10 flex items-center justify-center rounded-full bg-white/5 hover:bg-white/10 text-slate-300 transition-colors">
                        <Share2 className="w-5 h-5" />
                    </button>
                </div>
            </header>

            {/* Player Identity */}
            <section className="px-4 py-6 text-center shadow-lg bg-gradient-to-b from-nba-card/80 to-transparent relative overflow-hidden">
                <div className="absolute inset-0 bg-glass-gradient opacity-30 pointer-events-none" />
                <div className="w-24 h-24 mx-auto rounded-full bg-slate-800 border-2 border-slate-600 mb-3 overflow-hidden shadow-2xl relative z-10">
                    <img src={data.player.photo} alt={data.player.name} className="w-full h-full object-cover object-top" />
                </div>
                <h1 className="text-2xl font-bold text-white tracking-tight drop-shadow-md z-10 relative">{data.player.name}</h1>
                <p className="text-slate-400 font-semibold uppercase tracking-widest text-sm mt-1 z-10 relative">{data.player.team} • {data.market}</p>

                <div className="mt-4 inline-flex items-baseline gap-2 bg-slate-900/50 backdrop-blur-md px-6 py-2 rounded-2xl border border-white/10 z-10 relative">
                    <span className="text-sm font-medium text-slate-400">Line</span>
                    <span className="text-3xl font-black text-white text-glow">{data.line}</span>
                </div>
            </section>

            {/* Main Content */}
            <div className="px-4 space-y-4 mt-2">

                {/* Matchup & AI Grades */}
                <div className="grid grid-cols-2 gap-3">
                    <div className="glass-panel p-4 flex flex-col items-center justify-center relative overflow-hidden">
                        <div className="absolute -left-10 -bottom-10 w-24 h-24 bg-emerald-500/20 rounded-full blur-2xl"></div>
                        <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1 z-10">Matchup</span>
                        <span className="text-4xl font-black text-emerald-400 text-glow-over z-10">{data.matchup_grade.grade}</span>
                    </div>

                    <div className="glass-panel p-4 flex flex-col items-center justify-center relative overflow-hidden">
                        <div className="absolute -right-10 -bottom-10 w-24 h-24 bg-nba-primary/20 rounded-full blur-2xl"></div>
                        <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1 z-10">AI Hit Prob</span>
                        <span className="text-3xl font-bold text-white z-10">{data.prediction.hit_probability}%</span>
                    </div>
                </div>

                {/* Charts & L5 */}
                <div className="glass-panel p-4">
                    <div className="flex justify-between items-center mb-2">
                        <h2 className="font-bold text-white">Last 5 Games</h2>
                        <span className="bg-nba-over/20 text-nba-over font-bold px-2 py-0.5 rounded text-sm">
                            {data.hitRates.l5.hit_rate}% Hit
                        </span>
                    </div>

                    {/* Recharts Bar Chart Component */}
                    <PlayerChart
                        data={data.hitRates.l5.history.slice().reverse()}
                        line={data.line}
                        market={data.market}
                    />
                </div>

                {/* Split Stats */}
                <div className="glass-panel p-4 pb-5">
                    <h2 className="font-bold text-white mb-4">Stat Splits</h2>
                    <div className="space-y-3">
                        <div className="flex justify-between items-center border-b border-white/5 pb-2">
                            <span className="text-slate-400 font-medium">Home Avg</span>
                            <span className={cn("font-bold text-lg", data.splits.home_avg > data.line ? "text-nba-over text-glow-over" : "text-white")}>
                                {data.splits.home_avg}
                            </span>
                        </div>
                        <div className="flex justify-between items-center border-b border-white/5 pb-2">
                            <span className="text-slate-400 font-medium">Away Avg</span>
                            <span className={cn("font-bold text-lg", data.splits.away_avg > data.line ? "text-nba-over text-glow-over" : "text-white")}>
                                {data.splits.away_avg}
                            </span>
                        </div>
                        <div className="flex justify-between items-center pb-1">
                            <span className="text-slate-400 font-medium flex items-center gap-1">
                                Head-to-Head <ShieldAlert className="w-3.5 h-3.5" />
                            </span>
                            <span className={cn("font-bold text-lg", data.splits.h2h_avg > data.line ? "text-nba-over text-glow-over" : "text-white")}>
                                {data.splits.h2h_avg}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Floating Action Bar */}
            <div className="fixed bottom-0 left-0 right-0 p-4 max-w-md mx-auto z-50">
                <div className="glass-panel p-2 flex gap-2">
                    <button className="flex-1 bg-nba-over hover:bg-emerald-600 transition-colors text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(16,185,129,0.4)]">
                        Pick OVER
                    </button>
                    <button className="flex-1 bg-nba-under hover:bg-rose-600 transition-colors text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(244,63,94,0.4)]">
                        Pick UNDER
                    </button>
                </div>
            </div>

        </div>
    );
}
