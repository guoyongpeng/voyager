"""
配置管理器 - 管理应用配置
读取和保存 config.json，支持 API Key 加密存储
"""

import json
import os
from typing import Dict, Optional, Any
from .utils.crypto import encrypt_api_key, decrypt_api_key
from .constants import CONFIG_PATH


class ConfigManager:
    """配置管理器（单例模式）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """初始化配置管理器"""
        if self._initialized:
            return

        self.config_path = CONFIG_PATH
        self.config = self._load_config()
        self._initialized = True

    def _load_config(self) -> Dict:
        """
        加载配置文件

        Returns:
            Dict: 配置字典
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(self.config_path):
            default_config = self._get_default_config()
            self._save_config(default_config)
            return default_config

        # 读取配置文件
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"配置文件读取失败: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """
        获取默认配置

        Returns:
            Dict: 默认配置字典
        """
        return {
            "version": "1.0.0",
            "ai": {
                "provider": "",  # 空表示未配置
                "api_keys": {},
                "api_config": {
                    "zhipu": {
                        "model": "glm-4",
                        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions"
                    },
                    "tongyi": {
                        "model": "qwen-turbo",
                        "base_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
                    },
                    "wenxin": {
                        "model": "ERNIE-Bot-turbo",
                        "base_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
                    }
                },
                "temperature": 0.8,
                "max_tokens": 2000
            },
            "ui": {
                "theme": "light",
                "animation_enabled": True,
                "window_geometry": {
                    "width": 1200,
                    "height": 800
                }
            },
            "game": {
                "xp_curve": "exponential",
                "level_multiplier": 1.5,
                "base_xp_per_level": 100
            },
            "data": {
                "auto_backup": True,
                "backup_interval_days": 7,
                "last_backup": None
            }
        }

    def _save_config(self, config: Optional[Dict] = None):
        """
        保存配置到文件

        Args:
            config: 要保存的配置，如果为 None 则保存当前配置
        """
        if config is None:
            config = self.config

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"配置文件保存失败: {e}")

    def save(self):
        """保存当前配置"""
        self._save_config()

    # ==================== AI 配置相关 ====================

    def has_ai_key(self, provider: Optional[str] = None) -> bool:
        """
        检查是否配置了 AI Key

        Args:
            provider: AI 提供商名称，如果为 None 则检查当前提供商

        Returns:
            bool: True 表示已配置
        """
        if provider is None:
            provider = self.config.get('ai', {}).get('provider', '')

        if not provider:
            return False

        api_keys = self.config.get('ai', {}).get('api_keys', {})
        return provider in api_keys and bool(api_keys[provider])

    def get_ai_provider(self) -> str:
        """
        获取当前 AI 提供商

        Returns:
            str: 提供商名称，如 'zhipu'
        """
        return self.config.get('ai', {}).get('provider', '')

    def set_ai_provider(self, provider: str):
        """
        设置 AI 提供商

        Args:
            provider: 提供商名称
        """
        if 'ai' not in self.config:
            self.config['ai'] = {}

        self.config['ai']['provider'] = provider
        self.save()

    def get_api_key(self, provider: Optional[str] = None) -> str:
        """
        获取 API Key（解密后）

        Args:
            provider: 提供商名称，如果为 None 则使用当前提供商

        Returns:
            str: 解密后的 API Key
        """
        if provider is None:
            provider = self.get_ai_provider()

        if not provider:
            return ""

        api_keys = self.config.get('ai', {}).get('api_keys', {})
        encrypted_key = api_keys.get(provider, '')

        if not encrypted_key:
            return ""

        return decrypt_api_key(encrypted_key)

    def set_api_key(self, provider: str, api_key: str):
        """
        设置 API Key（加密后存储）

        Args:
            provider: 提供商名称
            api_key: API Key 明文
        """
        if 'ai' not in self.config:
            self.config['ai'] = {}

        if 'api_keys' not in self.config['ai']:
            self.config['ai']['api_keys'] = {}

        # 加密 API Key
        encrypted = encrypt_api_key(api_key)
        self.config['ai']['api_keys'][provider] = encrypted

        # 如果当前没有设置提供商，自动设置为这个
        if not self.config['ai'].get('provider'):
            self.config['ai']['provider'] = provider

        self.save()

    def get_ai_config(self, provider: Optional[str] = None) -> Dict:
        """
        获取 AI 配置

        Args:
            provider: 提供商名称

        Returns:
            Dict: AI 配置
        """
        if provider is None:
            provider = self.get_ai_provider()

        api_configs = self.config.get('ai', {}).get('api_config', {})
        return api_configs.get(provider, {})

    # ==================== 通用配置相关 ====================

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项（支持点号分隔的路径）

        Args:
            key: 配置键，如 "ui.theme" 或 "game.xp_curve"
            default: 默认值

        Returns:
            Any: 配置值
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        设置配置项（支持点号分隔的路径）

        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config

        # 导航到最后一级的父级
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # 设置值
        config[keys[-1]] = value
        self.save()

    def reset(self):
        """重置为默认配置"""
        self.config = self._get_default_config()
        self.save()


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("配置管理器测试")
    print("=" * 60)

    # 创建配置管理器
    config = ConfigManager()

    print("\n【1. 测试基本配置】")
    print(f"应用版本: {config.get('version')}")
    print(f"UI 主题: {config.get('ui.theme')}")
    print(f"经验曲线: {config.get('game.xp_curve')}")

    print("\n【2. 测试 AI 配置】")
    print(f"是否配置 AI: {config.has_ai_key()}")
    print(f"当前提供商: {config.get_ai_provider()}")

    # 测试设置 API Key
    print("\n【3. 测试 API Key 加密存储】")
    test_key = "sk-test-1234567890"
    config.set_api_key('zhipu', test_key)
    print(f"设置 API Key: {test_key}")

    # 读取 API Key
    retrieved_key = config.get_api_key('zhipu')
    print(f"读取 API Key: {retrieved_key}")
    print(f"验证: {'✅ 成功' if retrieved_key == test_key else '❌ 失败'}")

    print(f"是否配置 AI: {config.has_ai_key()}")

    print("\n【4. 测试配置修改】")
    config.set('ui.theme', 'dark')
    print(f"修改主题为: {config.get('ui.theme')}")

    print("\n" + "=" * 60)
    print("✅ 配置管理器测试完成！")
    print(f"配置文件位置: {config.config_path}")
    print("=" * 60)
