import requests
from bs4 import BeautifulSoup

import config
from strategy.bilibili_strategy import BilibiliStrategy
from models.video import Video

import re
import json


class BangumiStrategy(BilibiliStrategy):

    def __init__(self) -> None:
        super().__init__()

    def get_info_page(self, url) -> BeautifulSoup:
        response = requests.get(
            url=url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                'cookie': config.COOKIE
            },
        )
        response.raise_for_status()
        bs = BeautifulSoup(response.text, 'html.parser')

        return bs

    def get_video_title(self, bs: BeautifulSoup) -> str:
        video_title = bs.find_all('h1')[0].get_text()
        video_title = video_title.replace('/', '-')
        print(video_title)

        return video_title

    def get_param_json(self, bs: BeautifulSoup) -> str:
        '''
        获取所需要的参数avid和cid
        '''

        pattern = re.compile(
            r"window\.__INITIAL_STATE__=(.*};)", re.MULTILINE | re.DOTALL)
        script = bs.find("script", text=pattern)
        result = pattern.search(script.next).group(1)
        result = result.replace(result[-1], '')
        param_json = json.loads(result)

        return param_json

    def get_session_param(self, bs: BeautifulSoup) -> str:
        pass

    def get_video_page(self, aid: str, cid: str, epid: str, session: str) -> BeautifulSoup:
        response = requests.post(
            url='https://api.bilibili.com/pgc/player/web/playurl?avid={}&cid={}&qn=116&fnver=0&fnval=80&fourk=1&ep_id={}&session={}'.format(
                aid, cid, epid, session),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                'cookie': config.COOKIE
            },
        )
        response.raise_for_status()
        bs = BeautifulSoup(response.text, 'html.parser')
        print(bs)
        pass

    def get_video_json(self, bs: BeautifulSoup) -> str:
        pass

    def get(self, video: Video):
        bs = self.get_info_page(video.url)
        title = self.get_video_title(bs)
        param_json = self.get_param_json(bs)
        # video_json = self.get_video_json(bs)

        aid = param_json['epInfo']['aid']
        cid = param_json['epInfo']['cid']
        ep_id = param_json['epInfo']['id']
        # self.get_video_page(aid, cid, ep_id)


'''
# API
1. https://api.bilibili.com/pgc/player/web/playurl?avid=931871677&cid=375702034&qn=116&fnver=0&fnval=80&fourk=1&ep_id=409508&session=6bec9c995d114c65b27d9039cc381a9c

avid: 931871677 -> AV号 376930505
cid: 375702034 -> ep号里面获取的到

qn: 116
fnver: 0
fnval: 80
fourk: 1

ep_id: 409508 -> ep号码 409010
qn: 116

session: 6bec9c995d114c65b27d9039cc381a9c -> 加密
'''
