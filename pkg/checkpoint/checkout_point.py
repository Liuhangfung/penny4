import os
import sys
from abc import abstractmethod
import logging
from typing import Optional
import pathlib
import json
import time
from datetime import datetime

import aiofiles

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(project_root)
sys.path.append(parent_dir)


import config
from model.m_checkpoint import Checkpoint
from pkg.cache.abs_cache import AbstractCache
from pkg.cache.cache_factory import CacheFactory

logger = logging.getLogger(__name__)


def generate_checkpoint_id() -> str:
    """生成基于当前日期时间的检查点ID

    Returns:
        str: 格式为YYYYMMDDHHMMSS的时间戳字符串，如20250617183823
    """
    return datetime.now().strftime("%Y%m%d%H%M%S")


class BaseCheckpointRepo:
    @abstractmethod
    async def save_checkpoint(self, checkpoint: Checkpoint) -> Checkpoint:
        """保存检查点

        Args:
            checkpoint (Checkpoint): 检查点

        Returns:
            Checkpoint: 保存后的检查点
        """
        pass

    @abstractmethod
    async def load_checkpoint(
        self, platform: str, mode: str, id: Optional[str] = None
    ) -> Optional[Checkpoint]:
        """加载检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID

        Returns:
            Optional[Checkpoint]: 加载后的检查点
        """
        pass

    @abstractmethod
    async def delete_checkpoint(self, platform: str, mode: str, id: str):
        """删除检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID
        """
        pass

    @abstractmethod
    async def update_checkpoint(self, checkpoint: Checkpoint):
        """更新检查点，如果检查点不存在，则保存检查点

        Args:
            checkpoint (Checkpoint): 检查点
        """
        pass


class CheckpointJsonFileRepo(BaseCheckpointRepo):

    def __init__(self, cache_dir: str = "data/checkpoint"):
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def save_checkpoint(self, checkpoint: Checkpoint):
        """保存检查点

        Args:
            checkpoint (Checkpoint): 检查点
        """
        checkpoint_file = (
            self.cache_dir
            / f"{checkpoint.platform}_{checkpoint.mode}_{checkpoint.id}.json"
        )
        async with aiofiles.open(checkpoint_file, "w") as f:
            await f.write(json.dumps(checkpoint.model_dump()))

    async def load_checkpoint(
        self, platform: str, mode: str, id: Optional[str] = None
    ) -> Optional[Checkpoint]:
        """加载检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID
        """
        if id is None:
            # 模糊查询，获取最新的检查点
            checkpoint_files = list(self.cache_dir.glob(f"{platform}_{mode}*.json"))
            if not checkpoint_files:
                return None
            checkpoint_file = max(checkpoint_files, key=lambda x: x.stat().st_mtime)
        else:
            checkpoint_file = self.cache_dir / f"{platform}_{mode}_{id}.json"
            # 检查文件是否存在
            if not checkpoint_file.exists():
                return None

        async with aiofiles.open(checkpoint_file, "r") as f:
            return Checkpoint.model_validate_json(await f.read())

    async def delete_checkpoint(self, platform: str, mode: str, id: str):
        """删除检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID
        """
        checkpoint_file = self.cache_dir / f"{platform}_{mode}_{id}.json"
        if checkpoint_file.exists():
            checkpoint_file.unlink()

    async def update_checkpoint(self, checkpoint: Checkpoint):
        """更新检查点，如果检查点不存在，则保存检查点

        Args:
            checkpoint (Checkpoint): 检查点
        """
        if (
            await self.load_checkpoint(
                checkpoint.platform, checkpoint.mode, checkpoint.id
            )
            is None
        ):
            return await self.save_checkpoint(checkpoint)
        else:
            return await self.save_checkpoint(checkpoint)


