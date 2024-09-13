from abc import ABC, abstractmethod
from typing import Dict


class AbstractCrawler(ABC):

    @abstractmethod
    async def async_initialize(self):
        """
        Asynchronous Initialization
        Returns:

        """
        raise NotImplementedError

    @abstractmethod
    async def start(self):
        """
        Start the crawler
        Returns:

        """
        raise NotImplementedError

    @abstractmethod
    async def search(self):
        """
        Search the content
        Returns:

        """
        raise NotImplementedError


class AbstractStore(ABC):
    @abstractmethod
    async def store_content(self, content_item: Dict):
        """
        Store the content
        Args:
            content_item:

        Returns:

        """
        raise NotImplementedError

    @abstractmethod
    async def store_comment(self, comment_item: Dict):
        """
        Store the comment
        Args:
            comment_item:

        Returns:

        """
        raise NotImplementedError

    @abstractmethod
    async def store_creator(self, creator: Dict):
        """
        Store the creator
        Args:
            creator:

        Returns:

        """
        raise NotImplementedError


class AbstractApiClient(ABC):
    @abstractmethod
    async def request(self, method, url, **kwargs):
        """
        Send a request
        Args:
            method:
            url:
            **kwargs:

        Returns:

        """
        raise NotImplementedError
