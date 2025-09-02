import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AppState {
  // 应用信息
  appInfo: {
    version: string;
    buildTime: string;
    environment: 'development' | 'production' | 'test';
  };
  
  // 系统状态
  systemStatus: {
    isOnline: boolean;
    lastSyncTime: Date | null;
    syncInterval: number; // 同步间隔（毫秒）
  };
  
  // 用户偏好
  preferences: {
    language: 'zh-CN' | 'en-US';
    timezone: string;
    dateFormat: string;
    numberFormat: string;
    currency: string;
  };
  
  // 功能开关
  featureFlags: {
    realTimeData: boolean;
    advancedCharts: boolean;
    aiAnalysis: boolean;
    mobileApp: boolean;
  };
  
  // 操作
  updateAppInfo: (info: Partial<AppState['appInfo']>) => void;
  setSystemStatus: (status: Partial<AppState['systemStatus']>) => void;
  updatePreferences: (prefs: Partial<AppState['preferences']>) => void;
  toggleFeatureFlag: (feature: keyof AppState['featureFlags']) => void;
  setFeatureFlags: (flags: Partial<AppState['featureFlags']>) => void;
  
  // 系统操作
  checkOnlineStatus: () => void;
  syncData: () => Promise<void>;
  resetPreferences: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // 初始状态
      appInfo: {
        version: '1.0.0',
        buildTime: new Date().toISOString(),
        environment: 'development'
      },
      
      systemStatus: {
        isOnline: navigator.onLine,
        lastSyncTime: null,
        syncInterval: 30000 // 30秒
      },
      
      preferences: {
        language: 'zh-CN',
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        dateFormat: 'YYYY-MM-DD',
        numberFormat: 'zh-CN',
        currency: 'CNY'
      },
      
      featureFlags: {
        realTimeData: true,
        advancedCharts: false,
        aiAnalysis: false,
        mobileApp: false
      },

      // 更新应用信息
      updateAppInfo: (info) => {
        set((state) => ({
          appInfo: { ...state.appInfo, ...info }
        }));
      },

      // 设置系统状态
      setSystemStatus: (status) => {
        set((state) => ({
          systemStatus: { ...state.systemStatus, ...status }
        }));
      },

      // 更新用户偏好
      updatePreferences: (prefs) => {
        set((state) => ({
          preferences: { ...state.preferences, ...prefs }
        }));
      },

      // 切换功能开关
      toggleFeatureFlag: (feature) => {
        set((state) => ({
          featureFlags: {
            ...state.featureFlags,
            [feature]: !state.featureFlags[feature]
          }
        }));
      },

      // 设置功能开关
      setFeatureFlags: (flags) => {
        set((state) => ({
          featureFlags: { ...state.featureFlags, ...flags }
        }));
      },

      // 检查在线状态
      checkOnlineStatus: () => {
        const isOnline = navigator.onLine;
        set((state) => ({
          systemStatus: { ...state.systemStatus, isOnline }
        }));
      },

      // 同步数据
      syncData: async () => {
        set((state) => ({
          systemStatus: { ...state.systemStatus, lastSyncTime: new Date() }
        }));
        
        try {
          // 模拟数据同步
          await new Promise(resolve => setTimeout(resolve, 1000));
          console.log('Data sync completed');
        } catch (error) {
          console.error('Data sync failed:', error);
        }
      },

      // 重置偏好设置
      resetPreferences: () => {
        set({
          preferences: {
            language: 'zh-CN',
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            dateFormat: 'YYYY-MM-DD',
            numberFormat: 'zh-CN',
            currency: 'CNY'
          }
        });
      }
    }),
    {
      name: 'app-storage',
      partialize: (state) => ({ 
        preferences: state.preferences,
        featureFlags: state.featureFlags
      })
    }
  )
); 