class CheckpointRedisRepo(BaseCheckpointRepo):
    """基于Redis的检查点存储库

    使用项目的缓存工厂创建Redis客户端，支持：
    - 自动过期时间管理
    - 统一的缓存接口
    - 序列化/反序列化自动处理
    """

    def __init__(
        self, key_prefix: str = "checkpoint", expire_time: int = 86400 * 7
    ):  # 默认7天过期
        self.key_prefix = key_prefix
        self.expire_time = expire_time  # 检查点过期时间（秒）
        self.redis_cache_client: AbstractCache = CacheFactory.create_cache(
            cache_type=config.CACHE_TYPE_REDIS
        )

    def _get_checkpoint_key(self, platform: str, mode: str, id: str) -> str:
        """生成检查点的Redis key"""
        return f"{self.key_prefix}:{platform}:{mode}:{id}"

    def _get_timestamp_key(self, platform: str, mode: str, id: str) -> str:
        """生成时间戳的Redis key，用于记录检查点的创建/更新时间"""
        return f"{self.key_prefix}:timestamp:{platform}:{mode}:{id}"

    def get_checkpoint_ttl(self, platform: str, mode: str, id: str) -> int:
        """获取检查点的剩余生存时间

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID

        Returns:
            int: 剩余生存时间（秒），-1表示永不过期，-2表示键不存在
        """
        checkpoint_key = self._get_checkpoint_key(platform, mode, id)
        return self.redis_cache_client.ttl(checkpoint_key)

    async def save_checkpoint(self, checkpoint: Checkpoint) -> Checkpoint:
        """保存检查点

        Args:
            checkpoint (Checkpoint): 检查点

        Returns:
            Checkpoint: 保存后的检查点
        """
        if checkpoint.id is None:
            checkpoint.id = generate_checkpoint_id()

        checkpoint_key = self._get_checkpoint_key(
            checkpoint.platform, checkpoint.mode, checkpoint.id
        )
        timestamp_key = self._get_timestamp_key(
            checkpoint.platform, checkpoint.mode, checkpoint.id
        )

        # 使用AbstractCache接口存储检查点数据
        self.redis_cache_client.set(
            checkpoint_key, checkpoint.model_dump(), self.expire_time
        )

        # 存储时间戳用于后续查询最新检查点
        current_timestamp = int(time.time())
        self.redis_cache_client.set(timestamp_key, current_timestamp, self.expire_time)

        return checkpoint

    async def load_checkpoint(
        self, platform: str, mode: str, id: Optional[str] = None
    ) -> Optional[Checkpoint]:
        """加载检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID，如果为None则获取最新的检查点

        Returns:
            Optional[Checkpoint]: 加载后的检查点
        """
        if id is None:
            # 模糊查询，获取最新的检查点
            pattern = f"{self.key_prefix}:{platform}:{mode}:*"
            keys = self.redis_cache_client.keys(pattern)

            if not keys:
                return None

            # 获取每个检查点的时间戳，找到最新的
            latest_key = None
            latest_timestamp = 0

            for key in keys:
                # 从key中提取id
                checkpoint_id = key.split(":")[-1]
                timestamp_key = self._get_timestamp_key(platform, mode, checkpoint_id)
                timestamp = self.redis_cache_client.get(timestamp_key)

                if timestamp and int(timestamp) > latest_timestamp:
                    latest_timestamp = int(timestamp)
                    latest_key = key

            if latest_key is None:
                return None

            # 获取最新检查点的数据
            checkpoint_data = self.redis_cache_client.get(latest_key)
        else:
            # 精确查询
            checkpoint_key = self._get_checkpoint_key(platform, mode, id)
            checkpoint_data = self.redis_cache_client.get(checkpoint_key)

        if checkpoint_data is None:
            return None

        # 直接验证数据（AbstractCache已经处理了序列化）
        return Checkpoint.model_validate(checkpoint_data)

    async def delete_checkpoint(self, platform: str, mode: str, id: str):
        """删除检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID
        """
        checkpoint_key = self._get_checkpoint_key(platform, mode, id)
        timestamp_key = self._get_timestamp_key(platform, mode, id)

        # 删除检查点数据和时间戳
        self.redis_cache_client.delete(checkpoint_key)
        self.redis_cache_client.delete(timestamp_key)

    async def update_checkpoint(self, checkpoint: Checkpoint):
        """更新检查点，如果检查点不存在，则保存检查点

        Args:
            checkpoint (Checkpoint): 检查点
        """
        if checkpoint.id is None:
            checkpoint.id = generate_checkpoint_id()

        # 检查检查点是否存在
        existing_checkpoint = await self.load_checkpoint(
            checkpoint.platform, checkpoint.mode, checkpoint.id
        )

        if existing_checkpoint is None:
            # 检查点不存在，创建新的
            await self.save_checkpoint(checkpoint)
        else:
            # 检查点存在，更新数据
            checkpoint_key = self._get_checkpoint_key(
                checkpoint.platform, checkpoint.mode, checkpoint.id
            )
            timestamp_key = self._get_timestamp_key(
                checkpoint.platform, checkpoint.mode, checkpoint.id
            )

            # 使用AbstractCache接口更新检查点数据
            self.redis_cache_client.set(
                checkpoint_key, checkpoint.model_dump(), self.expire_time
            )

            # 更新时间戳
            current_timestamp = int(time.time())
            self.redis_cache_client.set(
                timestamp_key, current_timestamp, self.expire_time
            )


class CheckpointManager:
    def __init__(self, checkpoint_repo: BaseCheckpointRepo):
        self.checkpoint_repo = checkpoint_repo

    async def save_checkpoint(self, checkpoint: Checkpoint) -> Checkpoint:
        """保存检查点

        Args:
            checkpoint (Checkpoint): 检查点
        """
        logger.info(f"保存检查点: {checkpoint.model_dump_json()}")
        if checkpoint.id is None:
            checkpoint.id = generate_checkpoint_id()

        await self.checkpoint_repo.save_checkpoint(checkpoint)
        return await self.load_checkpoint(
            checkpoint.platform, checkpoint.mode, checkpoint.id
        )

    async def update_checkpoint(self, checkpoint: Checkpoint) -> Checkpoint:
        """更新检查点

        Args:
            checkpoint (Checkpoint): 检查点
        """
        logger.info(f"更新检查点: {checkpoint.model_dump_json()}")
        await self.checkpoint_repo.update_checkpoint(checkpoint)
        return await self.load_checkpoint(
            checkpoint.platform, checkpoint.mode, checkpoint.id
        )

    async def load_checkpoint(
        self, platform: str, mode: str, id: Optional[str] = None
    ) -> Optional[Checkpoint]:
        """加载检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID
        """
        logger.info(f"加载检查点: {platform}, {mode}, {id}")
        return await self.checkpoint_repo.load_checkpoint(platform, mode, id)

    async def delete_checkpoint(self, platform: str, mode: str, id: str):
        """删除检查点

        Args:
            platform (str): 平台
            mode (str): 模式
            id (str): 检查点ID
        """
        logger.info(f"删除检查点: {platform}, {mode}, {id}")
        return await self.checkpoint_repo.delete_checkpoint(platform, mode, id)
