import os
import shutil
import subprocess
import time

import httpx
import moviepy.editor as mp

from tqdm import tqdm

from strategy.bilibili_strategy import BilibiliStrategy
from strategy.default import DefaultStrategy
from strategy.bangumi import BangumiStrategy
from models.category import Category
from models.video import Video
import config


class BilibiliExecutor():

    _strategies = {
        Category.default: DefaultStrategy(),
        Category.bangumi: BangumiStrategy(),
    }

    @property
    def strategy(self) -> BilibiliStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BilibiliStrategy):
        self._strategy = strategy

    def get_video(self, url) -> Video:
        """根据 URL 自动识别视频类型"""
        category = self._detect_category(url)
        video = Video(url, category)
        return video

    def _detect_category(self, url: str) -> int:
        """
        根据 URL 模式识别视频分类

        普通视频：
        - https://www.bilibili.com/video/BV*
        - https://www.bilibili.com/video/av*

        番剧/电影/OGV：
        - https://www.bilibili.com/bangumi/play/ss*  (season)
        - https://www.bilibili.com/bangumi/play/ep*  (episode)
        """
        if '/bangumi/play/' in url:
            return Category.bangumi
        return Category.default

    def get(self, url: str) -> Video:
        video = self.get_video(url)
        strategy = self._strategies[video.category]
        # 按照不同mode获取视频各项信息
        video = strategy.get(video)

        return video


class BilibiliDownloader():
    '''下载视频和音频类'''

    def __init__(self) -> None:
        # 存放下载视频的文件夹路径
        self.temp_path = config.TEMP_PATH
        self.headers = {
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

    def download_video(self, video) -> None:
        video_url = video.video_url
        audio_url = video.audio_url

        # 如果是分P视频（包括第1部分），在文件名中添加分P标识
        # 这样可以避免多个分P之间的文件名冲突
        if hasattr(video, 'part_number') and video.part_number >= 1:
            video_filename = f'{video.title}_P{video.part_number}.mp4'
            audio_filename = f'{video.title}_P{video.part_number}.mp3'
        else:
            video_filename = video.title + '.mp4'
            audio_filename = video.title + '.mp3'

        # 创建文件夹存放下载的视频
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)

        print(f"\n📥 下载视频：{video_filename}")
        self._download(video_url, os.path.join(self.temp_path, video_filename))
        # urllib.request.urlretrieve(url=video_url, filename=os.path.join(self.temp_path, video_filename), reporthook=self._schedule)
        print("✅ 视频下载完成")

        print(f"\n🎵 下载音频：{audio_filename}")
        self._download(audio_url, os.path.join(self.temp_path, audio_filename))
        # urllib.request.urlretrieve(url=audio_url, filename=os.path.join(self.temp_path, audio_filename), reporthook=self._schedule)
        print("✅ 音频下载完成")

    def _download(self, url, filename, max_retries=3, retry_delay=5) -> None:
        retries = 0
        while retries < max_retries:
            try:
                # 检查文件是否已存在
                file_size = 0
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)

                # 设置请求头 Range 字段，用于断点续传
                self.headers["Range"] = f"bytes={file_size}-"
                with httpx.stream("GET", url, headers=self.headers) as response:
                    if response.status_code == 416:
                        print("文件已经下载完毕")
                        return

                    # 总的文件大小包括已下载的部分
                    total_size = (
                        int(response.headers.get("content-length", 0)) + file_size
                    )

                    mode = "ab" if file_size > 0 else "wb"

                    # 使用 tqdm 显示进度条
                    with open(filename, mode) as file, tqdm(
                        total=total_size, unit="B", unit_scale=True, initial=file_size
                    ) as progress_bar:
                        for chunk in response.iter_bytes():
                            if chunk:
                                file.write(chunk)
                                progress_bar.update(len(chunk))  # 更新进度条
                return # 下载成功，退出函数
            except (httpx.RemoteProtocolError, httpx.RequestError) as e:
                retries += 1
                print(f"下载过程中出现错误: {e}，正在重试 ({retries}/{max_retries})...")
                time.sleep(retry_delay)

        print("下载失败，已达到最大重试次数")


class VideoMerge():
    '''合并视频和音频类'''

    def __init__(self) -> None:
        # 存放下载视频的文件夹路径
        self.temp_path = config.TEMP_PATH
        # 存放合并后的文件夹路径
        self.path = config.OUTPUT_PATH

    def merge_video(self, video) -> None:
        # 如果是分P视频（包括第1部分），在文件名中添加分P标识
        # 这样可以避免多个分P之间的文件名冲突
        if hasattr(video, 'part_number') and video.part_number >= 1:
            video_filename = f'{video.title}_P{video.part_number}.mp4'
            audio_filename = f'{video.title}_P{video.part_number}.mp3'
        else:
            video_filename = video.title + '.mp4'
            audio_filename = video.title + '.mp3'

        # 创建文件夹存放合并的视频
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # 如果 ffmpeg 存在，则用其合并视频和音频
        if shutil.which("ffmpeg"):
            print(f"\n🎬 合并视频和音频...")
            result = subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    os.path.join(self.temp_path, video_filename),
                    "-i",
                    os.path.join(self.temp_path, audio_filename),
                    "-c:v",
                    "copy",
                    "-c:a",
                    "copy",
                    os.path.join(self.path, video_filename),
                    "-y",  # 自动覆盖已存在的文件
                ],
                stdout=subprocess.DEVNULL,  # 隐藏标准输出
                stderr=subprocess.DEVNULL,  # 隐藏错误输出
            )
            if result.returncode != 0:
                print(f"⚠️  ffmpeg 合并失败，退出代码: {result.returncode}")
        else:
            print(f"\n🎬 使用 moviepy 合并视频和音频...")
            clip = mp.VideoFileClip(os.path.join(
                self.temp_path, video_filename)).subclip()
            clip.write_videofile(os.path.join(self.path, video_filename), audio=os.path.join(
                self.temp_path, audio_filename), preset="ultrafast", threads=8)

        print("✅ 视频合成完成")

        # TODO：OSError: [Errno 39] Directory not empty
        os.remove(os.path.join(self.temp_path, video_filename))
        os.remove(os.path.join(self.temp_path, audio_filename))
        os.removedirs(self.temp_path)
