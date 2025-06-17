from .checkout_point import (
    CheckpointJsonFileRepo,
    CheckpointRedisRepo,
    CheckpointManager,
)


def create_checkpoint_manager(
    storage_type: str = "file", **kwargs
) -> CheckpointManager:
    """创建检查点管理器的工厂函数

    Args:
        storage_type (str): 存储类型，支持 "file" 或 "redis"
        **kwargs: 额外的参数传递给对应的存储库构造函数

    Returns:
        CheckpointManager: 检查点管理器实例
    """
    if storage_type.lower() == "redis":
        repo = CheckpointRedisRepo(**kwargs)
    elif storage_type.lower() == "file":
        repo = CheckpointJsonFileRepo(**kwargs)
    else:
        raise ValueError(f"不支持的存储类型: {storage_type}")

    return CheckpointManager(repo)
