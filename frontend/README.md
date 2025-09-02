# 股票分析系统前端

基于React + TypeScript + Ant Design + Tailwind CSS构建的现代化前端应用。

## 技术栈

- **框架**: React 19 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design 5
- **样式框架**: Tailwind CSS
- **路由**: React Router DOM
- **HTTP客户端**: Axios
- **状态管理**: React Hooks (可扩展为Zustand/Redux)
- **代码规范**: ESLint + TypeScript

## 项目结构

```
src/
├── components/          # 组件目录
│   ├── common/         # 通用组件
│   ├── layout/         # 布局组件
│   └── ui/            # UI组件
├── pages/              # 页面组件
├── hooks/              # 自定义Hooks
├── utils/              # 工具函数
├── services/           # API服务
├── store/              # 状态管理
├── types/              # TypeScript类型定义
├── constants/          # 常量定义
└── styles/             # 样式文件
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 预览构建结果

```bash
npm run preview
```

## 开发指南

### 组件开发规范

1. 使用函数式组件 + TypeScript
2. 组件文件使用PascalCase命名
3. 导出使用默认导出
4. 使用Tailwind CSS进行样式设计
5. 复杂组件使用Ant Design组件库

### 代码规范

- 使用ESLint进行代码检查
- 遵循TypeScript严格模式
- 使用Prettier进行代码格式化
- 组件props必须定义TypeScript接口

### 样式指南

- 优先使用Tailwind CSS工具类
- 自定义样式使用@layer指令
- 避免与Ant Design样式冲突
- 响应式设计使用Tailwind断点

## 功能特性

- 🎨 现代化UI设计
- 📱 响应式布局
- 🔐 用户认证系统
- 📊 数据可视化
- 🚀 高性能构建
- 🧪 TypeScript类型安全

## 环境变量

创建`.env.local`文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 部署

项目支持多种部署方式：

- 静态文件部署
- Docker容器化
- CDN加速

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License
