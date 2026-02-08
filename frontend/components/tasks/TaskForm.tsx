'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { Plus } from 'lucide-react';

interface TaskFormProps {
  onAddTask: (title: string, description?: string) => void;
}

const TaskForm = ({ onAddTask }: TaskFormProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length > 255) {
      setError('Title must be 255 characters or less');
      return;
    }

    onAddTask(title, description);
    setTitle('');
    setDescription('');
    setError('');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-onyx-800 rounded-xl shadow-black-touch border border-onyx-600 p-6 mb-6"
    >
      <motion.h2
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-xl font-semibold text-onyx-50 mb-4 flex items-center gap-2"
      >
        <Plus className="w-5 h-5 text-emerald-400" />
        Add New Task
      </motion.h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <motion.div
          animate={{ borderColor: error ? '#F43F5E' : isFocused ? '#00FFAA' : '#2A2A2A' }}
          transition={{ duration: 0.2 }}
        >
          <Input
            label="Task Title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="What needs to be done?"
            required
            className="w-full"
          />
        </motion.div>

        <div>
          <Input
            label="Description (Optional)"
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add details..."
            className="w-full"
          />
        </div>

        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-rose-900/20 border-l-4 border-rose-500 p-3 text-rose-400 text-sm rounded-r"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        <div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 text-black px-6 py-3 rounded-lg font-medium hover:shadow-emerald-glow transition-all duration-200 flex items-center justify-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Add Task
          </motion.button>
        </div>
      </form>
    </motion.div>
  );
};

export default TaskForm;
