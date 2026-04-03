'use client';

import { MatchState, BallData } from '../lib/api';
import styles from './ScoreCard.module.css';

interface ScoreCardProps {
  matchState: MatchState | null;
  balls: BallData[];
  matchName: string;
  matchFormat: string;
}

export default function ScoreCard({ matchState, balls, matchName, matchFormat }: ScoreCardProps) {
  const lastBalls = balls.slice(-12);
  const battingTeam = balls.length > 0 ? balls[balls.length - 1]?.batting_team : '';
  const bowlingTeam = balls.length > 0 ? balls[balls.length - 1]?.bowling_team : '';

  const formatBadgeClass =
    matchFormat === 'T20' ? 'badge-t20' :
    matchFormat === 'ODI' ? 'badge-odi' : 'badge-test';

  return (
    <div className={`${styles.scorecard} glass-panel`}>
      <div className={styles.header}>
        <h2 className={styles.title}>Live Scorecard</h2>
        <span className={`badge ${formatBadgeClass}`}>{matchFormat}</span>
      </div>

      {!matchState ? (
        <div className={styles.waiting}>
          <div className={styles.spinner} />
          <p>Waiting for match data...</p>
        </div>
      ) : (
        <>
          {/* Main Score */}
          <div className={styles.mainScore}>
            <div className={styles.teamBatting}>
              <span className={styles.teamLabel}>{battingTeam}</span>
              <div className={styles.scoreDisplay}>
                <span className={styles.runs}>{matchState.total_runs}</span>
                <span className={styles.separator}>/</span>
                <span className={styles.wickets}>{matchState.total_wickets}</span>
              </div>
              <span className={styles.oversText}>
                ({matchState.current_over}.{matchState.current_ball} ov)
              </span>
            </div>
          </div>

          {/* Run Rates */}
          <div className={styles.rateGrid}>
            <div className={styles.rateStat}>
              <span className={styles.rateLabel}>CRR</span>
              <span className={styles.rateValue}>{matchState.current_rr}</span>
            </div>
            {matchState.required_rr && (
              <div className={styles.rateStat}>
                <span className={styles.rateLabel}>RRR</span>
                <span className={`${styles.rateValue} ${styles.rateRequired}`}>
                  {matchState.required_rr}
                </span>
              </div>
            )}
          </div>

          {/* Current Batsman */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>At the Crease</h3>
            <div className={styles.batsmanRow}>
              <div className={styles.batsmanInfo}>
                <span className={styles.strikerIcon}>🏏</span>
                <span className={styles.batsmanName}>{matchState.striker}</span>
              </div>
              <div className={styles.batsmanStats}>
                <span className={styles.statBig}>{matchState.striker_runs}</span>
                <span className={styles.statSmall}>({matchState.striker_balls})</span>
              </div>
            </div>
          </div>

          {/* Partnership */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Partnership</h3>
            <div className={styles.partnershipBar}>
              <div className={styles.partnershipStats}>
                <span>{matchState.partnership_runs} runs</span>
                <span className={styles.partnershipBalls}>
                  {matchState.partnership_balls} balls
                </span>
              </div>
              <div className={styles.barTrack}>
                <div
                  className={styles.barFill}
                  style={{ width: `${Math.min((matchState.partnership_runs / 50) * 100, 100)}%` }}
                />
              </div>
            </div>
          </div>

          {/* Current Bowler */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Bowling</h3>
            <div className={styles.bowlerRow}>
              <div className={styles.bowlerInfo}>
                <span className={styles.bowlerIcon}>⚡</span>
                <span className={styles.bowlerName}>{matchState.bowler}</span>
              </div>
              <div className={styles.bowlerFigures}>
                {matchState.bowler_figures}
              </div>
            </div>
          </div>

          {/* Recent Deliveries */}
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Recent Deliveries</h3>
            <div className={styles.ballTracker}>
              {lastBalls.map((ball, i) => (
                <div
                  key={i}
                  className={`${styles.ball} ${
                    ball.is_wicket ? styles.ballWicket :
                    ball.runs === 4 ? styles.ballFour :
                    ball.runs === 6 ? styles.ballSix :
                    ball.runs === 0 ? styles.ballDot :
                    styles.ballRun
                  }`}
                >
                  {ball.is_wicket ? 'W' : ball.runs}
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
