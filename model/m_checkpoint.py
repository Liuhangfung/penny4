from pydantic import BaseModel, Field
from typing import Optional


class Checkpoint(BaseModel):
    """
    检查点
    """

    # 主键
    id: Optional[str] = Field(None, description="检查点ID")

    # 基础字段
    platform: str = Field(
        ..., description="平台名称，如 xhs、dy、ks、bili、wb、tieba、zhihu"
    )
    mode: str = Field(..., description="模式：search/detail/creator")

    # 搜索模式相关字段
    current_search_keyword: Optional[str] = Field(None, description="当前搜索关键词")
    current_page: Optional[int] = Field(None, description="当前页码")

    # 创作者模式相关字段
    current_creator_id: Optional[str] = Field(None, description="当前创作者ID")

    # 帖子相关字段（搜索模式、详情模式、创作者模式都可能用到）
    current_note_id: Optional[str] = Field(None, description="当前帖子ID")
    current_note_comment_cursor: Optional[str] = Field(
        None, description="当前帖子评论游标"
    )
