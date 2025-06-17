import os
import sys
import asyncio
import time
from typing import Optional

# 添加项目根目录到sys.path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from model.m_checkpoint import Checkpoint
from pkg.checkpoint.checkout_point import (
    CheckpointRedisRepo,
    CheckpointJsonFileRepo,
    CheckpointManager,
)


def create_checkpoint_manager(
    storage_type: str = "redis", **kwargs
) -> CheckpointManager:
    """工厂函数，创建不同类型的检查点管理器

    Args:
        storage_type (str): 存储类型，'redis' 或 'file'
        **kwargs: 传递给存储库的参数

    Returns:
        CheckpointManager: 检查点管理器实例
    """
    if storage_type == "redis":
        repo = CheckpointRedisRepo(**kwargs)
    elif storage_type == "file":
        repo = CheckpointJsonFileRepo(**kwargs)
    else:
        raise ValueError(f"不支持的存储类型: {storage_type}")

    return CheckpointManager(repo)


async def test_redis_checkpoint_repo():
    """测试Redis检查点存储库"""
    print("=== 测试优化后的Redis检查点存储库 ===")

    # 创建Redis检查点存储库（使用缓存工厂）
    redis_repo = CheckpointRedisRepo(expire_time=3600)  # 1小时过期
    checkpoint_manager = CheckpointManager(redis_repo)

    # 创建测试检查点
    test_checkpoint = Checkpoint(
        platform="xhs",
        mode="search",
        current_search_keyword="测试关键词",
        current_page=1,
        current_note_id="test_note_123",
    )

    print("=== 测试保存检查点 ===")
    saved_checkpoint = await checkpoint_manager.save_checkpoint(test_checkpoint)
    print(f"保存的检查点ID: {saved_checkpoint.id}")

    # 测试TTL功能
    if saved_checkpoint.id:
        ttl = redis_repo.get_checkpoint_ttl("xhs", "search", saved_checkpoint.id)
        print(f"检查点TTL: {ttl}秒")

    print("\n=== 测试加载检查点（通过ID） ===")
    loaded_checkpoint = await checkpoint_manager.load_checkpoint(
        "xhs", "search", saved_checkpoint.id
    )
    if loaded_checkpoint:
        print(f"加载的检查点: {loaded_checkpoint.model_dump_json()}")

    print("\n=== 测试加载最新检查点（不指定ID） ===")
    latest_checkpoint = await checkpoint_manager.load_checkpoint("xhs", "search")
    if latest_checkpoint:
        print(f"最新检查点: {latest_checkpoint.model_dump_json()}")

    print("\n=== 测试更新检查点 ===")
    if latest_checkpoint:
        latest_checkpoint.current_page = 2
        latest_checkpoint.current_search_keyword = "更新后的关键词"
        updated_checkpoint = await checkpoint_manager.update_checkpoint(
            latest_checkpoint
        )
        print(f"更新后的检查点: {updated_checkpoint.model_dump_json()}")

    print("\n=== 测试删除检查点 ===")
    if saved_checkpoint.id:
        await checkpoint_manager.delete_checkpoint("xhs", "search", saved_checkpoint.id)
        print("检查点已删除")

        # 验证删除
        deleted_checkpoint = await checkpoint_manager.load_checkpoint(
            "xhs", "search", saved_checkpoint.id
        )
        print(f"删除后的查询结果: {deleted_checkpoint}")


