import yaml

from utils.logger_handler import logger
from utils.path_tool import get_absolute_path


def load_rag_config(config_path: str = get_absolute_path("config/rag.yml"),
                    encoding="utf-8"):
    """
    加载yml文件，以便读取文件内容
    :param config_path:
    :param encoding:
    :return:
    """
    with open(config_path, "r", encoding=encoding) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def load_agent_config(config_path: str = get_absolute_path("config/agent.yml"),
                      encoding="utf-8"):
    """
    加载yml文件，以便读取文件内容
    :param config_path:
    :param encoding:
    :return:
    """
    with open(config_path, "r", encoding=encoding) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def load_chroma_config(config_path: str = get_absolute_path("config/chroma.yml"),
                       encoding="utf-8"):
    """
    加载yml文件，以便读取文件内容
    :param config_path:
    :param encoding:
    :return:
    """
    with open(config_path, "r", encoding=encoding) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def load_prompt_config(config_path: str = get_absolute_path("config/prompt.yml"),
                       encoding="utf-8"):
    """
    加载yml文件，以便读取文件内容
    :param config_path:
    :param encoding:
    :return:
    """
    logger.info(f"config_path:{config_path}")
    with open(config_path, "r", encoding=encoding) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


rag_conf = load_rag_config()
agent_conf = load_agent_config()
chroma_conf = load_chroma_config()
prompt_conf = load_prompt_config()

if __name__ == '__main__':
    print(rag_conf["chat_model_name"])
    print(rag_conf["embedding_model_name"])
    print(prompt_conf["report_prompt_path"])
    print(prompt_conf["main_prompt_path"])
