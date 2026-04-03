'use client';

import { useEffect, useState } from 'react';
import { fetchMatches, Match } from './lib/api';
import MatchCard from './components/MatchCard';
import styles from './page.module.css';

export default function HomePage() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchMatches();
        setMatches(data);
      } catch {
        setError(true);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className={styles.page}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <div className={styles.herobadge}>
            <span className={styles.heroBadgeDot} />
            AI-Powered Cricket Analysis
          </div>
          <h1 className={styles.heroTitle}>
            Real-Time <span className="text-gradient">Tactical</span> Cricket
            <br />Match Analyzer
          </h1>
          <p className={styles.heroDesc}>
            Live ball-by-ball tactical insights powered by LLaMA 3.3 70B. Watch AI decode bowling
            patterns, batting pressure points, and field placement strategies in real-time.
          </p>
          <div className={styles.heroStats}>
            <div className={styles.heroStat}>
              <span className={styles.heroStatValue}>{'<1s'}</span>
              <span className={styles.heroStatLabel}>Insight Latency</span>
            </div>
            <div className={styles.heroStatDivider} />
            <div className={styles.heroStat}>
              <span className={styles.heroStatValue}>70B</span>
              <span className={styles.heroStatLabel}>Parameter Model</span>
            </div>
            <div className={styles.heroStatDivider} />
            <div className={styles.heroStat}>
              <span className={styles.heroStatValue}>Live</span>
              <span className={styles.heroStatLabel}>SSE Streaming</span>
            </div>
          </div>
        </div>

        {/* Decorative elements */}
        <div className={styles.heroGlow} />
        <div className={styles.heroOrb1} />
        <div className={styles.heroOrb2} />
      </section>

      {/* Matches Grid */}
      <section className={styles.matchesSection}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Available Matches</h2>
          <p className={styles.sectionDesc}>
            Select a match to start real-time tactical analysis
          </p>
        </div>

        {loading && (
          <div className={styles.matchesGrid}>
            {[1, 2, 3, 4].map(i => (
              <div key={i} className={`${styles.skeletonCard} glass-panel`}>
                <div className={`skeleton ${styles.skLine1}`} />
                <div className={`skeleton ${styles.skLine2}`} />
                <div className={`skeleton ${styles.skLine3}`} />
                <div className={`skeleton ${styles.skLine4}`} />
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className={styles.errorState}>
            <p>⚠️ Could not connect to the backend. Make sure FastAPI is running on port 8000.</p>
          </div>
        )}

        {!loading && !error && (
          <div className={styles.matchesGrid}>
            {matches.map((match, i) => (
              <MatchCard key={match.id} match={match} index={i} />
            ))}
          </div>
        )}
      </section>

      {/* Features Section */}
      <section className={styles.features}>
        <div className={styles.featureGrid}>
          <div className={`${styles.featureCard} glass-panel`}>
            <div className={`${styles.featureIcon} ${styles.featureIconCyan}`}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
            </div>
            <h3 className={styles.featureName}>Real-Time Streaming</h3>
            <p className={styles.featureDesc}>
              Ball-by-ball updates and AI insights stream via SSE — no page refresh needed.
            </p>
          </div>
          <div className={`${styles.featureCard} glass-panel`}>
            <div className={`${styles.featureIcon} ${styles.featureIconAmber}`}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
            </div>
            <h3 className={styles.featureName}>AI Tactical Insights</h3>
            <p className={styles.featureDesc}>
              LLaMA 3.3 70B analyzes patterns every 3 balls — bowling, batting, field placement.
            </p>
          </div>
          <div className={`${styles.featureCard} glass-panel`}>
            <div className={`${styles.featureIcon} ${styles.featureIconPurple}`}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 3v18h18"/>
                <path d="M7 16l4-8 4 4 4-8"/>
              </svg>
            </div>
            <h3 className={styles.featureName}>Momentum Charts</h3>
            <p className={styles.featureDesc}>
              Visual run-rate trends, wicket markers, and scoring momentum updated every over.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
