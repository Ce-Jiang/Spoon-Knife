from faker import Faker
import pandas as pd
import random
from datetime import datetime

# ======================
# 初始化 Faker（中文）
# ======================
fake = Faker("zh_CN")

# ======================
# 中国身份证生成（18 位，含校验位）
# ======================
def _generate_realistic_cn_id():
    """
    生成规则正确的中国居民身份证号（18 位，含校验位）
    用于 mock / DLP / audit 测试，不对应任何真实个人
    """

    # 合法存在的行政区划码（示例）
    area_codes = [
        "110101",  # 北京
        "310101",  # 上海
        "440103",  # 广州
        "440104",
        "320102",  # 南京
        "330106",  # 杭州
        "510104",  # 成都
        "420106"   # 武汉
    ]
    area = random.choice(area_codes)

    # 出生日期（YYYYMMDD，自动补零）
    birth = datetime(
        random.randint(1970, 2005),
        random.randint(1, 12),
        random.randint(1, 28)
    ).strftime("%Y%m%d")

    # 顺序码（3 位）
    seq = f"{random.randint(100, 999)}"

    # 前 17 位
    id17 = area + birth + seq

    # 校验位（ISO 7064 MOD 11-2）
    weights = [7, 9, 10, 5, 8, 4, 2,
               1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_map = "10X98765432"
    checksum = sum(int(id17[i]) * weights[i] for i in range(17))
    check_code = check_map[checksum % 11]

    return id17 + check_code


# ======================
# MasterCard 生成（Luhn 校验）
# ======================
def luhn_checksum(number: str) -> int:
    digits = [int(d) for d in number]
    checksum = 0
    parity = len(digits) % 2

    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d

    return (10 - checksum % 10) % 10


def generate_mastercard():
    """
    生成 MasterCard 模拟卡号（16 位，含 Luhn 校验）
    BIN 覆盖 51–55 / 2221–2720
    """

    if random.random() < 0.5:
        prefix = str(random.randint(51, 55))
    else:
        prefix = str(random.randint(2221, 2720))

    body_length = 15 - len(prefix)
    body = prefix + ''.join(str(random.randint(0, 9)) for _ in range(body_length))

    check_digit = luhn_checksum(body)
    return body + str(check_digit)


# ======================
# 其他字段生成
# ======================
def generate_name():
    return fake.name()


def generate_phone():
    return fake.phone_number()


# ======================
# 批量生成数据
# ======================
def create_mock_data(count=100):
    data_list = []

    for _ in range(count):
        row = {
            "姓名": generate_name(),
            "手机号": generate_phone(),
            "身份证号": _generate_realistic_cn_id(),
            "MasterCard信用卡号": generate_mastercard(),
            "地址": fake.address(),
            "邮箱": fake.email()
        }
        data_list.append(row)

    return data_list


# ======================
# 主程序：导出 Excel
# ======================
if __name__ == "__main__":
    mock_count = 2000

    mock_data = create_mock_data(mock_count)

    df = pd.DataFrame(mock_data)

    excel_filename = "DLP_Mock_个人敏感信息_MasterCard_2000.xlsx"
    df.to_excel(excel_filename, index=False, engine="openpyxl")

    print(f"✅ 已成功生成 {mock_count} 条模拟数据")
    print(f"📁 文件已保存为：{excel_filename}")