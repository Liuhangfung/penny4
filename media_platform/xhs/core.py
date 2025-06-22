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
import random
from asyncio import Task
from typing import Callable, Dict, List, Optional

from tenacity import RetryError

import config
from config.base_config import PER_NOTE_MAX_COMMENTS_COUNT
import constant
from base.base_crawler import AbstractCrawler
from model.m_checkpoint import Checkpoint
from model.m_xiaohongshu import CreatorUrlInfo, NoteUrlInfo
from pkg.account_pool.pool import AccountWithIpPoolManager
from pkg.checkpoint import create_checkpoint_manager
from pkg.checkpoint.checkout_point import CheckpointManager
from pkg.proxy.proxy_ip_pool import ProxyIpPool, create_ip_pool
from pkg.tools import utils
from repo.platform_save_data import xhs as xhs_store
from var import crawler_type_var, source_keyword_var

from .client import XiaoHongShuClient
from .exception import DataFetchError
from .field import FeedType, SearchSortType
from .help import parse_creator_info_from_creator_url, parse_note_info_from_note_url


class XiaoHongShuCrawler(AbstractCrawler):
    def __init__(self) -> None:
        self.xhs_client = XiaoHongShuClient()
        self.checkpoint_manager: CheckpointManager = create_checkpoint_manager()

        # 限制并发数
        self.crawler_note_task_semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        self.crawler_note_comment_semaphore = asyncio.Semaphore(
            config.MAX_CONCURRENCY_NUM
        )

    async def async_initialize(self):
        """
        Asynchronous Initialization
        Returns:

        """
        utils.logger.info(
            "[XiaoHongShuCrawler.async_initialize] Begin async initialize"
        )

        # 账号池和IP池的初始化
        proxy_ip_pool: Optional[ProxyIpPool] = None
        if config.ENABLE_IP_PROXY:
            # xhs对代理验证还行，可以选择长时长的IP，比如30分钟一个IP
            # 快代理：私密代理->按IP付费->专业版->IP有效时长为30分钟, 购买地址：https://www.kuaidaili.com/?ref=ldwkjqipvz6c
            proxy_ip_pool = await create_ip_pool(
                config.IP_PROXY_POOL_COUNT, enable_validate_ip=True
            )

        # 初始化账号池
        account_with_ip_pool = AccountWithIpPoolManager(
            platform_name=constant.XHS_PLATFORM_NAME,
            account_save_type=config.ACCOUNT_POOL_SAVE_TYPE,
            proxy_ip_pool=proxy_ip_pool,
        )
        await account_with_ip_pool.async_initialize()

        self.xhs_client.account_with_ip_pool = account_with_ip_pool
        await self.xhs_client.update_account_info()

        # 设置爬虫类型
        crawler_type_var.set(config.CRAWLER_TYPE)

    async def start(self) -> None:
        """
        Start the crawler
        Returns:

        """
        if config.CRAWLER_TYPE == "search":
            # Search for notes and retrieve their comment information.
            await self.search()
        elif config.CRAWLER_TYPE == "detail":
            # Get the information and comments of the specified post
            await self.get_specified_notes()
        elif config.CRAWLER_TYPE == "creator":
            # Get creator's information and their notes and comments
            await self.get_creators_and_notes()
        elif config.CRAWLER_TYPE == "homefeed":
            # Get homefeed notes and comments
            await self.get_homefeed_notes()
        else:
            pass

        utils.logger.info("[XiaoHongShuCrawler.start] Xhs Crawler finished ...")

    @staticmethod
    def _get_search_keyword_list() -> List[str]:
        """
        Get search keyword list

        Returns:
            List[str]: search keyword list
        """
        return config.KEYWORDS.split(",")

    def _find_keyword_index_in_keyword_list(self, keyword: str) -> int:
        """
        Find keyword index in keyword list

        Args:
            keyword: keyword

        Returns:
            int: keyword index
        """
        keyword_list = self._get_search_keyword_list()
        for index, keyword_item in enumerate(keyword_list):
            if keyword_item == keyword:
                return index
        return -1

    async def search(self) -> None:
        """
        Search for notes and retrieve their comment information.
        Returns:

        """
        utils.logger.info(
            "[XiaoHongShuCrawler.search] Begin search xiaohongshu keywords"
        )
        keyword_list = self._get_search_keyword_list()
        checkpoint = Checkpoint(
            platform=constant.XHS_PLATFORM_NAME, mode="search", current_search_page=1
        )

        # 如果开启了断点续爬，则加载检查点
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.XHS_PLATFORM_NAME,
                mode="search",
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[XiaoHongShuCrawler.search] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
                keyword_index = self._find_keyword_index_in_keyword_list(
                    lastest_checkpoint.current_search_keyword
                )
                if keyword_index == -1:
                    utils.logger.error(
                        f"[XiaoHongShuCrawler.search] Keyword {lastest_checkpoint.current_search_keyword} not found in keyword list"
                    )
                    return
                keyword_list = keyword_list[keyword_index:]

        for keyword in keyword_list:
            source_keyword_var.set(keyword)

            # 按关键字保存检查点，后面的业务行为都是基于这个检查点来更新page信息，所以需要先保存检查点
            checkpoint.current_search_keyword = keyword
            await self.checkpoint_manager.save_checkpoint(checkpoint)

            utils.logger.info(
                f"[XiaoHongShuCrawler.search] Current search keyword: {keyword}"
            )
            page = checkpoint.current_search_page
            saved_note_count = (page - 1) * 20
            while saved_note_count <= config.CRAWLER_MAX_NOTES_COUNT:
                try:
                    utils.logger.info(
                        f"[XiaoHongShuCrawler.search] search xhs keyword: {keyword}, page: {page}"
                    )
                    note_id_list: List[str] = []
                    xsec_tokens: List[str] = []
                    notes_res = await self.xhs_client.get_note_by_keyword(
                        keyword=keyword,
                        page=page,
                        sort=(
                            SearchSortType(config.SORT_TYPE)
                            if config.SORT_TYPE != ""
                            else SearchSortType.GENERAL
                        ),
                    )
                    utils.logger.info(
                        f"[XiaoHongShuCrawler.search] Search notes res count:{len(notes_res.get('items', []))}"
                    )
                    if not notes_res or not notes_res.get("has_more", False):
                        utils.logger.info("No more content!")
                        break

                    task_list = []
                    for post_item in notes_res.get("items", {}):
                        if post_item.get("model_type") in ("rec_query", "hot_query"):
                            continue

                        note_id = post_item.get("id")
                        if not note_id:
                            continue

                        note_id_list.append(note_id)
                        xsec_tokens.append(post_item.get("xsec_token"))

                        if await self.checkpoint_manager.check_note_is_crawled_in_checkpoint(
                                checkpoint_id=checkpoint.id, note_id=note_id
                        ):
                            utils.logger.info(
                                f"[XiaoHongShuCrawler.search] Note {note_id} is already crawled, skip"
                            )
                            saved_note_count += 1
                            continue

                        # 添加爬取帖子任务到检查点， 这个时候还没有爬取帖子，所以is_success_crawled为False
                        # 后续 task_list 被asyncio.gather 并发调度之后，根据爬取note_id来更新is_success_crawled为True
                        await self.checkpoint_manager.add_crawled_note_task_to_checkpoint(
                            checkpoint_id=checkpoint.id,
                            note_id=note_id,
                            extra_params_info={
                                "xsec_source": post_item.get("xsec_source"),
                                "xsec_token": post_item.get("xsec_token"),
                            },
                        )

                        task = asyncio.create_task(
                            self.get_note_detail_async_task(
                                note_id=note_id,
                                xsec_source=post_item.get("xsec_source"),
                                xsec_token=post_item.get("xsec_token"),
                                checkpoint_id=checkpoint.id,
                            )
                        )
                        task_list.append(task)

                    note_details = await asyncio.gather(*task_list)
                    for note_detail in note_details:
                        if note_detail:
                            saved_note_count += 1
                            await xhs_store.update_xhs_note(note_detail)

                    await self.batch_get_note_comments(
                        note_id_list, xsec_tokens, checkpoint_id=checkpoint.id
                    )

                    page += 1

                except Exception as ex:
                    utils.logger.error(
                        f"[XiaoHongShuCrawler.search] Search notes error: {ex}"
                    )
                    # 发生异常了，则打印当前爬取的关键词和页码，用于后续继续爬取
                    utils.logger.info(
                        "------------------------------------------记录当前爬取的关键词和页码------------------------------------------"
                    )
                    for i in range(3):
                        utils.logger.error(
                            f"[XiaoHongShuCrawler.search] Current keyword: {keyword}, page: {page}"
                        )
                    utils.logger.info(
                        "------------------------------------------记录当前爬取的关键词和页码---------------------------------------------------"
                    )

                    utils.logger.info(
                        f"[XiaoHongShuCrawler.search] 可以在配置文件中开启断点续爬功能，继续爬取当前关键词的信息"
                    )
                    return

                finally:
                    lastest_checkpoint = (
                        await self.checkpoint_manager.load_checkpoint_by_id(
                            checkpoint.id
                        )
                    )
                    if lastest_checkpoint:
                        lastest_checkpoint.current_search_page = page
                        await self.checkpoint_manager.update_checkpoint(
                            lastest_checkpoint
                        )

    def _find_creator_index_in_creator_list(self, creator_id: str) -> int:
        """
        Find creator index in creator list

        Args:
            creator_id: creator id

        Returns:
            int: creator index
        """
        creator_list = config.XHS_CREATOR_URL_LIST
        for index, creator_item in enumerate(creator_list):
            creator_url_info: CreatorUrlInfo = parse_creator_info_from_creator_url(
                creator_item
            )
            if creator_url_info.creator_id == creator_id:
                return index
        return -1

    async def get_all_notes_by_creator(
            self,
            user_id: str,
            crawl_interval: float = 1.0,
            xsec_token: str = "",
            xsec_source: str = "",
            checkpoint_id: str = "",
    ) -> List[Dict]:
        """
        获取指定用户下的所有发过的帖子，该方法会一直查找一个用户下的所有帖子信息
        Args:
            user_id: 用户ID
            crawl_interval: 爬取一次的延迟单位（秒）
            xsec_token: 验证token
            xsec_source: 渠道来源
            checkpoint_id: 检查点ID

        Returns:

        """
        checkpoint = await self.checkpoint_manager.load_checkpoint_by_id(checkpoint_id)
        if not checkpoint:
            raise Exception(
                f"[XiaoHongShuCrawler.get_all_notes_by_creator] Get checkpoint error, checkpoint_id: {checkpoint_id}"
            )

        result = []
        notes_has_more = True
        notes_cursor = checkpoint.current_creator_page or ""
        saved_creator_count = 0
        while notes_has_more and saved_creator_count <= config.CRAWLER_MAX_NOTES_COUNT:
            notes_res = await self.xhs_client.get_notes_by_creator(
                user_id,
                notes_cursor,
                xsec_token=xsec_token,
                xsec_source=xsec_source,
            )

            if not notes_res:
                utils.logger.error(
                    f"[XiaoHongShuClient.get_notes_by_creator] The current creator may have been banned by xhs, so they cannot access the data."
                )
                break

            notes_has_more = notes_res.get("has_more", False)
            notes_cursor = notes_res.get("cursor", "")

            if "notes" not in notes_res:
                utils.logger.info(
                    f"[XiaoHongShuClient.get_all_notes_by_creator] No 'notes' key found in response: {notes_res}"
                )
                break

            notes = notes_res["notes"]
            utils.logger.info(
                f"[XiaoHongShuClient.get_all_notes_by_creator] got user_id:{user_id} notes len : {len(notes)}, notes_cursor: {notes_cursor}"
            )
            await self.fetch_creator_notes_detail(notes, checkpoint_id=checkpoint_id)
            await asyncio.sleep(crawl_interval)
            result.extend(notes)
            saved_creator_count += len(notes)

            # 需要加载最新的检查点，因为在fetch_creator_notes_detail方法中，有对检查点左边
            checkpoint = await self.checkpoint_manager.load_checkpoint_by_id(checkpoint_id)
            checkpoint.current_creator_page = notes_cursor
            await self.checkpoint_manager.update_checkpoint(checkpoint)
        return result

    async def get_creators_and_notes(self) -> None:
        """
        Get creator's information and their notes and comments
        Returns:

        """
        utils.logger.info(
            "[XiaoHongShuCrawler.get_creators_and_notes] Begin get xiaohongshu creators"
        )
        checkpoint = Checkpoint(platform=constant.XHS_PLATFORM_NAME, mode="creator")
        creator_list = config.XHS_CREATOR_URL_LIST
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.XHS_PLATFORM_NAME,
                mode="creator",
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[XiaoHongShuCrawler.get_creators_and_notes] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
                creator_index = self._find_creator_index_in_creator_list(
                    lastest_checkpoint.current_creator_id
                )
                if creator_index == -1:
                    utils.logger.error(
                        f"[XiaoHongShuCrawler.get_creators_and_notes] Creator {lastest_checkpoint.current_creator_id} not found in creator list"
                    )
                    creator_index = 0

                creator_list = creator_list[creator_index:]

        for creator_url in creator_list:
            creator_url_info: CreatorUrlInfo = parse_creator_info_from_creator_url(
                creator_url
            )
            checkpoint.current_creator_id = creator_url_info.creator_id
            await self.checkpoint_manager.save_checkpoint(checkpoint)

            createor_info: Optional[Dict] = await self.xhs_client.get_creator_info(
                user_id=creator_url_info.creator_id,
                xsec_token=creator_url_info.xsec_token,
                xsec_source=creator_url_info.xsec_source,
            )
            if not createor_info:
                raise Exception(
                    f"[XiaoHongShuCrawler.get_creators_and_notes] Get creator info error, user_id: {creator_url_info.creator_id}"
                )

            await xhs_store.save_creator(
                creator_url_info.creator_id, creator=createor_info
            )

            # Get all note information of the creator
            await self.get_all_notes_by_creator(
                user_id=creator_url_info.creator_id,
                crawl_interval=0,
                xsec_token=creator_url_info.xsec_token,
                xsec_source=creator_url_info.xsec_source,
                checkpoint_id=checkpoint.id,
            )

    async def fetch_creator_notes_detail(
            self, note_list: List[Dict], checkpoint_id: str = ""
    ):
        """
         Concurrently obtain the specified post list and save the data
        Args:
            note_list:
            checkpoint_id:

        Returns:

        """
        task_list, note_ids, xsec_tokens = [], [], []
        for note_item in note_list:
            note_id = note_item.get("note_id", "")
            if not note_id:
                continue

            note_ids.append(note_id)
            xsec_tokens.append(note_item.get("xsec_token", ""))

            if await self.checkpoint_manager.check_note_is_crawled_in_checkpoint(
                    checkpoint_id=checkpoint_id, note_id=note_item.get("note_id", "")
            ):
                utils.logger.info(
                    f"[XiaoHongShuCrawler.fetch_creator_notes_detail] Note {note_item.get('note_id', '')} is already crawled, skip"
                )
                continue

            await self.checkpoint_manager.add_crawled_note_task_to_checkpoint(
                checkpoint_id=checkpoint_id,
                note_id=note_item.get("note_id", ""),
                extra_params_info={
                    "xsec_source": note_item.get("xsec_source", ""),
                    "xsec_token": note_item.get("xsec_token", ""),
                },
            )
            task = self.get_note_detail_async_task(
                note_id=note_item.get("note_id", ""),
                xsec_source=note_item.get("xsec_source", ""),
                xsec_token=note_item.get("xsec_token", ""),
                checkpoint_id=checkpoint_id,
            )
            task_list.append(task)

        note_details = await asyncio.gather(*task_list)
        for note_detail in note_details:
            if note_detail:
                await xhs_store.update_xhs_note(note_detail)

        await self.batch_get_note_comments(
            note_ids, xsec_tokens, checkpoint_id=checkpoint_id
        )

    async def get_specified_notes(self):
        """
        Get the information and comments of the specified post
        must be specified note_id, xsec_source, xsec_token
        Returns:

        """
        utils.logger.info(
            "[XiaoHongShuCrawler.get_specified_notes] Begin get xiaohongshu specified notes"
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
                    f"[XiaoHongShuCrawler.get_specified_notes] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
        await self.checkpoint_manager.save_checkpoint(checkpoint)

        xsec_tokens: List[str] = []
        need_get_comment_note_ids: List[str] = []
        get_note_detail_task_list: List[asyncio.Task] = []

        for full_note_url in config.XHS_SPECIFIED_NOTE_URL_LIST:
            note_url_info: NoteUrlInfo = parse_note_info_from_note_url(full_note_url)
            utils.logger.info(
                f"[XiaoHongShuCrawler.get_specified_notes] Parse note url info: {note_url_info}"
            )

            need_get_comment_note_ids.append(note_url_info.note_id)
            xsec_tokens.append(note_url_info.xsec_token)

            if await self.checkpoint_manager.check_note_is_crawled_in_checkpoint(
                    checkpoint_id=checkpoint.id, note_id=note_url_info.note_id
            ):
                utils.logger.info(
                    f"[XiaoHongShuCrawler.get_specified_notes] Note {note_url_info.note_id} is already crawled, skip"
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

            crawler_task = self.get_note_detail_async_task(
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

        await self.batch_get_note_comments(
            need_get_comment_note_ids, xsec_tokens, checkpoint_id=checkpoint.id
        )

    async def get_note_detail_async_task(
            self,
            note_id: str,
            xsec_source: str,
            xsec_token: str,
            checkpoint_id: str,
    ) -> Optional[Dict]:
        """
        Get note detail from html or api

        Args:
            note_id: note id
            xsec_source: xsec source
            xsec_token: xsec token
            checkpoint_id: checkpoint id
        Returns:
            note detail
        """
        note_detail, note_detail_from_html, note_detail_from_api = None, None, None
        async with self.crawler_note_task_semaphore:
            try:
                note_detail_from_html: Optional[Dict] = (
                    await self.xhs_client.get_note_by_id_from_html(
                        note_id, xsec_source, xsec_token
                    )
                )
                if not note_detail_from_html:
                    note_detail_from_api: Optional[Dict] = (
                        await self.xhs_client.get_note_by_id(
                            note_id, xsec_source, xsec_token
                        )
                    )
                note_detail = note_detail_from_html or note_detail_from_api
                if note_detail:
                    note_detail.update(
                        {"xsec_token": xsec_token, "xsec_source": xsec_source}
                    )
                    return note_detail

            except DataFetchError as ex:
                utils.logger.error(
                    f"[XiaoHongShuCrawler.get_note_detail_async_task] Get note detail error: {ex}"
                )
                return None

            except KeyError as ex:
                utils.logger.error(
                    f"[XiaoHongShuCrawler.get_note_detail_async_task] have not fund note detail note_id:{note_id}, err: {ex}"
                )
                return None

            except RetryError as ex:
                utils.logger.error(
                    f"[XiaoHongShuCrawler.get_note_detail_async_task] Get note detail error: {ex}"
                )
                return None

            finally:
                is_success_crawled = note_detail is not None
                await self.checkpoint_manager.update_crawled_note_task_to_checkpoint(
                    checkpoint_id=checkpoint_id,
                    note_id=note_id,
                    is_success_crawled=is_success_crawled,
                    is_success_crawled_comments=False,
                    current_note_comment_cursor=None,
                )

    async def batch_get_note_comments(
            self,
            note_list: List[str],
            xsec_tokens=None,
            checkpoint_id: str = "",
    ):
        """
        Batch get note comments
        Args:
            note_list:
            xsec_tokens:
            checkpoint_id:

        Returns:

        """
        if xsec_tokens is None:
            xsec_tokens = []
        if not config.ENABLE_GET_COMMENTS:
            utils.logger.info(
                f"[XiaoHongShuCrawler.batch_get_note_comments] Crawling comment mode is not enabled"
            )
            return

        utils.logger.info(
            f"[XiaoHongShuCrawler.batch_get_note_comments] Begin batch get note comments, note list: {note_list}"
        )
        task_list: List[Task] = []
        for index, note_id in enumerate(note_list):

            # 先判断checkpoint中该note的is_success_crawled_comments是否为True，如果为True，则跳过
            if await self.checkpoint_manager.check_note_comments_is_crawled_in_checkpoint(
                    checkpoint_id=checkpoint_id, note_id=note_id
            ):
                utils.logger.info(
                    f"[XiaoHongShuCrawler.batch_get_note_comments] Note {note_id} is already crawled comments, skip"
                )
                continue

            task = asyncio.create_task(
                self.get_comments_async_task(
                    note_id,
                    xsec_token=xsec_tokens[index],
                    checkpoint_id=checkpoint_id,
                ),
                name=note_id,
            )
            task_list.append(task)
        await asyncio.gather(*task_list)

    async def get_comments_async_task(
            self,
            note_id: str,
            xsec_token: str = "",
            checkpoint_id: str = "",
    ):
        """
        Get note comments with keyword filtering and quantity limitation
        Args:
            note_id: note id
            xsec_token: xsec token
            checkpoint_id: checkpoint id

        Returns:

        """
        async with self.crawler_note_comment_semaphore:
            utils.logger.info(
                f"[XiaoHongShuCrawler.get_comments_async_task] Begin get note id comments {note_id}"
            )
            await self.get_note_all_comments(
                note_id=note_id,
                crawl_interval=random.random(),
                callback=xhs_store.batch_update_xhs_note_comments,
                xsec_token=xsec_token,
                checkpoint_id=checkpoint_id,
            )

    async def get_note_all_comments(
            self,
            note_id: str,
            crawl_interval: float = 1.0,
            callback: Optional[Callable] = None,
            xsec_token: str = "",
            checkpoint_id: str = "",
    ) -> List[Dict]:
        """
        获取指定笔记下的所有一级评论，该方法会一直查找一个帖子下的所有评论信息
        Args:
            note_id: 笔记ID
            crawl_interval: 爬取一次笔记的延迟单位（秒）
            callback: 一次笔记爬取结束后
            xsec_token: 验证token
            checkpoint_id: 检查点ID

        Returns:

        """
        current_comment_cursor = ""
        lastest_comment_cursor = await self.checkpoint_manager.get_note_comment_cursor(
            checkpoint_id=checkpoint_id, note_id=note_id
        )
        if lastest_comment_cursor:
            utils.logger.info(
                f"[XiaoHongShuCrawler.get_note_all_comments] Lastest comment cursor: {lastest_comment_cursor}"
            )
            current_comment_cursor = lastest_comment_cursor

        result = []
        comments_has_more = True
        comments_cursor = current_comment_cursor  # 首次用外部传入的 cursor

        utils.logger.info(
            f"[XiaoHongShuCrawler.get_note_all_comments] Begin get note {note_id} all comments, current_comment_cursor: {current_comment_cursor}"
        )

        while comments_has_more:
            comments_res = await self.xhs_client.get_note_comments(
                note_id, comments_cursor, xsec_token
            )
            comments_has_more = comments_res.get("has_more", False)
            comments_cursor = comments_res.get("cursor", "")

            # 更新评论游标到checkpoint中
            if comments_cursor:
                await self.checkpoint_manager.update_note_comment_cursor(
                    checkpoint_id=checkpoint_id,
                    note_id=note_id,
                    comment_cursor=comments_cursor,
                )

            if "comments" not in comments_res:
                utils.logger.info(
                    f"[XiaoHongShuClient.get_note_all_comments] No 'comments' key found in response: {comments_res}"
                )
                break
            comments = comments_res["comments"]
            if callback:
                await callback(note_id, comments, xsec_token)

            await asyncio.sleep(crawl_interval)
            result.extend(comments)

            if (
                    PER_NOTE_MAX_COMMENTS_COUNT
                    and len(result) >= PER_NOTE_MAX_COMMENTS_COUNT
            ):
                utils.logger.info(
                    f"[XiaoHongShuClient.get_note_all_comments] The number of comments exceeds the limit: {PER_NOTE_MAX_COMMENTS_COUNT}"
                )
                break
            sub_comments = await self.get_comments_all_sub_comments(
                comments, crawl_interval, callback, xsec_token
            )
            result.extend(sub_comments)

        # 更新评论游标，标记为该帖子的评论已爬取
        await self.checkpoint_manager.update_note_comment_cursor(
            checkpoint_id=checkpoint_id,
            note_id=note_id,
            comment_cursor=comments_cursor,
            is_success_crawled_comments=True,
        )

        return result

    async def get_comments_all_sub_comments(
            self,
            comments: List[Dict],
            crawl_interval: float = 1.0,
            callback: Optional[Callable] = None,
            xsec_token: str = "",
    ) -> List[Dict]:
        """
        获取指定一级评论下的所有二级评论, 该方法会一直查找一级评论下的所有二级评论信息
        Args:
            comments: 评论列表
            crawl_interval: 爬取一次评论的延迟单位（秒）
            callback: 一次评论爬取结束后
            xsec_token: 验证token

        Returns:

        """
        if not config.ENABLE_GET_SUB_COMMENTS:
            utils.logger.info(
                f"[XiaoHongShuCrawler.get_comments_all_sub_comments] Crawling sub_comment mode is not enabled"
            )
            return []

        result = []
        for comment in comments:
            note_id = comment.get("note_id")
            sub_comments = comment.get("sub_comments")
            if sub_comments and callback:
                await callback(note_id, sub_comments, xsec_token)

            sub_comment_has_more = comment.get("sub_comment_has_more")
            if not sub_comment_has_more:
                continue

            root_comment_id = comment.get("id")
            sub_comment_cursor = comment.get("sub_comment_cursor")

            while sub_comment_has_more:
                comments_res = await self.xhs_client.get_note_sub_comments(
                    note_id,
                    root_comment_id,
                    10,
                    sub_comment_cursor,
                    xsec_token,
                )
                sub_comment_has_more = comments_res.get("has_more", False)
                sub_comment_cursor = comments_res.get("cursor", "")
                if "comments" not in comments_res:
                    utils.logger.info(
                        f"[XiaoHongShuClient.get_comments_all_sub_comments] No 'comments' key found in response: {comments_res}"
                    )
                    break
                comments = comments_res["comments"]
                if callback:
                    await callback(note_id, comments, xsec_token, root_comment_id)
                await asyncio.sleep(crawl_interval)
                result.extend(comments)
        return result

    async def get_homefeed_notes(self):
        """
        Get homefeed notes and comments
        Returns:

        """
        utils.logger.info(
            "[XiaoHongShuCrawler.get_homefeed_notes] Begin get xiaohongshu homefeed notes"
        )

        # 初始化检查点
        checkpoint = Checkpoint(
            platform=constant.XHS_PLATFORM_NAME,
            mode="homefeed",
            current_homefeed_cursor="",
            current_homefeed_note_index=0
        )

        # 如果开启了断点续爬，则加载检查点
        if config.ENABLE_CHECKPOINT:
            lastest_checkpoint = await self.checkpoint_manager.load_checkpoint(
                platform=constant.XHS_PLATFORM_NAME,
                mode="homefeed",
                checkpoint_id=config.SPECIFIED_CHECKPOINT_ID,
            )
            if lastest_checkpoint:
                checkpoint = lastest_checkpoint
                utils.logger.info(
                    f"[XiaoHongShuCrawler.get_homefeed_notes] Load lastest checkpoint: {lastest_checkpoint.id}"
                )
        await self.checkpoint_manager.save_checkpoint(checkpoint)

        current_cursor = checkpoint.current_homefeed_cursor or ""
        note_index = checkpoint.current_homefeed_note_index or 0
        saved_note_count = 0
        note_num = 18

        while saved_note_count <= config.CRAWLER_MAX_NOTES_COUNT:
            try:
                utils.logger.info(
                    f"[XiaoHongShuCrawler.get_homefeed_notes] Get homefeed notes, current_cursor: {current_cursor}, note_index: {note_index}, note_num: {note_num}"
                )

                homefeed_notes_res = await self.xhs_client.get_homefeed_notes(
                    category=FeedType.RECOMMEND,
                    cursor=current_cursor,
                    note_index=note_index,
                    note_num=note_num,
                )
                if not homefeed_notes_res:
                    utils.logger.info(
                        f"[XiaoHongShuCrawler.get_homefeed_notes] No more content!"
                    )
                    break

                cursor_score = homefeed_notes_res.get("cursor_score", "")
                if not cursor_score:
                    utils.logger.info(
                        f"[XiaoHongShuCrawler.get_homefeed_notes] No more content!"
                    )
                    break

                items: List[Dict] = homefeed_notes_res.get("items", [])
                note_id_list, xsec_tokens = [], []
                task_list = []

                # 首页推荐信息流比较特殊，每一次打开首页推荐的信息流都不一样的概率较大，如果上一次的checkpoint中存在未爬取的帖子信息，如果参考之前搜索关键词和创作者主页的那种方式来实现，会漏很多帖子列表信息
                # 所以在这里往，task_list中，先讲上一次检测点中未爬取的帖子列表创建爬取任务，放进去
                compensation_note_ids = set()
                for note_item in checkpoint.crawled_note_list:
                    if not note_item.is_success_crawled:
                        task = self.get_note_detail_async_task(
                            note_id=note_item.note_id,
                            xsec_source=note_item.extra_params_info.get("xsec_source", ""),
                            xsec_token=note_item.extra_params_info.get("xsec_token", ""),
                            checkpoint_id=checkpoint.id,
                        )
                        task_list.append(task)
                        compensation_note_ids.add(note_item.note_id)

                for post_item in items:
                    if post_item.get("model_type") not in ("rec_query", "hot_query"):
                        note_id = post_item.get("id")
                        if not note_id:
                            continue

                        note_id_list.append(note_id)
                        xsec_tokens.append(post_item.get("xsec_token", ""))

                        # 检查笔记是否已经被爬取过
                        if await self.checkpoint_manager.check_note_is_crawled_in_checkpoint(
                                checkpoint_id=checkpoint.id, note_id=note_id
                        ):
                            utils.logger.info(
                                f"[XiaoHongShuCrawler.get_homefeed_notes] Note {note_id} is already crawled, skip"
                            )
                            saved_note_count += 1
                            continue

                        # 添加爬取帖子任务到检查点
                        await self.checkpoint_manager.add_crawled_note_task_to_checkpoint(
                            checkpoint_id=checkpoint.id,
                            note_id=note_id,
                            extra_params_info={
                                "xsec_source": "pc_feed",
                                "xsec_token": post_item.get("xsec_token", ""),
                            },
                        )

                        if note_id not in compensation_note_ids:
                            task = asyncio.create_task(
                                self.get_note_detail_async_task(
                                    note_id=note_id,
                                    xsec_source="pc_feed",
                                    xsec_token=post_item.get("xsec_token", ""),
                                    checkpoint_id=checkpoint.id,
                                )
                            )
                            task_list.append(task)

                note_details = await asyncio.gather(*task_list)
                for note_detail in note_details:
                    if note_detail:
                        saved_note_count += 1
                        await xhs_store.update_xhs_note(note_detail)

                await self.batch_get_note_comments(
                    note_id_list, xsec_tokens, checkpoint_id=checkpoint.id
                )

                current_cursor = cursor_score
                note_index += note_num

            except Exception as ex:
                utils.logger.error(
                    f"[XiaoHongShuCrawler.get_homefeed_notes] Get homefeed notes error: {ex}"
                )
                # 发生异常了，则打印当前爬取的游标和索引，用于后续继续爬取
                utils.logger.info(
                    "------------------------------------------记录当前爬取的游标和索引------------------------------------------"
                )
                for i in range(3):
                    utils.logger.error(
                        f"[XiaoHongShuCrawler.get_homefeed_notes] Current cursor: {current_cursor}, note_index: {note_index}"
                    )
                utils.logger.info(
                    "------------------------------------------记录当前爬取的游标和索引---------------------------------------------------"
                )

                utils.logger.info(
                    f"[XiaoHongShuCrawler.get_homefeed_notes] 可以在配置文件中开启断点续爬功能，继续爬取当前位置的信息"
                )
                return

            finally:
                # 更新检查点状态
                lastest_checkpoint = (
                    await self.checkpoint_manager.load_checkpoint_by_id(checkpoint.id)
                )
                lastest_checkpoint.current_homefeed_cursor = current_cursor
                lastest_checkpoint.current_homefeed_note_index = note_index
                await self.checkpoint_manager.update_checkpoint(lastest_checkpoint)

        utils.logger.info(
            "[XiaoHongShuCrawler.get_homefeed_notes] XiaoHongShu homefeed notes crawler finished ..."
        )
