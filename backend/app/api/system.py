# -*- coding: utf-8 -*-
"""
系统管理API接口
包含系统重启、配置管理等接口
"""

from flask_api import APIBlueprint, request, status
import subprocess
import os
import traceback
import logging

# 创建蓝图
system_blueprint = APIBlueprint('system', __name__)

@system_blueprint.route('/restart_system', methods=['POST'])
def restart_system():
    """API endpoint to restart the application."""
    logging.info("接收到重启系统的API请求")
    try:
        # 查找 start.sh 脚本的路径
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'start.sh'))
        
        if not os.path.exists(script_path):
            logging.error(f"重启脚本未找到: {script_path}")
            return {'success': False, 'error': '重启脚本未找到'}, status.HTTP_500_INTERNAL_SERVER_ERROR

        # 在后台启动重启命令
        subprocess.Popen(['bash', script_path, 'restart'])
        
        logging.info(f"成功执行重启脚本: {script_path} restart")
        return {'success': True, 'message': '重启指令已发送'}

    except Exception as e:
        logging.error(f"执行重启时发生异常: {traceback.format_exc()}")
        return {'success': False, 'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR 