"""
加密工具 - API Key 安全存储
使用 Fernet 对称加密，密钥基于机器特征生成
"""

import base64
import hashlib
import uuid
from cryptography.fernet import Fernet


def get_machine_key() -> bytes:
    """
    基于机器特征生成加密密钥

    Returns:
        bytes: 32字节的密钥
    """
    # 获取机器的 MAC 地址作为种子
    mac = uuid.getnode()

    # 使用 SHA-256 哈希生成固定长度的密钥材料
    key_material = hashlib.sha256(str(mac).encode()).digest()

    # 转换为 Fernet 需要的格式（base64 编码）
    return base64.urlsafe_b64encode(key_material)


def encrypt_api_key(api_key: str) -> str:
    """
    加密 API Key

    Args:
        api_key: 明文 API Key

    Returns:
        str: 加密后的 API Key
    """
    if not api_key:
        return ""

    try:
        f = Fernet(get_machine_key())
        encrypted = f.encrypt(api_key.encode())
        return encrypted.decode()
    except Exception as e:
        print(f"加密失败: {e}")
        return ""


def decrypt_api_key(encrypted_key: str) -> str:
    """
    解密 API Key

    Args:
        encrypted_key: 加密的 API Key

    Returns:
        str: 明文 API Key
    """
    if not encrypted_key:
        return ""

    try:
        f = Fernet(get_machine_key())
        decrypted = f.decrypt(encrypted_key.encode())
        return decrypted.decode()
    except Exception as e:
        print(f"解密失败: {e}")
        return ""


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("加密工具测试")
    print("=" * 60)

    # 测试加密和解密
    test_key = "sk-test-1234567890abcdef"
    print(f"\n原始 API Key: {test_key}")

    # 加密
    encrypted = encrypt_api_key(test_key)
    print(f"加密后: {encrypted[:50]}..." if len(encrypted) > 50 else f"加密后: {encrypted}")

    # 解密
    decrypted = decrypt_api_key(encrypted)
    print(f"解密后: {decrypted}")

    # 验证
    if decrypted == test_key:
        print("\n✅ 加密/解密测试成功！")
    else:
        print("\n❌ 加密/解密测试失败！")

    print("=" * 60)
