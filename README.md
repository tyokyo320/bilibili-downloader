# Bilibili视频下载

## 功能说明

- [x] B站视频下载
- [x] 支持使用账号cookie下载大会员视频
- [ ] 支持番剧下载【未完成】

## 运行环境

Python3.8+

## 安装依赖库

```bash
pip3 install -r requirements.txt
```

## 运行方法

```bash
# python main.py [av号或BV号]
python main.py BV1t7411a75K

下载的视频清晰度：高清 1080P
开始下载视频： 日语版《好想爱这个世界啊》翻唱【鹿乃】.mp4
开始下载音频： 日语版《好想爱这个世界啊》翻唱【鹿乃】.mp3
Moviepy - Building video /home/user/Programming/Python/bilibili-downloader/bilibili_video/日语版《好想爱这个世界啊》翻唱【鹿乃】.mp4.
Moviepy - Writing video /home/user/Programming/Python/bilibili-downloader/bilibili_video/日语版《好想爱这个世界啊》翻唱【鹿乃】.mp4

Moviepy - Done!                                                                                                                                                                                                                                                                    
Moviepy - video ready /home/user/Programming/Python/bilibili-downloader/bilibili_video/日语版《好想爱这个世界啊》翻唱【鹿乃】.mp4
视频合成结束
总计用时：2分钟32秒
```

## COOKIE设置说明

打开`config.py`，替换cookie中的`SESSDATA`值

替换方法：

1. 浏览器登录B站，打开要下载的视频页
2. `Ctrl + Shift + I`或者鼠标右键选择检查，然后选择`网络`
3. `Ctrl + R`刷新网页，选择第一个，请求表头中找到`cookie`
4. cookie中找到`SESSDATA`值替换

