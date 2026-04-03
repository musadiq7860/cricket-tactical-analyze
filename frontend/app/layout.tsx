import type { Metadata } from "next";
import "./globals.css";
import Header from "./components/Header";

export const metadata: Metadata = {
  title: "CricketAI — Real-Time Tactical Match Analyzer",
  description:
    "AI-powered real-time cricket match analysis with tactical insights, live scoring, and match momentum visualization. Powered by LLaMA 3.3 70B.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main style={{ position: "relative", zIndex: 1, minHeight: "calc(100vh - 60px)" }}>
          {children}
        </main>
      </body>
    </html>
  );
}
