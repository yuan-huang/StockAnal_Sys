# 开发环境搭建

## 概述

本文档将指导你如何搭建完整的开发环境，包括必要的工具、依赖和配置。

## 系统要求

### 最低要求
- **操作系统**：Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **内存**：8GB RAM
- **存储**：20GB 可用空间
- **网络**：稳定的互联网连接

### 推荐配置
- **操作系统**：Windows 11, macOS 12+, Ubuntu 20.04+
- **内存**：16GB RAM
- **存储**：50GB 可用空间
- **网络**：高速互联网连接

## 必需工具

### 1. 代码编辑器
- **推荐**：Visual Studio Code
- **下载地址**：https://code.visualstudio.com/
- **扩展插件**：
  - ESLint
  - Prettier
  - GitLens
  - Auto Rename Tag

### 2. 版本控制
- **Git**：https://git-scm.com/
- **GitHub Desktop**（可选）：https://desktop.github.com/

### 3. 包管理器
- **Node.js**：https://nodejs.org/ (推荐 LTS 版本)
- **npm**：随 Node.js 安装
- **yarn**（可选）：`npm install -g yarn`

### 4. 数据库
- **MySQL**：https://dev.mysql.com/downloads/
- **Redis**：https://redis.io/download
- **MongoDB**（可选）：https://www.mongodb.com/try/download/community

## 环境搭建步骤

### 步骤 1：安装基础工具

```bash
# 检查 Node.js 版本
node --version
npm --version

# 安装全局依赖
npm install -g nodemon
npm install -g pm2
npm install -g typescript
```

### 步骤 2：克隆项目

```bash
# 克隆项目仓库
git clone https://github.com/your-project/your-repo.git
cd your-repo

# 安装项目依赖
npm install
```

### 步骤 3：环境配置

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑环境配置
# 配置数据库连接、API 密钥等
```

### 步骤 4：数据库初始化

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE your_project_dev;

# 运行数据库迁移
npm run db:migrate

# 初始化测试数据
npm run db:seed
```

### 步骤 5：启动开发服务器

```bash
# 启动后端服务
npm run dev:server

# 启动前端开发服务器
npm run dev:client

# 启动所有服务
npm run dev
```

## 开发工具配置

### VS Code 配置

创建 `.vscode/settings.json`：

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "files.associations": {
    "*.env*": "dotenv"
  }
}
```

### ESLint 配置

创建 `.eslintrc.js`：

```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended'
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    'no-console': 'warn',
    'prefer-const': 'error'
  }
};
```

### Prettier 配置

创建 `.prettierrc`：

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

## 常用开发命令

```bash
# 代码检查
npm run lint

# 代码格式化
npm run format

# 运行测试
npm run test

# 构建项目
npm run build

# 启动生产环境
npm run start
```

## 调试配置

### VS Code 调试配置

创建 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Server",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/src/server.ts",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "env": {
        "NODE_ENV": "development"
      }
    }
  ]
}
```

## 常见问题

### 1. 依赖安装失败
```bash
# 清除 npm 缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install
```

### 2. 端口被占用
```bash
# 查找占用端口的进程
netstat -ano | findstr :3000

# 杀死进程
taskkill /PID <进程ID> /F
```

### 3. 数据库连接失败
- 检查数据库服务是否启动
- 验证连接字符串和凭据
- 确认防火墙设置

## 下一步

- [编码规范](./coding-standards.md) - 代码标准
- [开发流程](./development-workflow.md) - 工作流程
- [测试指南](./testing.md) - 测试说明

## 获取帮助

- **文档**：查看项目文档
- **Issues**：在 GitHub 上提交问题
- **讨论**：参与社区讨论
- **邮件**：联系开发团队
