'use client';

import { useEffect, useRef } from 'react';
import { Insight } from '../hooks/useSSE';
import styles from './InsightsPanel.module.css';

interface InsightsPanelProps {
  insights: Insight[];
  currentStreamingInsight: string;
  isConnected: boolean;
}

export default function InsightsPanel({
  insights,
  currentStreamingInsight,
  isConnected,
}: InsightsPanelProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [insights, currentStreamingInsight]);

  const getInsightIcon = (text: string) => {
    if (text.startsWith('🎯')) return '🎯';
    if (text.startsWith('📊')) return '📊';
    if (text.startsWith('🏏')) return '🏏';
    if (text.startsWith('🔄')) return '🔄';
    if (text.startsWith('⚡')) return '⚡';
    if (text.startsWith('📈')) return '📈';
    if (text.startsWith('🏆')) return '🏆';
    if (text.startsWith('🌡️')) return '🌡️';
    if (text.startsWith('⚔️')) return '⚔️';
    if (text.startsWith('⚠️')) return '⚠️';
    return '💡';
  };

  const getInsightCategory = (text: string) => {
    if (text.includes('Bowling Pattern') || text.includes('bowling')) return 'Bowling';
    if (text.includes('Scoring') || text.includes('Batting') || text.includes('batting')) return 'Batting';
    if (text.includes('Field') || text.includes('field')) return 'Field';
    if (text.includes('Momentum') || text.includes('momentum')) return 'Momentum';
    if (text.includes('Partnership') || text.includes('partnership')) return 'Partnership';
    if (text.includes('Tactical') || text.includes('tactical')) return 'Tactical';
    if (text.includes('Wicket') || text.includes('wicket')) return 'Wicket';
    return 'Analysis';
  };

  const getCategoryClass = (category: string) => {
    switch (category) {
      case 'Bowling': return styles.catBowling;
      case 'Batting': return styles.catBatting;
      case 'Field': return styles.catField;
      case 'Momentum': return styles.catMomentum;
      case 'Wicket': return styles.catWicket;
      default: return styles.catDefault;
    }
  };

  return (
    <div className={`${styles.panel} glass-panel`}>
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <h2 className={styles.title}>AI Tactical Insights</h2>
          <span className={styles.poweredBy}>Powered by LLaMA 3.3 70B</span>
        </div>
        <div className={`${styles.connectionStatus} ${isConnected ? styles.connected : styles.disconnected}`}>
          <div className={styles.connDot} />
          <span>{isConnected ? 'Streaming' : 'Offline'}</span>
        </div>
      </div>

      <div className={styles.insightsList} ref={scrollRef}>
        {insights.length === 0 && !currentStreamingInsight && (
          <div className={styles.emptyState}>
            <div className={styles.emptyIcon}>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M12 2a10 10 0 100 20 10 10 0 000-20zM12 6v6l4 2"/>
              </svg>
            </div>
            <p className={styles.emptyTitle}>Waiting for match data</p>
            <p className={styles.emptyDesc}>
              AI insights will appear here as the match progresses.
              Analysis is generated every 3 deliveries.
            </p>
          </div>
        )}

        {insights.map((insight, index) => {
          const icon = getInsightIcon(insight.text);
          const category = getInsightCategory(insight.text);
          const categoryClass = getCategoryClass(category);
          // Remove leading emoji from text for cleaner display
          const cleanText = insight.text.replace(/^[\p{Emoji}\u200d\ufe0f]+\s*/u, '');

          return (
            <div
              key={insight.id}
              className={styles.insightCard}
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <div className={styles.insightHeader}>
                <div className={styles.insightMeta}>
                  <span className={styles.insightIcon}>{icon}</span>
                  <span className={`${styles.insightCategory} ${categoryClass}`}>{category}</span>
                </div>
                <span className={styles.insightOver}>
                  Over {insight.over}.{insight.ball}
                </span>
              </div>
              <div className={styles.insightBody}>
                <p className={styles.insightText}>{cleanText}</p>
              </div>
            </div>
          );
        })}

        {/* Currently streaming insight */}
        {currentStreamingInsight && (
          <div className={`${styles.insightCard} ${styles.streaming}`}>
            <div className={styles.insightHeader}>
              <div className={styles.insightMeta}>
                <span className={styles.insightIcon}>{getInsightIcon(currentStreamingInsight)}</span>
                <span className={`${styles.insightCategory} ${styles.catDefault}`}>
                  {getInsightCategory(currentStreamingInsight)}
                </span>
              </div>
              <div className={styles.streamingIndicator}>
                <span className={styles.streamDot} />
                <span className={styles.streamDot} />
                <span className={styles.streamDot} />
              </div>
            </div>
            <div className={styles.insightBody}>
              <p className={styles.insightText}>
                {currentStreamingInsight.replace(/^[\p{Emoji}\u200d\ufe0f]+\s*/u, '')}
                <span className={styles.cursor}>|</span>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
