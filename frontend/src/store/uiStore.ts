import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UIState {
  // 主题设置
  theme: 'light' | 'dark' | 'auto';
  
  // 侧边栏状态
  sidebarCollapsed: boolean;
  
  // 全局加载状态
  globalLoading: boolean;
  
  // 通知设置
  notifications: {
    enabled: boolean;
    sound: boolean;
    desktop: boolean;
  };
  
  // 布局设置
  layout: {
    headerHeight: number;
    sidebarWidth: number;
    contentPadding: number;
  };
  
  // 操作
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark' | 'auto') => void;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setGlobalLoading: (loading: boolean) => void;
  updateNotificationSettings: (settings: Partial<UIState['notifications']>) => void;
  updateLayoutSettings: (settings: Partial<UIState['layout']>) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      // 初始状态
      theme: 'light',
      sidebarCollapsed: false,
      globalLoading: false,
      notifications: {
        enabled: true,
        sound: true,
        desktop: true
      },
      layout: {
        headerHeight: 64,
        sidebarWidth: 200,
        contentPadding: 24
      },

      // 切换主题
      toggleTheme: () => {
        const currentTheme = get().theme;
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        set({ theme: newTheme });
        
        // 应用主题到body
        document.body.setAttribute('data-theme', newTheme);
      },

      // 设置主题
      setTheme: (theme: 'light' | 'dark' | 'auto') => {
        set({ theme });
        document.body.setAttribute('data-theme', theme);
      },

      // 切换侧边栏
      toggleSidebar: () => {
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed }));
      },

      // 设置侧边栏状态
      setSidebarCollapsed: (collapsed: boolean) => {
        set({ sidebarCollapsed: collapsed });
      },

      // 设置全局加载状态
      setGlobalLoading: (loading: boolean) => {
        set({ globalLoading: loading });
      },

      // 更新通知设置
      updateNotificationSettings: (settings) => {
        set((state) => ({
          notifications: { ...state.notifications, ...settings }
        }));
      },

      // 更新布局设置
      updateLayoutSettings: (settings) => {
        set((state) => ({
          layout: { ...state.layout, ...settings }
        }));
      }
    }),
    {
      name: 'ui-storage',
      partialize: (state) => ({ 
        theme: state.theme,
        sidebarCollapsed: state.sidebarCollapsed,
        notifications: state.notifications,
        layout: state.layout
      })
    }
  )
); 