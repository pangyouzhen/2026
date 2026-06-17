import functools
import os

import pandas as pd
from loguru import logger
from retry import retry

# 假设 logger 和 retry 已经在外部定义好

@retry(Exception, tries=3, delay=2)
def func_utils(csv_path, csv_name, *args, **kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            # 1. 提前获取 date，用于拼接文件路径
            # 建议加上默认值或校验，防止调用时忘记传 date 导致 KeyError
            date = kw.get("date") 
            if date is None:
                raise ValueError("调用被装饰函数时，必须通过 kwargs 传入 'date' 参数")

            # 2. 拼接目标文件路径
            target_file = f"{csv_path}/{csv_name}_{date}.csv"

            # 3. 核心逻辑：如果文件已存在，直接读取并返回，跳过 func 执行
            if os.path.exists(target_file):
                logger.info(f"文件已存在: {target_file}，跳过执行 {func.__name__}，直接读取缓存数据")
                result = pd.read_csv(target_file, encoding="utf-8")
                return result

            # 4. 文件不存在，正常执行原函数
            logger.info(f"{func.__name__}的参数 {csv_path=}, {csv_name=}")
            result = func(*args, **kw)
            
            # 5. 将 date 写入结果并保存
            result["date"] = date
            
            # 6. 保存前确保目录存在（防止因路径不存在报错）
            os.makedirs(csv_path, exist_ok=True)
            
            result.to_csv(target_file, index=False, encoding="utf-8")
            logger.info(f"{func.__name__}_{date} 存储csv数据成功")
            
            return result

        return wrapper

    return decorator