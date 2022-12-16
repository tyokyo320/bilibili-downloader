# Bilibili视频下载

<div align="center">
    <img src="docs/bilibili-logo.png">
</div>

<div align=center>
    <img src="https://img.shields.io/badge/python-3.8%2B-blue"/>
    <img src="https://img.shields.io/badge/requests-2.25.1-green"/>
    <img src="https://img.shields.io/badge/urllib3-1.26.3-green"/>
    <img src="https://img.shields.io/badge/beautifulsoup4-4.9.3-green"/>
    <img src="https://img.shields.io/badge/moviepy-1.0.3-green"/>
</div>

## :pushpin: 功能说明

- [x] B站视频下载
- [x] 支持使用账号cookie下载大会员视频
- [x] 批量下载
- [ ] 下载进度条【待修复】
- [ ] 支持番剧下载【待更新】
- [ ] 添加代理【待更新】
- [ ] 其他【待更新】

## :white_check_mark: 安装依赖库

```bash
pip3 install -r requirements.txt
```

## :pencil2: COOKIE设置说明

打开`config.py`，**需要定期(30天)替换**cookie

替换方法：

1. 浏览器登录B站，打开要下载的视频页
2. `Ctrl + Shift + I`或者鼠标右键选择检查，然后选择`网络`
3. `Ctrl + R`刷新网页，选择第一个，请求表头中找到`cookie`

![](docs/set-cookie.png)

## :pencil2: 下载链接添加说明

打开`config.py`，在 `URL` 列表种添加视频 URL

```py
# 下载视频的 URL
URL = [
    'https://www.bilibili.com/video/BV1M4411c7P4/?spm_id_from=333.999.0.0&vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',
    'https://www.bilibili.com/video/BV1hB4y147j8/?spm_id_from=333.337.search-card.all.click',
]
```

## :rocket: 运行方法

`python main.py`

```bash
# python main.py
python main.py

マリーゴールド-万寿菊 -あいみょん【璃露】
下载的视频清晰度：高清 1080P
开始下载视频： マリーゴールド-万寿菊 -あいみょん【璃露】.mp4
【下载视频完毕】
开始下载音频： マリーゴールド-万寿菊 -あいみょん【璃露】.mp3
【下载音频完毕】
マリーゴールド-万寿菊 -あいみょん【璃露】
Moviepy - Building video /home/users/work/repos/bilibili-downloader/output/マリーゴールド-万寿菊 -あいみょん【璃露】.mp4.
Moviepy - Writing video /home/users/work/repos/bilibili-downloader/output/マリーゴールド-万寿菊 -あいみょん【璃露】.mp4

Moviepy - Done !                                                                                                                                                                                                                                                                
Moviepy - video ready /home/users/work/repos/bilibili-downloader/output/マリーゴールド-万寿菊 -あいみょん【璃露】.mp4
视频合成结束
🌛勾指起誓🌛 中日英3语版【雨音月奈】
下载的视频清晰度：高清 1080P
开始下载视频： 🌛勾指起誓🌛 中日英3语版【雨音月奈】.mp4
【下载视频完毕】
开始下载音频： 🌛勾指起誓🌛 中日英3语版【雨音月奈】.mp3
【下载音频完毕】
🌛勾指起誓🌛 中日英3语版【雨音月奈】
Moviepy - Building video /home/users/work/repos/bilibili-downloader/output/🌛勾指起誓🌛 中日英3语版【雨音月奈】.mp4.
Moviepy - Writing video /home/users/work/repos/bilibili-downloader/output/🌛勾指起誓🌛 中日英3语版【雨音月奈】.mp4

Moviepy - Done !                                                                                                                                                                                                                                                                
Moviepy - video ready /home/users/work/repos/bilibili-downloader/output/🌛勾指起誓🌛 中日英3语版【雨音月奈】.mp4
视频合成结束
总计用时：4分钟10秒
```

## :tv: 运行效果

![](docs/screen.gif)
