import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/components/providers/AuthProvider';
import { Navbar } from '@/components/layout/Navbar';
import { Providers } from './providers';
import LayoutWrapper from '@/components/LayoutWrapper';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Onyx Todo App',
  description: 'A premium todo application with black-touch UI',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.className} bg-onyx-900 text-onyx-50`}>
        <Providers>
          <AuthProvider>
            <div className="min-h-screen bg-onyx-900">
              <LayoutWrapper>
                <Navbar />
                <main className="container mx-auto px-4 py-8">
                  {children}
                </main>
              </LayoutWrapper>
            </div>
          </AuthProvider>
        </Providers>
      </body>
    </html>
  );
}
