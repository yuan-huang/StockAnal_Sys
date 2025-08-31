# 🗂️ 状态管理使用指南

## 📋 概述

项目使用 **Zustand** 作为状态管理解决方案，它是一个轻量级、类型安全的状态管理库。

## 🏗️ Store 架构

### 1. **AuthStore** - 用户认证状态
```typescript
import { useAuthStore } from '@/store';

// 在组件中使用
const { user, isAuthenticated, login, logout } = useAuthStore();

// 登录
const handleLogin = async () => {
  const success = await login(email, password);
  if (success) {
    // 登录成功，跳转到仪表板
  }
};
```

**主要功能：**
- 用户登录/登出
- 用户注册
- 用户资料更新
- Token 管理
- 自动持久化到 localStorage

### 2. **StockStore** - 股票数据状态
```typescript
import { useStockStore } from '@/store';

const { 
  stocks, 
  watchlist, 
  fetchStocks, 
  addToWatchlist 
} = useStockStore();

// 获取股票列表
useEffect(() => {
  fetchStocks();
}, []);

// 添加到关注列表
const handleAddToWatchlist = (symbol: string) => {
  addToWatchlist(symbol);
};
```

**主要功能：**
- 股票列表管理
- 股票搜索和筛选
- 关注列表管理
- 分页支持
- 错误处理

### 3. **PortfolioStore** - 投资组合状态
```typescript
import { usePortfolioStore } from '@/store';

const { 
  portfolios, 
  currentPortfolio, 
  createPortfolio, 
  addStock 
} = usePortfolioStore();

// 创建投资组合
const handleCreatePortfolio = async () => {
  const success = await createPortfolio('我的投资组合');
  if (success) {
    // 创建成功
  }
};
```

**主要功能：**
- 投资组合 CRUD 操作
- 股票添加/移除
- 收益计算
- 数据持久化

### 4. **UIStore** - 界面状态
```typescript
import { useUIStore } from '@/store';

const { 
  theme, 
  sidebarCollapsed, 
  toggleTheme, 
  toggleSidebar 
} = useUIStore();

// 切换主题
const handleThemeToggle = () => {
  toggleTheme();
};

// 切换侧边栏
const handleSidebarToggle = () => {
  toggleSidebar();
};
```

**主要功能：**
- 主题切换（明/暗模式）
- 侧边栏状态管理
- 通知设置
- 布局配置

### 5. **AppStore** - 应用全局状态
```typescript
import { useAppStore } from '@/store';

const { 
  preferences, 
  featureFlags, 
  updatePreferences, 
  toggleFeatureFlag 
} = useAppStore();

// 更新语言设置
const handleLanguageChange = (language: string) => {
  updatePreferences({ language });
};

// 切换功能开关
const handleToggleAI = () => {
  toggleFeatureFlag('aiAnalysis');
};
```

**主要功能：**
- 应用配置管理
- 用户偏好设置
- 功能开关控制
- 系统状态监控

## 🔧 使用模式

### 基础用法
```typescript
import { useAuthStore } from '@/store';

function LoginForm() {
  const { login, isLoading, error } = useAuthStore();
  
  const handleSubmit = async (values: LoginForm) => {
    const success = await login(values.email, values.password);
    if (success) {
      // 处理成功逻辑
    }
  };
  
  return (
    <Form onSubmit={handleSubmit}>
      {error && <Alert message={error} type="error" />}
      <Button type="primary" loading={isLoading}>
        登录
      </Button>
    </Form>
  );
}
```

### 选择器模式（性能优化）
```typescript
import { useAuthStore } from '@/store';

// 只订阅需要的状态，避免不必要的重渲染
const user = useAuthStore(state => state.user);
const isAuthenticated = useAuthStore(state => state.isAuthenticated);

// 或者使用 shallow 比较
import { shallow } from 'zustand/shallow';

const { user, isAuthenticated } = useAuthStore(
  state => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
  shallow
);
```

### 异步操作
```typescript
import { useStockStore } from '@/store';

function StockList() {
  const { stocks, fetchStocks, isLoading, error } = useStockStore();
  
  useEffect(() => {
    fetchStocks();
  }, []);
  
  if (isLoading) return <Loading />;
  if (error) return <Error message={error} />;
  
  return (
    <div>
      {stocks.map(stock => (
        <StockCard key={stock.id} stock={stock} />
      ))}
    </div>
  );
}
```

## 🚀 最佳实践

### 1. **Store 设计原则**
- 单一职责：每个 store 负责特定的业务领域
- 扁平化：避免深层嵌套的状态结构
- 不可变性：使用不可变的方式更新状态

### 2. **性能优化**
- 使用选择器避免不必要的重渲染
- 合理使用 `shallow` 比较
- 避免在 store 中存储计算值

### 3. **错误处理**
- 每个异步操作都要有错误处理
- 提供用户友好的错误信息
- 记录错误日志用于调试

### 4. **持久化策略**
- 敏感数据（如 token）不持久化
- 用户偏好设置可以持久化
- 使用 `partialize` 选择需要持久化的字段

## 🔍 调试技巧

### 1. **Redux DevTools 集成**
```typescript
import { devtools } from 'zustand/middleware';

export const useStore = create(
  devtools(
    (set) => ({ ... }),
    { name: 'store-name' }
  )
);
```

### 2. **状态快照**
```typescript
// 在控制台查看当前状态
console.log(useStore.getState());

// 订阅状态变化
useStore.subscribe(console.log);
```

### 3. **时间旅行调试**
```typescript
// 重置到特定状态
useStore.setState(previousState);
```

## 📚 扩展阅读

- [Zustand 官方文档](https://github.com/pmndrs/zustand)
- [React 状态管理最佳实践](https://react.dev/learn/managing-state)
- [TypeScript 与状态管理](https://www.typescriptlang.org/docs/)

## 🆘 常见问题

### Q: 如何添加新的 store？
A: 在 `src/store/` 目录下创建新文件，然后在 `index.ts` 中导出

### Q: 如何处理 store 之间的依赖？
A: 使用 `get()` 方法获取其他 store 的状态，或创建组合 store

### Q: 如何测试 store？
A: 使用 Jest 和 `@testing-library/react-hooks` 进行测试

### Q: 如何迁移到其他状态管理库？
A: Zustand 的 API 设计简洁，迁移成本较低，可以逐步替换 