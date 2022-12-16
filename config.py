import os

# 程序根目录（请勿修改）
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# 文件临时输出目录
TEMP_PATH = os.path.join(BASE_PATH, "temp")
# 视频输出目录
OUTPUT_PATH = os.path.join(BASE_PATH, "output")

# B站登录后获取的SESSDATA，CURRENT_QUALITY
# 定期更换COOKIE的值即可
COOKIE = 'buvid3=C5DA0AE5-EE6D-EC73-9C00-91643BB46A8508801infoc; b_nut=1663765808; i-wanna-go-back=-1; _uuid=FA89AA2B-DBC5-B651-3CC3-10108358FB358F11641infoc; buvid_fp_plain=undefined; DedeUserID=8366997; DedeUserID__ckMd5=b6567189d34e3723; nostalgia_conf=-1; b_ut=5; LIVE_BUVID=AUTO2616639434883138; hit-dyn-v2=1; buvid4=B22C1C1E-1184-C156-CE40-6069992045F409598-022092121-dbRG%2F63tuEZELCfw2OMgQw%3D%3D; hit-new-style-dyn=0; CURRENT_QUALITY=0; CURRENT_FNVAL=4048; rpdid=|(u|J|~~kJk~0J\'uYY)Yuuu|Y; SESSDATA=298698bb%2C1685424266%2Cbaba2%2Ac2; bili_jct=fff2e0e3ba510b35980175c124d37003; blackside_state=1; bp_article_offset_8366997=738033208792186900; fingerprint=ba212c0b9b265f06e25f216357e01581; buvid_fp=1ce661df5c741a8eb7525c6ae0aa0af3; sid=7s9j100c; PVID=1; theme_style=light; b_lsid=9B8A91027_1851AECBF75; bp_video_offset_8366997=740260806485082200; _dfcaptcha=535b285812d02dccfee87a4f182c7bfb; innersign=1'

# 下载视频的 URL
URL = [
    'https://www.bilibili.com/video/BV1M4411c7P4/?spm_id_from=333.999.0.0&vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',
    'https://www.bilibili.com/video/BV1hB4y147j8/?spm_id_from=333.337.search-card.all.click',
]
