本地开发环境搭建

# 1. 下载python 3.11.9 版本
https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip


# 2. 生成venv环境
uv venv --python {python3.11.9的解压后的路径目录} .venv

例如：
```
uv venv --python E:\uv_python_install_dir\python-3.11.9-embed-amd64 .venv
```

# 3. 执行包同步
uv sync

# 4.复制 env-example 改成 .env  
配置数据库参数， mongodb 和 redis的参数
