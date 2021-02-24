import urllib.request

import sys
import os
import re


class BilibiliDownloader():
    '''下载视频和音频类'''

    def __init__(self, video, audio):
        self.video = video
        self.audio = audio
        # 存放下载视频的文件夹路径
        self.temp_path = os.path.join(os.path.abspath('.'), 'temp')

    def download_video(self):
        title = re.sub(r'[\/:*?"<>|]', '-', self.video['title'])
        video_url = self.video['video_url']
        filename = title + '.mp4'
        print("开始下载视频：", filename)

        # 创建文件夹存放下载的视频
        os.makedirs(self.temp_path, exist_ok=True)

        urllib.request.urlretrieve(
            url=video_url, filename=os.path.join(self.temp_path, filename), reporthook=self.schedule)

    def download_audio(self):
        title = re.sub(r'[\/:*?"<>|]', '-', self.audio['title'])
        audio_url = self.audio['audio_url']
        filename = title + '.mp3'
        print("开始下载音频：", filename)

        # 创建文件夹存放下载的视频
        os.makedirs(self.temp_path, exist_ok=True)

        urllib.request.urlretrieve(
            url=audio_url, filename=os.path.join(self.temp_path, filename), reporthook=self.schedule)

    def schedule(self, blocknum, blocksize, totalsize):
        '''
        urllib.urlretrieve 的回调函数
        :param blocknum: 已经下载的数据块
        :param blocksize: 数据块的大小
        :param totalsize: 远程文件的大小
        :return:
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        s = ('#' * round(percent)).ljust(100, '-')
        sys.stdout.write("%.2f%%" % percent + '[ ' + s + ']' + '\r')
        sys.stdout.flush()
