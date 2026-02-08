'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import { LogOut, User, Plus, Home, BarChart3, Menu, X } from 'lucide-react';
import { useState } from 'react';

export const Navbar = () => {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navLinks = [
    { href: '/', label: 'Home', icon: Home },
    { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { href: '/tasks', label: 'Tasks', icon: Plus },
  ];

  return (
    <nav className="bg-onyx-800/80 backdrop-blur-md border-b border-onyx-600 sticky top-0 z-50 shadow-black-touch">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-2">
            <motion.div
              whileHover={{ scale: 1.05, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
              className="text-2xl font-bold bg-gradient-to-r from-emerald-400 via-emerald-300 to-amber-400 bg-clip-text text-transparent"
            >
              Todo App
            </motion.div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link key={link.href} href={link.href}>
                  <motion.div
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-emerald-500/20 to-amber-500/20 text-emerald-400 shadow-emerald-glow'
                        : 'hover:bg-onyx-700/50 text-onyx-300 hover:text-emerald-400'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      <motion.div
                        animate={isActive ? { rotate: 360 } : {}}
                        transition={{ duration: 0.5, ease: "easeInOut" }}
                        className="w-4 h-4"
                      >
                        <link.icon className="w-full h-full" />
                      </motion.div>
                      <span className="font-medium">{link.label}</span>
                    </div>
                  </motion.div>
                </Link>
              );
            })}
          </div>

          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <div className="hidden md:flex items-center space-x-3">
                  <div className="flex items-center space-x-2 bg-onyx-700/50 px-3 py-1.5 rounded-full border border-onyx-600">
                    <User className="w-4 h-4 text-emerald-400" />
                    <span className="text-sm text-onyx-300">
                      {user.email.split('@')[0]}
                    </span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={logout}
                    className="flex items-center space-x-2 text-onyx-300 hover:text-rose-400 hover:bg-onyx-700/50"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Sign Out</span>
                  </Button>
                </div>

                {/* Mobile Menu Button */}
                <button
                  onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                  className="md:hidden text-onyx-300 hover:text-emerald-400 transition-colors"
                >
                  {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                </button>
              </>
            ) : (
              <div className="hidden md:flex space-x-2">
                <Link href="/auth/login">
                  <Button variant="outline" size="sm" className="text-onyx-300 border-onyx-600 hover:bg-onyx-700 hover:text-emerald-400 transition-all duration-300">
                    Sign In
                  </Button>
                </Link>
                <Link href="/auth/signup">
                  <Button size="sm" className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-black hover:from-emerald-400 hover:to-emerald-500 shadow-emerald-glow hover:shadow-lg transition-all duration-300">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="absolute top-16 left-0 right-0 bg-onyx-800/95 backdrop-blur-md border-b border-onyx-600 md:hidden py-4 px-4"
              >
                <div className="flex flex-col space-y-3">
                  {navLinks.map((link) => {
                    const isActive = pathname === link.href;
                    return (
                      <Link key={link.href} href={link.href} onClick={() => setIsMobileMenuOpen(false)}>
                        <div className={`px-4 py-3 rounded-lg transition-colors ${
                          isActive
                            ? 'bg-gradient-to-r from-emerald-500/20 to-amber-500/20 text-emerald-400'
                            : 'hover:bg-onyx-700 text-onyx-300'
                        }`}>
                          <div className="flex items-center space-x-3">
                            <link.icon className="w-5 h-5" />
                            <span className="font-medium">{link.label}</span>
                          </div>
                        </div>
                      </Link>
                    );
                  })}

                  {!user && (
                    <div className="flex flex-col space-y-2 pt-2">
                      <Link href="/auth/login" onClick={() => setIsMobileMenuOpen(false)}>
                        <Button variant="outline" className="w-full text-onyx-300 border-onyx-600 hover:bg-onyx-700 hover:text-emerald-400">
                          Sign In
                        </Button>
                      </Link>
                      <Link href="/auth/signup" onClick={() => setIsMobileMenuOpen(false)}>
                        <Button className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 text-black hover:from-emerald-400 hover:to-emerald-500">
                          Sign Up
                        </Button>
                      </Link>
                    </div>
                  )}

                  {user && (
                    <div className="pt-2">
                      <div className="flex items-center space-x-3 bg-onyx-700/50 px-3 py-2 rounded-lg border border-onyx-600 mb-2">
                        <User className="w-4 h-4 text-emerald-400" />
                        <span className="text-sm text-onyx-300">
                          {user.email.split('@')[0]}
                        </span>
                      </div>
                      <Button
                        variant="outline"
                        className="w-full text-onyx-300 border-onyx-600 hover:bg-onyx-700 hover:text-rose-400"
                        onClick={logout}
                      >
                        <LogOut className="w-4 h-4 mr-2" />
                        Sign Out
                      </Button>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};