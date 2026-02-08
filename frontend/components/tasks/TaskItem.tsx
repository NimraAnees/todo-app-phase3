'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Button from '@/components/ui/Button';
import { CheckCircle, Circle, Edit3, Trash2 } from 'lucide-react';

interface TaskItemProps {
  task: {
    id: string;
    title: string;
    description?: string;
    status: string; // "pending" | "in_progress" | "completed"
    created_at: string;
  };
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onUpdate: (id: string, title: string, description: string) => void;
}

const TaskItem = ({ task, onToggle, onDelete, onUpdate }: TaskItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleSave = () => {
    onUpdate(task.id, editTitle, editDescription);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.3 }}
      className="border rounded-lg p-4 mb-3 bg-onyx-800 border-onyx-600 shadow-black-touch hover:shadow-black-hover transition-shadow duration-300"
    >
      <AnimatePresence mode="wait">
        {isEditing ? (
          <motion.div
            key="edit-form"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="space-y-3"
          >
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 dark:bg-onyx-700 dark:border-onyx-600 dark:text-onyx-50"
              placeholder="Task title"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 dark:bg-onyx-700 dark:border-onyx-600 dark:text-onyx-50"
              placeholder="Task description (optional)"
              rows={3}
            />
            <div className="flex gap-2">
              <Button
                onClick={handleSave}
                variant="primary"
                size="sm"
                className="flex items-center gap-2"
              >
                <CheckCircle className="w-4 h-4" />
                Save
              </Button>
              <Button
                onClick={handleCancel}
                variant="secondary"
                size="sm"
                className="flex items-center gap-2"
              >
                Cancel
              </Button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="task-view"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="flex items-start">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onToggle(task.id)}
                className="mt-1"
              >
                {task.status === 'completed' ? (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="w-5 h-5 rounded-full bg-emerald-500 flex items-center justify-center"
                  >
                    <CheckCircle className="w-4 h-4 text-black" />
                  </motion.div>
                ) : (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="w-5 h-5 rounded-full border-2 border-onyx-500 flex items-center justify-center"
                  >
                    <motion.div
                      className="w-3 h-3 rounded-full bg-transparent"
                      whileHover={{ backgroundColor: '#666666' }}
                    />
                  </motion.div>
                )}
              </motion.button>

              <div className="ml-3 flex-1 min-w-0">
                <motion.h3
                  className={`text-lg font-medium ${task.status === 'completed' ? 'line-through text-onyx-400' : 'text-onyx-50'}`}
                  animate={{ textDecoration: task.status === 'completed' ? 'line-through' : 'none' }}
                >
                  {task.title}
                </motion.h3>
                {task.description && (
                  <motion.p
                    className={`mt-1 text-sm ${task.status === 'completed' ? 'line-through text-onyx-400' : 'text-onyx-300'}`}
                    animate={{ textDecoration: task.status === 'completed' ? 'line-through' : 'none' }}
                  >
                    {task.description}
                  </motion.p>
                )}
                <p className="mt-1 text-xs text-onyx-400">
                  Created: {formatDate(task.created_at)}
                </p>
              </div>

              <div className="flex gap-1 ml-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setIsEditing(true)}
                  className="p-2 rounded-md hover:bg-onyx-700 transition-colors"
                >
                  <Edit3 className="w-4 h-4 text-emerald-400" />
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => onDelete(task.id)}
                  className="p-2 rounded-md hover:bg-rose-900/20 transition-colors"
                >
                  <Trash2 className="w-4 h-4 text-rose-400" />
                </motion.button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default TaskItem;
