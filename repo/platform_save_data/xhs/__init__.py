# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。


# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/1/14 17:34
# @Desc    :
import json
from typing import Dict, List

import config
from base.base_crawler import AbstractStore
from model.m_xhs import XhsComment, XhsCreator, XhsNote
from pkg.tools import utils
from repo.platform_save_data.xhs.xhs_store_impl import (
    XhsCsvStoreImplement,
    XhsDbStoreImplement,
    XhsJsonStoreImplement,
)
from var import source_keyword_var


class XhsStoreFactory:
    STORES = {
        "csv": XhsCsvStoreImplement,
        "db": XhsDbStoreImplement,
        "json": XhsJsonStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = XhsStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError(
                "[XhsStoreFactory.create_store] Invalid save option only supported csv or db or json ..."
            )
        return store_class()


def _get_video_url_arr(note_item: Dict) -> List[str]:
    """获取视频URL数组（内部辅助函数）"""
    if note_item.get("type") != "video":
        return []

    video_arr = []
    origin_video_key = (
        note_item.get("video", {}).get("consumer", {}).get("origin_video_key", "")
    )
    if not origin_video_key:
        origin_video_key = (
            note_item.get("video", {}).get("consumer", {}).get("originVideoKey", "")
        )

    if not origin_video_key:
        videos = (
            note_item.get("video", {})
            .get("media", {})
            .get("stream", {})
            .get("h264", [])
        )
        if isinstance(videos, list):
            video_arr = [v.get("master_url", "") for v in videos if v.get("master_url")]
    else:
        video_arr = [f"http://sns-video-bd.xhscdn.com/{origin_video_key}"]

    return video_arr


async def batch_update_xhs_notes(notes: List[XhsNote]):
    """
    批量更新小红书笔记
    Args:
        notes: 笔记列表
    """
    if not notes:
        return

    for note_item in notes:
        await update_xhs_note(note_item)


async def update_xhs_note(note_item: XhsNote):
    """
    更新小红书笔记
    Args:
        note_item: 笔记对象
    """
    note_item.source_keyword = source_keyword_var.get()
    local_db_item = note_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    print_title = note_item.title[:30] or note_item.desc[:30]
    utils.logger.info(
        f"[store.xhs.update_xhs_note] xhs note, id: {note_item.note_id}, title: {print_title}"
    )
    await XhsStoreFactory.create_store().store_content(local_db_item)


async def batch_update_xhs_note_comments(comments: List[XhsComment]):
    """
    批量更新小红书笔记评论
    Args:
        comments: 评论列表
    """
    if not comments:
        return

    for comment_item in comments:
        await update_xhs_note_comment(comment_item)


async def batch_update_xhs_note_comments_from_dict(
    note_id: str, comments: List[Dict], note_xsec_token: str, root_comment_id: str = ""
):
    """
    从字典批量更新小红书笔记评论（兼容旧接口）
    Args:
        note_id: 笔记ID
        comments: 评论数据列表
        note_xsec_token: xsec_token
        root_comment_id: 根评论ID
    """
    if not comments:
        return

    for comment_item in comments:
        await update_xhs_note_comment_from_dict(
            note_id, comment_item, note_xsec_token, root_comment_id
        )


async def update_xhs_note_comment(comment_item: XhsComment):
    """
    更新小红书笔记评论
    Args:
        comment_item: 评论对象
    """
    local_db_item = comment_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    utils.logger.info(
        f"[store.xhs.update_xhs_note_comment] xhs note comment, note_id: {comment_item.note_id}, comment_id: {comment_item.comment_id}"
    )
    await XhsStoreFactory.create_store().store_comment(local_db_item)


async def update_xhs_note_comment_from_dict(
    note_id: str, comment_item: Dict, note_xsec_token: str, root_comment_id: str = ""
):
    """
    从字典更新小红书笔记评论（兼容旧接口）
    Args:
        note_id: 笔记ID
        comment_item: 原始评论数据字典
        note_xsec_token: xsec_token
        root_comment_id: 根评论ID
    """
    user_info = comment_item.get("user_info", {})
    comment_id = comment_item.get("id", "")
    comment_pictures = [
        item.get("url_default", "") for item in comment_item.get("pictures", [])
    ]
    target_comment = comment_item.get("target_comment", {})

    xhs_comment = XhsComment(
        comment_id=comment_id,
        parent_comment_id=root_comment_id,
        target_comment_id=target_comment.get("id", ""),
        note_id=note_id,
        content=comment_item.get("content", ""),
        create_time=str(comment_item.get("create_time", "")),
        ip_location=comment_item.get("ip_location", ""),
        sub_comment_count=str(comment_item.get("sub_comment_count", "")),
        like_count=str(comment_item.get("like_count", "")),
        pictures=",".join(comment_pictures),
        note_url=f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={note_xsec_token}&xsec_source=pc_search",
        user_id=user_info.get("user_id", ""),
        nickname=user_info.get("nickname", ""),
        avatar=user_info.get("image", ""),
    )

    await update_xhs_note_comment(xhs_comment)


async def save_creator(creator: XhsCreator):
    """
    保存小红书创作者信息
    Args:
        creator: 创作者对象
    """
    if not creator:
        return

    local_db_item = creator.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})

    utils.logger.info(
        f"[store.xhs.save_creator] creator: {creator.user_id} - {creator.nickname}"
    )
    await XhsStoreFactory.create_store().store_creator(local_db_item)


async def save_creator_from_dict(user_id: str, creator: Dict):
    """
    从字典保存小红书创作者信息（兼容旧接口）
    Args:
        user_id: 用户ID
        creator: 原始创作者数据字典
    """
    user_info = creator.get("basicInfo", {})

    follows = ""
    fans = ""
    interaction = ""
    for i in creator.get("interactions", []):
        if i.get("type") == "follows":
            follows = str(i.get("count", ""))
        elif i.get("type") == "fans":
            fans = str(i.get("count", ""))
        elif i.get("type") == "interaction":
            interaction = str(i.get("count", ""))

    xhs_creator = XhsCreator(
        user_id=user_id,
        nickname=user_info.get("nickname", ""),
        gender="女" if user_info.get("gender") == 1 else "男",
        avatar=user_info.get("images", ""),
        desc=user_info.get("desc", ""),
        ip_location=user_info.get("ipLocation", ""),
        follows=follows,
        fans=fans,
        interaction=interaction,
        tag_list=json.dumps(
            {tag.get("tagType"): tag.get("name") for tag in creator.get("tags", [])},
            ensure_ascii=False,
        ),
    )

    await save_creator(xhs_creator)
