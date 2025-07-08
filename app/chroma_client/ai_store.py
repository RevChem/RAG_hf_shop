from typing import AsyncGenerator, Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_huggingface import HuggingFaceEndpoint
from loguru import logger

from app.config import settings


class ChatWithAI:
    def __init__(self, provider:Literal["mistral", "mistral_Nemo"] = "mistral"):
        self.provider = provider
        if provider == "mistral":
            self.llm = HuggingFaceEndpoint(
                repo_id=settings.HF_MODEL_NAME,  
                task="text-generation",
                huggingfacehub_api_token=settings.HF_API_TOKEN.get_secret_value(),  
            )
        elif provider == "mistral_Nemo":
            self.llm = HuggingFaceEndpoint(
                repo_id=settings.HF_MODEL_NAME_2,  
                provider="cohere",
                max_new_tokens=100,
                do_sample=False,
                huggingfacehub_api_token=settings.HF_API_TOKEN.get_secret_value(), 
                task="text-generation", 
            )
        else:
            raise ValueError(f"Неподдерживаемый провайдер: {provider}")


    async def astream_response(
        self, formatted_context: str, query: str
    ) -> AsyncGenerator[str, None]:
        try:
            system_message = SystemMessage(
                content="""Ты — менеджер интернет-магазина. Отвечаешь по делу без лишних вступлений. Свой ответ, в первую очередь, ориентируй на переданный контекст. Если информации недостаточно - пробуй получить ответы из своей базы знаний."""
            )
            human_message = HumanMessage(
                content=f"Вопрос: {query}\nКонтекст: {formatted_context}. Ответ форматируй в markdown!"
            )
            logger.info(f"Начинаем стриминг ответа для запроса: {query}")
            async for chunk in self.llm.astream([system_message, human_message]):
                if chunk.content: 
                    logger.debug(f"Получен чанк: {chunk.content[:50]}...")
                    yield chunk.content
            logger.info("Стриминг ответа завершен")
        except Exception as e:
            logger.error(f"Ошибка при стриминге ответа: {e}")
            yield "Произошла ошибка при стриминге ответа."