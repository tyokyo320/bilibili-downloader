from bs4 import BeautifulSoup


import config
import requests
import time
import json
import re


class BilibiliInfo:
    '''获取视频和音频相关信息类'''

    def __init__(self, bv):
        # 视频页地址
        self.url = 'https://www.bilibili.com/video/' + bv

    def get_video_page(self):
        response = requests.get(
            url=self.url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                'cookie': config.COOKIE
            },
        )

        if response.status_code == 200:
            return response.text
        raise Exception('failed')

    def get_video_quality(self, id):
        '''
        id参数对应视频清晰度，非会员用户只能下载到高清1080P，这里默认可以下载的最高的清晰度

        - 120：超清 4K (需要大会员的cookie中的SESSDATA值)
        - 116: 高清 1080P60 (需要大会员)
        - 112: 高清 1080P+ (需要大会员)
        - 80: 高清 1080P
        - 74: 高清 720P60 (需要大会员)
        - 64: 高清 720P
        - 32: 清晰 480P
        - 16: 流畅 360P
        '''

        quality = {
            120: '超清 4K',
            116: '高清 1080P60',
            112: '高清 1080P+',
            80: '高清 1080P',
            74: '高清 720P60',
            64: '高清 720P',
            32: '清晰 480P',
            16: '流畅 360P',
        }

        print(f'下载的视频清晰度：{quality[id]}')

    def get_video_info(self, page):
        try:
            bs = BeautifulSoup(page, 'html.parser')
            # 取视频标题
            video_title = bs.find('span', 'tit').get_text()

            # 取视频链接
            pattern = re.compile(
                r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL)
            script = bs.find("script", text=pattern)
            result = pattern.search(script.next).group(1)

            temp = json.loads(result)

            # 取第一个视频链接
            for item in temp['data']['dash']['video']:
                if 'baseUrl' in item.keys():
                    video_url = item['baseUrl']
                    self.get_video_quality(item['id'])
                    break

            return {
                'title': video_title,
                'video_url': video_url
            }
        except requests.RequestException:
            print('视频链接错误，请重新更换')
            exit(1)

    def get_audio_info(self, page):
        try:
            bs = BeautifulSoup(page, "html.parser")
            # 获取音频标题
            audio_title = bs.find('span', 'tit').get_text()

            # 获取音频连接
            pattern = re.compile(r'window\.__playinfo__=(.*?)$')
            script = bs.find('script', text=pattern)
            result = pattern.search(script.next).group(1)

            temp = json.loads(result)

            # 取第一个音频链接
            for item in temp['data']['dash']['audio']:
                if 'baseUrl' in item.keys():
                    audio_url = item['baseUrl']
                    break

            return {
                'title': audio_title,
                'audio_url': audio_url
            }

        except requests.RequestException:
            print('音频链接错误，请重新更换')
            exit(1)
