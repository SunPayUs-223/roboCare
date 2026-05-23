"""
为整个工程提供统一的绝对路径，
"""
import os


def get_project_root() -> str:
    """
    获取工程所在的根目录
    :return: 工程根目录
    """
    # 获取当前py文件的路径
    current_file = os.path.abspath(__file__)
    # 文件所在目录的路径
    current_dir = os.path.dirname(current_file)
    # 根目录路径
    project_root_path = os.path.dirname(current_dir)
    return project_root_path


def get_absolute_path(relative_path: str) -> str:
    """
    :param relative_path: 文件相对路径
    :return: 文件的绝对路径
    """
    root_path = get_project_root()
    return os.path.join(root_path, relative_path)


if __name__ == '__main__':
    print(get_absolute_path('config/test.py'))