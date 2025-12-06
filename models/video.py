import re
from urllib.parse import urlparse, parse_qs


class Video():

    def __init__(self, url: str, category: int) -> None:
        self.url = url
        self.category = category
        # 从 URL 中提取分P参数（如果存在）
        self.part_number = self._extract_part_number(url)

    def _extract_part_number(self, url: str) -> int:
        """从URL中提取分P参数，如果不存在则返回1"""
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            # 获取 p 参数，如果不存在则默认为 1
            part = query_params.get('p', ['1'])[0]
            return int(part)
        except (ValueError, IndexError):
            return 1

    def set_title(self, title: str) -> None:
        pattern = re.compile(r'[<>:"\/\\|\?\*]')
        self.title = re.sub(pattern, "", title)

    def set_quality(self, id: int) -> None:
        self.quality = {
            127: '超高清 8K',
            126: '杜比视界 4K',
            120: '超清 4K',
            116: '高清 1080P60',
            112: '高清 1080P+',
            80: '高清 1080P',
            74: '高清 720P60',
            64: '高清 720P',
            32: '清晰 480P',
            16: '流畅 360P',
        }
        self.quality_id = id
        print(f'📺 清晰度：{self.quality[id]}')

    def set_video_url(self, video_url: str) -> None:
        self.video_url = video_url

    def set_audio_url(self, audio_url: str) -> None:
        self.audio_url = audio_url
