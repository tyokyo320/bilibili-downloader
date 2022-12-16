import os

import moviepy.editor as mp
import urllib

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
        # set category
        category = Category.default
        # category = Category.bangumi
        video = Video(url, category)

        return video

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

        video_filename = video.title + '.mp4'
        audio_filename = video.title + '.mp3'

        # 创建文件夹存放下载的视频
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)

        print("开始下载视频：", video_filename)
        self._download(video_url, os.path.join(self.temp_path, video_filename))
        # urllib.request.urlretrieve(url=video_url, filename=os.path.join(self.temp_path, video_filename), reporthook=self._schedule)
        print("【下载视频完毕】")

        print("开始下载音频：", audio_filename)
        self._download(audio_url, os.path.join(self.temp_path, audio_filename))
        # urllib.request.urlretrieve(url=audio_url, filename=os.path.join(self.temp_path, audio_filename), reporthook=self._schedule)
        print("【下载音频完毕】")

    def _download(self, url, filename) -> None:
        request = urllib.request.Request(url, headers=self.headers)
        response = urllib.request.urlopen(request).read()
        with open(os.path.join(self.temp_path, filename), mode='wb') as f:
            f.write(response)

    # def _schedule(self, block_count, block_size, total_size) -> None:
    #     '''
    #     urllib.urlretrieve 的回调函数
    #     :param block_count: 已经下载的数据块
    #     :param block_size: 数据块的大小
    #     :param total_size: 远程文件的大小
    #     :return:
    #     '''
    #     # percent = 100.0 * block_count * block_size / total_size
    #     # if percent > 100:
    #     #     percent = 100
    #     # s = ('#' * round(percent)).ljust(100, '-')
    #     # sys.stdout.write("%.2f%%" % percent + '[ ' + s + ']' + '\r')
    #     # sys.stdout.flush()

    #     percentage = 100.0 * block_count * block_size / total_size
    #     if percentage > 100:
    #         percentage = 100
    #     max_bar = 50
    #     bar_num = int(percentage / (100 / max_bar))
    #     progress_element = '=' * bar_num
    #     if bar_num != max_bar:
    #         progress_element += '>'
    #     bar_fill = ' '
    #     bar = progress_element.ljust(max_bar, bar_fill)
    #     total_size_kb = total_size / 1024
    #     print(f'[{bar}] {percentage:.2f}% ({total_size_kb:.0f}KB)\r', end='')


class VideoMerge():
    '''合并视频和音频类'''

    def __init__(self) -> None:
        # 存放下载视频的文件夹路径
        self.temp_path = config.TEMP_PATH
        # 存放合并后的文件夹路径
        self.path = config.OUTPUT_PATH

    def merge_video(self, video) -> None:
        print(video.title)
        video_filename = video.title + '.mp4'
        audio_filename = video.title + '.mp3'

        # 创建文件夹存放合并的视频
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        clip = mp.VideoFileClip(os.path.join(
            self.temp_path, video_filename)).subclip()
        clip.write_videofile(os.path.join(self.path, video_filename), audio=os.path.join(
            self.temp_path, audio_filename), preset="ultrafast", threads=8)
        print("视频合成结束")

        # TODO：OSError: [Errno 39] Directory not empty
        os.remove(os.path.join(self.temp_path, video_filename))
        os.remove(os.path.join(self.temp_path, audio_filename))
        os.removedirs(self.temp_path)
