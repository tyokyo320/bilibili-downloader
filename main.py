import time

from strategy.bilibili_executor import BilibiliExecutor
from strategy.bilibili_executor import BilibiliDownloader
from strategy.bilibili_executor import VideoMerge


class BFacade():

    def __init__(self):
        self.crawler = BilibiliExecutor()
        self.downloader = BilibiliDownloader()
        self.merger = VideoMerge()

    def download(self, urls):
        for url in urls:
            video = self.crawler.get(url)
            self.downloader.download_video(video)
            self.merger.merge_video(video)

def main():

    # 开始下载时刻
    start_time = time.time()

    b = BFacade()
    b.download([
        'https://www.bilibili.com/video/BV17t411w7S2?spm_id_from=333.337.search-card.all.click&vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',
        'https://www.bilibili.com/video/BV1zY4y1E7WX?p=7&vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',
        # 'https://www.bilibili.com/video/BV1ox41147NZ?spm_id_from=333.337.search-card.all.click',
    ])

    # 计算用时
    end_time = time.time()
    times = round(end_time - start_time)
    minutes = times // 60
    times %= 60
    seconds = times
    print(f"总计用时：{minutes}分钟{seconds}秒")


if __name__ == '__main__':
    main()
