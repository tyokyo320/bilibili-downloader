import os

# 程序根目录（请勿修改）
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# 文件临时输出目录
TEMP_PATH = os.path.join(BASE_PATH, "temp")
# 视频输出目录
OUTPUT_PATH = os.path.join(BASE_PATH, "output")

# B站登录后获取的SESSDATA，CURRENT_QUALITY
# 定期更换COOKIE的值即可
COOKIE = 'buvid3=5EF59BBB-DADF-AC38-2862-7E588DAA63F567589infoc; b_nut=1763285667; _uuid=F428A1C1-417D-8849-BAAF-810510A74B126972040infoc; home_feed_column=4; browser_resolution=1016-1045; buvid4=C41C1D3C-CA9D-5596-B4EF-1493932BBB8C68965-025111617-zyhkyNiMl7JwzP8ZDdUFdg%3D%3D; buvid_fp=563263ed7718f630443e30a1295bc3bb; DedeUserID=8366997; DedeUserID__ckMd5=b6567189d34e3723; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; rpdid=|(u)Y|~m|k|J0J\'u~YJk)l~Rm; ogv_device_support_hdr=0; CURRENT_QUALITY=80; bp_t_offset_8366997=1141010903165042688; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjUwMjYxMTYsImlhdCI6MTc2NDc2Njg1NiwicGx0IjotMX0.70OV9kjVay3Ycx4i4MOyBFpTlLuuDAjLKHJrb9Dmu5A; bili_ticket_expires=1765026056; SESSDATA=a534c864%2C1780487599%2C56c3a%2Ac2CjCPZ5QwiWX6AoDPkowM1T7BALO4wnThggVedHuecekJxAcYO7QwmFM-TgoK7_X9-wcSVnRQUFozUHZMZTBIWXFrTVJxTHFuM0F3WGhXNUZQTEhkQkp6bWdTMWhZSWNucjhSemJvRUgxbElVa3JCOElvckR3YkFnUHEzNk5JMjItOVV0b1NSajd3IIEC; bili_jct=b1e977189e44c623c16e4ef97798ab36; sid=6wovs0jf; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; b_lsid=21857D5D_19AF2C37D7E'

URL = [
    # 普通视频
    'https://www.bilibili.com/video/BV1M4411c7P4/?vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',
    'https://www.bilibili.com/video/BV1hB4y147j8/?spm_id_from=333.337.search-card.all.click&vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',

    # 分P视频（第1个分P）
    'https://www.bilibili.com/video/BV1TnsZzHEcz/?vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63&spm_id_from=333.788.videopod.episodes',

    # 分P视频（第2个分P）
    'https://www.bilibili.com/video/BV1TnsZzHEcz/?p=2&vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',

    # 番剧/电影（需要中国大陆 IP）
    # 'https://www.bilibili.com/bangumi/play/ss39429',      # 电影
    # 'https://www.bilibili.com/bangumi/play/ep271002',     # 番剧单集（暂不支持）
]