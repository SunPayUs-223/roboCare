import logging
import os
from datetime import datetime
# TODO 日志文件的结构需要优化：按日期生成当日的四个日志级别的文件，每天一个日志文件
from utils.path_tool import get_absolute_path

# 日志保存根目录
LOG_ROOT = get_absolute_path("logs")

# 确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)
# 日志格式配置 asctime时间：日志级别：文件：日志内容
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(levelname)s -%(filename)s:%(lineno)d- %(message)s'
)


def get_logger(name: str = "roboCare",
               console_level: int = logging.INFO,
               file_level: int = logging.DEBUG,
               log_file=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加Handler
    if logger.handlers:
        return logger

    # 控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    # 文件handler
    if not log_file:
        # 生成实时日志文件
        log_file = os.path.join(LOG_ROOT, f"{name}.{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# 快捷获取日志管理器: 直接创建好，到时候引入即可
logger = get_logger()

if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.warning("调试日志")
