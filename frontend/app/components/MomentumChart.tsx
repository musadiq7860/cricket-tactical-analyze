'use client';

import { useMemo } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceDot,
  Legend,
} from 'recharts';
import { OverData } from '../lib/api';
import styles from './MomentumChart.module.css';

interface MomentumChartProps {
  overs: OverData[];
}

interface ChartDataPoint {
  over: string;
  runs: number;
  totalRuns: number;
  runRate: number;
  wicket: boolean;
}

/* eslint-disable @typescript-eslint/no-explicit-any */

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload as ChartDataPoint;
    return (
      <div className={styles.tooltip}>
        <div className={styles.tooltipHeader}>Over {data.over}</div>
        <div className={styles.tooltipRow}>
          <span className={styles.tooltipLabel}>Runs in over</span>
          <span className={styles.tooltipValue}>{data.runs}</span>
        </div>
        <div className={styles.tooltipRow}>
          <span className={styles.tooltipLabel}>Total</span>
          <span className={styles.tooltipValueTotal}>{data.totalRuns}</span>
        </div>
        <div className={styles.tooltipRow}>
          <span className={styles.tooltipLabel}>Run Rate</span>
          <span className={styles.tooltipValueRR}>{data.runRate}</span>
        </div>
        {data.wicket && (
          <div className={styles.tooltipWicket}>⚡ Wicket fell</div>
        )}
      </div>
    );
  }
  return null;
};

export default function MomentumChart({ overs }: MomentumChartProps) {
  const chartData: ChartDataPoint[] = useMemo(() => {
    return overs.map(o => ({
      over: `${o.over + 1}`,
      runs: o.runs,
      totalRuns: o.total_runs,
      runRate: o.run_rate,
      wicket: o.wicket_in_over,
    }));
  }, [overs]);

  const wicketOvers = chartData.filter(d => d.wicket);
  const maxRuns = Math.max(...chartData.map(d => d.runs), 12);

  return (
    <div className={`${styles.chart} glass-panel`}>
      <div className={styles.header}>
        <h2 className={styles.title}>Match Momentum</h2>
        <div className={styles.legend}>
          <div className={styles.legendItem}>
            <div className={`${styles.legendDot} ${styles.dotRuns}`} />
            <span>Runs/Over</span>
          </div>
          <div className={styles.legendItem}>
            <div className={`${styles.legendDot} ${styles.dotWicket}`} />
            <span>Wicket</span>
          </div>
        </div>
      </div>

      <div className={styles.chartContainer}>
        {chartData.length === 0 ? (
          <div className={styles.emptyState}>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" opacity="0.3">
              <path d="M3 3v18h18" />
              <path d="M7 16l4-8 4 4 4-8" />
            </svg>
            <p>Chart updates after each over</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="runsGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#06d6a0" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#06d6a0" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="rrGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#38bdf8" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#38bdf8" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="rgba(148,163,184,0.06)"
                vertical={false}
              />
              <XAxis
                dataKey="over"
                tick={{ fill: '#64748b', fontSize: 11, fontFamily: 'JetBrains Mono' }}
                axisLine={{ stroke: 'rgba(148,163,184,0.1)' }}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#64748b', fontSize: 11, fontFamily: 'JetBrains Mono' }}
                axisLine={false}
                tickLine={false}
                domain={[0, maxRuns + 4]}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="runs"
                stroke="#06d6a0"
                strokeWidth={2.5}
                fill="url(#runsGradient)"
                dot={{ r: 3, fill: '#06d6a0', stroke: '#060a13', strokeWidth: 2 }}
                activeDot={{ r: 5, fill: '#06d6a0', stroke: '#060a13', strokeWidth: 2, filter: 'url(#glow)' }}
              />
              {/* Wicket markers */}
              {wicketOvers.map((w, i) => (
                <ReferenceDot
                  key={i}
                  x={w.over}
                  y={w.runs}
                  r={8}
                  fill="#ef476f"
                  stroke="#060a13"
                  strokeWidth={2}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Stats Row */}
      {chartData.length > 0 && (
        <div className={styles.statsRow}>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Highest Over</span>
            <span className={styles.statValue}>
              {Math.max(...chartData.map(d => d.runs))}
            </span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Lowest Over</span>
            <span className={styles.statValue}>
              {Math.min(...chartData.map(d => d.runs))}
            </span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Current RR</span>
            <span className={`${styles.statValue} ${styles.statCyan}`}>
              {chartData[chartData.length - 1]?.runRate || '0.00'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
