from bs4 import BeautifulSoup
import httpx

import config
from strategy.bilibili_strategy import BilibiliStrategy
from models.video import Video

import re
import json


class DefaultStrategy(BilibiliStrategy):

    def __init__(self) -> None:
        super().__init__()
        # 启用自动重定向
        self.session = httpx.Client(follow_redirects=True)
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            "Content-Type": "application/json; charset=utf-8",
            'cookie': config.COOKIE,
            'pragma': 'no-cache',
            'referer': 'https://space.bilibili.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
        }

    def get_video_page(self, url: str) -> BeautifulSoup:
        response = self.session.get(
            url=url,
            headers=self.session.headers
        )

        response.raise_for_status()
        bs = BeautifulSoup(response.text, 'html.parser')
        return bs

    def get_video_title(self, bs: BeautifulSoup) -> str:
        # 普通视频优先使用 <h1> 标签
        h1_tag = bs.find('h1')
        if h1_tag:
            video_title = h1_tag.get_text()
            return video_title

        # 备用方案：使用 <title> 标签
        title_tag = bs.find('title')
        if title_tag:
            return title_tag.get_text()

        raise ValueError("无法获取视频标题")

    def get_video_json(self, bs: BeautifulSoup) -> dict:
        """只处理 window.__playinfo__ 格式（普通视频）"""
        pattern = re.compile(r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL)
        script = bs.find("script", text=pattern)

        if script is None:
            raise ValueError(
                "未找到视频数据 (window.__playinfo__)。\n"
                "可能原因：\n"
                "1. URL 不是普通视频类型（可能是番剧/电影，应使用 BangumiStrategy）\n"
                "2. 视频已下架或不存在\n"
                "3. 需要登录或会员权限"
            )

        result = pattern.search(script.next).group(1)
        video_json = json.loads(result)
        return video_json

    def get(self, video: Video) -> Video:
        bs = self.get_video_page(video.url)
        title = self.get_video_title(bs)
        json_data = self.get_video_json(bs)

        # 获取所有可用的视频质量（按质量ID降序排列）
        # Bilibili API 返回的 video 数组已按质量从高到低排序
        # 索引 [0] 是最高可用质量
        video_streams = json_data['data']['dash']['video']
        audio_streams = json_data['data']['dash']['audio']

        # 选择最高质量（第一个元素）
        # print("可用视频质量列表（ID）:", [v['id'] for v in video_streams])
        best_video = video_streams[0]
        quality_id = best_video['id']
        video_url = best_video['baseUrl']

        # 选择最高质量音频
        best_audio = audio_streams[0]
        audio_url = best_audio['baseUrl']

        # 显示所有可用质量（用于调试）
        available_qualities = list(set([v['id'] for v in video_streams]))
        available_qualities.sort(reverse=True)

        video.set_title(title)
        video.set_quality(quality_id)
        video.set_video_url(video_url)
        video.set_audio_url(audio_url)

        # 如果最高质量低于720P，提示用户可能的原因
        if quality_id < 64:  # 64 = 720P
            print(f"\n⚠️  当前最高可用质量较低 (ID={quality_id})")
            print("   可能原因：")
            print("   • 账号无会员权限（大会员可下载高清画质）")
            print("   • 地理位置限制（海外IP可能被限制画质）")
            print("   • 视频本身只有低画质版本")
            if len(available_qualities) > 1:
                print(f"   可用画质列表: {available_qualities}")

        return video
