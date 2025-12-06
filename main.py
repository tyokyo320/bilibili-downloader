import time
import asyncio
import os
import shutil

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
        self._lock = asyncio.Lock()

    async def download_single(self, url):
        """下载单个视频"""
        video = await self.crawler.get(url)
        print(f"\n{'=' * 60}")
        print(f"📹 {video.title}")
        print(f"{'=' * 60}")
        await self.downloader.download_video(video)
        self.merger.merge_video(video)

        # 使用锁保护共享资源
        async with self._lock:
            self.downloaded_videos.append(video)

    async def download(self, urls):
        """并发下载所有视频"""
        # 创建所有下载任务
        tasks = [self.download_single(url) for url in urls]
        # 并发执行所有任务
        await asyncio.gather(*tasks)


async def async_main():
    """异步主函数"""
    # 开始下载时刻
    start_time = time.time()

    b = BFacade()
    await b.download(config.URL)

    # 计算用时
    end_time = time.time()
    times = round(end_time - start_time)
    minutes = times // 60
    times %= 60
    seconds = times

    # 清理临时目录
    if os.path.exists(config.TEMP_PATH):
        try:
            shutil.rmtree(config.TEMP_PATH)
            print(f"\n🧹 已清理临时文件")
        except Exception as e:
            print(f"\n⚠️  清理临时目录失败: {e}")

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


def main():
    """同步入口，运行异步主函数"""
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