async def test_json_file_checkpoint_repo():
    """测试JSON文件检查点存储库"""
    print("\n\n=== 测试JSON文件检查点存储库 ===")

    # 创建JSON文件检查点存储库
    json_repo = CheckpointJsonFileRepo(cache_dir="data/test_checkpoint")
    checkpoint_manager = CheckpointManager(json_repo)

    # 创建测试检查点
    test_checkpoint = Checkpoint(
        platform="dy",  # 使用不同的平台进行测试
        mode="creator",
        current_creator_id="test_creator_456",
        current_page=1,
        current_note_id="dy_note_789",
    )

    print("=== 测试保存检查点到文件 ===")
    saved_checkpoint = await checkpoint_manager.save_checkpoint(test_checkpoint)
    print(f"保存的检查点ID: {saved_checkpoint.id}")
    print(
        f"检查点文件应该保存在: data/test_checkpoint/{test_checkpoint.platform}_{test_checkpoint.mode}_{saved_checkpoint.id}.json"
    )

    print("\n=== 测试从文件加载检查点（通过ID） ===")
    loaded_checkpoint = await checkpoint_manager.load_checkpoint(
        "dy", "creator", saved_checkpoint.id
    )
    if loaded_checkpoint:
        print(f"从文件加载的检查点: {loaded_checkpoint.model_dump_json()}")

    print("\n=== 测试从文件加载最新检查点（不指定ID） ===")
    latest_checkpoint = await checkpoint_manager.load_checkpoint("dy", "creator")
    if latest_checkpoint:
        print(f"最新检查点（基于文件修改时间）: {latest_checkpoint.model_dump_json()}")

    # 创建第二个检查点，测试最新检查点的选择
    test_checkpoint2 = Checkpoint(
        platform="dy",
        mode="creator",
        current_creator_id="test_creator_789",
        current_page=2,
        current_note_id="dy_note_456",
    )

    print("\n=== 测试保存第二个检查点 ===")
    await asyncio.sleep(1)  # 确保时间戳不同
    saved_checkpoint2 = await checkpoint_manager.save_checkpoint(test_checkpoint2)
    print(f"第二个检查点ID: {saved_checkpoint2.id}")

    print("\n=== 测试获取最新检查点（应该是较新的） ===")
    latest_checkpoint = await checkpoint_manager.load_checkpoint("dy", "creator")
    if latest_checkpoint:
        print(f"最新检查点ID: {latest_checkpoint.id}")
        print(f"最新检查点创作者ID: {latest_checkpoint.current_creator_id}")

    print("\n=== 测试更新文件检查点 ===")
    if latest_checkpoint:
        latest_checkpoint.current_page = 5
        latest_checkpoint.current_creator_id = "updated_creator_999"
        updated_checkpoint = await checkpoint_manager.update_checkpoint(
            latest_checkpoint
        )
        print(f"更新后的检查点: {updated_checkpoint.model_dump_json()}")

    print("\n=== 测试删除文件检查点 ===")
    if saved_checkpoint.id:
        await checkpoint_manager.delete_checkpoint("dy", "creator", saved_checkpoint.id)
        print(f"检查点 {saved_checkpoint.id} 已删除")

        # 验证删除
        deleted_checkpoint = await checkpoint_manager.load_checkpoint(
            "dy", "creator", saved_checkpoint.id
        )
        print(f"删除后的查询结果: {deleted_checkpoint}")

    # 清理第二个检查点
    if saved_checkpoint2.id:
        await checkpoint_manager.delete_checkpoint(
            "dy", "creator", saved_checkpoint2.id
        )
        print(f"检查点 {saved_checkpoint2.id} 也已删除")


async def test_factory_functions():
    """测试工厂函数创建不同类型的检查点管理器"""
    print("\n\n=== 测试工厂函数 ===")

    # 使用工厂函数创建Redis管理器
    redis_manager = create_checkpoint_manager("redis", expire_time=1800)
    print("✅ Redis检查点管理器创建成功")

    # 使用工厂函数创建文件管理器
    file_manager = create_checkpoint_manager("file", cache_dir="data/factory_test")
    print("✅ 文件检查点管理器创建成功")

    # 测试创建检查点
    test_checkpoint = Checkpoint(
        platform="test",
        mode="factory",
        current_search_keyword="工厂测试",
        current_page=1,
    )

    # 分别保存到两个存储后端
    redis_saved = await redis_manager.save_checkpoint(test_checkpoint)
    print(f"✅ Redis保存成功，ID: {redis_saved.id}")

    test_checkpoint.id = None  # 重置ID以创建新检查点
    file_saved = await file_manager.save_checkpoint(test_checkpoint)
    print(f"✅ 文件保存成功，ID: {file_saved.id}")

    # 清理测试数据
    if redis_saved.id:
        await redis_manager.delete_checkpoint("test", "factory", redis_saved.id)
    if file_saved.id:
        await file_manager.delete_checkpoint("test", "factory", file_saved.id)
    print("✅ 测试数据清理完成")


async def run_all_tests():
    """运行所有测试"""
    print("开始运行检查点存储库测试...")
    await test_redis_checkpoint_repo()
    await test_json_file_checkpoint_repo()
    await test_factory_functions()

    print("\n🎉 所有测试完成！")
    print("主要功能验证：")
    print("✅ Redis存储库 - 统一缓存接口")
    print("✅ JSON文件存储库 - 本地文件管理")
    print("✅ 工厂函数 - 灵活的存储库创建")
    print("✅ TTL查询 - Redis专用功能")
    print("✅ 最新检查点查询 - 两种存储都支持")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
