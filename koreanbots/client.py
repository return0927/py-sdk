"""
MIT License

Copyright (c) 2020 매리

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from asyncio import sleep
from logging import getLogger
from .http import HTTPClient
from .errors import HTTPException
from .model import Category as CategoryModel
log = getLogger(__name__)

class Client:
    r"""discord.py Client를 기반으로 한 KoreanBots 클라이언트를 반환합니다.
    이 클래스는 KoreanBots API와 연결됩니다.

    일부 옵션이 :class:`Client`에 전달될 수 있습니다.

    파라미터
    -----------
    Bot: :class:`discord.Client`
        discord.py의 클라이언트 입니다.
        이 클라이언트를 사용하여 길드 정보를 얻습니다.
    Token: :class:`str`
        KoreanBots의 토큰입니다.
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        비동기를 사용하기 위한 :class:`asyncio.AbstractEventLoop`입니다.
        기본값은 ``None``이며, 기본 :class:`asyncio.AbstractEventLoop`는 :func:`asyncio.get_event_loop()`를 사용하여 얻습니다.
    postCount: Optional[:class:`bool`]
        자동으로 ``1800``초마다 길드 정보를 KoreanBots에 전송할지 설정합니다. 기본값은 ``True``입니다. 

    속성
    -----------
    loop: :class:`asyncio.AbstractEventLoop`
        HTTP 리퀘스트에 사용되는 :class:`asyncio.AbstractEventLoop` 클래스 입니다.
    http: :class:`.HTTPClient`
        API 호출에 사용되는 :class:`koreanbots.HTTPClient` 클래스 입니다.
    """

    def __init__(self, Bot, Token, loop=None, postCount=True):
        self.Bot = Bot
        self.loop = loop or Bot.loop
        self.http = HTTPClient(Token, loop=loop)
        if postCount:
            self.loop.create_task(self.postCount())
    
    async def postCount(self):
        await self.Bot.wait_until_ready()
        while not self.Bot.is_closed():
            log.info('Autoposting guild count to koreanbots.')

            try:
                await self.postGuildCount()
            except HTTPException:
                pass
            await sleep(1800)
    
    async def postGuildCount(self):
        r"""|coro|

        :class:`discord.Client`의 :attr:`.guilds`의 수를 KoreanBots API로 보냅니다.

        예외
        --------
        :exc:`.errors.AuthorizeError`
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        :exc:`.errors.Unauthrized`
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        :exc:`.errors.Forbidden`
            접근 권한이 없습니다.
        :exc:`.errors.NotFound`
            찾을 수 없습니다, 파라미터를 확인하세요.
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """

        GuildCounts = len(self.Bot.guilds)
        await self.http.postGuildCount(GuildCounts)

    async def getVote(self, user_id: int):
        r"""|coro|

        주어진 유저ID의 하트 정보를 가져옵니다.

        파라미터
        -------------
        user_id: :class:`int`
            정보를 가져올 유저의 ID

        예외
        --------
        :exc:`.errors.AuthorizeError`
            토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다.
        :exc:`.errors.Unauthrized`
            인증되지 않았습니다, KoreanBots 토큰이 잘못되었을 수 있습니다.
        :exc:`.errors.Forbidden`
            접근 권한이 없습니다.
        :exc:`.errors.NotFound`
            찾을 수 없습니다, 파라미터를 확인하세요.
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        return await self.http.getVote(user_id)

    async def getBot(self, bot_id: int):
        r"""|coro|

        주어진 봇ID의 KoreanBots 정보를 가져옵니다.

        파라미터
        -------------
        bot_id: :class:`int`
            정보를 가져올 봇의 ID

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        return await self.http.getBot(bot_id)

    async def getBots(self, page: int=1):
        r"""|coro|

        KoreanBots의 봇 리스트를 가져옵니다.

        파라미터
        -------------
        page: Optional[:class:`int`]
            봇 리스트의 페이지입니다. 기본값은 ``1``입니다.

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        return await self.http.getBots(page)

    async def searchBots(self, query: str, page: int=1):
        r"""|coro|

        주어진 문자열로 KoreanBots 봇을 검색합니다.

        파라미터
        -------------
        query: :class:`str`
            검색할 봇의 이름
        page: Optional[:class:`int`]
            봇 리스트의 페이지입니다. 기본값은 ``1``입니다.

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        return await self.http.searchBots(query, page)

    async def getBotsByCategory(self, category: CategoryModel, page: int=1):
        r"""|coro|

        주어진 카테고리에 해당하는 KoreanBots 정보를 가져옵니다.

        파라미터
        -------------
        category: :class:`.Category`
            KoreanBots의 카테고리
        page: Optional[:class:`int`]
            봇 리스트의 페이지입니다. 기본값은 ``1``입니다.

        예외
        --------
        :exc:`.errors.HTTPException`
            알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        return await self.http.getBotsByCategory(category, page)