"use client";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceLine,
    Cell
} from 'recharts';

interface GameStat {
    game_id: string | number;
    date: string;
    opponent: string;
    value: number;
    is_hit: boolean;
}

interface PlayerChartProps {
    data: GameStat[];
    line: number;
    market: string;
}

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;
        return (
            <div className="glass-panel p-3 text-sm">
                <p className="font-bold text-white mb-1">{data.date} vs {data.opponent}</p>
                <p className="text-slate-300">
                    Result: <span className={`font-bold ${data.is_hit ? 'text-nba-over' : 'text-nba-under'}`}>{data.value}</span>
                </p>
            </div>
        );
    }
    return null;
};

export default function PlayerChart({ data, line, market }: PlayerChartProps) {
    // Recharts needs an array of objects
    return (
        <div className="w-full h-[250px] mt-4">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    data={data}
                    margin={{ top: 20, right: 0, left: -25, bottom: 0 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                    <XAxis
                        dataKey="opponent"
                        tick={{ fill: '#94a3b8', fontSize: 10 }}
                        axisLine={false}
                        tickLine={false}
                    />
                    <YAxis
                        tick={{ fill: '#94a3b8', fontSize: 10 }}
                        axisLine={false}
                        tickLine={false}
                    />
                    <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />

                    <ReferenceLine y={line} stroke="#38bdf8" strokeDasharray="3 3" strokeWidth={2}>
                        {/* <Label value={`Line: ${line}`} position="insideTopLeft" fill="#38bdf8" fontSize={10} /> */}
                    </ReferenceLine>

                    <Bar dataKey="value" radius={[4, 4, 0, 0]} maxBarSize={40}>
                        {data.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={entry.is_hit ? '#10b981' : '#f43f5e'}
                                className="transition-all duration-300 hover:opacity-80"
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
