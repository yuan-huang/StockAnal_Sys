#!/usr/bin/env python3
# scripts/test_mongo_logging.py
"""
测试MongoDB日志配置的脚本
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from app.web.init_app import initialize_application, setup_logging

def test_mongo_logging():
    """测试MongoDB日志功能"""
    print("开始测试MongoDB日志配置...")
    
    # 初始化应用程序
    success = initialize_application()
    if not success:
        print("❌ 应用程序初始化失败")
        return False
    
    # 设置日志
    setup_logging()
    
    # 获取logger
    logger = logging.getLogger('test_mongo_logging')
    
    print("✅ 应用程序初始化成功")
    
    # 测试不同级别的日志
    try:
        logger.info("🔍 测试INFO级别日志 - MongoDB日志测试")
        logger.warning("⚠️ 测试WARNING级别日志 - 这是一个警告消息")
        logger.error("❌ 测试ERROR级别日志 - 这是一个错误消息")
        
        # 测试带有额外信息的日志
        logger.info("📊 股票分析测试", extra={
            'stock_code': 'TEST001',
            'market_type': 'A股',
            'analysis_type': '技术分析'
        })
        
        print("✅ 日志测试完成")
        print("📝 请检查以下位置的日志:")
        print("   1. 控制台输出 (上方显示)")
        print("   2. MongoDB数据库 -> tradingagents -> app_logs 集合")
        print("   3. 日志文件 (如果配置)")
        
        return True
        
    except Exception as e:
        print(f"❌ 日志测试失败: {e}")
        return False

def check_database_connections():
    """检查数据库连接状态"""
    print("\n检查数据库连接状态...")
    
    from app.web.init_app import get_mongo_db, get_redis
    
    # 检查MongoDB
    try:
        mongo_db = get_mongo_db()
        if mongo_db:
            collections = mongo_db.list_collection_names()
            print(f"✅ MongoDB连接正常")
            print(f"   数据库: {mongo_db.name}")
            print(f"   集合数量: {len(collections)}")
            if 'app_logs' in collections:
                print("   ✅ app_logs集合已存在")
            else:
                print("   ℹ️ app_logs集合将在首次写入日志时创建")
        else:
            print("❌ MongoDB连接失败")
    except Exception as e:
        print(f"❌ MongoDB连接错误: {e}")
    
    # 检查Redis
    try:
        redis_client = get_redis()
        if redis_client:
            redis_info = redis_client.info()
            print(f"✅ Redis连接正常")
            print(f"   版本: {redis_info.get('redis_version', 'Unknown')}")
            print(f"   内存使用: {redis_info.get('used_memory_human', 'Unknown')}")
        else:
            print("❌ Redis连接失败")
    except Exception as e:
        print(f"❌ Redis连接错误: {e}")

def main():
    """主函数"""
    print("="*60)
    print("MongoDB日志配置测试")
    print("="*60)
    
    # 检查环境变量
    print("检查环境变量...")
    required_vars = ['MONGO_HOST', 'MONGO_PORT', 'MONGO_DB_NAME']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未设置")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ 缺少环境变量: {', '.join(missing_vars)}")
        print("请检查.env文件配置")
        return
    
    # 检查数据库连接
    check_database_connections()
    
    # 测试日志功能
    print("\n" + "="*60)
    success = test_mongo_logging()
    
    print("\n" + "="*60)
    if success:
        print("🎉 MongoDB日志配置测试完成!")
        print("\n使用方法:")
        print("1. 在您的代码中导入: from app.core.init_app import initialize_application, setup_logging")
        print("2. 在应用启动时调用: initialize_application() 和 setup_logging()")
        print("3. 使用标准logging: logger = logging.getLogger('your_module'); logger.info('message')")
    else:
        print("❌ 测试失败，请检查配置")

if __name__ == "__main__":
    main() 