# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  

import asyncio
from typing import List, TYPE_CHECKING

import config
import constant
from model.m_checkpoint import Checkpoint
from model.m_xiaohongshu import NoteUrlInfo
from pkg.tools import utils
from repo.platform_save_data import xhs as xhs_store
from ..help import parse_note_info_from_note_url
from .base_handler import BaseHandler

if TYPE_CHECKING:
    from ..client import XiaoHongShuClient
    from pkg.checkpoint.checkout_point import CheckpointManager
    from ..processors.note_processor import NoteProcessor
    from ..processors.comment_processor import CommentProcessor


class DetailHandler(BaseHandler):
    """Handles detail-based crawling operations for specified notes"""
    
    def __init__(
        self,
        xhs_client: "XiaoHongShuClient",
        checkpoint_manager: "CheckpointManager",
        note_processor: "NoteProcessor",
        comment_processor: "CommentProcessor"
    ):
        """
        Initialize detail handler
        
        Args:
            xhs_client: XiaoHongShu API client
            checkpoint_manager: Checkpoint manager for resume functionality
            note_processor: Note processing component
            comment_processor: Comment processing component
        """
        super().__init__(xhs_client, checkpoint_manager, note_processor, comment_processor)
    
    async def handle(self) -> None:
        """
        Handle detail-based crawling
        
        Returns:
            None
        """
        await self.get_specified_notes()
    
    async def get_specified_notes(self):
        """
        Get the information and comments of the specified post
        must be specified note_id, xsec_source, xsec_token
        Returns:
            None
        """
        utils.logger.info(
            "[DetailHandler.get_specified_notes] Begin get xiaohongshu specified notes"
        )

        checkpoint = Checkpoint(platform=constant.XHS_PLATFORM_NAME, mode="detail")

        # 如果开启了断点续爬，则加载检查点
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.XHS_PLATFORM_NAME,
                mode="detail",
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[DetailHandler.get_specified_notes] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
        await self.checkpoint_manager.save_checkpoint(checkpoint)

        xsec_tokens: List[str] = []
        need_get_comment_note_ids: List[str] = []
        get_note_detail_task_list: List[asyncio.Task] = []

        for full_note_url in config.XHS_SPECIFIED_NOTE_URL_LIST:
            note_url_info: NoteUrlInfo = parse_note_info_from_note_url(full_note_url)
            utils.logger.info(
                f"[DetailHandler.get_specified_notes] Parse note url info: {note_url_info}"
            )

            need_get_comment_note_ids.append(note_url_info.note_id)
            xsec_tokens.append(note_url_info.xsec_token)

            if await self.checkpoint_manager.check_note_is_crawled_in_checkpoint(
                checkpoint_id=checkpoint.id, note_id=note_url_info.note_id
            ):
                utils.logger.info(
                    f"[DetailHandler.get_specified_notes] Note {note_url_info.note_id} is already crawled, skip"
                )
                continue

            # 添加爬取帖子任务到检查点， 这个时候还没有爬取帖子，所以is_success_crawled为False
            # 后续 task_list 被asyncio.gather 并发调度之后，根据爬取note_id来更新is_success_crawled为True
            await self.checkpoint_manager.add_crawled_note_task_to_checkpoint(
                checkpoint_id=checkpoint.id,
                note_id=note_url_info.note_id,
                extra_params_info={
                    "xsec_source": note_url_info.xsec_source,
                    "xsec_token": note_url_info.xsec_token,
                },
            )

            crawler_task = self.note_processor.get_note_detail_async_task(
                note_id=note_url_info.note_id,
                xsec_source=note_url_info.xsec_source,
                xsec_token=note_url_info.xsec_token,
                checkpoint_id=checkpoint.id,
            )
            get_note_detail_task_list.append(crawler_task)

        note_details = await asyncio.gather(*get_note_detail_task_list)
        for note_detail in note_details:
            if note_detail:
                await xhs_store.update_xhs_note(note_detail)

        await self.comment_processor.batch_get_note_comments(
            need_get_comment_note_ids, xsec_tokens, checkpoint_id=checkpoint.id
        )
