'use client';

import Link from 'next/link';
import styles from './Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <Link href="/" className={styles.brand}>
          <div className={styles.logo}>
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="14" cy="14" r="12" stroke="url(#grad)" strokeWidth="2" fill="none"/>
              <path d="M10 8L18 14L10 20V8Z" fill="url(#grad)"/>
              <defs>
                <linearGradient id="grad" x1="0" y1="0" x2="28" y2="28">
                  <stop offset="0%" stopColor="#06d6a0"/>
                  <stop offset="100%" stopColor="#38bdf8"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div className={styles.brandText}>
            <span className={styles.brandName}>CricketAI</span>
            <span className={styles.brandSub}>Tactical Analyzer</span>
          </div>
        </Link>
        <nav className={styles.nav}>
          <div className={styles.statusDot} />
          <span className={styles.statusText}>System Online</span>
        </nav>
      </div>
    </header>
  );
}
