"""
业务状态码、错误码
"""

OK = 0

# 系统保留状态码
# 1000 - 1999


# 用户系统
# 2000 - 2999
PHONE_NUM_ERR = 2001        # 手机号格式错误
SMS_SEND_ERR = 2002         # 验证码发送失败
VERIFY_CODE_ERR = 2003      # 验证码错误
LOGIN_REQUIRED_ERR = 2004   # 用户认证错误
