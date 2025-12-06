import os

# 程序根目录（请勿修改）
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# 文件临时输出目录
TEMP_PATH = os.path.join(BASE_PATH, "temp")
# 视频输出目录
OUTPUT_PATH = os.path.join(BASE_PATH, "output")

# B站登录后获取的SESSDATA，CURRENT_QUALITY
# 定期更换COOKIE的值即可
COOKIE = 'enable_web_push=DISABLE; DedeUserID=628798162; DedeUserID__ckMd5=605ead5cb800a4c2; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; fingerprint=4424f22474243a774b09e01d3f4a9fd9; buvid_fp=4424f22474243a774b09e01d3f4a9fd9; enable_feed_channel=ENABLE; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; buvid4=13F1AE8B-7014-A8C7-2771-FEA0E79672AE29687-024091912-z/2NJuNlxjzkI1rXp6siyFOi63xXGqRD919BkRum+weAk1LtB4N5WoSL8zLI/37D; buvid3=EDDAD8BE-A773-CCAB-E914-3EAED568BE6E38705infoc; b_nut=1758287838; _uuid=B210DB5D1-6D98-18D2-F287-5937655964D143034infoc; hit-dyn-v2=1; rpdid=0zbf5KI0AJ|12WuhEWts|1F|3w1VcPJ0; LIVE_BUVID=AUTO5617619174864305; PVID=2; theme-switch-show=SHOWED; home_feed_column=5; browser_resolution=1652-913; ogv_device_support_hdr=0; CURRENT_QUALITY=120; selectedMode=false; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQ1MDY1NzgsImlhdCI6MTc2NDI0NzMxOCwicGx0IjotMX0.GucGNY_qgODr1I05_186nhSGGULRV4Ci3scIWQUGvV8; bili_ticket_expires=1764506518; SESSDATA=10da1bcf%2C1779799379%2Ced0a5%2Ab2CjCJM9GdqUTpEBWY4D4S5WIl70KXxChDUMXVoKP01QfYsREtfxdhML2XuouXJYKpyNYSVlB4ZkZFY1JlVWlHanotTzFIY3ZzVV9KQTJCVjhMcGlIRTQyeHpKNkVkVm1OUE11aVpkZ1BoSG1pbmt0OUpwRGpZVy16Q0lIY2Nua3N5anRaOHRmNXNnIIEC; bili_jct=94b135657c2bd65caf5caf4b2493b856; bp_t_offset_628798162=1139922889164718080; b_lsid=E87361CA_19AC59767D0; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; CURRENT_FNVAL=4048; sid=5udzg0du'

# 下载视频的 URL
#
# 支持的视频类型：
#
# 1. 普通视频 (自动使用 DefaultStrategy)
#    - URL 格式: https://www.bilibili.com/video/BV* 或 /video/av*
#    - 特点: 快速下载，无需特殊处理
#    - 示例: 'https://www.bilibili.com/video/BV1M4411c7P4'
#
# 2. 分P视频 (自动使用 DefaultStrategy)
#    - URL 格式: 视频链接 + ?p=分P号
#    - 特点: 每个分P独立下载
#    - 示例:
#      'https://www.bilibili.com/video/BV1TnsZzHEcz?p=1'  # 第1个分P
#      'https://www.bilibili.com/video/BV1TnsZzHEcz?p=2'  # 第2个分P
#
# 3. 番剧/电影 (自动使用 BangumiStrategy)
#    - URL 格式: https://www.bilibili.com/bangumi/play/ss* (season) 或 /ep* (episode)
#    - 特点: 可能有地区限制、会员限制
#    - 示例:
#      'https://www.bilibili.com/bangumi/play/ss39429'     # 电影 (season)
#      'https://www.bilibili.com/bangumi/play/ep271002'    # 单集 (episode)
#    - 注意:
#      ⚠️  海外地区可能无法下载（会显示地区限制错误）
#      ⚠️  需要使用中国大陆的 VPN/代理才能下载
#
# 使用方法：
# - 将要下载的视频链接添加到下面的列表中
# - 可以同时添加多个链接，程序会依次下载
# - 不需要手动指定视频类型，程序会自动识别

#
URL = [
    # 普通视频
    'https://www.bilibili.com/video/BV1M4411c7P4/?vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',
    'https://www.bilibili.com/video/BV1hB4y147j8/?spm_id_from=333.337.search-card.all.click&vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63',

    # 分P视频（第1个分P）
    'https://www.bilibili.com/video/BV1TnsZzHEcz?vd_source=9c3224b88b8a3c4cc210fc6ff9b28f63&spm_id_from=333.788.videopod.episodes',

    # 分P视频（第2个分P）
    'https://www.bilibili.com/video/BV1TnsZzHEcz?p=2',

    # 番剧/电影（需要中国大陆 IP）
    # 'https://www.bilibili.com/bangumi/play/ss39429',      # 电影
    # 'https://www.bilibili.com/bangumi/play/ep271002',     # 番剧单集（暂不支持）
]