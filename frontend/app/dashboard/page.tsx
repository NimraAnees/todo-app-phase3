'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import {
  Calendar,
  CheckCircle,
  Circle,
  BarChart3,
  TrendingUp,
  Clock
} from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();
  const { tasks, loading } = useTasks();
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    pending: 0,
    today: 0
  });

  useEffect(() => {
    if (tasks) {
      const completed = tasks.filter(task => task.status === 'completed').length;
      const pending = tasks.length - completed;
      const today = tasks.filter(task => {
        const todayDate = new Date().toISOString().split('T')[0];
        return task.created_at.startsWith(todayDate);
      }).length;

      setStats({
        total: tasks.length,
        completed,
        pending,
        today
      });
    }
  }, [tasks]);

  const statsCards = [
    {
      title: 'Total Tasks',
      value: stats.total,
      icon: BarChart3,
      color: 'from-emerald-500 to-emerald-600',
      change: '+12% from last week'
    },
    {
      title: 'Completed',
      value: stats.completed,
      icon: CheckCircle,
      color: 'from-emerald-400 to-emerald-500',
      change: '+8% from last week'
    },
    {
      title: 'Pending',
      value: stats.pending,
      icon: Clock,
      color: 'from-amber-500 to-amber-600',
      change: '-3% from last week'
    },
    {
      title: 'Today\'s Tasks',
      value: stats.today,
      icon: Calendar,
      color: 'from-amber-400 to-amber-500',
      change: '+5 from yesterday'
    }
  ];

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-onyx-900">
        <p className="text-onyx-300">Please sign in to view dashboard</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 bg-onyx-900 min-h-screen">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-8"
      >
        <h1 className="text-3xl md:text-4xl font-bold text-onyx-50 mb-2">
          Welcome back, {user.email.split('@')[0]}!
        </h1>
        <p className="text-onyx-300">
          Here's what's happening with your tasks today.
        </p>
      </motion.div>

      {/* Stats Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
          >
            <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300">
              <div className={`h-2 bg-gradient-to-r ${stat.color}`} />
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-onyx-400">
                  {stat.title}
                </CardTitle>
                <div className={`p-2 rounded-full bg-gradient-to-r ${stat.color}`}>
                  <stat.icon className="w-4 h-4 text-black" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-onyx-50">
                  {stat.value}
                </div>
                <p className="text-xs text-onyx-400 mt-1">
                  {stat.change}
                </p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-onyx-50">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <span>Recent Activity</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {loading ? (
                <div className="text-center py-8">
                  <p className="text-onyx-300">Loading your tasks...</p>
                </div>
              ) : tasks && tasks.length > 0 ? (
                tasks.slice(0, 5).map((task, index) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5 + index * 0.1, duration: 0.3 }}
                    className="flex items-center justify-between p-3 bg-onyx-700 rounded-lg"
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`p-1 rounded-full ${
                        task.status === 'completed'
                          ? 'bg-emerald-900/30'
                          : 'bg-amber-900/30'
                      }`}>
                        {task.status === 'completed' ? (
                          <CheckCircle className="w-4 h-4 text-emerald-400" />
                        ) : (
                          <Circle className="w-4 h-4 text-amber-400" />
                        )}
                      </div>
                      <div>
                        <p className="font-medium text-onyx-50">{task.title}</p>
                        <p className="text-sm text-onyx-400">
                          {new Date(task.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      task.status === 'completed'
                        ? 'bg-emerald-900/30 text-emerald-400'
                        : 'bg-amber-900/30 text-amber-400'
                    }`}>
                      {task.status === 'completed' ? 'Completed' : 'Pending'}
                    </span>
                  </motion.div>
                ))
              ) : (
                <div className="text-center py-8">
                  <p className="text-onyx-300">No tasks yet. Start by creating your first task!</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}