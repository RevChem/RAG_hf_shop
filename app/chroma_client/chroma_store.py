import torch
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger

from app.config import settings


class ChromaVectorStore:
    def __init__(self):
        self._store: Chroma | None = None

    async def init(self):
        logger.info("Инициализация ChromaVectorStore")
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Используем устройство для эмбеддингов: {device}")

            embeddings = HuggingFaceEmbeddings(
                model_name=settings.LM_MODEL_NAME,
                model_kwargs={"device": device},
                encode_kwargs={"normalize_embeddings": True},
            )

            self._store = Chroma(
                persist_directory=settings.CHROMA_PATH,
                embedding_function=embeddings,
                collection_name=settings.COLLECTION_NAME,
            )

            logger.success(
                f"'{settings.COLLECTION_NAME}' в '{settings.CHROMA_PATH}'"
            )
        except Exception as e:
            logger.exception(f"Ошибка при инициализации ChromaVectorStore: {e}")
            raise

    async def asimilarity_search(self, query: str, with_score: bool, k: int = 3):
        if not self._store:
            raise RuntimeError("ChromaVectorStore is not initialized.")
        logger.info(f"Поиск похожих документов по запросу: «{query}», top_k={k}")
        try:
            if with_score:
                results = await self._store.asimilarity_search_with_score(
                    query=query, k=k
                )
            else:
                results = await self._store.asimilarity_search(query=query, k=k)
            logger.debug(f"Найдено {len(results)} результатов.")
            return results
        except Exception as e:
            logger.exception(f"Ошибка при поиске: {e}")
            raise

    async def close(self):
        logger.info("Отключение ChromaVectorStore...")
        pass


chroma_vectorstore = ChromaVectorStore()


def get_vectorstore() -> ChromaVectorStore:
    return chroma_vectorstore
