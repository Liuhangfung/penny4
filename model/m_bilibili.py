from pydantic import BaseModel, Field


class CreatorQueryResponse(BaseModel):
    """
    查询创作者主页响应
    """

    nickname: str = Field(..., title="昵称", description="昵称")
    avatar: str = Field(default="", title="头像", description="头像")
    description: str = Field(default="", title="描述", description="描述")
    user_id: str = Field(default="", title="用户ID", description="用户ID")
    follower_count: str = Field(default="", title="粉丝数", description="粉丝数")
    following_count: str = Field(default="", title="关注数", description="关注数")
    content_count: str = Field(default="", title="作品数", description="作品数")



class VideoIdInfo(BaseModel):
    """
    批量获取视频评论的请求参数
    """
    aid: int = Field(..., title="B站的视频ID,用户不可见的，通常在一些列表接口中返回的，爬取评论需要这个ID")
    bvid: str = Field(..., title="B站的视频ID，用户可见的")
