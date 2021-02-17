# !/usr/bin/python
# -*- coding:utf-8 -*-
# time: 2021/02/16--15:49
__author__ = 'tyokyo320'

from bs4 import BeautifulSoup
import moviepy.editor as mp
import urllib.request
import requests
import time
import json
import sys
import re
import os


class BilibiliCrawler:

    def __init__(self, bv):
        # 视频页地址
        self.url = 'https://www.bilibili.com/video/' + bv
        # 下载开始时间
        self.start_time = time.time()

    def get_video_page(self, bv):
        url = f'https://www.bilibili.com/video/{bv}'
        response = requests.get(
            url=url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'
            },
        )

        if response.status_code == 200:
            return response.text
        raise Exception('failed')

    def get_video_info(self, html):
        try:
            bs = BeautifulSoup(html, 'html.parser')
            # 取视频标题
            video_title = bs.find('span', 'tit').get_text()

            # 取视频链接
            pattern = re.compile(r"window\.__playinfo__=(.*?)$", re.MULTILINE | re.DOTALL)
            script = bs.find("script", text=pattern)
            result = pattern.search(script.next).group(1)

            temp = json.loads(result)

            # 取第一个视频链接
            for item in temp['data']['dash']['video']:
                # print(item)
                if 'baseUrl' in item.keys():
                    video_url = item['baseUrl']
                    break

            return {
                'title': video_title,
                'video_url': video_url
            }
        except requests.RequestException:
            print('视频链接错误，请重新更换')
            exit(1)

    def get_audio_info(self, html: str):
        try:
            bs = BeautifulSoup(html, "html.parser")
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

    def download_video(self, video):
        title = re.sub(r'[\/:*?"<>|]', '-', video['title'])
        video_url = video['video_url']
        filename = title + '.mp4'
        print("开始下载视频：", filename)
        sys.stdout.flush()

        # 当前目录作为下载目录
        temp_path = os.path.join(sys.path[0], 'temp')

        # 创建文件夹存放下载的视频
        os.makedirs(temp_path, exist_ok=True)

        urllib.request.urlretrieve(
            url=video_url, filename=os.path.join(temp_path, filename), reporthook=self.schedule)

    def download_audio(self, audio):
        title = re.sub(r'[\/:*?"<>|]', '-', audio['title'])
        audio_url = audio['audio_url']
        filename = title + '.mp3'

        # 当前目录作为下载目录
        currentVideoPath = os.path.join(sys.path[0], 'temp')

        # 创建文件夹存放下载视频
        temp_path = os.path.join(sys.path[0], 'temp')

        urllib.request.urlretrieve(
            url=audio_url, filename=os.path.join(currentVideoPath, filename), reporthook=self.schedule)

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

    def merge_video(self, video, audio):
        title = re.sub(r'[\/:*?"<>|]', '-', video['title'])
        video_filename = title + '.mp4'
        audio_filename = title + '.mp3'
        temp_path = os.path.join(sys.path[0], 'temp')

        currentVideoPath = os.path.join(sys.path[0], 'bilibili_video')
        if not os.path.exists(currentVideoPath):
            os.mkdir(currentVideoPath)

        clip = mp.VideoFileClip(os.path.join(
            temp_path, video_filename)).subclip()
        clip.write_videofile(os.path.join(currentVideoPath, video_filename),
                             audio=os.path.join(temp_path, audio_filename))
        print("视频合成结束")

        os.remove(os.path.join(temp_path, video_filename))
        os.remove(os.path.join(temp_path, audio_filename))
        os.removedirs(temp_path)

        end_time = time.time()
        print(f"总计用时：{round(end_time - self.start_time)}秒")


if __name__ == '__main__':
    # argparse
    bv = sys.argv[1]
    bc = BilibiliCrawler(bv)
    text = bc.get_video_page(bv)
    video = bc.get_video_info(text)
    audio = bc.get_audio_info(text)
    bc.download_video(video)
    bc.download_audio(audio)
    bc.merge_video(video, audio)
