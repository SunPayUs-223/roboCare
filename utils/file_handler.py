import hashlib
import os.path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from utils.logger_handler import logger


def get_file_md5_hex(file_path) -> str:
    """
    获取文件的md5十六进制字符串，用来去重
    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        logger.error(f"文件{file_path}的md5计算失败，文件不存在！")
    if not os.path.isfile(file_path):
        logger.error(f"{file_path} 不是文件类型！")

    md5_obj = hashlib.md5()

    # 防止大文件加载，进行分片读取
    chunk_size = 4096
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                md5_obj.update(chunk)
        return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"{file_path}计算md5失败，{str(e)}")


def list_dir_with_allowed_type(path: str, allowed_types: tuple[str]) -> tuple[str] | tuple[str, ...]:
    """
    返回文件夹内的文件列表（允许的文件后缀）
    :param path:
    :param allowed_types:
    :return:
    """
    # 文件集合（绝对路径）
    files = []
    if not os.path.isdir(path):
        logger.error(f"{path}不是文件夹")
        return allowed_types

    for file in os.listdir(path):
        if file.endswith(allowed_types):
            files.append(os.path.join(path, file))
    return tuple(files)


def pdf_loader(file_path: str, password: str) -> list[Document]:
    return PyPDFLoader(
        file_path
        # password=password,
    ).load()


def text_loader(file_path: str) -> list[Document]:
    return TextLoader(file_path,encoding='utf-8').load()
