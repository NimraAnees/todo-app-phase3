'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import TaskList from '@/components/tasks/TaskList';
import ChatInterface from '@/components/chat/ChatInterface';
import { MessageSquare, ListTodo } from 'lucide-react';

const TasksPage = () => {
  const { loading, isAuthenticated } = useAuth();
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTasksUpdate = () => {
    // Trigger task list refresh when AI makes changes
    setRefreshTrigger(prev => prev + 1);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-onyx-900">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xl text-onyx-300"
        >
          Loading...
        </motion.div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-onyx-900">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-xl text-onyx-300"
        >
          Please log in to view your tasks
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-onyx-900 p-4 lg:p-8"
    >
      <div className="max-w-7xl mx-auto">
        {/* Page Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8 pt-6"
        >
          <h1 className="text-3xl lg:text-4xl font-bold text-onyx-50">AI Task Dashboard</h1>
          <p className="text-onyx-300 mt-2">Chat with AI to manage your tasks or use the task list directly</p>
        </motion.div>

        {/* Two Column Layout: Chat + Task List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: AI Chat Interface */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="space-y-4"
          >
            <div className="flex items-center gap-2 mb-4">
              <MessageSquare className="w-6 h-6 text-emerald-400" />
              <h2 className="text-xl font-semibold text-onyx-50">AI Assistant</h2>
            </div>
            <ChatInterface onTasksUpdate={handleTasksUpdate} />
          </motion.div>

          {/* Right: Task List */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-4"
          >
            <div className="flex items-center gap-2 mb-4">
              <ListTodo className="w-6 h-6 text-emerald-400" />
              <h2 className="text-xl font-semibold text-onyx-50">Your Tasks</h2>
            </div>
            <TaskList key={refreshTrigger} />
          </motion.div>
        </div>

        {/* Help Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-8 p-6 bg-onyx-800 border border-onyx-600 rounded-lg"
        >
          <h3 className="text-lg font-semibold text-onyx-50 mb-3">💡 How to Use</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-onyx-300">
            <div>
              <h4 className="font-medium text-emerald-400 mb-2">Via AI Chat:</h4>
              <ul className="space-y-1 list-disc list-inside">
                <li>"Create a task to buy groceries"</li>
                <li>"Show all my tasks"</li>
                <li>"Mark task as completed"</li>
                <li>"Delete the first task"</li>
                <li>"Update task title to..."</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-emerald-400 mb-2">Via Task List:</h4>
              <ul className="space-y-1 list-disc list-inside">
                <li>Click "Add Task" to create</li>
                <li>Click checkmark to complete</li>
                <li>Click edit icon to update</li>
                <li>Click trash icon to delete</li>
                <li>Changes sync with AI instantly</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default TasksPage;
