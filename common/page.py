# -*- coding: utf-8 -*-

from common.external_services.Pw.sessions.session import MyHttp
from common.external_services.Pw.sessions.agents import Agent


class Page(MyHttp):

    def __init__(self, page_url: str):
        headers = Agent.headers()
        super().__init__(headers)
        self.page_url = page_url



    async def get_content(self):
        response = await self.get_url(url=self.page_url, params={})
        print(response)





