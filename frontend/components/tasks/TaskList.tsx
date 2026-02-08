'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import TaskItem from '@/components/tasks/TaskItem';
import TaskForm from '@/components/tasks/TaskForm';
import { useAuth } from '@/hooks/useAuth';
import TasksService from '@/lib/api/tasks';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: string; // "pending" | "in_progress" | "completed"
  user_id?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
}

const TaskList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [isAuthenticated]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await TasksService.getAll();
      if (response.success && response.data) {
        setTasks(response.data);
      } else {
        setError(response.error || 'Failed to fetch tasks');
      }
    } catch (err) {
      setError('An error occurred while fetching tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description?: string) => {
    try {
      const response = await TasksService.create({ title, description });
      if (response.success && response.data) {
        setTasks(prev => [...prev, response.data!]);
      }
    } catch (err) {
      console.error('Error creating task:', err);
    }
  };

  const handleToggleTask = async (id: string) => {
    try {
      const response = await TasksService.toggleCompletion(id);
      if (response.success && response.data) {
        setTasks(prev => prev.map(task =>
          task.id === id ? response.data! : task
        ));
      }
    } catch (err) {
      console.error('Error toggling task:', err);
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      const response = await TasksService.delete(id);
      if (response.success) {
        setTasks(prev => prev.filter(task => task.id !== id));
      }
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const handleUpdateTask = async (id: string, title: string, description: string) => {
    try {
      const response = await TasksService.update(id, { title, description });
      if (response.success && response.data) {
        setTasks(prev => prev.map(task =>
          task.id === id ? response.data! : task
        ));
      }
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  if (!isAuthenticated) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-8"
      >
        <p className="text-onyx-300">Please log in to view your tasks</p>
      </motion.div>
    );
  }

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-center py-8"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="inline-block w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full mb-4"
        />
        <p className="text-onyx-300">Loading your tasks...</p>
      </motion.div>
    );
  }

  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="bg-rose-900/20 border-l-4 border-rose-500 p-4 mb-4 rounded-r"
      >
        <p className="text-rose-400">{error}</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="bg-onyx-900"
    >
      <TaskForm onAddTask={handleAddTask} />

      {tasks.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center py-12"
        >
          <div className="bg-onyx-800 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-onyx-600">
            <svg className="w-8 h-8 text-onyx-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
          </div>
          <p className="text-onyx-300 text-lg">No tasks yet</p>
          <p className="text-onyx-400">Add your first task above to get started!</p>
        </motion.div>
      ) : (
        <div className="mt-6 space-y-3">
          <AnimatePresence>
            {tasks.map(task => (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <TaskItem
                  task={task}
                  onToggle={handleToggleTask}
                  onDelete={handleDeleteTask}
                  onUpdate={handleUpdateTask}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </motion.div>
  );
};

export default TaskList;
