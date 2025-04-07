import bcrypt
def hash_password(password: str) -> bytes:
    """
    对给定的密码进行 bcrypt 哈希处理

    :param password: 明文密码
    :return: 密码哈希值（bytes 类型）
    """
    # 生成随机盐
    salt = bcrypt.gensalt()
    # 使用 bcrypt 对密码进行哈希处理
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
def verify_password(password: str, hashed: bytes) -> bool:
    """
    验证明文密码是否与 bcrypt 哈希匹配

    :param password: 明文密码
    :param hashed: 存储的密码哈希值
    :return: 如果匹配返回 True，否则返回 False
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
# 示例用法
if __name__ == "__main__":
    original_password = "mySecret123"
    # 获取哈希值（即“加密”后的结果）
    hashed_value = hash_password(original_password)
    print("哈希后的密码:", hashed_value)

    # 验证密码是否匹配
    if verify_password(original_password, hashed_value):
        print("密码验证成功！")
    else:
        print("密码验证失败！")

# 写在末尾，该函数为哈希函数，采取随机加盐的方式，因此每次哈希相同的字符串得到的结果都是不同的，验证逻辑就是，根据用户的用户名在数据库中查询相关的哈希过后的密文是什么样子的，然后在前端进行比较验证
# bcrypt为py自带的包，使用时直接导入即可