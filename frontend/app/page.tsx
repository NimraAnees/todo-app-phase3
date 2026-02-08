'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';

export default function HomePage() {
  const { user } = useAuth();

  return (
    <main className="min-h-screen bg-onyx-900">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center min-h-screen px-4 py-12 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl mx-auto text-center space-y-8"
        >
          {/* App Name - Large, Bold, Responsive */}
          <motion.h1
            className="text-4xl font-extrabold tracking-tight text-onyx-50 sm:text-5xl md:text-6xl"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            <span className="block bg-gradient-to-r from-emerald-400 via-emerald-300 to-amber-400 bg-clip-text text-transparent">
              Todo App
            </span>
            <span className="block text-onyx-300 text-3xl sm:text-4xl md:text-5xl mt-2">
              Streamline Your Productivity
            </span>
          </motion.h1>

          {/* Tagline - Clear Value Proposition */}
          <motion.p
            className="max-w-xl mx-auto text-lg text-onyx-300 sm:text-xl md:text-2xl"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            Organize your tasks. Boost your productivity.
            <span className="block mt-2">A sophisticated and elegant way to manage your daily tasks.</span>
          </motion.p>

          {/* CTA Buttons - Primary & Secondary */}
          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center mt-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            {user ? (
              <Link href="/tasks">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-black bg-gradient-to-r from-emerald-500 to-emerald-600 border border-transparent rounded-lg shadow-emerald-glow hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 min-h-[44px] min-w-[160px] transition-all"
                >
                  Go to Dashboard
                </motion.button>
              </Link>
            ) : (
              <>
                <Link href="/auth/signup">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-black bg-gradient-to-r from-emerald-500 to-emerald-600 border border-transparent rounded-lg shadow-emerald-glow hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 min-h-[44px] min-w-[160px] transition-all"
                  >
                    Get Started Free
                  </motion.button>
                </Link>

                <Link href="/auth/login">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-onyx-300 bg-onyx-800 border-2 border-onyx-600 rounded-lg shadow-sm hover:bg-onyx-700 hover:border-onyx-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 min-h-[44px] min-w-[160px] transition-all"
                  >
                    Sign In
                  </motion.button>
                </Link>
              </>
            )}
          </motion.div>

          {/* Feature Highlights */}
          <motion.div
            className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-16 pt-8 border-t border-onyx-700"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.8 }}
          >
            {[
              { emoji: '✨', title: 'Premium', desc: 'Sophisticated black-touch design' },
              { emoji: '🔒', title: 'Secure', desc: 'Your data is private and protected' },
              { emoji: '📱', title: 'Responsive', desc: 'Works on any device' }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="text-center p-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 + index * 0.1, duration: 0.5 }}
                whileHover={{ y: -5 }}
              >
                <div className="text-4xl mb-3">{feature.emoji}</div>
                <h3 className="font-semibold text-onyx-50 text-lg">{feature.title}</h3>
                <p className="text-onyx-400 text-sm mt-1">{feature.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </section>
    </main>
  );
}
