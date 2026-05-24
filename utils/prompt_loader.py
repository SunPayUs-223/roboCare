from utils.config_handler import prompt_conf
from utils.logger_handler import logger
from utils.path_tool import get_absolute_path


def load_system_prompt():
    try:
        main_prompt = prompt_conf["main_prompt_path"]
        absolute_path = get_absolute_path(main_prompt)
    except KeyError as e:
        logger.error(f"yaml中没有key：main_prompt_path")
        raise e

    try:
        return open(absolute_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"加载系统提示词错误：{str(e)}")
        raise e


def load_rag_prompt():
    abs_path = ""
    try:
        main_prompt = prompt_conf["rag_summarize_prompt_path"]
        abs_path = get_absolute_path(main_prompt)
        try:
            return open(abs_path, "r", encoding="utf-8").read()
        except Exception as e:
            logger.error(f"加载rag提示词错误：{str(e)}")
    except KeyError as e:
        logger.error(f"{abs_path}中没有key：rag_summarize_prompt_path")
        raise e


def load_report_prompt():
    abs_path = ""
    try:
        report_conf = prompt_conf["report_prompt_path"]
        abs_path = get_absolute_path(report_conf)
        try:
            return open(abs_path, "r", encoding="utf-8").read()
        except Exception as e:
            logger.error(f"加载chroma提示词错误：{str(e)}")
    except KeyError as e:
        logger.error(f"{abs_path}中没有key：report_prompt_path")
        raise e


if __name__ == '__main__':
    print(load_system_prompt())
