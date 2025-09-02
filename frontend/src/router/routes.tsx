import React, { lazy, Suspense } from 'react';
import { Route } from 'react-router-dom';
import { Spin } from 'antd';
import { mainMenuItems, adminMenuItems } from './menuConfig';
import type { MenuItem } from './menuConfig';

// 页面组件映射
const componentMap: Record<string, React.ComponentType<any>> = {
  Dashboard: lazy(() => import('../pages/Dashboard')),
  MarketOverview: lazy(() => import('../pages/MarketOverview')),
  MarketTrends: lazy(() => import('../pages/MarketTrends')),
  MarketSectors: lazy(() => import('../pages/MarketSectors')),
  StockScreening: lazy(() => import('../pages/StockScreening')),
  StockAnalysis: lazy(() => import('../pages/StockAnalysis')),
  StockRecommendations: lazy(() => import('../pages/StockRecommendations')),
  AiMonitor: lazy(() => import('../pages/AiMonitor')),
  Watchlist: lazy(() => import('../pages/Watchlist')),
  SystemSettings: lazy(() => import('../pages/SystemSettings')),
  SystemLogs: lazy(() => import('../pages/SystemLogs')),
  MessageCenter: lazy(() => import('../pages/MessageCenter')),
  PlaceholderPage: lazy(() => import('../pages/PlaceholderPage')),
};

// 加载中组件
const LoadingComponent = () => (
  <div style={{ 
    display: 'flex', 
    justifyContent: 'center', 
    alignItems: 'center', 
    height: '200px' 
  }}>
    <Spin size="large" />
  </div>
);

// 根据菜单项生成路由配置
const generateRoutes = (items: MenuItem[], parentPath = ''): React.ReactElement[] => {
  const routes: React.ReactElement[] = [];
  
  items.forEach(item => {
    if (item.path && item.component) {
      const Component = componentMap[item.component];
      if (Component) {
        routes.push(
          <Route
            key={item.path}
            path={item.path}
            element={
              <Suspense fallback={<LoadingComponent />}>
                <Component />
              </Suspense>
            }
          />
        );
      }
    }
    
    if (item.children) {
      routes.push(...generateRoutes(item.children, item.path));
    }
  });
  
  return routes;
};

// 生成所有路由
export const generateAllRoutes = (): React.ReactElement[] => {
  const allRoutes = [
    ...generateRoutes(mainMenuItems),
    ...generateRoutes(adminMenuItems),
  ];
  
  return allRoutes;
};

// 获取路由路径数组
export const getRoutePaths = (): string[] => {
  const paths: string[] = [];
  
  const extractPaths = (items: MenuItem[]) => {
    items.forEach(item => {
      if (item.path) {
        paths.push(item.path);
      }
      if (item.children) {
        extractPaths(item.children);
      }
    });
  };
  
  extractPaths(mainMenuItems);
  extractPaths(adminMenuItems);
  
  return paths;
};

// 根据路径获取组件名称
export const getComponentByPath = (path: string): string | null => {
  const findComponent = (items: MenuItem[]): string | null => {
    for (const item of items) {
      if (item.path === path) {
        return item.component || null;
      }
      if (item.children) {
        const found = findComponent(item.children);
        if (found) return found;
      }
    }
    return null;
  };
  
  return findComponent([...mainMenuItems, ...adminMenuItems]);
}; 