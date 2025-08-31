#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试依赖注入容器是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

def test_dependency_injection():
    """测试依赖注入容器"""
    try:
        print("正在测试依赖注入容器...")
        
        # 测试导入分析容器
        from app.analysis._analysis_container import AnalysisContainer
        print("✓ 成功导入 AnalysisContainer")
        
        # 测试导入核心容器
        from app.core._core_container import CoreContainer
        print("✓ 成功导入 CoreContainer")
        
        # 测试导入缓存类
        from app.core.cache import Cache
        print("✓ 成功导入 Cache")
        
        # 测试导入股票分析器
        from app.analysis.stock_analyzer import StockAnalyzer
        print("✓ 成功导入 StockAnalyzer")
        
        # 创建分析容器实例
        analysis_container = AnalysisContainer()
        print("✓ 成功创建 AnalysisContainer 实例")
        
        # 测试获取缓存提供者
        cache_provider = analysis_container.cache
        print("✓ 成功获取缓存提供者")
        
        # 测试获取股票分析器提供者
        stock_analyzer_provider = analysis_container.stock_analyzer
        print("✓ 成功获取股票分析器提供者")
        
        # 测试获取Redis客户端提供者
        redis_provider = analysis_container.redis_client
        print("✓ 成功获取Redis客户端提供者")
        
        print("\n🎉 所有依赖注入测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 依赖注入测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_integration():
    """测试Flask集成"""
    try:
        print("\n正在测试Flask集成...")
        
        # 测试导入Flask相关模块
        from flask import Flask
        print("✓ 成功导入 Flask")
        
        from flask_cors import CORS
        print("✓ 成功导入 CORS")
        
        from flask_swagger_ui import get_swaggerui_blueprint
        print("✓ 成功导入 get_swaggerui_blueprint")
        
        # 测试导入API蓝图
        from app.web.api import api_blueprint
        print("✓ 成功导入 API蓝图")
        
        # 测试导入页面路由
        from app.web.page_router import page_blueprint
        print("✓ 成功导入 页面路由")
        
        print("🎉 Flask集成测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ Flask集成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("股票分析系统 - 依赖注入测试")
    print("=" * 60)
    
    # 运行测试
    di_success = test_dependency_injection()
    flask_success = test_flask_integration()
    
    print("\n" + "=" * 60)
    if di_success and flask_success:
        print("🎉 所有测试通过！系统可以正常启动。")
    else:
        print("❌ 部分测试失败，请检查错误信息。")
    print("=" * 60) 