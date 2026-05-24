import os.path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from model.model_factory import embedding_model
from utils.config_handler import chroma_conf
from utils.file_handler import text_loader, pdf_loader, list_dir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from utils.path_tool import get_absolute_path


class VectorStoreService:

    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf['collection_name'],
            embedding_function=embedding_model,
            persist_directory=chroma_conf['persist_directory']
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf['chunk_size'],
            chunk_overlap=chroma_conf['chunk_overlap'],
            separators=chroma_conf['separators'],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={'k': chroma_conf['k']})

    def load_documents(self):
        """
        读取文件，转为document，存入向量库，注意要去重
        :param documents:
        :return:
        """

        def check_md5_hex(md5_for_check: str) -> bool:
            file_path = get_absolute_path(chroma_conf['md5_hex_store'])
            if not os.path.exists(file_path):
                # 创建文件，关闭
                open(file_path, 'w', encoding="utf-8").close()
                return False
            # 读取文件内容
            with open(file_path, 'r', encoding="utf-8") as f:
                for line in f:
                    line = line.strip()  # 去掉前后空格
                    if line == md5_for_check:
                        return True
            return False

        def save_md5_hex(md5_for_check: str) -> None:
            file_path = get_absolute_path(chroma_conf['md5_hex_store'])
            with open(file_path, 'a', encoding="utf-8") as f:
                f.write(md5_for_check + '\n')

        def get_file_documents(read_file_path: str):
            if read_file_path.endswith('.txt'):
                return text_loader(read_file_path)
            elif read_file_path.endswith('.pdf'):
                return pdf_loader(read_file_path,chroma_conf['password'])
            else:
                return []

        allowed_file_path: tuple[str, ...] = list_dir_with_allowed_type(get_absolute_path(chroma_conf['data_path']),
                                                                        tuple(chroma_conf['allow_knowledge_file_type']))
        for file_path in allowed_file_path:
            md5_hex = get_file_md5_hex(file_path)
            if check_md5_hex(md5_hex):
                logger.warning(f"{file_path} is already loaded in vector store")
                continue
            try:
                documents: list[Document] = get_file_documents(file_path)
                if not documents:
                    logger.warning(f"{documents} 无有效内容")
                    continue
                split_documents = self.splitter.split_documents(documents)
                if not split_documents:
                    logger.warning(f"{split_documents}中无有效内容")
                    continue
                self.vector_store.add_documents(split_documents)

                save_md5_hex(md5_hex)

                logger.info(f"{file_path} is loaded in vector store")
            except Exception as e:
                # exc_info=True记录堆栈信息
                logger.error(f"从{file_path}加载知识库失败：{str(e)}", exc_info=True)
                continue  # 不影响循环执行


if __name__ == '__main__':
    vector_store = VectorStoreService()
    vector_store.load_documents()
    retriever = vector_store.get_retriever()
    for doc in retriever.invoke("迷路"):
        print(doc.page_content)
        print("=" * 20)
