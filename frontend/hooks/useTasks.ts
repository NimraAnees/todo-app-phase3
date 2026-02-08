import { useState, useEffect } from 'react';
import TasksService, { type Task } from '@/lib/api/tasks';
import { useAuth } from './useAuth';

/**
 * useTasks Hook
 *
 * Updated to work with MCP endpoints and new Task interface
 * - Task uses 'status' field (not is_completed boolean)
 * - All operations use POST /mcp/* endpoints
 */
export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    } else {
      setTasks([]);
      setLoading(false);
    }
  }, [isAuthenticated]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
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

  const addTask = async (title: string, description?: string) => {
    try {
      const response = await TasksService.create({ title, description });
      if (response.success && response.data) {
        setTasks(prev => [...prev, response.data!]);
        return { success: true, data: response.data };
      }
      return { success: false, error: response.error };
    } catch (err) {
      console.error('Error creating task:', err);
      return { success: false, error: 'Failed to create task' };
    }
  };

  const updateTask = async (id: string, updates: { title?: string; description?: string; status?: string }) => {
    try {
      const response = await TasksService.update(id, updates);
      if (response.success && response.data) {
        setTasks(prev => prev.map(task => task.id === id ? response.data! : task));
        return { success: true, data: response.data };
      }
      return { success: false, error: response.error };
    } catch (err) {
      console.error('Error updating task:', err);
      return { success: false, error: 'Failed to update task' };
    }
  };

  const toggleTask = async (id: string) => {
    try {
      const response = await TasksService.toggleCompletion(id);
      if (response.success && response.data) {
        setTasks(prev => prev.map(task => task.id === id ? response.data! : task));
        return { success: true, data: response.data };
      }
      return { success: false, error: response.error };
    } catch (err) {
      console.error('Error toggling task:', err);
      return { success: false, error: 'Failed to toggle task' };
    }
  };

  const completeTask = async (id: string) => {
    try {
      const response = await TasksService.complete(id);
      if (response.success && response.data) {
        setTasks(prev => prev.map(task => task.id === id ? response.data! : task));
        return { success: true, data: response.data };
      }
      return { success: false, error: response.error };
    } catch (err) {
      console.error('Error completing task:', err);
      return { success: false, error: 'Failed to complete task' };
    }
  };

  const deleteTask = async (id: string) => {
    try {
      const response = await TasksService.delete(id);
      if (response.success) {
        setTasks(prev => prev.filter(task => task.id !== id));
        return { success: true };
      }
      return { success: false, error: response.error };
    } catch (err) {
      console.error('Error deleting task:', err);
      return { success: false, error: 'Failed to delete task' };
    }
  };

  return {
    tasks,
    loading,
    error,
    addTask,
    updateTask,
    toggleTask,
    completeTask,
    deleteTask,
    refetch: fetchTasks,
  };
};

export type { Task };
