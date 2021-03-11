from models import bilibili
from utils import download, merge
import threading
import time
import sys


def main(url):

    # 开始下载时刻
    start_time = time.time()

    # 获取视频和音频相关信息
    bi = bilibili.BilibiliInfo(url)
    page_info = bi.get_video_page()
    video_info = bi.get_video_info(page_info)
    audio_info = bi.get_audio_info(page_info)

    # 下载视频和音频
    bd = download.BilibiliDownloader(video_info, audio_info)

    # 创建线程池
    threadpool = []

    t1 = threading.Thread(target=bd.download_video)
    threadpool.append(t1)
    t2 = threading.Thread(target=bd.download_audio)
    threadpool.append(t2)

    # 开启多线程
    for th in threadpool:
        th.start()
    # 等待所有线程运行完毕
    for th in threadpool:
        th.join()

    # 开始合并视频
    vm = merge.VideoMerge(video_info, audio_info)
    vm.merge_video()

    # 计算用时
    end_time = time.time()
    times = round(end_time - start_time)
    minutes = times // 60
    times %= 60
    seconds = times
    print(f"总计用时：{minutes}分钟{seconds}秒")


if __name__ == '__main__':
    # URL
    url = sys.argv[1]
    main(url)
