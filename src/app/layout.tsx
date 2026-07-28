import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Woods Career Intelligence — Application & Ranking Command Center',
  description: 'Vercel-deployable interactive GUI dashboard for ranking job opportunities, analyzing PBS evidence fit scores, and tracking application lifecycles.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen text-slate-100 selection:bg-sky-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
