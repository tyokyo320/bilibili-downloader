class Video():

    def __init__(self, url: str, category: int) -> None:
        self.url = url
        self.category = category

    def set_title(self, title: str) -> None:
        self.title = title

    def set_quality(self, id: int) -> None:
        self.quality = {
            120: '超清 4K',
            116: '高清 1080P60',
            112: '高清 1080P+',
            80: '高清 1080P',
            74: '高清 720P60',
            64: '高清 720P',
            32: '清晰 480P',
            16: '流畅 360P',
        }
        print(f'下载的视频清晰度：{self.quality[id]}')

    def set_video_url(self, video_url: str) -> None:
        self.video_url = video_url

    def set_audio_url(self, audio_url: str) -> None:
        self.audio_url = audio_url
