from abc import ABC, abstractmethod
from typing import Optional

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.language_models import BaseChatModel

from utils.config_handler import rag_conf


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf['chat_model_name'])


class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        print("type:",type(rag_conf['embedding_model_name']))
        return DashScopeEmbeddings(model=rag_conf['embedding_model_name'])


chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()

if __name__ == '__main__':
    print(embedding_model)
    print(f"对象属性: {dir(embedding_model)}")
