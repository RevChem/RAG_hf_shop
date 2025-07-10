Данный проект представляет собой относительно простую RAG-систему, предназначенную для покупателей интернет-магазина. Включает в себя:

1. Парсинг данных о смартфонах с сохранением данных в ChromaDB
2. Использование языковых моделей через LangChain
3. API на FastAPI с авторизацией через JWT

### Переменные окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```
HF_MODEL_NAME = "deepseek-ai/DeepSeek-R1"
HF_MODEL_NAME_2 = "Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24"
HF_API_TOKEN = "..."
SECRET_KEY = ...  
ALGORITHM = HS256  
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

- https://github.com/decodingml/llm-twin-course/tree/main?tab=readme-ov-file
- https://habr.com/ru/companies/amvera/articles/902868/
- https://habr.com/ru/companies/amvera/articles/897830/
- https://habr.com/ru/companies/ruvds/articles/796885/
