from qiniu import Auth, put_file

from common import config


def upload(file_name, file_path):
    """
    本地文件上传至七牛云
    :param file_name:
    :param file_path:
    :return:
    """
    # 构建鉴权对象
    qn_auth = Auth(config.QN_ACCESS_KEY, config.QN_SECRET_KEY)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(config.QN_BUCKET_NAME, file_name, 3600)

    ret, info = put_file(token, file_name, file_path)

    return ret, info
