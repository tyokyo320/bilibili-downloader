import moviepy.editor as mp
import os
import re

import config


class VideoMerge():
    '''合并视频和音频类'''

    def __init__(self, video, audio):
        self.video = video
        self.audio = audio
        # 存放下载视频的文件夹路径
        self.temp_path = config.TEMP_PATH
        # 存放合并后的文件夹路径
        self.path = config.OUTPUT_PATH

    def merge_video(self):
        title = re.sub(r'[\/:*?"<>|]', '-', self.video['title'])
        video_filename = title + '.mp4'
        audio_filename = title + '.mp3'

        # 创建文件夹存放合并的视频
        os.makedirs(self.path, exist_ok=True)

        clip = mp.VideoFileClip(os.path.join(
            self.temp_path, video_filename)).subclip()
        clip.write_videofile(os.path.join(self.path, video_filename),
                             audio=os.path.join(self.temp_path, audio_filename), preset="ultrafast", threads=8)
        print("视频合成结束")

        os.remove(os.path.join(self.temp_path, video_filename))
        os.remove(os.path.join(self.temp_path, audio_filename))
        os.removedirs(self.temp_path)
