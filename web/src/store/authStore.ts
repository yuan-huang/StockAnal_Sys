import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '../types';

interface AuthState {
  // 状态
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // 操作
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (userData: Partial<User> & { password: string }) => Promise<boolean>;
  updateProfile: (userData: Partial<User>) => Promise<boolean>;
  refreshToken: () => Promise<boolean>;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // 初始状态
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      // 登录
      login: async (email: string, _password: string) => {
        set({ isLoading: true });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // 模拟登录成功
          const mockUser: User = {
            id: '1',
            username: 'admin',
            email: email,
            role: 'admin',
            avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin'
          };
          
          const mockToken = 'mock-jwt-token-' + Date.now();
          
          set({
            user: mockUser,
            token: mockToken,
            isAuthenticated: true,
            isLoading: false
          });
          
          // 存储到localStorage
          localStorage.setItem('token', mockToken);
          localStorage.setItem('user', JSON.stringify(mockUser));
          
          return true;
        } catch (error) {
          set({ isLoading: false });
          console.error('Login failed:', error);
          return false;
        }
      },

      // 登出
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false
        });
        
        // 清除localStorage
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      },

      // 注册
      register: async (userData) => {
        set({ isLoading: true });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // 模拟注册成功
          const newUser: User = {
            id: Date.now().toString(),
            username: userData.username || 'user',
            email: userData.email || '',
            role: 'user'
          };
          
          set({
            user: newUser,
            isLoading: false
          });
          
          return true;
        } catch (error) {
          set({ isLoading: false });
          console.error('Registration failed:', error);
          return false;
        }
      },

      // 更新用户资料
      updateProfile: async (userData) => {
        const currentUser = get().user;
        if (!currentUser) return false;
        
        set({ isLoading: true });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          const updatedUser = { ...currentUser, ...userData };
          set({ user: updatedUser, isLoading: false });
          
          // 更新localStorage
          localStorage.setItem('user', JSON.stringify(updatedUser));
          
          return true;
        } catch (error) {
          set({ isLoading: false });
          console.error('Profile update failed:', error);
          return false;
        }
      },

      // 刷新token
      refreshToken: async () => {
        const currentToken = get().token;
        if (!currentToken) return false;
        
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          
          const newToken = 'mock-jwt-token-' + Date.now();
          set({ token: newToken });
          
          // 更新localStorage
          localStorage.setItem('token', newToken);
          
          return true;
        } catch (error) {
          console.error('Token refresh failed:', error);
          return false;
        }
      },

      // 设置加载状态
      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      }
    }),
    {
      name: 'auth-storage', // localStorage的key
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token,
        isAuthenticated: state.isAuthenticated 
      })
    }
  )
); 