'use client';

import Link from 'next/link';
import { Match } from '../lib/api';
import styles from './MatchCard.module.css';

interface MatchCardProps {
  match: Match;
  index: number;
}

export default function MatchCard({ match, index }: MatchCardProps) {
  const isLive = match.status?.toLowerCase().includes('live');
  const isComplete = match.status?.toLowerCase().includes('complete') || match.status?.toLowerCase().includes('stumps');
  const formatBadgeClass =
    match.matchType === 'T20' ? 'badge-t20' :
    match.matchType === 'ODI' ? 'badge-odi' :
    match.matchType === 'Test' ? 'badge-test' : 'badge-t20';

  const team1 = match.tpiTeam1?.shortname || match.teams?.[0]?.substring(0, 3).toUpperCase() || 'TM1';
  const team2 = match.tpiTeam2?.shortname || match.teams?.[1]?.substring(0, 3).toUpperCase() || 'TM2';

  return (
    <Link
      href={`/match/${match.id}`}
      className={`${styles.card} glass-panel glass-panel-hover`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <div className={styles.cardHeader}>
        <div className={styles.badges}>
          {isLive && <span className="badge badge-live">Live</span>}
          {isComplete && <span className="badge badge-complete">Complete</span>}
          <span className={`badge ${formatBadgeClass}`}>{match.matchType}</span>
        </div>
      </div>

      <div className={styles.teams}>
        <div className={styles.team}>
          <div className={styles.teamAbbr}>{team1}</div>
          <div className={styles.teamName}>{match.teams?.[0] || 'Team 1'}</div>
          {match.score?.[0] && (
            <div className={styles.score}>
              <span className={styles.runs}>{match.score[0].r}/{match.score[0].w}</span>
              <span className={styles.overs}>({match.score[0].o} ov)</span>
            </div>
          )}
        </div>

        <div className={styles.vs}>
          <div className={styles.vsCircle}>VS</div>
        </div>

        <div className={styles.team}>
          <div className={styles.teamAbbr}>{team2}</div>
          <div className={styles.teamName}>{match.teams?.[1] || 'Team 2'}</div>
          {match.score?.[1] && (
            <div className={styles.score}>
              <span className={styles.runs}>{match.score[1].r}/{match.score[1].w}</span>
              <span className={styles.overs}>({match.score[1].o} ov)</span>
            </div>
          )}
        </div>
      </div>

      <div className={styles.cardFooter}>
        <div className={styles.venue}>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <span>{match.venue}</span>
        </div>
        <div className={styles.analyzeBtn}>
          Analyze
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </div>
      </div>

      {isLive && <div className={styles.liveGlow} />}
    </Link>
  );
}
