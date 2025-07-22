Данный проект представляет собой относительно простую RAG-систему, предназначенную для покупателей интернет-магазина. Включает в себя:

1. Парсинг данных о смартфонах с сохранением данных в ChromaDB
2. Использование языковых моделей Hugging Face (в комментариях также указана возможность использования deepseek или chatgpt при условии наличия API-токенов) через LangChain
3. API на FastAPI с авторизацией через JWT

### Переменные окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```
HF_MODEL_NAME = "deepseek-ai/DeepSeek-R1"   # Пример модели
HF_MODEL_NAME_2 = "Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24"   # Русскоязычная LLM
HF_API_TOKEN = "..."   # Токен доступа к Hugging Face
SECRET_KEY = ...   # Ключ для JWT-аутентификации
ALGORITHM = HS256   #  Алгоритм подписи JWT
```

### Запуск API 

```bash
uvicorn app.main:app --port 8000 --host 0.0.0.0
```

## Структура проекта

```
.
├── app/                  
│   ├── api/             
│   ├── core/             
│   ├── models/          
│   ├── services/         
│   ├── main.py
│   ├── config.py
│   ├── users.json
│   └── .env        
├── chroma_db/           
├── scripts/             
├── requirements.txt      
└── .env                 
```

## Используемые технологии

- **FastAPI** - веб-фреймворк для API
- **ChromaDB** - векторная база данных
- **LangChain** - работа с языковыми моделями
- **HuggingFace** - языковые модели и эмбеддинги
- **PyJWT** - аутентификация через JWT
- **BeautifulSoup** - парсинг данных \

## При создании проекта использовались следующие источники:

- **LangChain**: https://github.com/decodingml/llm-twin-course/tree/main?tab=readme-ov-file
- **LangChain** & **ChromaDB**:  https://habr.com/ru/companies/amvera/articles/902868/
- **LangChain** & **ChromaDB**: https://habr.com/ru/companies/amvera/articles/897830/
- **BeautifulSoup**: https://habr.com/ru/companies/ruvds/articles/796885/
