import time

from strategy.bilibili_executor import BilibiliExecutor
from strategy.bilibili_executor import BilibiliDownloader
from strategy.bilibili_executor import VideoMerge
import config


class BFacade():

    def __init__(self):
        self.crawler = BilibiliExecutor()
        self.downloader = BilibiliDownloader()
        self.merger = VideoMerge()
        self.downloaded_videos = []

    def download(self, urls):
        for url in urls:
            video = self.crawler.get(url)
            print(f"\n{'=' * 60}")
            print(f"📹 {video.title}")
            print(f"{'=' * 60}")
            self.downloader.download_video(video)
            self.merger.merge_video(video)
            self.downloaded_videos.append(video)


def main():

    # 开始下载时刻
    start_time = time.time()

    b = BFacade()
    b.download(config.URL)

    # 计算用时
    end_time = time.time()
    times = round(end_time - start_time)
    minutes = times // 60
    times %= 60
    seconds = times

    # 输出下载摘要
    print(f"\n{'=' * 60}")
    print("📊 下载摘要")
    print(f"{'=' * 60}")
    print(f"✅ 成功下载 {len(b.downloaded_videos)} 个视频")
    print(f"⏱️  总计用时：{minutes}分钟{seconds}秒")

    if b.downloaded_videos:
        print(f"\n已下载的视频：")
        for i, video in enumerate(b.downloaded_videos, 1):
            quality_name = video.quality.get(video.quality_id, f"未知 (ID={video.quality_id})")
            print(f"  {i}. {video.title} ({quality_name})")

    print(f"\n💾 视频保存位置：{config.OUTPUT_PATH}")
    print(f"{'=' * 60}\n")


if __name__ == '__main__':
    main()
