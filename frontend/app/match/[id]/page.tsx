'use client';

import { useParams } from 'next/navigation';
import { useSSE } from '../../hooks/useSSE';
import ScoreCard from '../../components/ScoreCard';
import InsightsPanel from '../../components/InsightsPanel';
import MomentumChart from '../../components/MomentumChart';
import styles from './page.module.css';
import { useEffect, useState } from 'react';
import { fetchMatchDetail, Match } from '../../lib/api';

export default function MatchPage() {
  const params = useParams();
  const matchId = params.id as string;
  const [matchDetail, setMatchDetail] = useState<Match | null>(null);
  
  const {
    isConnected,
    matchState,
    balls,
    overs,
    insights,
    currentStreamingInsight,
    isMatchEnd,
  } = useSSE(matchId);

  useEffect(() => {
    async function loadDetail() {
      const detail = await fetchMatchDetail(matchId);
      setMatchDetail(detail);
    }
    loadDetail();
  }, [matchId]);

  const matchName = matchDetail?.name || `Match ${matchId}`;
  const matchFormat = matchDetail?.matchType || 'T20';

  return (
    <div className={styles.page}>
      {/* Match Header Bar */}
      <div className={styles.matchBar}>
        <div className={styles.matchBarLeft}>
          <a href="/" className={styles.backButton}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            <span>Back</span>
          </a>
          <h1 className={styles.matchName}>{matchName}</h1>
          <div className={styles.matchMeta}>
            <span className={`badge badge-${matchFormat.toLowerCase() === 't20' ? 't20' : matchFormat.toLowerCase() === 'odi' ? 'odi' : 'test'}`}>
              {matchFormat}
            </span>
            {isConnected && <span className="badge badge-live">Live Analysis</span>}
            {isMatchEnd && <span className="badge badge-complete">Analysis Complete</span>}
          </div>
        </div>
        <div className={styles.matchBarRight}>
          {matchDetail?.venue && (
            <span className={styles.venue}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              {matchDetail.venue}
            </span>
          )}
        </div>
      </div>

      {/* Three-Panel Layout */}
      <div className={styles.panelGrid}>
        <div className={`${styles.panel} ${styles.panelLeft} animate-slide-left`}>
          <ScoreCard
            matchState={matchState}
            balls={balls}
            matchName={matchName}
            matchFormat={matchFormat}
          />
        </div>

        <div className={`${styles.panel} ${styles.panelCenter} animate-fade-in-up`}>
          <InsightsPanel
            insights={insights}
            currentStreamingInsight={currentStreamingInsight}
            isConnected={isConnected}
          />
        </div>

        <div className={`${styles.panel} ${styles.panelRight} animate-slide-right`}>
          <MomentumChart overs={overs} />
        </div>
      </div>
    </div>
  );
}
