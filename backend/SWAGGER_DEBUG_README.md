# Swagger Debug 模式配置说明

## 概述

本系统已实现 Swagger API 文档的智能配置功能，该功能仅在开发 debug 模式下启用，生产环境下自动禁用。

## 功能特性

### 🔧 智能配置
- **自动检测**: 系统自动检测 Flask 应用的 debug 模式
- **条件启用**: 仅在 `debug=True` 时启用 Swagger 文档
- **生产安全**: 生产环境下自动禁用，避免暴露 API 信息

### 📚 Swagger 文档
- **访问地址**: `/api/docs`
- **API 规范**: `/static/swagger.json`
- **中文界面**: 支持中文显示的应用名称

## 技术实现

### 核心函数
```python
def setup_swagger(app_instance):
    """
    配置 Swagger 文档支持
    仅在开发 debug 模式下启用
    
    Args:
        app_instance: Flask 应用实例
    """
    # 检查是否为 debug 模式
    if not app_instance.debug:
        logging.info("生产模式：Swagger 文档已禁用")
        return
    
    logging.info("开发模式：启用 Swagger 文档")
    # ... Swagger 配置逻辑
```

### 配置流程
1. **应用创建**: Flask 应用实例创建
2. **模式检测**: 检查 `app.debug` 状态
3. **条件配置**: 根据 debug 模式决定是否启用 Swagger
4. **蓝图注册**: 注册 Swagger UI 蓝图
5. **路由添加**: 添加文档访问路由

## 使用方法

### 开发环境
```python
# main.py
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port, debug=True)  # debug=True 启用 Swagger
```

### 生产环境
```python
# 生产部署时
app.run(host='0.0.0.0', port=port, debug=False)  # debug=False 禁用 Swagger
```

### 环境变量控制
```bash
# 通过环境变量控制
export FLASK_DEBUG=1    # 启用 debug 模式
export FLASK_DEBUG=0    # 禁用 debug 模式
```

## 启动日志

应用启动时会显示 debug 模式状态：

```
==================================================
应用启动
==================================================
依赖注入容器状态: <AnalysisContainer object>
Debug 模式: True
Swagger 文档已启用: /api/docs
```

## 安全考虑

### ✅ 安全特性
- **生产环境保护**: 生产环境下自动禁用 Swagger
- **访问控制**: 仅通过 debug 模式控制，无需额外配置
- **日志记录**: 记录 Swagger 启用/禁用状态

### ⚠️ 注意事项
- 确保生产环境部署时 `debug=False`
- 定期检查日志确认 Swagger 状态
- 不要在生产环境中手动启用 debug 模式

## 故障排除

### 常见问题

1. **Swagger 无法访问**
   - 检查应用是否在 debug 模式下运行
   - 查看启动日志确认 Swagger 状态

2. **生产环境出现 Swagger**
   - 确认 `debug=False`
   - 检查环境变量 `FLASK_DEBUG`

3. **导入错误**
   - 确认已安装 `flask-swagger-ui` 依赖
   - 检查 Python 路径配置

### 依赖要求
```bash
pip install flask-swagger-ui
```

## 版本信息

- **版本**: v2.1.0
- **修改者**: 熊猫大侠
- **功能**: Swagger 智能配置
- **兼容性**: Flask 2.x+, Python 3.7+
