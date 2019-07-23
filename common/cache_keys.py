"""
缓存 key 的 prefix 配置
"""

VERIFY_CODE_KEY_PREFIX = 'verify_code:{}'  # 验证码
SWIPE_LIMIT_PREFIX = 'swipe_limit:{}'  # 每日滑动次数

PROFILE_DATA_PREFIX = 'profile_data:{}'  # profile.to_dict 后的字典缓存

MODEL_PERFIX = 'model:{}:{}'  # 模型对象缓存

HOT_RANK = 'hot_rank'       # 滑动积分排行榜
