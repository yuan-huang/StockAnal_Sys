# app/core/config.py
import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path='data/config.json'):
        self.config_path = Path(config_path)
        self.defaults = {
            'OPENAI_API_URL': 'https://api.openai.com/v1',
            'OPENAI_API_KEY': '',
            'OPENAI_API_MODEL': 'gpt-4o',
            'NEWS_MODEL': 'gpt-4o',
            'EMBEDDING_MODEL': 'text-embedding-3-small',
            'FUNCTION_CALL_MODEL': 'gpt-4o'
        }
        self.json_config = self._load_json_config()

    def _load_json_config(self):
        """从 JSON 文件加载配置，如果文件不存在则返回空字典"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # 如果文件损坏或不可读，返回空配置
                return {}
        return {}

    def get(self, key):
        """
        按以下优先级获取配置值:
        1. 环境变量
        2. JSON 配置文件
        3. 默认值
        """
        # 1. 从环境变量获取
        value = os.getenv(key)
        if value is not None:
            return value
        
        # 2. 从 JSON 文件获取
        value = self.json_config.get(key)
        if value is not None:
            return value
            
        # 3. 从默认值获取
        return self.defaults.get(key)

    def save(self, settings_dict):
        """将设置保存到 JSON 配置文件"""
        # 确保目录存在
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 读取现有配置以保留未更改的值
        current_config = self._load_json_config()
        current_config.update(settings_dict)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(current_config, f, ensure_ascii=False, indent=4)
        
        # 重新加载内存中的配置
        self.json_config = self._load_json_config()

    def get_all_configurable_settings(self):
        """获取所有可配置项的当前值，用于在UI中显示"""
        return {
            'OPENAI_API_URL': self.get('OPENAI_API_URL'),
            'OPENAI_API_KEY': self.get('OPENAI_API_KEY'),
            'OPENAI_API_MODEL': self.get('OPENAI_API_MODEL'),
            'NEWS_MODEL': self.get('NEWS_MODEL'),
            'EMBEDDING_MODEL': self.get('EMBEDDING_MODEL'),
            'FUNCTION_CALL_MODEL': self.get('FUNCTION_CALL_MODEL')
        }

# 创建一个全局可用的配置管理器实例
config_manager = ConfigManager()
