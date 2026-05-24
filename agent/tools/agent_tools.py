"""
agent所需的工具
"""
import os
import random

from langchain_core.tools import tool

from rag.rag_service import RAGSummaryService
from utils.config_handler import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_absolute_path

rag_service = RAGSummaryService()
user_ids = ['1001', '1002', '1003', '1004', '1005', '1006', '1007']
month_arr = ['2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07']


@tool(description="从向量存储中检索参考资料工具")
def rag_summarize(query: str) -> str:
    return rag_service.rag_summarize(query)


@tool(description="获取天气的工具")
def get_weather(city: str) -> str:
    return f"{city}天气为晴天，气温28℃，空气湿度50%，风力1级，最近6小时无降雨"


@tool(description="获取用户所在城市工具")
def get_user_city() -> str:
    return random.choice(['深圳', '广州', '上海'])


@tool(description="获取用户id工具")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份")
def get_current_month() -> str:
    return random.choice(month_arr)


external_data = {}


def generate_external_data():
    """
    {
        "user_id": {
            "month":{"k1":v1,"k2":v2,...},
            "month":{"k1":v1,"k2":v2,...},
        }
    }
    :return:
    """
    if not external_data:
        abs_path = get_absolute_path(agent_conf['external_data_path'])
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"文件{abs_path}不存在")

        with open(abs_path, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]:  # 切片写法，
                line = line.strip()
                arr: list[str] = line.split(',')
                user_id: str = arr[0].replace('"', '')
                feature: str = arr[1].replace('"', '')
                efficiency: str = arr[2].replace('"', '')
                consumables: str = arr[3].replace('"', '')
                comparison: str = arr[4].replace('"', '')
                time: str = arr[5].replace('"', '')
                if not user_id in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    '特征': feature,
                    '效率': efficiency,
                    '耗材': consumables,
                    '对比': comparison
                }


@tool(description="从外部系统中获取用户的使用记录，返回字符串")
def fetch_records_from_external(user_id, month) -> str:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError as e:
        logger.warning(f"{fetch_records_from_external}没有检索到用户:{user_id}在{month}的使用记录数据")
        return ""


if __name__ == '__main__':
    print(fetch_records_from_external("1000", "2025-02"))
    print(fetch_records_from_external("1001", "2025-02"))