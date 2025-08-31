import React from 'react';
import {
  DashboardOutlined,
  BarChartOutlined,
  ScanOutlined,
  RobotOutlined,
  TagOutlined,
  HeartOutlined,
  MessageOutlined,
  SettingOutlined,
  LineChartOutlined,
  FundOutlined,
  ToolOutlined,
  StockOutlined,
  BulbOutlined,
  MonitorOutlined,
  SafetyOutlined,
  FileTextOutlined,
} from '@ant-design/icons';

// 菜单项接口定义
export interface MenuItem {
  key: string;
  icon: React.ReactNode;
  label: string;
  children?: MenuItem[];
  component?: string; // 对应的页面组件名称
  path?: string; // 实际路由路径
}

// 主菜单配置
export const mainMenuItems: MenuItem[] = [
  {
    key: '/dashboard',
    icon: <DashboardOutlined />,
    label: '仪表盘',
    component: 'Dashboard',
    path: '/dashboard',
  },
  {
    key: '/market',
    icon: <BarChartOutlined />,
    label: '市场行情',
    children: [
      {
        key: '/market/overview',
        icon: <BarChartOutlined />,
        label: '市场概览',
        component: 'MarketOverview',
        path: '/market/overview',
      },
      {
        key: '/market/trends',
        icon: <LineChartOutlined />,
        label: '趋势分析',
        component: 'MarketTrends',
        path: '/market/trends',
      },
      {
        key: '/market/sectors',
        icon: <FundOutlined />,
        label: '板块分析',
        component: 'MarketSectors',
        path: '/market/sectors',
      },
    ],
  },
  {
    key: '/stock-picker',
    icon: <ScanOutlined />,
    label: '智能选股',
    children: [
      {
        key: '/stock-picker/screening',
        icon: <ToolOutlined />,
        label: '股票筛选',
        component: 'StockScreening',
        path: '/stock-picker/screening',
      },
      {
        key: '/stock-picker/analysis',
        icon: <StockOutlined />,
        label: '深度分析',
        component: 'StockAnalysis',
        path: '/stock-picker/analysis',
      },
      {
        key: '/stock-picker/recommendations',
        icon: <BulbOutlined />,
        label: '推荐股票',
        component: 'StockRecommendations',
        path: '/stock-picker/recommendations',
      },
    ],
  },
  {
    key: '/ai-monitor',
    icon: <RobotOutlined />,
    label: 'AI盯盘',
    children: [
      {
        key: '/ai-monitor/realtime',
        icon: <MonitorOutlined />,
        label: '实时监控',
        component: 'AiMonitor',
        path: '/ai-monitor/realtime',
      },
      {
        key: '/ai-monitor/alerts',
        icon: <SafetyOutlined />,
        label: '智能预警',
        component: 'AiMonitor',
        path: '/ai-monitor/alerts',
      },
      {
        key: '/ai-monitor/patterns',
        icon: <ScanOutlined />,
        label: '模式识别',
        component: 'AiMonitor',
        path: '/ai-monitor/patterns',
      },
    ],
  },
  {
    key: '/trading-strategy',
    icon: <TagOutlined />,
    label: '交易策略',
    children: [
      {
        key: '/trading-strategy/backtest',
        icon: <LineChartOutlined />,
        label: '策略回测',
        component: 'PlaceholderPage',
        path: '/trading-strategy/backtest',
      },
      {
        key: '/trading-strategy/signals',
        icon: <BulbOutlined />,
        label: '交易信号',
        component: 'PlaceholderPage',
        path: '/trading-strategy/signals',
      },
      {
        key: '/trading-strategy/portfolio',
        icon: <FileTextOutlined />,
        label: '组合管理',
        component: 'PlaceholderPage',
        path: '/trading-strategy/portfolio',
      },
    ],
  },
  {
    key: '/watchlist',
    icon: <HeartOutlined />,
    label: '关注列表',
    children: [
      {
        key: '/watchlist/stocks',
        icon: <StockOutlined />,
        label: '关注股票',
        component: 'Watchlist',
        path: '/watchlist/stocks',
      },
      {
        key: '/watchlist/portfolios',
        icon: <FundOutlined />,
        label: '关注组合',
        component: 'PlaceholderPage',
        path: '/watchlist/portfolios',
      },
      {
        key: '/watchlist/alerts',
        icon: <SafetyOutlined />,
        label: '价格提醒',
        component: 'PlaceholderPage',
        path: '/watchlist/alerts',
      },
    ],
  },
  {
    key: '/message-center',
    icon: <MessageOutlined />,
    label: '消息中心',
    children: [
      {
        key: '/message-center/notifications',
        icon: <SafetyOutlined />,
        label: '系统通知',
        component: 'MessageCenter',
        path: '/message-center/notifications',
      },
      {
        key: '/message-center/alerts',
        icon: <BulbOutlined />,
        label: '预警消息',
        component: 'MessageCenter',
        path: '/message-center/alerts',
      },
      {
        key: '/message-center/reports',
        icon: <FileTextOutlined />,
        label: '分析报告',
        component: 'MessageCenter',
        path: '/message-center/reports',
      },
    ],
  },
];

// 管理员菜单配置
export const adminMenuItems: MenuItem[] = [
  {
    key: '/settings',
    icon: <SettingOutlined />,
    label: '系统设置',
    component: 'SystemSettings',
    path: '/settings',
  },
  {
    key: '/logs',
    icon: <FileTextOutlined />,
    label: '日志查看',
    component: 'SystemLogs',
    path: '/logs',
  },
];

// 用户菜单配置
export const userMenuItems = [
  {
    key: 'profile',
    icon: <SettingOutlined />,
    label: '个人资料',
  },
  {
    key: 'settings',
    icon: <SettingOutlined />,
    label: '设置',
  },
  {
    type: 'divider' as const,
  },
  {
    key: 'logout',
    icon: <SettingOutlined />,
    label: '退出登录',
  },
];

// 获取所有路由路径的扁平化数组
export const getAllRoutes = (): string[] => {
  const routes: string[] = [];
  
  const extractRoutes = (items: MenuItem[]) => {
    items.forEach(item => {
      if (item.path) {
        routes.push(item.path);
      }
      if (item.children) {
        extractRoutes(item.children);
      }
    });
  };
  
  extractRoutes(mainMenuItems);
  extractRoutes(adminMenuItems);
  
  return routes;
};

// 根据路径查找菜单项
export const findMenuItemByPath = (path: string): MenuItem | null => {
  const searchInItems = (items: MenuItem[]): MenuItem | null => {
    for (const item of items) {
      if (item.path === path) {
        return item;
      }
      if (item.children) {
        const found = searchInItems(item.children);
        if (found) return found;
      }
    }
    return null;
  };
  
  return searchInItems([...mainMenuItems, ...adminMenuItems]);
};

// 根据路径查找父级菜单
export const findParentMenuByPath = (path: string): MenuItem | null => {
  for (const item of mainMenuItems) {
    if (item.children) {
      const hasChild = item.children.some(child => child.path === path);
      if (hasChild) {
        return item;
      }
    }
  }
  return null;
}; 