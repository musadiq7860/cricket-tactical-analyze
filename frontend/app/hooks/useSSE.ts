'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { MatchState, BallData, OverData, getStreamUrl } from '../lib/api';

export interface Insight {
  id: string;
  over: number;
  ball: number;
  text: string;
  isStreaming: boolean;
}

export interface SSEState {
  isConnected: boolean;
  matchState: MatchState | null;
  balls: BallData[];
  overs: OverData[];
  insights: Insight[];
  sessionId: string | null;
  isMatchEnd: boolean;
  currentStreamingInsight: string;
}

export function useSSE(matchId: string | null) {
  const [state, setState] = useState<SSEState>({
    isConnected: false,
    matchState: null,
    balls: [],
    overs: [],
    insights: [],
    sessionId: null,
    isMatchEnd: false,
    currentStreamingInsight: '',
  });

  const eventSourceRef = useRef<EventSource | null>(null);
  const insightCounterRef = useRef(0);

  const connect = useCallback(() => {
    if (!matchId) return;

    // Close existing connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const url = getStreamUrl(matchId);
    const es = new EventSource(url);
    eventSourceRef.current = es;

    es.onopen = () => {
      setState(prev => ({ ...prev, isConnected: true }));
    };

    es.addEventListener('session_start', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setState(prev => ({ ...prev, sessionId: data.session_id }));
    });

    es.addEventListener('ball', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setState(prev => ({
        ...prev,
        matchState: data.state,
        balls: [...prev.balls, data.ball],
      }));
    });

    es.addEventListener('over_complete', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setState(prev => ({
        ...prev,
        overs: [...prev.overs, data],
      }));
    });

    es.addEventListener('insight_start', () => {
      setState(prev => ({
        ...prev,
        currentStreamingInsight: '',
      }));
    });

    es.addEventListener('insight_chunk', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setState(prev => ({
        ...prev,
        currentStreamingInsight: prev.currentStreamingInsight + data.text,
      }));
    });

    es.addEventListener('insight_complete', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      insightCounterRef.current += 1;
      const newInsight: Insight = {
        id: `insight_${insightCounterRef.current}`,
        over: data.over,
        ball: data.ball,
        text: data.full_text,
        isStreaming: false,
      };
      setState(prev => ({
        ...prev,
        insights: [...prev.insights, newInsight],
        currentStreamingInsight: '',
      }));
    });

    es.addEventListener('match_end', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setState(prev => ({
        ...prev,
        isMatchEnd: true,
        sessionId: data.session_id,
      }));
      es.close();
    });

    es.onerror = () => {
      setState(prev => ({ ...prev, isConnected: false }));
      es.close();
      // Auto-reconnect after 3 seconds
      setTimeout(() => connect(), 3000);
    };
  }, [matchId]);

  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setState(prev => ({ ...prev, isConnected: false }));
  }, []);

  useEffect(() => {
    if (matchId) {
      connect();
    }
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [matchId, connect]);

  return { ...state, connect, disconnect };
}
