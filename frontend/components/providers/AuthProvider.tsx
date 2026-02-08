'use client';

import React, { useState, useEffect, useContext, createContext } from 'react';
import { 
  saveToken, 
  getToken, 
  removeToken, 
  isAuthenticated as checkAuth, 
  getUserInfo 
} from '../../lib/utils/auth';

// Define the shape of our auth context
export interface AuthContextType {
  user: any;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  signup: (name: string, email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// AuthProvider component to wrap the app
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  // Check authentication status on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      console.log('Checking authentication status...');
      const token = getToken();
      console.log('Found token:', !!token);

      if (token) {
        const userInfo = getUserInfo();
        console.log('User info from token:', userInfo);

        if (userInfo) {
          setUser(userInfo);
          setIsAuth(true);
          console.log('Authentication restored from token');
        } else {
          // Token was expired, remove it
          console.log('Token was expired, removing');
          removeToken();
        }
      } else {
        console.log('No token found');
      }

      setLoading(false);
    };

    checkAuthStatus();
  }, []);

  // Login function
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      console.log('Attempting login for email:', email);
      setLoading(true);

      // Use the AuthService for API calls
      const AuthService = (await import('../../lib/api/auth')).default;
      const response = await AuthService.login({ email, password });

      console.log('Login response:', response);

      if (response.success && response.token) {
        console.log('Login successful, saving token');
        saveToken(response.token);

        // Get fresh user info from token
        const userInfo = getUserInfo();
        console.log('Setting user info:', userInfo);
        setUser(userInfo);
        setIsAuth(true);
        return true;
      } else {
        console.log('Login failed:', response.error);
      }

      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Signup function - returns { success, error? }
  const signup = async (name: string, email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      console.log('Attempting signup for:', name, email);
      setLoading(true);

      // Use the AuthService for API calls
      const AuthService = (await import('../../lib/api/auth')).default;
      const response = await AuthService.signup({ name, email, password });

      console.log('Signup response:', response);

      if (response.success && response.token) {
        console.log('Signup successful, saving token');
        saveToken(response.token);

        // Get fresh user info from token
        const userInfo = getUserInfo();
        console.log('Setting user info:', userInfo);
        setUser(userInfo);
        setIsAuth(true);
        return { success: true };
      }

      return { success: false, error: response.error || 'Signup failed' };
    } catch (error: any) {
      console.error('Signup error:', error);
      return { success: false, error: error.message || 'Signup failed' };
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    console.log('Initiating logout...');
    try {
      // Use the AuthService for API calls
      const AuthService = (await import('../../lib/api/auth')).default;
      await AuthService.logout();
      console.log('Backend logout completed');
    } catch (error) {
      console.error('Logout error:', error);
      // Continue with client-side cleanup even if backend call fails
    } finally {
      // Always remove token from local storage even if API call fails
      console.log('Clearing authentication state');
      removeToken();
      setUser(null);
      setIsAuth(false);
      console.log('Logout completed');
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    signup,
    logout,
    isAuthenticated: isAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
